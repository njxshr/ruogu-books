# 制作说明

元数据与版式配置：`book.json`。主稿：`manuscript/book.md`。作者固定为李钊，出版单位固定为若谷书房。

## 依赖与命令

安装 `build-ebook` 技能及其 Python 依赖（ReportLab、Pillow、pypdf），准备支持中文的可嵌入 TrueType 字体。本机使用系统 Arial Unicode；其他机器在 `book.json` 中调整字体路径。不要把字体文件复制进仓库。

在仓库根目录运行：

```bash
python3 books/office-agent/scripts/build_reading_editions.py
python3 ~/.codex/skills/build-ebook/scripts/validate_book.py --project books/office-agent --render --image-contacts
```

技能安装位置不同时，可为构建脚本增加 `--skill-dir /path/to/build-ebook`。PDF 渲染依赖 Poppler 的 `pdftoppm`。

本书脚本调用技能的封面、Markdown、PDF、EPUB 原生制作函数，并在项目内调整中文字号、行距、表格列宽和短表格分页；不修改技能文件。封面采用同一套蓝绿与金色的字体版式，无正文插图。

## 阅读包与链接

Markdown 包含 `companion/examples/` 和 `companion/sources.md`，保留练习内部的相对链接。PDF、EPUB 中指向本地材料的链接改为本仓库对应文件的网页地址；正式发布时必须同时上传这些材料。

EPUB 补充出版单位、权利说明与扉页版次；ZIP 的首项仍为不压缩的 `mimetype`。以 `output/` 为生成目录，任何内容修改回到主稿，再重新制作。

## 发布

Git 保存主稿、配置、脚本、封面及 Markdown 配套包。PDF、EPUB 不进入 Git，发布到本书独立的 `office-agent-v1.0` Release，以稳定的英文名称提供下载；Markdown 离线 ZIP 包完整包含 `output/markdown/` 内容。

发布前重新完成结构、链接、PDF 全页缩略图和关键页面、EPUB 封面目录前中后与窄屏检查。记录实际结果，更新页数、校验和与根目录 `目录.md`。校验和针对本次实际文件，重新构建后需要重新计算；PDF 构建时间、EPUB 标识和 ZIP 时间戳可能使字节校验和改变。
