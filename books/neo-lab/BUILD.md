# Neo Lab 构建说明

`manuscript/book.md` 为唯一正式书稿，`book.json` 为出版元数据与版式配置。修订应从主稿开始，再重新生成阅读版本。

## 构建三种格式

需要 Python 3，以及 Pillow、ReportLab、pypdf。进入本书目录后运行：

```sh
python scripts/build_ebook_local.py --project .
```

此处保留了原书的本地出版脚本，包含中文标题断行、前言与附录分页及联系信息支持。请保留该脚本的版式行为；用通用构建器直接替换可能改变既有排版。

构建输入为 `book.json`、`manuscript/book.md` 及其引用的 `assets/illustrations/` 图片和封面，不依赖分章草稿、原始研究文件或 `EDITORIAL_BRIEF.md`。所需 Python 库由运行环境提供，不在仓库内复制依赖包。中文字体位置在 `book.json` 中，换机器后应调整为可用、具备中文覆盖的字体。

产物写入 `output/markdown/`、`output/pdf/`、`output/epub/`；构建临时文件保存在 `tmp/`。Markdown 移动或下载时应连同同级 `assets/` 配图目录保留。

## 可选：重绘原创图示与封面

日常文字修订不需要重绘图片。`scripts/draw_figures.py` 是原书的绘图源程序，字体常量使用 macOS 路径，跨平台时应先调整字体。绘图前建立目录：

```sh
mkdir -p assets/masters assets/illustrations
```

只重绘封面：

```sh
python scripts/draw_figures.py cover
```

重绘全部图示和封面：

```sh
python scripts/draw_figures.py all
```

全部重绘会更新部分 `book.json` 版式配置。请先检查脚本中的版本日期和元数据，再在有意更换图示时执行。`assets/masters/` 为绘图输出，不是出版构建的输入。

## 构建后的验证

每次生成新版本后，重新检查结构、Markdown 图片、PDF 渲染与 EPUB 导航和实际阅读。若已配置 `build-ebook` 技能，可运行其 `validate_book.py --project <本书目录绝对路径> --render --image-contacts`，并目视检查最新 PDF 联系表与 EPUB 的封面、目录、早期章节、含图章节和末章。

本次上架保留原成品文件，未重新构建。一次性组装、修订和出版脚本准备程序不随书稿上架，避免覆盖正式主稿。
