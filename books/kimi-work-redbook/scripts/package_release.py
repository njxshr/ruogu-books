#!/usr/bin/env python3
"""Package the checked Kimi Work Redbook reading editions for GitHub Release."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

project = Path(__file__).resolve().parents[1]
config = json.loads((project / "book.json").read_text(encoding="utf-8"))
base = config["output_basename"]
markdown = project / "output" / "markdown" / f"{base}.md"
pdf = project / "output" / "pdf" / f"{base}.pdf"
epub = project / "output" / "epub" / f"{base}.epub"
release = project / "release"
release.mkdir(parents=True, exist_ok=True)

shutil.copy2(pdf, release / "kimi-work-redbook.pdf")
shutil.copy2(epub, release / "kimi-work-redbook.epub")
shutil.copy2(project / "tmp" / "cover-final.jpg", project / "assets" / "preview" / "cover.jpg")

archive_path = release / "kimi-work-redbook-markdown.zip"
with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    archive.write(markdown, f"{base}.md")
    for asset in sorted((markdown.parent / "assets").iterdir()):
        if asset.is_file():
            archive.write(asset, f"assets/{asset.name}")

lines = []
for name in ("kimi-work-redbook.pdf", "kimi-work-redbook.epub", "kimi-work-redbook-markdown.zip"):
    path = release / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {name}")
    print(f"{name}: {path.stat().st_size} bytes; sha256={digest}")
(release / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
