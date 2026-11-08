#!/usr/bin/env python3
"""Use build-ebook and keep companion-material links useful in each edition."""

import argparse
import importlib.util
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.etree import ElementTree as ET


def refine_layout(publisher):
    original_styles = publisher.pdf_styles
    original_spacer = publisher.Spacer

    def spacer(width, height, *args, **kwargs):
        result = original_spacer(width, height, *args, **kwargs)
        # The native builder inserts a 3pt spacer immediately before tables.
        # Carry the heading's keep-with-next through that spacer to the table.
        if height == 3:
            result.keepWithNext = True
        return result

    def styles(config):
        result = original_styles(config)
        result["body"].leading = 14.6
        result["h2"].fontSize, result["h2"].leading = 19.5, 26
        result["h3"].fontSize, result["h3"].leading = 12.4, 18.3
        result["h3"].spaceBefore, result["h3"].spaceAfter = 10, 5
        result["list"].fontSize, result["list"].leading = 8.8, 12.5
        result["list"].spaceAfter = 1
        result["table"].fontSize, result["table"].leading = 7.2, 10.5
        return result

    def table(rows, styles, width, config):
        count = max(map(len, rows))
        ratios = {2: [0.27, 0.73], 3: [0.22, 0.36, 0.42], 4: [0.20, 0.31, 0.31, 0.18]}.get(count)
        ratios = ratios or [1 / count] * count
        data = [[publisher.Paragraph(publisher.inline_markup(cell), styles["table_header"] if index == 0 else styles["table"])
                 for cell in row + [""] * (count - len(row))] for index, row in enumerate(rows)]
        result = publisher.LongTable(data, colWidths=[width * ratio for ratio in ratios], repeatRows=1, hAlign="LEFT")
        result.setStyle([
            ("BACKGROUND", (0, 0), (-1, 0), publisher.colors.HexColor(config["theme"]["primary"])),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [publisher.colors.white, publisher.colors.HexColor(config["theme"]["paper"])]),
            ("GRID", (0, 0), (-1, -1), 0.35, publisher.colors.HexColor("#C7D1D8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
        if result.wrap(width, 10000)[1] < 380:
            result.splitByRow = 0
        return result

    publisher.pdf_styles, publisher.table_flowable = styles, table
    publisher.Spacer = spacer


def complete_epub_metadata(epub, config):
    opf_ns, dc_ns = "http://www.idpf.org/2007/opf", "http://purl.org/dc/elements/1.1/"
    ET.register_namespace("", opf_ns)
    ET.register_namespace("dc", dc_ns)
    with zipfile.ZipFile(epub) as source:
        entries = [(info, source.read(info.filename)) for info in source.infolist()]
    updated = []
    for info, data in entries:
        if info.filename == "OEBPS/content.opf":
            root = ET.fromstring(data)
            metadata = root.find(f"{{{opf_ns}}}metadata")
            ET.SubElement(metadata, f"{{{dc_ns}}}publisher").text = config["publisher"]
            ET.SubElement(metadata, f"{{{dc_ns}}}rights").text = config["copyright"]
            data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        elif info.filename == "OEBPS/title.xhtml":
            extra = f'<p>出版：{publisher_text(config["publisher"])}</p><p>{publisher_text(config["edition"])}</p>'
            data = data.decode("utf-8").replace("</section>", extra + "</section>").encode("utf-8")
        updated.append((info, data))
    temporary = epub.with_suffix(".building")
    with zipfile.ZipFile(temporary, "w") as target:
        for info, data in updated:
            target.writestr(info, data)
    temporary.replace(epub)


def publisher_text(value):
    import html
    return html.escape(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=Path.home() / ".codex/skills/build-ebook")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("ebook_publisher", args.skill_dir / "scripts/build_ebook.py")
    publisher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(publisher)
    refine_layout(publisher)
    config = publisher.load_config(project)
    manuscript = publisher.project_path(project, config["manuscript"])
    original = manuscript.read_text(encoding="utf-8")
    web_text = original
    local_links = {}
    repository_path = f"{config['repository_url']}/blob/{config['repository_branch']}/books/office-agent/"
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", original):
        raw = match.group(1)
        url = urlsplit(raw)
        if url.scheme or not url.path:
            continue
        target = (manuscript.parent / url.path).resolve()
        if not target.is_file():
            raise FileNotFoundError(f"Missing companion material: {raw}")
        relative = target.relative_to(project).as_posix()
        fragment = f"#{url.fragment}" if url.fragment else ""
        local_links[raw] = f"companion/{relative}{fragment}"
        web_text = web_text.replace(f"]({raw})", f"]({repository_path}{quote(relative)}{fragment})")

    regular = publisher.first_existing(project, config.get("font_regular", ""), publisher.FONT_CANDIDATES)
    bold = publisher.first_existing(project, config.get("font_bold", ""), publisher.BOLD_FONT_CANDIDATES)
    cover = publisher.create_cover(project, config, regular, bold)
    (project / "assets").mkdir(exist_ok=True)
    shutil.copy2(cover, project / "assets/cover.jpg")
    markdown = publisher.package_markdown(project, config, original, manuscript)
    companion = markdown.parent / "companion"
    shutil.copytree(project / "examples", companion / "examples", dirs_exist_ok=True)
    shutil.copy2(project / "sources.md", companion / "sources.md")
    packaged = markdown.read_text(encoding="utf-8")
    for raw, replacement in local_links.items():
        packaged = packaged.replace(f"]({raw})", f"]({replacement})")
    markdown.write_text(packaged, encoding="utf-8")
    pdf = publisher.build_pdf(project, config, web_text, manuscript, cover, regular, bold)
    epub = publisher.build_epub(project, config, web_text, manuscript, cover)
    complete_epub_metadata(epub, config)
    publisher.lightweight_validate(config, markdown, pdf, epub)
    print(json.dumps({"markdown": str(markdown), "pdf": str(pdf), "epub": str(epub)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
