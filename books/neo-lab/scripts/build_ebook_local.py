#!/usr/bin/env python3
"""Build Markdown, PDF, and EPUB artifacts from a configured ebook project."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import re
import shutil
import uuid
import zipfile
from pathlib import Path

try:
    from PIL import Image as PILImage
    from PIL import ImageDraw, ImageEnhance, ImageFont
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4, A5, LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.platypus import (
        Image,
        KeepTogether,
        ListFlowable,
        ListItem,
        LongTable,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError as exc:
    raise SystemExit(
        "Missing publishing dependency. Use the Codex bundled Python runtime or install "
        "Pillow, pypdf, and reportlab. Original error: " + str(exc)
    ) from exc


DEFAULT_THEME = {
    "primary": "#17324D",
    "secondary": "#2F6F73",
    "accent": "#D99A3D",
    "ink": "#1F2937",
    "muted": "#667085",
    "paper": "#F7F3EA",
}
PAGE_SIZES = {"A5": A5, "A4": A4, "LETTER": LETTER}
FONT_CANDIDATES = [
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/arialuni.ttf"),
]
BOLD_FONT_CANDIDATES = [
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    Path("C:/Windows/Fonts/msyhbd.ttc"),
]


def safe_basename(text: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "_", text).strip(" ._")
    return cleaned or "ebook"


def load_config(project: Path) -> dict:
    path = project / "book.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing project config: {path}")
    config = json.loads(path.read_text(encoding="utf-8"))
    required = ("title", "author", "date", "language", "manuscript")
    missing = [key for key in required if not str(config.get(key, "")).strip()]
    if missing:
        raise ValueError(f"book.json is missing required values: {', '.join(missing)}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", config["date"]):
        raise ValueError("book.json date must use ISO format YYYY-MM-DD")
    config["subtitle"] = str(config.get("subtitle", ""))
    config["description"] = str(config.get("description") or config["subtitle"] or config["title"])
    config["output_basename"] = safe_basename(str(config.get("output_basename") or config["title"]))
    config["page_size"] = str(config.get("page_size", "A5")).upper()
    if config["page_size"] not in PAGE_SIZES:
        raise ValueError("page_size must be A5, A4, or LETTER")
    theme = dict(DEFAULT_THEME)
    theme.update(config.get("theme") or {})
    for key, value in theme.items():
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(value)):
            raise ValueError(f"theme.{key} must be a six-digit hex color")
    config["theme"] = theme
    config["identifier"] = str(
        config.get("identifier")
        or f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, config['title'] + '|' + config['author'])}"
    )
    return config


def project_path(project: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    return path.resolve() if path.is_absolute() else (project / path).resolve()


def first_existing(project: Path, configured: str, candidates: list[Path]) -> Path:
    if configured:
        path = project_path(project, configured)
        if not path.exists():
            raise FileNotFoundError(f"Configured font does not exist: {path}")
        return path
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "No Unicode font was found. Set font_regular and font_bold in book.json to local TTF/TTC files."
    )


def display_date(iso_date: str, language: str) -> str:
    if language.lower().startswith("zh"):
        year, month, day = iso_date.split("-")
        return f"{year} 年 {int(month):02d} 月 {int(day):02d} 日"
    return iso_date


def labels(language: str) -> dict[str, str]:
    if language.lower().startswith("zh"):
        return {
            "publication": "出版信息",
            "title": "书名",
            "author": "作者",
            "date": "出版日期",
            "edition": "版本",
            "publisher": "出版社",
            "email": "邮箱",
            "copyright": "版权说明",
            "toc": "目录",
            "title_page": "扉页",
            "body": "正文",
            "figure": "图",
        }
    return {
        "publication": "Publication information",
        "title": "Title",
        "author": "Author",
        "date": "Publication date",
        "edition": "Edition",
        "publisher": "Publisher",
        "email": "Email",
        "copyright": "Copyright",
        "toc": "Contents",
        "title_page": "Title page",
        "body": "Body",
        "figure": "Figure",
    }


def strip_cover_preamble(markdown: str) -> str:
    parts = re.split(r"(?m)^---\s*$", markdown, maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else markdown.strip()


def parse_markdown_blocks(markdown: str) -> list[dict]:
    lines = markdown.splitlines()
    blocks: list[dict] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append({"type": "p", "text": " ".join(part.strip() for part in paragraph)})
            paragraph.clear()

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip()
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("Unclosed fenced code block in manuscript")
            index += 1
            blocks.append({"type": "code", "language": language, "text": "\n".join(code_lines)})
            continue

        image_match = re.match(r"^!\[(.*?)\]\((.+?)\)$", stripped)
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        list_match = re.match(r"^\s*([-*+]|\d+\.)\s+(.+)$", line)
        if heading_match:
            flush_paragraph()
            blocks.append(
                {"type": "heading", "level": len(heading_match.group(1)), "text": heading_match.group(2).strip()}
            )
            index += 1
        elif image_match:
            flush_paragraph()
            blocks.append({"type": "image", "alt": image_match.group(1).strip(), "path": image_match.group(2).strip()})
            index += 1
        elif stripped == "---":
            flush_paragraph()
            blocks.append({"type": "hr"})
            index += 1
        elif stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            blocks.append({"type": "quote", "text": " ".join(quote_lines)})
        elif stripped.startswith("|") and "|" in stripped[1:]:
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            rows = [[cell.strip() for cell in row.strip("|").split("|")] for row in table_lines]
            if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
                rows.pop(1)
            blocks.append({"type": "table", "rows": rows})
        elif list_match:
            flush_paragraph()
            ordered = list_match.group(1)[0].isdigit()
            items = []
            while index < len(lines):
                current = re.match(r"^\s*([-*+]|\d+\.)\s+(.+)$", lines[index])
                if not current or current.group(1)[0].isdigit() != ordered:
                    break
                items.append(current.group(2).strip())
                index += 1
            blocks.append({"type": "list", "ordered": ordered, "items": items})
        else:
            paragraph.append(stripped)
            index += 1
    flush_paragraph()
    return blocks


def publication_blocks(markdown: str, language: str) -> list[dict]:
    blocks = parse_markdown_blocks(strip_cover_preamble(markdown))
    aliases = {"扉页"} if language.lower().startswith("zh") else {"titlepage", "halftitle", "half-title"}
    first_h2 = next(
        (index for index, block in enumerate(blocks) if block["type"] == "heading" and block["level"] == 2),
        None,
    )
    if first_h2 is None:
        return blocks
    normalized = re.sub(r"\s+", "", blocks[first_h2]["text"].casefold())
    if normalized not in aliases:
        return blocks
    next_h2 = next(
        (
            index
            for index in range(first_h2 + 1, len(blocks))
            if blocks[index]["type"] == "heading" and blocks[index]["level"] == 2
        ),
        len(blocks),
    )
    return blocks[:first_h2] + blocks[next_h2:]


def inline_markup(text: str, *, epub: bool = False, link_color: str = "#2F6F73") -> str:
    escaped = html.escape(text.strip(), quote=False)
    # Accept ordinary destinations plus one balanced pair of parentheses, as used by many scholarly URLs.
    link_pattern = re.compile(r"\[([^\]]+)\]\(((?:[^()]|\([^()]*\))+?)\)")

    def replace_link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(html.unescape(match.group(2)), quote=True)
        if epub:
            return f'<a href="{href}">{label}</a>'
        return f'<link href="{href}" color="{link_color}">{label}</link>'

    escaped = link_pattern.sub(replace_link, escaped)
    escaped = re.sub(r"`(.+?)`", r'<font color="' + link_color + r'">\1</font>', escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*(.+?)\*(?!\*)", r"<i>\1</i>", escaped)
    return escaped


def resolve_asset(project: Path, manuscript_path: Path, raw: str) -> Path:
    if re.match(r"^[a-z]+://", raw, flags=re.I):
        raise ValueError(f"Remote image URLs are not embedded automatically; download this image first: {raw}")
    candidates = [(manuscript_path.parent / raw).resolve(), (project / raw).resolve()]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Referenced image not found: {raw}")


def wrap_by_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for source_line in text.splitlines() or [""]:
        words = source_line.split()
        if " " in source_line.strip() and all(draw.textbbox((0, 0), word, font=font)[2] <= max_width for word in words):
            current_words: list[str] = []
            for word in words:
                proposal = " ".join(current_words + [word])
                if current_words and draw.textbbox((0, 0), proposal, font=font)[2] > max_width:
                    lines.append(" ".join(current_words))
                    current_words = [word]
                else:
                    current_words.append(word)
            if current_words:
                lines.append(" ".join(current_words))
            continue
        current = ""
        for char in source_line:
            proposal = current + char
            if current and draw.textbbox((0, 0), proposal, font=font)[2] > max_width:
                lines.append(current.rstrip())
                current = char.lstrip()
            else:
                current = proposal
        lines.append(current or " ")
    return lines


def balance_short_last_line(
    draw: ImageDraw.ImageDraw, lines: list[str], font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    if len(lines) < 2 or len(lines[-1].strip()) > 2:
        return lines
    combined = lines[-2].rstrip() + lines[-1].lstrip()
    candidates = sorted(range(1, len(combined)), key=lambda index: abs(len(combined) - 2 * index))
    for index in candidates:
        left, right = combined[:index].rstrip(), combined[index:].lstrip()
        if not left or not right:
            continue
        if draw.textbbox((0, 0), left, font=font)[2] <= max_width and draw.textbbox((0, 0), right, font=font)[2] <= max_width:
            return lines[:-2] + [left, right]
    return lines


def crop_to_cover(image: PILImage.Image, size: tuple[int, int]) -> PILImage.Image:
    target_w, target_h = size
    source_w, source_h = image.size
    scale = max(target_w / source_w, target_h / source_h)
    resized = image.resize((round(source_w * scale), round(source_h * scale)), PILImage.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def create_cover(project: Path, config: dict, regular_font: Path, bold_font: Path) -> Path:
    output = project / "tmp" / "cover-final.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    size = (1600, 2268)
    final_image = str(config.get("cover_image", "")).strip()
    if final_image:
        source = project_path(project, final_image)
        if not source.exists():
            raise FileNotFoundError(f"Configured cover_image does not exist: {source}")
        crop_to_cover(PILImage.open(source).convert("RGB"), size).save(output, "JPEG", quality=94)
        return output

    theme = config["theme"]
    background = str(config.get("cover_background", "")).strip()
    if background:
        source = project_path(project, background)
        if not source.exists():
            raise FileNotFoundError(f"Configured cover_background does not exist: {source}")
        canvas = crop_to_cover(PILImage.open(source).convert("RGB"), size)
        canvas = ImageEnhance.Contrast(canvas).enhance(1.06)
        canvas = ImageEnhance.Color(canvas).enhance(0.82)
        overlay = PILImage.new("RGBA", size, (10, 28, 45, 128))
        canvas = PILImage.alpha_composite(canvas.convert("RGBA"), overlay)
    else:
        canvas = PILImage.new("RGBA", size, theme["primary"])
        draw = ImageDraw.Draw(canvas, "RGBA")
        primary = tuple(int(theme["primary"][i : i + 2], 16) for i in (1, 3, 5))
        secondary = tuple(int(theme["secondary"][i : i + 2], 16) for i in (1, 3, 5))
        for y in range(size[1]):
            ratio = y / size[1]
            color = tuple(round(primary[i] * (1 - ratio) + secondary[i] * ratio) for i in range(3))
            draw.line((0, y, size[0], y), fill=color + (255,))
        draw.ellipse((-450, 1480, 1150, 2900), outline=theme["accent"], width=18)
        draw.ellipse((820, -520, 2080, 720), outline=(255, 255, 255, 55), width=12)
        for x in range(100, 1500, 95):
            draw.ellipse((x, 2040, x + 10, 2050), fill=(255, 255, 255, 85))

    draw = ImageDraw.Draw(canvas, "RGBA")
    title_size = 128 if len(config["title"]) <= 18 else 105 if len(config["title"]) <= 30 else 84
    title_font = ImageFont.truetype(str(bold_font), title_size)
    subtitle_font = ImageFont.truetype(str(regular_font), 48)
    meta_font = ImageFont.truetype(str(regular_font), 38)
    label_font = ImageFont.truetype(str(bold_font), 31)
    left, max_width = 150, 1300
    label = str(config.get("cover_label", "")).strip()
    if label:
        label_box = draw.textbbox((0, 0), label, font=label_font)
        label_w = label_box[2] - label_box[0]
        draw.rounded_rectangle((left, 190, left + label_w + 58, 260), radius=18, fill=theme["accent"])
        draw.text((left + 29, 205), label, font=label_font, fill="#14283B")

    y = 520
    title_lines = balance_short_last_line(
        draw, wrap_by_width(draw, config["title"], title_font, max_width), title_font, max_width
    )
    for line in title_lines:
        draw.text((left, y), line, font=title_font, fill="#FFFFFF", stroke_width=1, stroke_fill="#FFFFFF")
        y += title_size * 1.25
    if config["subtitle"]:
        y += 55
        draw.rectangle((left, y - 18, left + 140, y - 8), fill=theme["accent"])
        for line in wrap_by_width(draw, config["subtitle"], subtitle_font, max_width):
            draw.text((left, y), line, font=subtitle_font, fill="#EAF3F5")
            y += 68

    author_line = config["author"]
    date_line = display_date(config["date"], config["language"])
    draw.line((left, 1940, 1450, 1940), fill=(255, 255, 255, 90), width=2)
    draw.text((left, 2000), author_line, font=meta_font, fill="#FFFFFF")
    draw.text((left, 2065), date_line, font=meta_font, fill="#DCE8EB")
    canvas.convert("RGB").save(output, "JPEG", quality=94, optimize=True)
    return output


def register_fonts(regular_font: Path, bold_font: Path) -> None:
    pdfmetrics.registerFont(TTFont("BookSans", str(regular_font)))
    pdfmetrics.registerFont(TTFont("BookSansBold", str(bold_font)))
    pdfmetrics.registerFontFamily(
        "BookSans", normal="BookSans", bold="BookSansBold", italic="BookSans", boldItalic="BookSansBold"
    )


def pdf_styles(config: dict) -> dict[str, ParagraphStyle]:
    theme = config["theme"]
    base = getSampleStyleSheet()
    primary = colors.HexColor(theme["primary"])
    secondary = colors.HexColor(theme["secondary"])
    ink = colors.HexColor(theme["ink"])
    muted = colors.HexColor(theme["muted"])
    paper = colors.HexColor(theme["paper"])
    return {
        "body": ParagraphStyle(
            "BodyBook", parent=base["BodyText"], fontName="BookSans", fontSize=9.4, leading=15.7,
            textColor=ink, alignment=TA_JUSTIFY, firstLineIndent=18.8, spaceAfter=5,
            allowWidows=0, allowOrphans=0, wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "H2Book", parent=base["Heading1"], fontName="BookSansBold", fontSize=20.5, leading=28,
            textColor=primary, spaceBefore=6, spaceAfter=13, keepWithNext=True, wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "H3Book", parent=base["Heading2"], fontName="BookSansBold", fontSize=13.5, leading=20,
            textColor=secondary, spaceBefore=12, spaceAfter=7, keepWithNext=True, wordWrap="CJK",
        ),
        "h4": ParagraphStyle(
            "H4Book", parent=base["Heading3"], fontName="BookSansBold", fontSize=11, leading=17,
            textColor=colors.HexColor(theme["accent"]), spaceBefore=9, spaceAfter=5,
            keepWithNext=True, wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "QuoteBook", parent=base["BodyText"], fontName="BookSans", fontSize=8.9, leading=14.5,
            textColor=primary, backColor=paper, borderColor=secondary, borderWidth=0.8,
            borderPadding=(8, 10, 8, 10), leftIndent=5, rightIndent=5,
            spaceBefore=7, spaceAfter=9, wordWrap="CJK",
        ),
        "list": ParagraphStyle(
            "ListBook", parent=base["BodyText"], fontName="BookSans", fontSize=9.1, leading=14.8,
            textColor=ink, leftIndent=0, spaceAfter=2, wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "CaptionBook", parent=base["BodyText"], fontName="BookSans", fontSize=7.6, leading=11,
            textColor=muted, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10, wordWrap="CJK",
        ),
        "table": ParagraphStyle(
            "TableBook", parent=base["BodyText"], fontName="BookSans", fontSize=6.9, leading=10.2,
            textColor=ink, wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "TableHeaderBook", parent=base["BodyText"], fontName="BookSansBold", fontSize=7.2, leading=10.4,
            textColor=colors.white, alignment=TA_LEFT, wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "CodeBook", parent=base["Code"], fontName="BookSans", fontSize=7.8, leading=11.5,
            textColor=ink, backColor=paper, borderPadding=7, leftIndent=4, rightIndent=4,
            spaceBefore=6, spaceAfter=8, wordWrap="CJK",
        ),
        "title": ParagraphStyle(
            "TitlePage", parent=base["Title"], fontName="BookSansBold", fontSize=25, leading=34,
            textColor=primary, alignment=TA_CENTER, wordWrap="CJK", spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "SubtitlePage", parent=base["BodyText"], fontName="BookSans", fontSize=12, leading=20,
            textColor=secondary, alignment=TA_CENTER, wordWrap="CJK", spaceAfter=22,
        ),
        "meta": ParagraphStyle(
            "MetaPage", parent=base["BodyText"], fontName="BookSans", fontSize=9, leading=17,
            textColor=muted, alignment=TA_CENTER, wordWrap="CJK",
        ),
        "imprint": ParagraphStyle(
            "ImprintPage", parent=base["BodyText"], fontName="BookSans", fontSize=8.2, leading=14,
            textColor=ink, wordWrap="CJK", spaceAfter=6,
        ),
        "toc0": ParagraphStyle(
            "TOC0", fontName="BookSansBold", fontSize=9.1, leading=14.2,
            textColor=primary, leftIndent=0, firstLineIndent=0, spaceBefore=3, wordWrap="CJK",
        ),
        "toc1": ParagraphStyle(
            "TOC1", fontName="BookSans", fontSize=7.4, leading=11,
            textColor=ink, leftIndent=12, firstLineIndent=0, wordWrap="CJK",
        ),
    }


class BookDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable) -> None:
        level = getattr(flowable, "_book_level", None)
        if level not in (0, 1):
            return
        title = getattr(flowable, "_book_title", "")
        bookmark = getattr(flowable, "_book_bookmark", "")
        if not title or not bookmark:
            return
        self.canv.bookmarkPage(bookmark)
        self.canv.addOutlineEntry(title, bookmark, level=level, closed=level == 0)
        self.notify("TOCEntry", (level, title, self.page + 1, bookmark))


def make_pdf_heading(text: str, level: int, styles: dict, counter: int, link_color: str, breaks=None) -> Paragraph:
    style = styles["h2"] if level == 2 else styles["h3"] if level == 3 else styles["h4"]
    bookmark = f"section-{counter}"
    display = inline_markup((breaks or {}).get(text, text), link_color=link_color).replace("\n", "<br/>")
    paragraph = Paragraph(f'<a name="{bookmark}"/>{display}', style)
    paragraph._book_level = 0 if level == 2 else 1 if level == 3 else 2
    paragraph._book_title = text
    paragraph._book_bookmark = bookmark
    return paragraph


def table_flowable(rows: list[list[str]], styles: dict, width: float, config: dict) -> LongTable:
    column_count = max(len(row) for row in rows)
    normalized = [row + [""] * (column_count - len(row)) for row in rows]
    link_color = config["theme"]["secondary"]
    data = []
    for row_index, row in enumerate(normalized):
        style = styles["table_header"] if row_index == 0 else styles["table"]
        data.append([Paragraph(inline_markup(cell, link_color=link_color), style) for cell in row])
    table = LongTable(data, colWidths=[width / column_count] * column_count, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(config["theme"]["primary"])),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(config["theme"]["paper"])]),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C7D1D8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
    return table


def image_flowables(
    block: dict, project: Path, manuscript_path: Path, styles: dict, max_width: float, config: dict
) -> list:
    path = resolve_asset(project, manuscript_path, block["path"])
    with PILImage.open(path) as image:
        width, height = image.size
    ratio = min(max_width / width, (90 * mm) / height)
    image = Image(str(path), width=width * ratio, height=height * ratio)
    figure_label = labels(config["language"])["figure"]
    return [KeepTogether([image, Paragraph(inline_markup(block["alt"]), styles["caption"])])]


def build_pdf(
    project: Path,
    config: dict,
    markdown: str,
    manuscript_path: Path,
    cover_path: Path,
    regular_font: Path,
    bold_font: Path,
) -> Path:
    register_fonts(regular_font, bold_font)
    styles = pdf_styles(config)
    page_size = PAGE_SIZES[config["page_size"]]
    tmp_dir = project / "tmp" / "pdfs"
    output_dir = project / "output" / "pdf"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    body_pdf = tmp_dir / "body.pdf"
    cover_pdf = tmp_dir / "cover.pdf"
    final_pdf = output_dir / f"{config['output_basename']}.pdf"
    theme = config["theme"]
    ui = labels(config["language"])

    doc = BookDocTemplate(
        str(body_pdf), pagesize=page_size, leftMargin=18 * mm, rightMargin=15 * mm,
        topMargin=19 * mm, bottomMargin=17 * mm, title=config["title"],
        author=config["author"], subject=config["description"],
    )

    def page_header_footer(canvas, current_doc) -> None:
        body_page = canvas.getPageNumber()
        if body_page <= 3:
            return
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#CDD6DC"))
        canvas.setLineWidth(0.4)
        canvas.line(current_doc.leftMargin, page_size[1] - 13 * mm, page_size[0] - current_doc.rightMargin, page_size[1] - 13 * mm)
        canvas.setFont("BookSans", 6.8)
        canvas.setFillColor(colors.HexColor(theme["muted"]))
        canvas.drawString(current_doc.leftMargin, page_size[1] - 10.5 * mm, config["title"][:55])
        canvas.drawCentredString(page_size[0] / 2, 9 * mm, str(body_page + 1))
        canvas.restoreState()

    story = [Spacer(1, 42 * mm), Paragraph(inline_markup(config.get("pdf_title_display", config["title"])).replace("\n", "<br/>"), styles["title"])]
    if config["subtitle"]:
        story.append(Paragraph(inline_markup(config["subtitle"]), styles["subtitle"]))
    story.extend(
        [
            Spacer(1, 18 * mm),
            Paragraph(inline_markup(config["author"]), styles["meta"]),
            Paragraph(display_date(config["date"], config["language"]), styles["meta"]),
            PageBreak(),
            Paragraph(ui["publication"], styles["h2"]),
            Paragraph(f"{ui['title']}: {inline_markup(config['title'])}", styles["imprint"]),
            Paragraph(f"{ui['author']}: {inline_markup(config['author'])}", styles["imprint"]),
            Paragraph(f"{ui['date']}: {display_date(config['date'], config['language'])}", styles["imprint"]),
        ]
    )
    for key in ("email", "edition", "publisher", "copyright"):
        if str(config.get(key, "")).strip():
            story.append(Paragraph(f"{ui[key]}: {inline_markup(str(config[key]))}", styles["imprint"]))
    story.extend([PageBreak(), Paragraph(ui["toc"], styles["h2"])])
    toc = TableOfContents()
    toc.levelStyles = [styles["toc0"], styles["toc1"]]
    story.extend([toc, PageBreak()])

    blocks = publication_blocks(markdown, config["language"])
    heading_counter = 0
    seen_section = False
    current_section = ""
    preface_style = ParagraphStyle("PrefaceBody", parent=styles["body"], leading=14.0, spaceAfter=3.5)
    for block in blocks:
        kind = block["type"]
        if kind == "heading":
            level = block["level"]
            if level == 1:
                continue
            if level == 2:
                current_section = block["text"]
                if seen_section:
                    if current_section in config.get("pdf_continuous_sections", []):
                        story.append(Spacer(1, 16))
                    else:
                        story.append(PageBreak())
                seen_section = True
            heading_counter += 1
            story.append(make_pdf_heading(block["text"], level, styles, heading_counter, theme["secondary"], config.get("pdf_heading_breaks")))
        elif kind == "p":
            story.append(Paragraph(inline_markup(block["text"], link_color=theme["secondary"]), preface_style if current_section.startswith("前言") else styles["body"]))
        elif kind == "quote":
            story.append(Paragraph(inline_markup(block["text"], link_color=theme["secondary"]), styles["quote"]))
        elif kind == "list":
            items = [
                ListItem(Paragraph(inline_markup(item, link_color=theme["secondary"]), styles["list"]), leftIndent=6)
                for item in block["items"]
            ]
            story.append(
                ListFlowable(
                    items, bulletType="1" if block["ordered"] else "bullet",
                    start="1" if block["ordered"] else "•", leftIndent=17,
                    bulletFontName="BookSans", bulletFontSize=8,
                    bulletColor=colors.HexColor(theme["secondary"]), spaceAfter=6,
                )
            )
        elif kind == "table" and block["rows"]:
            table = table_flowable(block["rows"], styles, doc.width, config)
            story.extend([Spacer(1, 3), KeepTogether([table]) if len(block["rows"]) <= 12 else table, Spacer(1, 8)])
        elif kind == "image":
            story.extend(image_flowables(block, project, manuscript_path, styles, doc.width, config))
        elif kind == "code":
            code = html.escape(block["text"], quote=False).replace("\n", "<br/>")
            story.append(Paragraph(code or " ", styles["code"]))

    doc.multiBuild(story, onFirstPage=page_header_footer, onLaterPages=page_header_footer)

    cover_canvas = pdfcanvas.Canvas(str(cover_pdf), pagesize=page_size)
    cover_canvas.setTitle(config["title"])
    cover_canvas.setAuthor(config["author"])
    cover_canvas.drawImage(str(cover_path), 0, 0, width=page_size[0], height=page_size[1], preserveAspectRatio=False, mask="auto")
    cover_canvas.showPage()
    cover_canvas.save()

    writer = PdfWriter()
    for source in (cover_pdf, body_pdf):
        for page in PdfReader(str(source)).pages:
            writer.add_page(page)
    writer.add_metadata({"/Title": config["title"], "/Author": config["author"], "/Subject": config["description"]})
    with final_pdf.open("wb") as handle:
        writer.write(handle)
    return final_pdf


def slugify(text: str) -> str:
    normalized = re.sub(r"\s+", "-", text.strip())
    normalized = re.sub(r"[^\w\u4e00-\u9fff-]", "", normalized)
    return normalized[:80] or "section"


def xhtml_document(title: str, body: str, language: str, body_class: str = "") -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{html.escape(language)}" lang="{html.escape(language)}">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles/book.css"/>
</head>
<body class="{html.escape(body_class)}">
{body}
</body>
</html>
"""


def epub_css(config: dict) -> str:
    theme = config["theme"]
    return f"""
@charset "utf-8";
html {{ font-family: "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", serif; color: {theme['ink']}; }}
body {{ margin: 5%; line-height: 1.75; text-align: justify; }}
body.cover {{ margin: 0; padding: 0; text-align: center; }}
.cover img {{ display: block; width: 100%; height: auto; margin: 0; }}
.title-page {{ min-height: 80vh; display: flex; flex-direction: column; justify-content: center; text-align: center; }}
.title-page p {{ text-indent: 0; }}
h1, h2, h3, h4 {{ font-family: "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", sans-serif; page-break-after: avoid; }}
h2 {{ color: {theme['primary']}; font-size: 1.65em; border-bottom: 0.15em solid {theme['accent']}; padding-bottom: 0.35em; margin-top: 0.6em; }}
h3 {{ color: {theme['secondary']}; font-size: 1.25em; margin-top: 1.5em; }}
h4 {{ color: {theme['accent']}; font-size: 1.05em; margin-top: 1.25em; }}
p {{ text-indent: 2em; margin: 0.55em 0; }}
blockquote {{ margin: 1em 0; padding: 0.8em 1em; background: {theme['paper']}; border-left: 0.35em solid {theme['secondary']}; color: {theme['primary']}; }}
ul, ol {{ padding-left: 1.6em; }} li {{ margin: 0.35em 0; }}
figure {{ margin: 1.4em 0; text-align: center; page-break-inside: avoid; }}
figure img {{ max-width: 100%; height: auto; }}
figcaption {{ color: {theme['muted']}; font-size: 0.82em; margin-top: 0.4em; }}
.table-wrap {{ overflow-x: auto; margin: 1em 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.78em; }}
th {{ background: {theme['primary']}; color: white; padding: 0.55em; text-align: left; }}
td {{ border: 1px solid #c7d1d8; padding: 0.5em; vertical-align: top; }}
tr:nth-child(even) td {{ background: {theme['paper']}; }}
pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: {theme['paper']}; padding: 0.8em; font-size: 0.82em; line-height: 1.5; }}
hr {{ border: 0; border-top: 1px solid #cdd6dc; margin: 1.5em 0; }}
a {{ color: {theme['secondary']}; text-decoration: none; }}
nav ol {{ list-style-type: none; padding-left: 1em; }} nav > ol {{ padding-left: 0; }} nav li {{ margin: 0.45em 0; }}
""".strip()


def block_to_html(block: dict, image_map: dict[Path, str], project: Path, manuscript_path: Path, config: dict) -> str:
    kind = block["type"]
    if kind == "heading":
        level = block["level"]
        text = block["text"]
        return f'<h{level} id="{slugify(text)}">{inline_markup(text, epub=True)}</h{level}>'
    if kind == "p":
        return f"<p>{inline_markup(block['text'], epub=True)}</p>"
    if kind == "quote":
        return f"<blockquote>{inline_markup(block['text'], epub=True)}</blockquote>"
    if kind == "hr":
        return "<hr/>"
    if kind == "list":
        tag = "ol" if block["ordered"] else "ul"
        items = "".join(f"<li>{inline_markup(item, epub=True)}</li>" for item in block["items"])
        return f"<{tag}>{items}</{tag}>"
    if kind == "table":
        rows = block["rows"]
        head = "".join(f"<th>{inline_markup(cell, epub=True)}</th>" for cell in rows[0])
        body = "".join(
            "<tr>" + "".join(f"<td>{inline_markup(cell, epub=True)}</td>" for cell in row) + "</tr>"
            for row in rows[1:]
        )
        return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    if kind == "image":
        source = resolve_asset(project, manuscript_path, block["path"])
        return (
            f'<figure><img src="{image_map[source]}" alt="{html.escape(block["alt"], quote=True)}"/>'
            f"<figcaption>{inline_markup(block['alt'], epub=True)}</figcaption></figure>"
        )
    if kind == "code":
        language = html.escape(block.get("language", ""), quote=True)
        return f'<pre><code class="language-{language}">{html.escape(block["text"])}</code></pre>'
    return ""


def epub_chapters(markdown: str, language: str) -> list[tuple[str, list[dict], list[tuple[str, str]]]]:
    blocks = [
        block for block in publication_blocks(markdown, language)
        if not (block["type"] == "heading" and block["level"] == 1)
    ]
    chapters: list[tuple[str, list[dict], list[tuple[str, str]]]] = []
    current_title = labels(language)["body"]
    current_blocks: list[dict] = []
    subheadings: list[tuple[str, str]] = []
    for block in blocks:
        if block["type"] == "heading" and block["level"] == 2:
            if current_blocks:
                chapters.append((current_title, current_blocks, subheadings))
            current_title = block["text"]
            current_blocks = [block]
            subheadings = []
        else:
            current_blocks.append(block)
            if block["type"] == "heading" and block["level"] == 3:
                subheadings.append((block["text"], slugify(block["text"])))
    if current_blocks:
        chapters.append((current_title, current_blocks, subheadings))
    return chapters or [(labels(language)["body"], [{"type": "p", "text": ""}], [])]


def build_epub(project: Path, config: dict, markdown: str, manuscript_path: Path, cover_path: Path) -> Path:
    output_dir = project / "output" / "epub"
    output_dir.mkdir(parents=True, exist_ok=True)
    final_epub = output_dir / f"{config['output_basename']}.epub"
    build_dir = project / "tmp" / "epub-build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    oebps = build_dir / "OEBPS"
    meta_inf = build_dir / "META-INF"
    (oebps / "styles").mkdir(parents=True)
    (oebps / "images").mkdir(parents=True)
    meta_inf.mkdir(parents=True)

    (build_dir / "mimetype").write_text("application/epub+zip", encoding="ascii")
    (meta_inf / "container.xml").write_text(
        """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
""",
        encoding="utf-8",
    )
    (oebps / "styles" / "book.css").write_text(epub_css(config), encoding="utf-8")

    image_sources = {cover_path}
    for block in parse_markdown_blocks(strip_cover_preamble(markdown)):
        if block["type"] == "image":
            image_sources.add(resolve_asset(project, manuscript_path, block["path"]))
    image_map: dict[Path, str] = {}
    for index, source in enumerate(sorted(image_sources, key=lambda item: (item.name, str(item)))):
        suffix = source.suffix.lower() or ".bin"
        filename = f"img-{index:03d}{suffix}"
        shutil.copy2(source, oebps / "images" / filename)
        image_map[source] = f"images/{filename}"

    language = config["language"]
    ui = labels(language)
    cover_xhtml = xhtml_document(
        config["title"],
        f'<div class="cover"><img src="{image_map[cover_path]}" alt="{html.escape(config["title"], quote=True)}"/></div>',
        language,
        "cover",
    )
    (oebps / "cover.xhtml").write_text(cover_xhtml, encoding="utf-8")
    title_body = (
        '<section class="title-page">'
        f"<h1>{html.escape(config['title'])}</h1>"
        + (f"<p>{html.escape(config['subtitle'])}</p>" if config["subtitle"] else "")
        + f"<p>{html.escape(config['author'])}</p>"
        + (f"<p>{html.escape(config['publisher'])}</p>" if config.get("publisher") else "")
        + (f"<p>邮箱：{html.escape(config['email'])}</p>" if config.get("email") else "")
        + f"<p>{html.escape(display_date(config['date'], language))}</p>"
        + (f"<p>{html.escape(config['edition'])}</p>" if config.get("edition") else "")
        + (f"<p>{html.escape(config['copyright'])}</p>" if config.get("copyright") else "")
        + "</section>"
    )
    (oebps / "title.xhtml").write_text(xhtml_document(config["title"], title_body, language), encoding="utf-8")

    chapter_records = []
    for index, (chapter_title, blocks, subheadings) in enumerate(epub_chapters(markdown, language), start=1):
        filename = f"chapter-{index:03d}.xhtml"
        body = "\n".join(block_to_html(block, image_map, project, manuscript_path, config) for block in blocks)
        (oebps / filename).write_text(xhtml_document(chapter_title, body, language), encoding="utf-8")
        chapter_records.append((filename, chapter_title, subheadings))

    nav_items = [f'<li><a href="title.xhtml">{html.escape(ui["title_page"])}</a></li>']
    for filename, chapter_title, subheadings in chapter_records:
        nested = ""
        if subheadings:
            nested = "<ol>" + "".join(
                f'<li><a href="{filename}#{anchor}">{html.escape(title)}</a></li>'
                for title, anchor in subheadings
            ) + "</ol>"
        nav_items.append(f'<li><a href="{filename}">{html.escape(chapter_title)}</a>{nested}</li>')
    nav_body = (
        '<nav epub:type="toc" id="toc" xmlns:epub="http://www.idpf.org/2007/ops">'
        f"<h1>{html.escape(ui['toc'])}</h1><ol>" + "".join(nav_items) + "</ol></nav>"
    )
    (oebps / "nav.xhtml").write_text(xhtml_document(ui["toc"], nav_body, language), encoding="utf-8")

    ncx_points = [
        f'<navPoint id="nav-title" playOrder="1"><navLabel><text>{html.escape(ui["title_page"])}</text></navLabel><content src="title.xhtml"/></navPoint>'
    ]
    for play_order, (filename, chapter_title, _) in enumerate(chapter_records, start=2):
        ncx_points.append(
            f'<navPoint id="nav-{play_order}" playOrder="{play_order}"><navLabel><text>{html.escape(chapter_title)}</text></navLabel>'
            f'<content src="{filename}"/></navPoint>'
        )
    toc_ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="{html.escape(config['identifier'], quote=True)}"/></head>
  <docTitle><text>{html.escape(config['title'])}</text></docTitle>
  <navMap>{''.join(ncx_points)}</navMap>
</ncx>
"""
    (oebps / "toc.ncx").write_text(toc_ncx, encoding="utf-8")

    image_items = []
    cover_image_id = ""
    for index, source in enumerate(sorted(image_sources, key=lambda item: (item.name, str(item)))):
        href = image_map[source]
        media = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
        item_id = f"image-{index}"
        properties = ' properties="cover-image"' if source == cover_path else ""
        if source == cover_path:
            cover_image_id = item_id
        image_items.append(f'<item id="{item_id}" href="{href}" media-type="{media}"{properties}/>')
    chapter_items = "".join(
        f'<item id="chapter-{index}" href="{filename}" media-type="application/xhtml+xml"/>'
        for index, (filename, _, _) in enumerate(chapter_records, start=1)
    )
    spine_items = "".join(f'<itemref idref="chapter-{index}"/>' for index in range(1, len(chapter_records) + 1))
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="{html.escape(language)}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{html.escape(config['identifier'])}</dc:identifier>
    <dc:title>{html.escape(config['title'])}</dc:title>
    <dc:creator>{html.escape(config['author'])}</dc:creator>
    <dc:publisher>{html.escape(config.get('publisher', ''))}</dc:publisher>
    <dc:language>{html.escape(language)}</dc:language>
    <dc:date>{config['date']}</dc:date>
    <dc:description>{html.escape(config['description'])}</dc:description>
    <meta property="dcterms:modified">{config['date']}T00:00:00Z</meta>
    <meta name="cover" content="{cover_image_id}"/>
  </metadata>
  <manifest>
    <item id="css" href="styles/book.css" media-type="text/css"/>
    <item id="cover-page" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="title-page" href="title.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    {''.join(image_items)}
    {chapter_items}
  </manifest>
  <spine toc="ncx">
    <itemref idref="cover-page" linear="yes"/>
    <itemref idref="title-page"/>
    <itemref idref="nav"/>
    {spine_items}
  </spine>
</package>
"""
    (oebps / "content.opf").write_text(opf, encoding="utf-8")

    final_epub.unlink(missing_ok=True)
    with zipfile.ZipFile(final_epub, "w") as archive:
        archive.write(build_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(build_dir.rglob("*")):
            if path.is_dir() or path == build_dir / "mimetype":
                continue
            archive.write(path, path.relative_to(build_dir), compress_type=zipfile.ZIP_DEFLATED)
    return final_epub


def package_markdown(project: Path, config: dict, markdown: str, manuscript_path: Path) -> Path:
    output_dir = project / "output" / "markdown"
    asset_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    if asset_dir.exists():
        shutil.rmtree(asset_dir)
    asset_dir.mkdir(parents=True)
    replacements: dict[str, str] = {}
    image_blocks = [block for block in parse_markdown_blocks(markdown) if block["type"] == "image"]
    for index, block in enumerate(image_blocks, start=1):
        raw = block["path"]
        if raw in replacements:
            continue
        source = resolve_asset(project, manuscript_path, raw)
        filename = f"{index:03d}-{safe_basename(source.stem)}{source.suffix.lower()}"
        shutil.copy2(source, asset_dir / filename)
        replacements[raw] = f"assets/{filename}"
    packaged = markdown
    for raw, replacement in replacements.items():
        packaged = packaged.replace(f"]({raw})", f"]({replacement})")
    output = output_dir / f"{config['output_basename']}.md"
    output.write_text(packaged.rstrip() + "\n", encoding="utf-8")
    return output


def lightweight_validate(config: dict, markdown_path: Path, pdf_path: Path, epub_path: Path) -> None:
    markdown = markdown_path.read_text(encoding="utf-8")
    if config["title"] not in markdown or config["author"] not in markdown:
        raise ValueError("Packaged Markdown is missing the configured title or author")
    reader = PdfReader(str(pdf_path))
    if len(reader.pages) < 4:
        raise ValueError(f"PDF is unexpectedly short: {len(reader.pages)} pages")
    with zipfile.ZipFile(epub_path) as archive:
        if archive.namelist()[0] != "mimetype" or archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("Invalid EPUB ZIP structure")
        if config["title"].encode("utf-8") not in archive.read("OEBPS/content.opf"):
            raise ValueError("EPUB metadata is missing the configured title")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    config = load_config(project)
    manuscript_path = project_path(project, config["manuscript"])
    if not manuscript_path.exists():
        raise FileNotFoundError(f"Missing manuscript: {manuscript_path}")
    markdown = manuscript_path.read_text(encoding="utf-8")
    if len(markdown.strip()) < 100:
        raise ValueError("Manuscript is too short to publish")

    regular_font = first_existing(project, str(config.get("font_regular", "")), FONT_CANDIDATES)
    bold_font = first_existing(project, str(config.get("font_bold", "")), BOLD_FONT_CANDIDATES)
    cover = create_cover(project, config, regular_font, bold_font)
    markdown_output = package_markdown(project, config, markdown, manuscript_path)
    pdf_output = build_pdf(project, config, markdown, manuscript_path, cover, regular_font, bold_font)
    epub_output = build_epub(project, config, markdown, manuscript_path, cover)
    lightweight_validate(config, markdown_output, pdf_output, epub_output)

    print(f"MARKDOWN={markdown_output}")
    print(f"PDF={pdf_output}")
    print(f"EPUB={epub_output}")
    print(f"PDF_PAGES={len(PdfReader(str(pdf_output)).pages)}")
    print(f"MARKDOWN_CHARS={len(markdown)}")


if __name__ == "__main__":
    main()
