# 制作与维护

唯一主稿为 manuscript/book.md，元数据在 book.json。以 build-ebook 技能制作，项目脚本修订中文标题字号、行距及短表格分页；无新增正文插图。

```sh
python books/professional-judgment/scripts/build_book.py
python ~/.codex/skills/build-ebook/scripts/validate_book.py --project books/professional-judgment --render
```

依赖 ReportLab、Pillow、pypdf、Poppler 和本机 Arial Unicode 字体。换机应在配置中修改字体路径。修订后重新制作，再查看 PDF 全页缩略图及 EPUB 实际阅读显示，更新离线包与校验和。PDF／EPUB 不随 Git 提交，后续远程附件按书房既有 Release 方式提供。
