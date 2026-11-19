#!/usr/bin/env python3
"""Update the two public book catalogues without duplicating existing entries."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TAG = 'expanded-books-20261119-v1.1'
BOOKS = [
    ('after-disconnection', '断网之后', 50),
    ('good-technology', '好技术的尺度', 50),
    ('idea-to-work', '从想法到作品', 51),
    ('customer-decisions', '客户如何决定', 50),
    ('machine-companionship', '机器陪伴', 51),
    ('organizational-memory', '组织记忆', 50),
    ('restraint', '克制', 51),
    ('quantified-self', '被量化的自己', 50),
    ('solo-editorial', '一人编辑部', 51),
    ('professional-judgment', '答案之后：AI 时代的专业判断', 52),
    ('solo-company', '一人公司的真实边界', 54),
    ('ai-native-sales', 'AI 原生销售：从工具提效到决策共创', 56),
]
for filename in ['README.md', '目录.md']:
    path = ROOT / filename
    text = path.read_text()
    lines = text.splitlines()
    found = set()
    for index, line in enumerate(lines):
        for slug, title, pages in BOOKS:
            if not line.startswith('| [') or f'](books/{slug}/README.md)' not in line:
                continue
            assert title in line and slug not in found, (filename, slug)
            found.add(slug)
            line, count = re.subn(r'PDF（\d+页）', f'PDF（{pages}页）', line)
            assert count == 1, (filename, slug, 'PDF page count')
            line, count = re.subn(
                rf'releases/download/[^/]+/(?={re.escape(slug)}(?:\.|-markdown\.zip))',
                f'releases/download/{TAG}/', line)
            assert count == 3, (filename, slug, count)
            if slug in {'professional-judgment', 'solo-company', 'ai-native-sales'}:
                line = line.replace('第一版 · 1.0；2026-11-10 | 2026-11-10 |',
                                    '增订版 · 1.1；原书 2026-11-10 | 2026-11-19 |')
            else:
                line = line.replace('第一版 · 2026-11-11',
                                    '增订版 · 1.1；原书 2026-11-11；2026-11-19 增订')
            lines[index] = line
    assert found == {book[0] for book in BOOKS}, (filename, found)
    text = '\n'.join(lines) + '\n'
    old_heading = '## 2026-11-11 新书九种'
    assert text.count(old_heading) == 1
    text = text.replace(old_heading, '## 2026-11-19 增订：九种短篇')
    old_intro = '九本均为李钊著，保留原书出版单位“晓翊工作室”，由若谷书房整理上架。每本含八章、前言、附录与参考资料。'
    assert text.count(old_intro) == 1
    text = text.replace(old_intro,
        '九本均为李钊著，保留原书出版单位“晓翊工作室”、原日期和原八章，由若谷书房整理上架。2026-11-19 增订版 1.1 增加实践章节与工作表，每本完成 20 轮有记录的内容与质量工作，PDF 均达到 50 页以上。')
    old_link = '[本批次下载与校验和](https://github.com/njxshr/ruogu-books/releases/tag/new-books-20261111-v1.0)'
    assert text.count(old_link) == 1
    text = text.replace(old_link,
        f'[本批增订版下载与总校验表](https://github.com/njxshr/ruogu-books/releases/tag/{TAG})')
    text = text.replace('从客户研究到验证、谈判与复盘的八阶段协作方法。',
                        '从客户研究、价值验证到方案承诺与上线交接的协作方法。')
    if filename == 'README.md':
        text = text.replace('现有十本成品书均提供 Markdown 在线阅读、PDF、EPUB 和包含配套材料的 Markdown 离线包。',
                            '各本已上架作品均提供 Markdown 在线阅读、PDF、EPUB 和包含实际生成资源的 Markdown 离线包。')
        text = text.replace('《答案之后》《一人公司的真实边界》《AI 原生销售》见 [A1—A3 第一版 Release](https://github.com/njxshr/ruogu-books/releases/tag/a1-a3-v1.0)。',
                            f'十二本增订版见 [2026-11-19 增订 Release](https://github.com/njxshr/ruogu-books/releases/tag/{TAG})；原出版记录仍保留。')
        old_status = 'A1《答案之后》、A2《一人公司的真实边界》、A3《AI 原生销售》已完成第一版 1.0 并发布；A4—A6、B1—B6 九种已于 2026-11-11 完成第一版并上架。'
        assert text.count(old_status) == 1
        text = text.replace(old_status,
            'A1—A3 与 A4—A6、B1—B6 十二本已于 2026-11-19 完成增订版 1.1；其他既有作品和上架记录保留。')
    else:
        old_status = 'A1—A3 已完成第一版并发布；A4—A6、B1—B6 九种已于 2026-11-11 上架，见上表。'
        assert text.count(old_status) == 1
        text = text.replace(old_status,
            'A1—A3 与 A4—A6、B1—B6 十二本已于 2026-11-19 完成增订版 1.1；其他既有作品和上架记录保留。')
    path.write_text(text)
    print(filename, 'updated', len(BOOKS), 'books')
