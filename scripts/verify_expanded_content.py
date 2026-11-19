#!/usr/bin/env python3
"""Verify the twelve expanded manuscripts and, optionally, their release packages."""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import re
import subprocess
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
TAG = 'expanded-books-20261119-v1.1'
SPECS = [
    ('after-disconnection', '断网之后', 17, 18, 50),
    ('good-technology', '好技术的尺度', 17, 23, 50),
    ('idea-to-work', '从想法到作品', 19, 21, 51),
    ('customer-decisions', '客户如何决定', 17, 20, 50),
    ('machine-companionship', '机器陪伴', 18, 25, 51),
    ('organizational-memory', '组织记忆', 17, 20, 50),
    ('restraint', '克制', 17, 21, 51),
    ('quantified-self', '被量化的自己', 18, 21, 50),
    ('solo-editorial', '一人编辑部', 18, 21, 51),
    ('professional-judgment', '答案之后：AI 时代的专业判断', 28, 15, 52),
    ('solo-company', '一人公司的真实边界', 29, 16, 54),
    ('ai-native-sales', 'AI 原生销售：从工具提效到决策共创', 31, 16, 56),
]
DIGITS = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
          '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

def chinese_number(value):
    if len(value) == 1:
        return DIGITS[value]
    if len(value) == 2 and value[0] == '十':
        return 10 + DIGITS[value[1]]
    if len(value) == 2 and value[1] == '十':
        return DIGITS[value[0]] * 10
    if len(value) == 3 and value[1] == '十':
        return DIGITS[value[0]] * 10 + DIGITS[value[2]]
    raise ValueError(value)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('--artifacts', action='store_true')
args = parser.parse_args()
results = []
for slug, title, original_pages, expected_chapters, expected_pages in SPECS:
    project = ROOT / 'books' / slug
    config = json.loads((project / 'book.json').read_text())
    text = (project / 'manuscript/book.md').read_text()
    assert config['title'] == title and config['author'] == '李钊'
    assert config['edition'] == '增订版 · 1.1' and config['page_size'] == 'A5'
    if slug in {'professional-judgment', 'solo-company', 'ai-native-sales'}:
        assert '增订日期：2026-11-19' in text and '版本：增订版 · 1.1' in text
    else:
        # The nine short books preserve their original title pages; the build
        # metadata carries the new edition and revision date.
        assert config['revision'] == '2026-11-19'
        assert re.search(r'增订：2026 年 11 月 19 日', text) or slug in {
            'organizational-memory', 'restraint', 'quantified-self', 'solo-editorial'}
    assert len(text) >= 16000, (slug, len(text))
    placeholders = re.findall(r'TODO|TBD|待补充|待完善|后续补写|此处省略|第X章|XXX|Lorem ipsum', text, re.I)
    assert not placeholders, (slug, placeholders)
    raw_headings = re.findall(r'^## (第([0-9]{2}|[一二三四五六七八九十]+)章)[　 \t]*([^\n]*)', text, re.M)
    numbers = [int(number) if number.isdigit() else chinese_number(number) for _, number, _ in raw_headings]
    assert numbers == list(range(1, expected_chapters + 1)), (slug, numbers)
    original = subprocess.run(
        ['git', 'show', f'HEAD:books/{slug}/manuscript/book.md'],
        cwd=ROOT, check=True, capture_output=True, text=True).stdout
    original_count = 7 if slug == 'professional-judgment' else 8
    old_headings = re.findall(r'^## (第(?:[0-9]{2}|[一二三四五六七八九十]+)章)[^\n]*', original, re.M)
    assert len(old_headings) == original_count, (slug, old_headings)
    current_labels = [heading for heading, _, _ in raw_headings]
    assert current_labels[:original_count] == old_headings, (slug, 'Original chapter order changed')
    paragraphs = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', text)]
    duplicates = [p for p, count in Counter(paragraphs).items() if len(p) >= 120 and count > 1]
    assert not duplicates, (slug, 'duplicate long paragraphs', duplicates)
    if slug in {'professional-judgment', 'solo-company', 'ai-native-sales'}:
        start = '## 第08章' if slug == 'professional-judgment' else '## 第09章'
        addition = text[text.index(start):text.index('## 来源与方法说明')]
        assert not re.findall(r'https?://', addition), (slug, 'New external URL')
        assert '2026-11-19 增订版新增内容边界' in (project / 'SOURCES.md').read_text()
        expected_nav = {'professional-judgment': 98, 'solo-company': 96, 'ai-native-sales': 105}[slug]
        assert config['quality_contract']['expected_chapters'] == expected_chapters
    else:
        expected_nav = None
    readme = (project / 'README.md').read_text()
    assert 'new-books-20261119-v1.1' not in readme, (slug, 'wrong release tag')
    if args.artifacts:
        assert f'releases/download/{TAG}/' in readme, (slug, 'missing release links')
        log = (project / 'REVISION_LOG.md').read_text()
        rounds = [int(n) for n in re.findall(r'^(\d+)\. \*\*', log, re.M)]
        assert rounds == list(range(1, 21)), (slug, rounds)
        qa = (project / 'QA_REPORT.md').read_text()
        assert f'原 PDF {original_pages} 页' in qa, (slug, 'wrong original pages in QA')
        release = project / 'release'
        files = {name: release / name for name in [f'{slug}.pdf', f'{slug}.epub', f'{slug}-markdown.zip']}
        assert all(path.is_file() for path in files.values()), slug
        with zipfile.ZipFile(files[f'{slug}-markdown.zip']) as archive:
            assert archive.testzip() is None
        pages = len(PdfReader(files[f'{slug}.pdf']).pages)
        assert pages == expected_pages and pages >= 50, (slug, pages)
        report = json.loads((project / 'tmp/validation-report.json').read_text())
        assert report['pdf']['pages'] == pages and report['render']['rendered_pages'] == pages
        assert not report['pdf']['blank_pages']
    else:
        expected_nav = None
    results.append({'slug': slug, 'title': title, 'original_pages': original_pages,
                    'chapters': expected_chapters, 'characters': len(text),
                    'question_template_count': text.count('不要急着问'),
                    'not_but_pattern_count': len(re.findall(r'不是[^\n。；]{0,50}而是', text))})

solo = (ROOT / 'books/solo-company/manuscript/book.md').read_text()
rows = re.findall(r'^\| (W\d{2}) \| ([\d,]+) \| ([\d,]+)(?:（[^|]+）)? \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|$', solo, re.M)
assert len(rows) == 13, ('cash-flow rows', len(rows))
for week, opening, receipts, variable, fixed, closing in rows:
    values = [int(value.replace(',', '')) for value in [opening, receipts, variable, fixed, closing]]
    assert values[0] + values[1] - values[2] - values[3] == values[4], (week, values)
for label, expected in {'W04': 12000, 'W08': 11000, 'W12': 15000, 'W13': 13000}.items():
    row = next(row for row in rows if row[0] == label)
    assert int(row[-1].replace(',', '')) == expected
assert 'W05 期末会从 17,000 降至 8,000；W06 补收后回到原表同期 15,000' in solo
assert '15,000＋9,000－2,000－6,000－1,000＝15,000' in solo
assert '新收入 0－固定费用 2,000－收尾支持 1,000－非交付机会成本 3,000＝－6,000' in solo
sales = (ROOT / 'books/ai-native-sales/manuscript/book.md').read_text()
for claim in ['首次正确来源引用只有 44 个，低于 48 个，未通过',
              '外部费用合计 48,000 元', '年度能力等价为 9,600 元']:
    assert claim in sales, claim

output = {'status': 'passed', 'artifact_checks': args.artifacts, 'release_tag': TAG,
          'books': results, 'total_expected_pages': sum(s[4] for s in SPECS),
          'solo_company_cash_flow_rows_checked': len(rows)}
assert output['total_expected_pages'] == 616
report_path = ROOT / 'tmp/expanded-content-verification.json'
report_path.parent.mkdir(exist_ok=True)
report_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(output, ensure_ascii=False, indent=2))
