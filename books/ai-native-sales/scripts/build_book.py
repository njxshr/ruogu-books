#!/usr/bin/env python3
"""Build this book through build-ebook with Chinese typography and table pagination."""
import importlib.util
import sys
from pathlib import Path
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
        result["title"].fontSize = 22
        result["h2"].fontSize, result["h2"].leading = 18, 25
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



if __name__ == "__main__":
    skill = Path.home()/".codex/skills/build-ebook/scripts/build_ebook.py"
    spec = importlib.util.spec_from_file_location("publisher", skill)
    publisher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(publisher)
    refine_layout(publisher)
    sys.argv = [str(skill), "--project", str(Path(__file__).resolve().parents[1])]
    publisher.main()
