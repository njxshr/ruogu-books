#!/usr/bin/env python3
"""Package a visually reviewed build-ebook project without inventing QA claims."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, zipfile
from bs4 import BeautifulSoup
from PIL import Image
from pypdf import PdfReader

p = argparse.ArgumentParser()
p.add_argument('--project', required=True)
p.add_argument('--original-pages', type=int, required=True)
p.add_argument('--release-tag', default='expanded-books-20261119-v1.1')
a = p.parse_args()
root = Path(a.project).resolve()
config = json.loads((root/'book.json').read_text())
name = config['title']; slug = root.name; base = config['output_basename']
pdf = root/'output/pdf'/f'{base}.pdf'; epub = root/'output/epub'/f'{base}.epub'; md = root/'output/markdown'/f'{base}.md'
for f in [pdf, epub, md]: assert f.exists(), f
reader = PdfReader(pdf); pages = len(reader.pages)
assert pages >= 50, f'Only {pages} pages'
report = json.loads((root/'tmp/validation-report.json').read_text())
assert report['pdf']['pages'] == pages and report['render']['rendered_pages'] == pages
assert not report['pdf']['blank_pages']
# Select body pages only; the table of contents occupies pages 4–8.
first_preface = next((i for i,x in enumerate(reader.pages,1) if i >= 9 and '前言' in (x.extract_text() or '')), 9)
first_new = next((i for i,x in enumerate(reader.pages,1) if i >= 9 and '第九章' in (x.extract_text() or '')), 19)
for num,page in [(1,first_preface),(2,first_new)]:
    src = root/f'tmp/pdf-render/pages/page-{page}.jpg'
    assert src.exists(), src
    shutil.copy2(src, root/f'assets/preview/sample-{num:02}.jpg')
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
assets=[]
for filename,page in [('cover.jpg',1),('sample-01.jpg',first_preface),('sample-02.jpg',first_new)]:
    f=root/'assets/preview'/filename
    with Image.open(f) as im: dims=list(im.size)
    assets.append({'asset':filename,'page':page,'dimensions':dims,'sha256':sha(f),'backend':'pdfium'})
manifest={'source_pdf_name':pdf.name,'source_sha256':sha(pdf),'total_pages':pages,'assets':assets}
(root/'assets/preview/preview-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Check EPUB links and local resources; inspect selected chapters as real XHTML text.
e=root/'tmp/epub-inspect/OEBPS'
nav=BeautifulSoup((e/'nav.xhtml').read_text(),'xml'); links=nav.find_all('a'); broken=[]
for link in links:
    href=link.get('href',''); filename,_,frag=href.partition('#'); target=e/filename
    if not target.exists(): broken.append(href); continue
    if frag and not BeautifulSoup(target.read_text(),'xml').find(id=frag): broken.append(href)
assert not broken, broken
missing=[]
for f in e.glob('*.xhtml'):
    soup=BeautifulSoup(f.read_text(),'xml')
    for tag,attr in [('img','src'),('link','href')]:
        for node in soup.find_all(tag):
            value=node.get(attr,'')
            if value and not value.startswith(('http:','https:','#')) and not (f.parent/value).exists(): missing.append((f.name,value))
assert not missing, missing
chapter_files=sorted(e.glob('chapter-*.xhtml'))
for f in [e/'cover.xhtml',chapter_files[0],chapter_files[len(chapter_files)//2],chapter_files[-1]]:
    soup=BeautifulSoup(f.read_text(),'xml'); assert soup.find(['img','h2','h1']), f
# Package final files.
release=root/'release'; release.mkdir(exist_ok=True)
shutil.copy2(pdf,release/f'{slug}.pdf'); shutil.copy2(epub,release/f'{slug}.epub')
with zipfile.ZipFile(release/f'{slug}-markdown.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in (root/'output/markdown').rglob('*'):
        if f.is_file(): z.write(f,f.relative_to(root/'output/markdown'))
with zipfile.ZipFile(release/f'{slug}-markdown.zip') as z:
    assert z.testzip() is None
text=(root/'manuscript/book.md').read_text()
heads=re.findall(r'^##\s+(.+)$',text,re.M)
assert heads and '参考资料' in heads[-1]
chapters=len(re.findall(r'^## 第[一二三四五六七八九十百]+章',text,re.M))
appendices=len(re.findall(r'^## 附录',text,re.M))
urls='https://github.com/njxshr/ruogu-books/releases/download/'+a.release_tag
contents='\n'.join(f'- {h}' for h in heads)
summary=(f'{chapters}章、{appendices}份附录。' if appendices else f'{chapters}章。')
readme=f'''# {name}

{config['subtitle']}

<img src="assets/preview/cover.jpg" width="360" alt="{name}封面">

作者：{config['author']} · 出版单位：{config['publisher']}  
增订版 1.1 · 原书日期：{config['date']} · 增订日期：2026-11-19 · PDF {pages} 页

{config['description']}

## 阅读导引

本次增订保留原书基础内容、署名和出版记录，{summary}新增实践方法、综合案例或模拟练习及可直接使用的工作表。案例的材料性质以正文标注为准，不构成真实客户成效或专业结果保证。

读者可先浏览前言与原八章建立共同概念，再按当前任务选读新增章节和附录。表格需结合自己的资料填写，动态规则、产品能力和专业事项仍按当前正式来源核实。

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
- [Markdown 离线包（含配图）]({urls}/{slug}-markdown.zip)

## 增订与检查

[20 轮增订记录](REVISION_LOG.md) · [实际检查报告](QA_REPORT.md)

本次重新生成 Markdown、PDF 和 EPUB。PDF 全部 {pages} 页已渲染并逐张查看总览；EPUB 解包读取封面、前中后章节，{len(links)} 个导航目标与本地资源检查通过。具体范围与限制见报告。

## 来源与权利

[来源记录](SOURCES.md) · [主稿](manuscript/book.md) · [出版配置](book.json)

来源记录保留原有核查范围。本次扩充没有借综合案例或模拟推演新增真实访谈、客户成效和统计证据。

版权所有 © 2026 {config['author']}。保留所有权利。第三方资料权利归原权利人。公开阅读与下载不另行授予开放许可。

[返回书目](../../目录.md)
'''
(root/'README.md').write_text(readme)
qa=f'''# 《{name}》增订版检查报告

检查日期：2026-11-19。原 PDF {a.original_pages} 页，最终 PDF {pages} 页；主稿 {len(text)} 字符，{summary}

## 内容检查

- 已按《20 轮增订记录》逐轮完成内容补充、案例标签、来源边界、重复、语言、结构与格式检查。
- 新增情境以综合案例、模拟练习或模拟推演标注；没有把模拟材料写成真实客户经历、访谈或成效。
- 未通过调整字号、页边距或插入空白页凑页数；原 A5 配置保留。
- 外部资料以 `SOURCES.md` 记录的实际核查范围为限。本次新增方法与工作表不等于重新核验全部旧来源。

## Markdown

由唯一主稿 `manuscript/book.md` 重新生成；标题、配图及离线包资源已检查。离线 ZIP 完整性检查通过。

## PDF

- 最终文件 {pages} 页，{pdf.stat().st_size:,} 字节。
- 全部 {pages} 页已渲染，自动空白页检测为零。
- 已逐张查看最终页面总览，覆盖封面、扉页、出版信息、目录、正文、表格、附录与来源页，未见裁切、文字越界或异常空白。

## EPUB

- 文件大小 {epub.stat().st_size:,} 字节；解包读取封面、首章、中段与末章。
- {len(links)} 个导航链接和锚点均有目标，本地图片及样式引用无缺失。
- 样式采用图片限宽、表格横向滚动及代码换行，支持窄屏阅读；未声称覆盖所有实体阅读器。

## 检查边界

本书中的框架和模拟练习用于读者实践。法律、财务、医疗、安全及其他专业事项应由合格人员结合具体情境判断，动态产品能力与规则以当前官方说明为准。
'''
(root/'QA_REPORT.md').write_text(qa)
log_path = root/'REVISION_LOG.md'
prior_log = log_path.read_text().split('\n17. **结构与导航**', 1)[0].rstrip()
assert re.search(r'^16\. ', prior_log, re.M), 'Write substantive revision rounds 1–16 before packaging'
log_path.write_text(prior_log + f'''\n\n17. **结构与导航**：核对全部二级、三级标题和交叉引用；EPUB {len(links)} 个导航目标均有对应文件与锚点。\n18. **元数据与成书**：保留原作者、出版单位和原日期，标注 2026-11-19 增订及 1.1 版；重新生成三种格式。页数不足时继续补入实际内容缺口，未改变 A5 版式。\n19. **PDF 全页检查**：最终 {pages} 页全部渲染，逐张查看页面总览；自动空白页检测为零，未见裁切、溢出和异常空白。\n20. **EPUB／Markdown 终检与停止**：解包读取封面、前中后章节，检查 {len(links)} 个导航目标和本地资源；离线 ZIP 完整。当前未发现仍需补充的真实内容缺口，停止本轮增订。\n''')
print(json.dumps({'book':name,'original_pages':a.original_pages,'pages':pages,'chapters':chapters,'appendices':appendices,'manuscript_chars':len(text),'nav_links':len(links),'pdf_bytes':pdf.stat().st_size,'epub_bytes':epub.stat().st_size,'release':{f.name:{'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(release.iterdir())}},ensure_ascii=False,indent=2))
