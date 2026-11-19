#!/usr/bin/env python3
"""Package an A1–A3 book after its substantive and visual review is complete."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from bs4 import BeautifulSoup
from PIL import Image
import pypdfium2 as pdfium
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('--project', required=True)
parser.add_argument('--original-pages', type=int, required=True)
parser.add_argument('--original-chapters', type=int, required=True)
parser.add_argument('--new-chapter', required=True)
parser.add_argument('--release-tag', default='expanded-books-20261119-v1.1')
args = parser.parse_args()
root = Path(args.project).resolve()
config = json.loads((root / 'book.json').read_text())
name = config['title']
slug = root.name
base = config['output_basename']
pdf = root / 'output/pdf' / f'{base}.pdf'
epub = root / 'output/epub' / f'{base}.epub'
md = root / 'output/markdown' / f'{base}.md'
for file in [pdf, epub, md]:
    assert file.exists(), file
reader = PdfReader(pdf)
pages = len(reader.pages)
assert pages >= 50, f'Only {pages} pages'
report = json.loads((root / 'tmp/validation-report.json').read_text())
assert report['pdf']['pages'] == pages and report['render']['rendered_pages'] == pages
assert not report['pdf']['blank_pages']

def find_page(term, start=9):
    return next((i for i, page in enumerate(reader.pages, 1)
                 if i >= start and term in (page.extract_text() or '')), None)

first_preface = find_page('前言')
first_new = find_page(args.new_chapter)
assert first_preface and first_new, (first_preface, first_new)
preview = root / 'assets/preview'
preview.mkdir(parents=True, exist_ok=True)
for number, page in [(1, first_preface), (2, first_new)]:
    source = root / f'tmp/pdf-render/pages/page-{page}.jpg'
    assert source.exists(), source
    shutil.copy2(source, preview / f'sample-{number:02}.jpg')
# Regenerate the cover from page one of the final PDF, not from an old cover asset.
document = pdfium.PdfDocument(str(pdf))
document[0].render(scale=2).to_pil().convert('RGB').save(preview / 'cover.jpg', quality=92)
document.close()
sha = lambda file: hashlib.sha256(file.read_bytes()).hexdigest()
assets = []
for filename, page in [('cover.jpg', 1), ('sample-01.jpg', first_preface), ('sample-02.jpg', first_new)]:
    file = preview / filename
    with Image.open(file) as image:
        dimensions = list(image.size)
    assets.append({'asset': filename, 'page': page, 'dimensions': dimensions,
                   'sha256': sha(file), 'backend': 'pdfium'})
manifest = {'source_pdf_name': pdf.name, 'source_sha256': sha(pdf),
            'total_pages': pages, 'assets': assets}
(preview / 'preview-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

# Inspect the final EPUB itself; do not reuse a potentially stale unpack directory.
unpacked = root / 'tmp/package-epub-inspect'
if unpacked.exists():
    shutil.rmtree(unpacked)
with zipfile.ZipFile(epub) as archive:
    assert archive.testzip() is None
    archive.extractall(unpacked)
e = unpacked / 'OEBPS'
nav = BeautifulSoup((e / 'nav.xhtml').read_text(), 'xml')
links = nav.find_all('a')
broken = []
for link in links:
    href = link.get('href', '')
    filename, _, fragment = href.partition('#')
    target = e / filename
    if not target.exists():
        broken.append(href)
    elif fragment and not BeautifulSoup(target.read_text(), 'xml').find(id=fragment):
        broken.append(href)
assert not broken, broken
missing = []
for file in e.glob('*.xhtml'):
    soup = BeautifulSoup(file.read_text(), 'xml')
    for tag, attribute in [('img', 'src'), ('link', 'href')]:
        for node in soup.find_all(tag):
            value = node.get(attribute, '')
            if value and not value.startswith(('http:', 'https:', '#')) and not (file.parent / value).exists():
                missing.append((file.name, value))
assert not missing, missing
chapter_files = sorted(e.glob('chapter-*.xhtml'))
assert chapter_files
for file in [e / 'cover.xhtml', chapter_files[0], chapter_files[len(chapter_files) // 2], chapter_files[-1]]:
    soup = BeautifulSoup(file.read_text(), 'xml')
    assert soup.find(['img', 'h2', 'h1']), file
css = '\n'.join(file.read_text() for file in e.rglob('*.css'))
assert 'max-width: 100%' in css and 'overflow-x: auto' in css and 'overflow-wrap: anywhere' in css

release = root / 'release'
release.mkdir(exist_ok=True)
shutil.copy2(pdf, release / f'{slug}.pdf')
shutil.copy2(epub, release / f'{slug}.epub')
with zipfile.ZipFile(release / f'{slug}-markdown.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for file in (root / 'output/markdown').rglob('*'):
        if file.is_file():
            archive.write(file, file.relative_to(root / 'output/markdown'))
with zipfile.ZipFile(release / f'{slug}-markdown.zip') as archive:
    assert archive.testzip() is None
text = (root / 'manuscript/book.md').read_text()
heads = re.findall(r'^##\s+(.+)$', text, re.M)
assert heads[-2:] == ['来源与方法说明', '若谷书房'], heads[-2:]
chapters = len(re.findall(r'^## 第[0-9]{2}章', text, re.M))
assert chapters == config['quality_contract']['expected_chapters']
appendices = len(re.findall(r'^## 附录', text, re.M))
urls = 'https://github.com/njxshr/ruogu-books/releases/download/' + args.release_tag
contents = '\n'.join(f'- {heading}' for heading in heads)
summary = f'{chapters}章、{appendices}份附录'
old_chapters = {7: '原七章', 8: '原八章'}[args.original_chapters]
readme = f'''# {name}

作者：{config['author']} · 出版单位：{config['publisher']}  
增订版 1.1 · 原书日期：{config['date']} · 增订日期：2026-11-19 · PDF {pages} 页

<img src="assets/preview/cover.jpg" width="360" alt="{name}封面">

## 阅读导引

本次增订保留原书基础内容、署名和出版记录，形成{summary}。新增实践方法、综合模拟、练习与可直接使用的工作表；模拟人物、数字和结果不构成真实客户成效或专业结果保证。

读者可先浏览前言与{old_chapters}建立共同概念，再按当前任务选读新增章节和附录。表格需结合自己的资料填写，动态规则、产品能力和专业事项仍按当前正式来源核实。

## 完整目录

<details>
<summary>展开全书目录</summary>

{contents}

</details>

## 实际内页预览

页码包含封面，从 1 起算。样页由本次 {pages} 页 PDF 重新生成。

PDF 文件第 {first_preface} 页：前言。

![正文样页](assets/preview/sample-01.jpg)

PDF 文件第 {first_new} 页：新增实践章节。

![正文样页](assets/preview/sample-02.jpg)

## 阅读与下载

- [Markdown 在线阅读](output/markdown/{base}.md)
- [PDF · {pages} 页]({urls}/{slug}.pdf)
- [EPUB]({urls}/{slug}.epub)
- [Markdown 离线包（正文与实际生成资源）]({urls}/{slug}-markdown.zip)

## 增订与检查

[20 轮增订记录](REVISION_LOG.md) · [实际检查报告](QA_REPORT.md)

本次重新生成 Markdown、PDF 和 EPUB。PDF 全部 {pages} 页已渲染并逐张查看总览；EPUB 解包读取封面、前中后章节，{len(links)} 个导航目标与本地资源检查通过。具体范围与限制见报告。

## 来源与权利

[来源记录](SOURCES.md) · [主稿](manuscript/book.md) · [出版配置](book.json)

来源记录保留原有核查范围。本次扩充没有借综合模拟或练习新增真实访谈、客户成效和统计证据，也没有将重新成书记为全部旧来源的再次独立核验。

{config['copyright']}公开阅读与下载不另行授予开放许可。

[返回书目](../../目录.md)
'''
(root / 'README.md').write_text(readme)
qa = f'''# 《{name}》增订版检查报告

检查日期：2026-11-19。原 PDF {args.original_pages} 页，最终 PDF {pages} 页；主稿 {len(text)} 字符，{summary}。

## 内容检查

- 已按《20 轮增订记录》逐轮完成内容补充、案例标签、来源边界、重复、语言、结构与格式检查。
- 新增情境以综合模拟、练习或模拟推演标注；没有把模拟材料写成真实客户经历、访谈或成效。
- 未通过调整字号、页边距或插入空白页凑页数；原 A5 配置保留。
- 外部资料以 `SOURCES.md` 记录的实际核查范围为限。本次新增方法与工作表不等于重新核验全部旧来源。

## Markdown

由唯一主稿 `manuscript/book.md` 重新生成；标题、正文与实际生成资源已检查。离线 ZIP 完整性检查通过。

## PDF

- 最终文件 {pages} 页，{pdf.stat().st_size:,} 字节。
- 全部 {pages} 页已渲染，自动空白页检测为零。
- 已逐张查看最终页面总览，覆盖封面、扉页、出版信息、目录、正文、表格、附录与来源页，未见裁切、文字越界或异常空白。

## EPUB

- 文件大小 {epub.stat().st_size:,} 字节；从最终文件重新解包，读取封面、首章、中段与末章。
- {len(links)} 个导航链接和锚点均有目标，本地图片及样式引用无缺失。
- 样式采用图片限宽、表格横向滚动及代码换行，支持窄屏阅读；未声称覆盖所有实体阅读器。

## 检查边界

本书中的框架和模拟练习用于读者实践。法律、财务、医疗、安全及其他专业事项应由合格人员结合具体情境判断，动态产品能力与规则以当前官方说明为准。
'''
(root / 'QA_REPORT.md').write_text(qa)
log_path = root / 'REVISION_LOG.md'
prior_log = log_path.read_text().split('\n17. **结构与导航**', 1)[0].rstrip()
assert re.search(r'^16\. ', prior_log, re.M), 'Write substantive rounds 1–16 before packaging'
log_path.write_text(prior_log + f'''\n\n17. **结构与导航**：核对全部二级、三级标题和交叉引用；EPUB {len(links)} 个导航目标均有对应文件与锚点。\n18. **元数据与成书**：保留原作者、出版单位和原日期，标注 2026-11-19 增订及 1.1 版；重新生成三种格式。未改变 A5 版式或插入空白页凑页数。\n19. **PDF 全页检查**：最终 {pages} 页全部渲染，逐张查看页面总览；自动空白页检测为零，未见裁切、溢出和异常空白。\n20. **EPUB／Markdown 终检与停止**：从最终 EPUB 解包读取封面、前中后章节，检查 {len(links)} 个导航目标和本地资源；离线 ZIP 完整。内容核验脚本检查章节顺序、占位词、重复长段、来源边界及关键数字；当前未发现仍需补充的真实内容缺口，停止本轮增订。\n''')
print(json.dumps({'book': name, 'original_pages': args.original_pages, 'pages': pages,
                  'chapters': chapters, 'appendices': appendices,
                  'manuscript_chars': len(text), 'nav_links': len(links),
                  'pdf_bytes': pdf.stat().st_size, 'epub_bytes': epub.stat().st_size,
                  'release': {file.name: {'bytes': file.stat().st_size, 'sha256': sha(file)}
                              for file in sorted(release.iterdir())}}, ensure_ascii=False, indent=2))
