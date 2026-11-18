# 若谷书房上架记录

记录更新日期：2026-11-18。

本记录分别保存首批五本已有成品书的整理记录，以及新作《把办公 Agent 用起来》的制作与上架记录。

## 首批五本：已有成品整理

整理日期：2026-11-08。以下五本保留作品的原有书名、署名、出版日期、版本、正文、配图与版权说明。整理与上架日期单独记录，不替代原书日期，也不表示重新创作或重新制作了阅读版本。

| 书籍目录 | 版本 | 原书日期 | 最近修订记录日期 | PDF 页数 |
| --- | --- | --- | --- | ---: |
| [Neo Lab](books/neo-lab/README.md) | 第一版 · 2026年9月 | 2026-09-23 | 2026-09-23 | 105 |
| [销售与售前分析工具全书](books/sales-presales-tools/README.md) | 重制修订版 | 2026-07-25 | 2026-08-17 | 172 |
| [道德经新解](books/dao-de-jing/README.md) | 第一版，81 幅正文插图 | 2026-08-07 | 2026-08-09（含检查补记） | 291 |
| [国央企 FDE 工程师实战手册](books/soe-fde-handbook/README.md) | 第一版·WPS Comate 增订 | 2026-08-05 | 2026-08-11 | 95 |
| [金融行业 FDE 工程师实战手册](books/finance-fde-handbook/README.md) | 第一版·金融行业增订 | 2026-07-25 | 2026-08-24 | 97 |

### 保存与检查

五本书各自保留一份 `manuscript/book.md`、实际引用的出版配图、封面资源、`book.json`、来源台账与修订记录，以及 Markdown、PDF、EPUB 成品。阅读版 Markdown 的同级 `assets/` 配套保存。

Git 仓库保存主稿、出版资源与 Markdown 在线阅读包。PDF、EPUB 和包含配图的 Markdown 离线 ZIP 通过 [v2026.11.08 Release](https://github.com/njxshr/ruogu-books/releases/tag/v2026.11.08)提供下载，首页及书籍目录链接到相应附件。本地仍保留 `output/pdf/` 和 `output/epub/`，两个二进制成品目录不随 Git 提交。附件使用稳定的英文书籍标识命名，书内中文标题、元数据与文件内容保持不变。

首批整理复制逐文件核对 SHA-256，保持既有文件内容不变；另复核成品结构、图片引用、元数据与现有检查记录的一致性。各书历史制作与审查过程见对应 `REVISION_LOG.md`。Release 附件校验和见 [SHA256SUMS.txt](SHA256SUMS.txt)，在线 Markdown 包校验和见 [MARKDOWN_SHA256SUMS.txt](MARKDOWN_SHA256SUMS.txt)。首批整理没有重新构建或改写这五本书籍。

首批视觉复核记录了一处既有分页待改项：《道德经新解》PDF 第 250 页仅有第 71 章的考据提示框，留白较多。内容完整，可在后续版式修订中调整；整理时保留原成品。结构检查中的“无空白页”不等于所有页面的内容密度一致。

《销售与售前分析工具全书》PDF 第 156 页、EPUB 的“十二张可直接使用的工作画布”开头有一段介绍连续重复两遍，标点略有差异，登记为后续编辑修订项。两处问题均不影响文件完整性，本次未改写对应成品。

金融行业手册的扉页标题末字“册”单独换行，目录第 10 页仅余一条末项，登记为后续版式优化项；内容未发生丢失或裁切。

首批来源项目中的研究输入、旧版电子书、分章草稿、原始图像母版、临时渲染页与工作脚本不纳入该批上架。`my_book` 中对应的 `manuscript/book.md` 是后续维护的主稿；来源项目保留作导入前档案，不并行修订。

国央企手册仅采用 95 页正式增订 PDF，排除较早的 85 页批注版；其 `_new.epub` 与正式 EPUB 字节完全相同，仅保留正式文件。金融手册采用 2026-08-24 金融行业增订版。两书的资料核查日期保留原记录，不将既有工程手册重新宣称为当前监管或产品能力意见。

## 新作：《把办公 Agent 用起来》

制作日期：2026-11-08。作者为李钊，工作室及出版单位为若谷书房，版本为第一版 · 1.0。内容经用户确认后，以本地 `manuscript/book.md` 为主稿，使用 `build-ebook` 制作 Markdown、PDF 与 EPUB。全书包括三篇十五章、两份附录，PDF 为 72 页。

书籍入口见 [README](books/office-agent/README.md)，在线阅读见 [Markdown](books/office-agent/output/markdown/把办公Agent用起来.md)。下载使用独立的 [office-agent-v1.0 Release](https://github.com/njxshr/ruogu-books/releases/tag/office-agent-v1.0)：[PDF](https://github.com/njxshr/ruogu-books/releases/download/office-agent-v1.0/office-agent.pdf)、[EPUB](https://github.com/njxshr/ruogu-books/releases/download/office-agent-v1.0/office-agent.epub)、[Markdown 离线包](https://github.com/njxshr/ruogu-books/releases/download/office-agent-v1.0/office-agent-markdown.zip)。离线包包含模拟练习的原始材料、实际本地交付及来源台账；PDF、EPUB 中的配套材料链接指向仓库。

本轮已完成以下本地检查：

- 主稿与 Markdown 阅读版均为连续 15 章，署名及出版单位一致，未发现常见占位文字。
- 检查主稿、Markdown 阅读版及随书材料的 105 个本地链接与锚点，均有效；配套材料副本与原件一致。
- PDF 共 72 页，无空白页；已复核最终渲染页的视觉版式。
- EPUB 包结构通过检查，包含 121 个导航项；浏览器抽查封面、目录、前段、中段、后段及窄屏显示通过，目录跳转通过。

模拟材料、实际生成的本地文件、组织设计建议与未来推演分别标注。来源台账保留外部资料的支持范围，不将一次模拟练习写成真实业务提效结果。以上记录为已完成的本地制作与检查。本书独立 Release 已于 2026-11-08 正式发布，四份附件的 GitHub 文件大小与 SHA-256 均与本地一致；主稿、配套材料和目录已同步，版本标签指向出版提交 `857a13d`。

## 新作：《AI时代人物志》

2026-11-10发布第一版1.0，李钊著、若谷书房出版。22章、3份附录、84项来源，PDF63页。使用[独立Release](https://github.com/njxshr/ruogu-books/releases/tag/ai-portraits-v1.0)提供PDF、EPUB、Markdown离线包和附件校验和。完成最终PDF全部页渲染查看、EPUB结构和浏览器阅读抽查；具体范围与限制见[QA_REPORT](books/ai-portraits/QA_REPORT.md)。独立传记事实复审及实验复现未开展。其他作品与既有上架记录保留。



### 发布核验

已发布[ai-portraits-v1.0](https://github.com/njxshr/ruogu-books/releases/tag/ai-portraits-v1.0)，标签指向出版提交fac798bd195f83f20abbb37d68b1aa543efab687。GitHub Release API确认四份附件均已上传，文件大小与SHA-256逐一与本地一致。本轮只发布本书及书房目录资料，其他筹备书稿不纳入提交。

## A1—A3：第一版 1.0 本地成书

2026-11-10 按用户要求完成《答案之后》《一人公司的真实边界》《AI 原生销售》的 Markdown、PDF、EPUB 与 Markdown 离线包。PDF 分别为 28、29、31 页，均完成最终全页缩略图检查，EPUB 完成结构、目录跳转与浏览器前中后、封面结尾及窄屏抽查。各书 QA_REPORT.md 和 SHA256SUMS.txt 保存实际结果与校验和。仅登记本地成品，尚未推送或创建 Release，不改变其他作品的发布记录。

## 后续修订

1. 在相应书籍的主稿中修改，补充来源与修订记录。
2. 按各书构建说明重新制作受影响的阅读版本，遵循 `build-ebook` 的检查规范。Neo Lab 使用保留的自定义出版脚本，详见其 [BUILD.md](books/neo-lab/BUILD.md)。
3. 完成结构与实际阅读检查，更新校验和、版本及目录日期。
4. 已有版本信息与更新说明保持一致，再推送到 GitHub。

后续选题《智能生活》（Agent）尚未开始创作。独立 HTML 教程未列入上述三格式成品书。

## A1—A3 远程发布

2026-11-10，按用户明确要求将三本第一版推送至 GitHub，下载附件使用 [a1-a3-v1.0 Release](https://github.com/njxshr/ruogu-books/releases/tag/a1-a3-v1.0)。Release 已正式发布（非草稿），标签指向出版提交 `8603ee7dafe53e8639712dc16e315b1684cd8e9c`。GitHub Release API 返回的十份附件（九份阅读文件及一份 SHA256SUMS.txt）的大小和 SHA-256 与本地逐项一致。已有作品和发布记录保留。

## 2026-11-11 新书九种

发布标签：`new-books-20261111-v1.0`。保留原书署名、晓翊工作室出版信息和 2026-11-11 日期。

- 《被量化的自己》：PDF 18 页；Markdown、PDF、EPUB。
- 《从想法到作品》：PDF 19 页；Markdown、PDF、EPUB。
- 《一人编辑部》：PDF 18 页；Markdown、PDF、EPUB。
- 《组织记忆》：PDF 17 页；Markdown、PDF、EPUB。
- 《客户如何决定》：PDF 17 页；Markdown、PDF、EPUB。
- 《断网之后》：PDF 17 页；Markdown、PDF、EPUB。
- 《机器陪伴》：PDF 18 页；Markdown、PDF、EPUB。
- 《好技术的尺度》：PDF 17 页；Markdown、PDF、EPUB。
- 《克制》：PDF 17 页；Markdown、PDF、EPUB。

本次核对格式存在、PDF 页数与元数据、Markdown 配图引用、EPUB ZIP 完整性，打包并计算 SHA-256；查看九本实际封面与正文第 7 页与第 10 或 11 页预览。原有检查记录不等同于本次重新核查全部来源或逐页审读。

## 新作：《Kimi Work 红皮书》

2026-11-16 形成第一版 · 1.0，2026-11-17 完成 20 轮专项审校、美化与最终复查。作者李钊，出版单位若谷书房。全书九章、四份附录，附通用任务委托模板、交付验收清单、排错表、练习路径和两张原创图示，PDF 共 55 页。书籍入口见 [README](books/kimi-work-redbook/README.md)，在线阅读见 [Markdown](books/kimi-work-redbook/output/markdown/Kimi_Work_红皮书.md)，下载使用 [kimi-work-redbook-v1.0 Release](https://github.com/njxshr/ruogu-books/releases/tag/kimi-work-redbook-v1.0)。

已完成主稿与阅读包一致性检查、PDF 全部 55 页渲染查看、重点表格与代码块原页检查、固定页眉与页码检查，以及 EPUB 结构与浏览器预览。最终校验记录 24 个 manifest 项目、67 个导航链接，无空白内页。实际检查范围和限制见 [QA_REPORT](books/kimi-work-redbook/QA_REPORT.md)，逐轮修改见 [REVISION_LOG](books/kimi-work-redbook/REVISION_LOG.md)。

“岚桥设备”及书中人物、材料和结果为原创模拟，未据此宣称真实客户成效或产品提效。[kimi-work-redbook-v1.0 Release](https://github.com/njxshr/ruogu-books/releases/tag/kimi-work-redbook-v1.0) 已于 2026-11-17 正式发布，PDF、EPUB、Markdown 离线包与 `SHA256SUMS.txt` 四份远端附件已逐份下载核对，大小、SHA-256 及逐字节比较均与本地一致。

## 新作：《企业的制度剖面》

2026-11-17 完成第一版 · 1.0 成书。作者李钊，出版单位若谷书房。全书四篇十五章、三个附录、17 项参考资料，PDF 共 72 页。书籍入口见 [README](books/enterprise-ownership/README.md)，在线阅读版见 [Markdown](books/enterprise-ownership/output/markdown/企业的制度剖面_李钊_20261117.md)。

本书完成 20 轮专项编辑与检查，新增任务阅读路线、制度分析链、五维绩效框架、会议记录、现金压力情景、创新验证分级、交割后一百天整合、证据记录字段和综合示例输出约束。最终 PDF 全部 72 页已渲染查看；EPUB 结构检查记录 33 个 manifest 项、130 个导航链接，并在内置浏览器实际查看封面、目录、前言、第二章、第八章、附录 A 和参考资料，目录跳转、图片加载及 444 像素窄屏重排通过。具体范围见 [QA_REPORT](books/enterprise-ownership/QA_REPORT.md)，逐轮修改见 [REVISION_LOG](books/enterprise-ownership/REVISION_LOG.md)。

本地附件已经生成：`enterprise-ownership.pdf`、`enterprise-ownership.epub`、`enterprise-ownership-markdown.zip` 与 `SHA256SUMS.txt`，三份阅读附件的大小和 SHA-256 已复核，离线 ZIP 完整性通过。资料核验日期保留 2026-11-16，不把 11-17 的编辑与成书记为重新核验外部来源。

[enterprise-ownership-v1.0 Release](https://github.com/njxshr/ruogu-books/releases/tag/enterprise-ownership-v1.0) 已于 2026-11-17 正式发布。2026-11-18 通过 GitHub Release 附件接口逐份下载四份远端附件，大小、SHA-256 及逐字节比较均与本地一致。两本书已通过 Pull Request #1 以压缩合并方式同步到主分支，合并提交为 `4c71d7ef7f4493f11873d88fdf2ce2bedd22549a`。合并前已比对远端分支与本地的 614 份文件，路径与 Git blob SHA 全部一致。其他既有作品和上架记录均保留。
