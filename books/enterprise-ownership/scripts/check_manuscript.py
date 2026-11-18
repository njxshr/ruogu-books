#!/usr/bin/env python3
"""Content-only checks for the C1 manuscript; does not claim PDF/EPUB validation."""
from pathlib import Path
import collections
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "book.md"
text = MANUSCRIPT.read_text(encoding="utf-8")
lines = text.splitlines()
errors = []
notes = []

def require(condition, message):
    if not condition:
        errors.append(message)

require(text.startswith("# 企业的制度剖面\n\n央企、国企、混合所有制与私企\n"), "front matter title/subtitle mismatch")
require("作者：李钊" in text and "日期：2026 年 11 月 17 日" in text, "author/date missing")
require("版本：第一版 · 1.0" in text, "edition missing")
require("工作室与出版单位：若谷书房" in text, "publisher missing")
require(text.count("../assets/diagram-analysis-chain.png") == 1 and text.count("../assets/diagram-performance.png") == 1, "two diagrams must be referenced once each")

expected = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五"]
chapters = re.findall(r"^## 第([一二三四五六七八九十]+)章　(.+)$", text, re.M)
require([n for n, _ in chapters] == expected, f"chapter sequence mismatch: {[n for n, _ in chapters]}")
require(len(re.findall(r"^### 本章小结$", text, re.M)) == 15, "every chapter must have one summary")
for title in ["## 第一篇　概念与制度地图", "## 第二篇　分类型运行剖析", "## 第三篇　放在同一把尺上比较", "## 第四篇　进入真实场景", "## 附录 A　企业制度分析工作表", "## 附录 B　常见概念速查", "## 附录 C　综合示例：同一行业，三种制度组合", "## 参考资料"]:
    require(title in text, f"missing major section: {title}")

for marker in ["TODO", "TBD", "待写", "待补", "说明本书为什么值得读", "从读者的问题出发", "作为一名AI", "作为 AI", "哪种企业更好", "哪类企业必然更好"]:
    require(marker not in text, f"placeholder or meta text found: {marker}")

# Narrative prose should explain mechanisms directly. Keep functional questions
# in tables, numbered/bulleted checklists, and URL query strings.
paired_contrasts = re.findall(r"(?:不是|并非|并不是|不在于)[^。\n]{0,100}?(?:而是|而在于)", text)
require(not paired_contrasts, f"templated paired contrasts found: {paired_contrasts}")
narrative_questions = []
in_references = False
for line_number, line in enumerate(lines, 1):
    if line.startswith("## 参考资料"):
        in_references = True
    if in_references or line.startswith("|") or line.startswith("-") or re.match(r"^\d+\.", line):
        continue
    without_urls = re.sub(r"https?://\S+", "", line)
    if "？" in without_urls or "?" in without_urls:
        narrative_questions.append(line_number)
require(not narrative_questions, f"question marks in narrative prose near lines: {narrative_questions}")

paragraphs = [re.sub(r"\s+", "", p) for p in re.split(r"\n\s*\n", text)]
long_paragraphs = [p for p in paragraphs if len(p) > 80 and not p.startswith("|")]
duplicates = [p[:50] for p, n in collections.Counter(long_paragraphs).items() if n > 1]
require(not duplicates, f"duplicate long paragraphs: {duplicates}")

require("## 参考资料" in text, "references missing")
body, refs = text.split("## 参考资料", 1)
body_urls = set(re.findall(r"\]\((https?://[^)]+)\)", body))
ref_urls = set(re.findall(r"\]\((https?://[^)]+)\)", refs))
require(body_urls == ref_urls, f"inline/reference URL mismatch: body-only={body_urls-ref_urls}; refs-only={ref_urls-body_urls}")
require(len(ref_urls) == 17, f"expected 17 unique sources, got {len(ref_urls)}")
require(len(re.findall(r"^\d+\. \[", refs, re.M)) == 17, "reference numbering must be 1-17")

# Check pipe-table column counts within each contiguous table.
i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        block = []
        start = i + 1
        while i < len(lines) and lines[i].startswith("|"):
            block.append(lines[i])
            i += 1
        counts = [line.count("|") for line in block]
        require(len(set(counts)) == 1, f"inconsistent table columns near line {start}: {counts}")
        if len(block) >= 2:
            require(bool(re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", block[1])), f"table separator missing near line {start}")
    else:
        i += 1

config = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
require(config["author"] == "李钊" and config["publisher"] == "若谷书房", "config branding mismatch")
require(config["edition"] == "第一版 · 1.0", "config edition mismatch")
require(config["date"] == "2026-11-17", "config date mismatch")
require(config.get("cover_background") == "assets/cover-background.png", "cover background missing")
require((ROOT / config["cover_background"]).is_file(), "cover background file missing")
for image in ("diagram-analysis-chain.png", "diagram-performance.png"):
    require((ROOT / "assets" / image).is_file(), f"diagram missing: {image}")
require(config.get("quality_contract", {}).get("expected_chapters") == 15, "quality contract chapter count mismatch")
require(config.get("publisher_slogan") == "内容来自全人类的智慧，感谢AI的高效率整合", "publisher slogan mismatch")

ledger = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
ids = re.findall(r"\| C1-(\d{2}) \|", ledger)
require(ids == [f"{n:02d}" for n in range(1, 18)], f"source ledger IDs mismatch: {ids}")

notes.extend([
    f"chapters={len(chapters)}",
    f"chapter_summaries={len(re.findall(r'^### 本章小结$', text, re.M))}",
    f"unique_sources={len(ref_urls)}",
    f"characters_including_markup={len(text)}",
    f"real_case_mentions={text.count('真实案例')}",
    f"composite_case_mentions={text.count('综合案例')}",
    f"illustrative_case_mentions={text.count('示意情境')}",
])
for note in notes:
    print(note)
if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)
print("PASS: content-only manuscript checks")
