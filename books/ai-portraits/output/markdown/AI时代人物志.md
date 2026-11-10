# AI时代人物志

科学家的成长、技术的来路与大模型的诞生

作者：李钊  
工作室与出版单位：若谷书房  
日期：2026-11-10  
版本：第一版 · 1.0

内容来自全人类的智慧，感谢AI的高效率整合

---

## 前言　屏幕上的名字，背后的人

我们认识人工智能，往往从一个输入框开始。

输入问题，等待片刻，屏幕上出现文字、代码或图像。随后，我们开始记住一些名字：DeepSeek、Gemini、Kimi、ChatGPT、Claude。它们进入工作和生活的速度，快过我们理解它们的速度。

这些名字并不处于同一层次。OpenAI、Anthropic是机构名称；Gemini是Google的模型与产品品牌；Kimi属于月之暗面；DeepSeek既用于称呼机构，也出现在模型与服务名称中。品牌帮助公众辨认产品，却容易遮住技术的来路。

一本人物志，可以把这条来路重新接起来。

李飞飞帮助人们看见数据基础设施的价值。吴恩达把机器学习带进更多人的课堂。辛顿、勒丘恩、本吉奥推动神经网络成为能够学习复杂表示的工具。注意力机制和Transformer的研究者改变了信息之间的连接方式。姚顺雨等研究员则把语言模型接到行动、反馈与任务之中。随后，新的研究组织把论文、算力、反馈、产品和资本汇聚起来，形成我们今天接触到的智能服务。

本书写的是这些交汇处的人。我们关注他们提出了什么问题，做出了哪些可核实的工作，这些工作为什么有用，又留下了什么困难。对童年故事、私人动机和会议室里的戏剧性瞬间，没有可靠依据就不写。

本书是一部通识短书。研究主线主要落在1980年代至2025年的公开里程碑，编写日期不代表最新产品资料已经全部收录。各章所述职务尽量放回相应历史时点。论文和机构资料可以证明某项工作存在，却未必能独立证明一家公司的宣传结论。

阅读时，请记住两点：大多数突破属于团队；技术成就也不意味着它的提出者在所有社会问题上都正确。

## 第一章　李飞飞：让机器有一个可以学习的世界

### 在校园与干洗店之间

李飞飞的求学经历里，有两种并行的日常。移居美国后，她需要适应英语和新的学校生活，也在餐馆与家里的干洗店工作。斯坦福HAI对其回忆录的介绍记载，她收到普林斯顿全额奖学金通知时，还请两位学校顾问帮忙确认录取信。大学为她打开另一种生活，家庭的生计却没有随之从日程中消失。[S44]

她于1999年获得普林斯顿物理学学士学位，2005年在加州理工学院获得电气工程博士学位。物理、视觉与神经科学出现在同一条求学路上，让她的研究来路比“计算机科学家”这个职业称呼更宽。[S45]

李飞飞后来组织的数据项目，需要让大量日常图像成为研究材料。而在她自己的成长中，学习也始终发生在日常生活里：校园课程与家庭生计需要同时照顾。两者不能构成简单的因果解释，却让“科学家”这个称呼有了更具体的生活背景。

### 从图像问题到数据问题

识别一张图片，对人而言往往发生得很快。对计算机而言，图片首先是一组数字。它必须学习哪些变化只是光线、角度和背景改变，哪些变化意味着对象不同。

李飞飞参与推动的ImageNet，把这个困难转化为一个可以共同工作的研究对象。2009年的论文由邓嘉、董玮、Richard Socher、李佳、李凯和李飞飞共同署名，提出大规模、具有层级组织的图像数据库。[S01]

在人物传记里，人们容易把价值集中到新算法上。数据集则像实验室里的仪器：看上去是准备工作，却决定实验能否开展、研究结果能否比较。ImageNet的重要性，也应从这种公共条件来理解。

### 分类是一种选择

**机制解释：**训练图像分类模型，需要让图片与类别发生联系。如果样本过于单一，模型可能把背景当作对象的特征；如果类别本身含混，准确率也未必有清楚含义。

可以用一个示意例子理解：训练集中，船总是出现在水上，模型就可能更多依赖水面纹理。换成船坞里的船，表现便会改变。这是解释数据偏差的例子，不是对ImageNet某次实验结果的描述。

因此，建设数据集涉及概念、采集、标注和质量控制。每个环节都包含人的判断。机器学习到的世界，首先经过人们组织。

### 她让什么变得可见

本书对李飞飞贡献的理解，是把“供机器学习的世界如何建立”推到研究中心。这样的贡献与设计网络同样重要，但它们解决的问题不同。

也要保留边界：图像分类不能代表全部视觉理解，识别物体不能自动推出对物理关系、人的处境或行动后果的理解。李飞飞这一章留给全书的线索是：讨论智能，必须同时讨论它获得经验的方式。

## 第二章　吴恩达：把人工智能变成可以学习的能力

### 从三所学校到一间没有围墙的课堂

吴恩达的官方履历依次列出卡内基梅隆大学学士、麻省理工学院硕士和加州大学伯克利分校博士学位。跨越不同学校之后，他逐渐承担研究、教学和机构建设等不同角色。[S46]

2011年，他在斯坦福开展在线机器学习课程，随后与Daphne Koller共同创办Coursera。平台的董事履历把这门早期课程与后来的创办工作联系起来。[S47] 读者今天可以在屏幕前暂停一段讲解，重看一个算法，这种平常的学习方式，也有自己的制度与技术来路。

吴恩达这一段轨迹的鲜明之处，是研究工作与传播工作持续并行。我们可以沿着学位、课程和组织记录追踪这种变化，而不必把它包装成从少年时代就已注定的使命。

### 研究之外的另一种瓶颈

如果先进方法只有少数实验室能够掌握，技术的社会影响就会受限。吴恩达的人物位置，在于他同时连接了研究、工程与教育。

其官方履历记录了他在Google Brain创立早期的领导工作；Coursera记录了吴恩达与Daphne Koller于2012年共同创办平台。DeepLearning.AI则把2017年列为创立年份。[S02][S03][S04]

这些是不同的工作。研究组织寻找新能力，课程帮助人建立理解路径，教育平台扩大接触机会。不能仅用“AI导师”四个字把它们压缩成一个模糊标签。

### 课程为什么能改变技术的传播

**作者解读：**一门课程的作用，是把专家习惯省略的中间步骤补出来。训练集、验证集、损失函数、过拟合，这些概念只有组成解决问题的顺序，才会成为可使用的知识。

以识别产品缺陷为示意例子：学习者可能一开始只问模型选得是否先进；学过误差分析后，他会进一步检查漏检来自哪些类别、标注是否一致、生产现场是否改变了照明。问题从“模型够不够大”转向“失败发生在哪里”。

这个例子不代表吴恩达某个项目的实际成效，它说明教育如何改变工程判断。

### 普及也需要边界

学过课程，并不等于已经有能力负责所有应用。一个演示可以只展示成功样本；一个实际系统需要处理异常、维护数据、持续评测，并明确责任。

本书把吴恩达视为能力传播者。李飞飞这一章讨论机器从什么材料中学习；吴恩达这一章则讨论人如何学会建设和判断机器系统。AI时代的基础设施里，也包含课程、教材和共同语言。

## 第三章　辛顿：让多层网络学会修改自己

### 心理学毕业生与木匠的一年

辛顿在剑桥学习实验心理学，后来做过一年木匠，再回到大学研究人工智能，1978年获得爱丁堡大学博士学位。UCL的校史人物介绍还记录了他此后在萨塞克斯、加州、卡内基梅隆等地的研究经历，以及1987年迁往多伦多的节点。[S48]

这条路没有把心理学、手工劳动和计算机研究切成彼此无关的身份。它至少提醒我们，后来被奖项概括的科学生涯，曾包含离开校园、重新选择和迁移。木匠经历不能用来证明某项算法的灵感来源；它的价值在于恢复一段真实的人生间隔。

带着这段经历再读反向传播，辛顿便不只是站在领奖台上的名字：他也曾走过一条尚不能预知结果的路。

### 难处在于信用如何分配

一个系统给出错误答案，究竟应该调整哪一处？多层神经网络包含大量参数，输出错误只告诉我们结果不对，不能直接指出每个参数应当如何变化。

1986年，David Rumelhart、Geoffrey Hinton和Ronald Williams发表关于通过反向传播学习表示的论文，成为这一研究传统的重要文献。[S05]

将反向传播说成辛顿一人从无到有发明，会抹去方法更长的历史，也会漏掉这篇论文的共同作者。更可靠的写法，是明确文献和贡献发生的位置。

### 从误差到表示

**机制解释：**网络先计算输出与目标之间的差异，再用链式法则计算参数对误差的影响，沿梯度方向调整。多次迭代后，中间层可能形成对任务有用的表示。

它可以类比为逐段检查一条加工流水线，不过类比只帮助理解。真实计算依赖可微函数与数值优化，并不存在一个在内部逐个判断责任的人。

“表示”是理解深度学习的关键词：过去需要人工指定的某些特征，能够在训练中形成。但表示有用不等于它与人的概念完全相同，参数也不是一组能直接读出的事实档案。

### 奖项与历史尺度

辛顿与Yoshua Bengio、Yann LeCun共同获得2018年图灵奖；2024年，辛顿与John Hopfield获得诺贝尔物理学奖。这些记录确认了相关工作的历史分量。[S06][S07]

奖项选择若干代表人物，研究却依赖更广泛的积累。写人物志需要保留这种尺度差异：我们可以通过一个人进入历史，不能让一个人替代历史。

## 第四章　勒丘恩与何恺明：让视觉网络找到结构

### 两条从学校走向工业实验室的路

勒丘恩在法国接受工程教育并完成博士训练，1987年前往多伦多从事研究，次年进入贝尔实验室。这是法国科学院人物介绍所记录的早期路径。[S49] 神经网络的探索由此跨过学校与工业实验室的边界；研究者既要处理理论问题，也会面对系统能否真正识别输入的困难。

何恺明于2007年从清华大学毕业，2011年在香港中文大学获得博士学位，随后在微软亚洲研究院工作，2016年至2024年在FAIR从事研究，2024年加入MIT。[S50] 将这些节点放到残差网络之前，可以看出他多年围绕视觉与深度学习积累问题的过程。

两人的经历不应被压缩成“名校培养出名人”。更值得继续追踪的是，学校和实验室分别提供了什么问题、合作关系和试验条件。

### 为什么图像需要结构

一幅图像中的相邻像素往往有关联。同一对象出现在不同位置，也不应该完全失去可识别性。视觉网络的设计因此不能只考虑参数数量，还要考虑怎样利用这种结构。

ACM对2018年图灵奖的介绍，把Yann LeCun在卷积神经网络等方面的工作列入深度学习发展的重要贡献。[S06]

**机制解释：**卷积网络让一组可学习的局部滤波器在不同位置重复使用，从而利用局部关系与参数共享。它为视觉任务提供了有价值的归纳偏置，即在开始学习前，架构已经偏向某些合理的规律。

### 深下去为什么会困难

2015年，何恺明、张祥雨、任少卿和孙剑发表深度残差学习论文。论文处理的核心困难，是更深的网络并不自然更容易训练。[S08]

**机制解释：**残差连接为信息提供一条直接相加的路径，让一个模块学习对输入的修正。它改善了深层网络的优化条件，但不能理解成任意叠加层数都会带来好结果。

这里发生的是一种设计观念变化：既要问模型能表示什么，也要问训练过程是否容易找到有用的参数。

### 两种贡献如何接上

本书把勒丘恩和何恺明放在同一章，是为了呈现结构设计的连续问题，并非把两人的研究视为相同。卷积强调局部性与共享，残差强调信息通路与优化。它们在视觉研究中发挥作用，其思想也影响了更广泛的网络设计。

模型的进步，常常来自给学习过程安排一条更可行的路。

## 第五章　本吉奥与注意力研究者：让模型知道该看哪里

### 在一个研究社区里长久工作

本吉奥2019年的公开报告把1982年至1991年列为在麦吉尔大学完成本科、硕士与博士学习的阶段。[S51] 与一次次公司发布会相比，这种长时间的求学与研究积累不够醒目，却更接近科学工作的日常尺度。

读本吉奥，也需要读他的合作者。注意力论文上的Bahdanau与Cho，不是围绕一位名人摆放的配角；他们共同界定问题并提出方法。把导师、学生和同事写进同一段研究史，人物的成长才有可以辨认的环境。

沿着这些合作关系阅读，本吉奥的研究生涯逐渐从一个名字变成一个社区：不同的人带来问题，在共同的方法上继续工作，新的研究者又由此找到自己的方向。

### 一句话不应被过早压缩

翻译长句时，模型既要保留整体意思，也要在生成某个词时找到对应内容。如果把源句信息全部挤进一个固定长度的表示，重要细节可能难以保留。

2014年，Dzmitry Bahdanau、Kyunghyun Cho和Yoshua Bengio提出联合学习对齐与翻译的方法，成为神经网络注意力研究的重要里程碑。[S09]

### 注意力意味着什么

**机制解释：**模型在生成不同位置的输出时，对输入中的不同部分分配不同权重，再聚合相关信息。这使它不必始终依赖同一个压缩表示。

例如，把“他把书放在桌上，因为那里比较干燥”翻译成另一种语言时，不同输出词需要利用不同上下文。注意力提供的是可学习的信息选择方式。它与人的注意有可比之处，但名称不证明两者拥有相同心理过程。

本吉奥在这段历史中的贡献，也不能单独拿走Bahdanau和Cho的署名。尊重作者名单，是防止人物叙述滑向名人归功的一项简单办法。

### 一项机制打开的空间

注意力的重要性，在于改变模型访问上下文的方式。它没有一次解决语言理解，也没有自动消除歧义。它让后来的研究者能够继续追问：如果这种信息连接方式足够有用，是否可以把它放到架构中心？

下一章的Transformer，就站在这个问题上。

## 第六章　Transformer八位作者：一次共同署名的转折

### 论文之前：田野中的语言与办公室里的机器

南加州大学对校友的报道，为Transformer作者提供了一个具体的早期片段：Vaswani于2012年赴巴布亚新几内亚，参与濒危语言相关的自然语言处理项目。报道也记录了导师对他在办公室组装GPU工作站的回忆。技术史中的“语言”，在这里曾与具体社区中的语言保存问题相遇。[S52]

同一篇学校报道确认，Vaswani于2014年获得该校计算机科学博士学位，Parmar于2015年获得计算机科学硕士学位。[S52] 两人的训练背景提供了理解共同工作的入口，却不足以把八位作者之间的具体分工全部还原。

因此，鲜活的人物细节与完整的团队名单应当并存：前者帮助我们看见研究生活，后者防止故事只剩下最容易讲述的两个人。

### 把名单完整写出来

2017年的《Attention Is All You Need》由Ashish Vaswani、Noam Shazeer、Niki Parmar、Jakob Uszkoreit、Llion Jones、Aidan N. Gomez、Łukasz Kaiser和Illia Polosukhin共同署名。[S10]

完整列出八个名字，是本章的一部分。今天的产品品牌比论文作者更容易被记住，但架构的公共传播始于这种能够核对的共同工作。

### 把信息关系放到中心

**机制解释：**自注意力让序列中不同位置的信息发生加权联系；多头机制允许模型形成多组联系；位置信息则帮助系统处理顺序。原始Transformer包含编码器和解码器，后来流行的许多语言模型采用了不同的结构变体。

这意味着“使用Transformer”只说明一个架构家族，不能据此断言所有产品内部相同。训练材料、参数规模、优化、后训练和服务方式都会改变最终能力。

原论文针对序列转换任务提出架构，其影响远超最初实验。后来的成功不能倒过来解释为作者当年已经完成今天的全部产品设想。

### 共同成果怎样变成基础设施

**作者解读：**Transformer的重要性，还来自它能被反复实现、改造和扩展。一个方法进入公共研究之后，其他团队可以在相对共同的语言上讨论改进。

DeepSeek、Gemini、Kimi和GPT系列之间存在竞争，也共享着这样的研究积累。理解这层关系，能够同时看见差异与继承。

## 第七章　萨顿与巴托：让行动从后果中学习

### 一段始于1978年的师生合作

萨顿本科在斯坦福学习心理学，后来转到马萨诸塞大学阿默斯特分校，获得计算机与信息科学的硕士和博士学位。ACM的获奖介绍记载，他与巴托的合作始于1978年，巴托先后担任他的博士及博士后导师。[S53]

心理学中的学习问题与计算机中的算法问题，在这段经历里发生交汇。读者不必因此把强化学习等同于某种完整心理学理论，但可以理解它为何持续关心行动、反馈与经验。

人物关系也有自己的时间长度。论文标题和奖项年份只是几个醒目的节点，一段合作则可能跨越数十年。把这个尺度补回来，能够让“奠基者”从抽象称号重新成为共同工作过的人。

### 监督并不总是现成答案

分类任务可以给每张图片一个标签。但一个行动系统经常需要做出连续选择，而且好坏要到较晚时才能判断。

Richard Sutton与Andrew Barto是现代强化学习的重要奠基者。ACM将2024年图灵奖授予两人，以表彰其相关贡献。[S11]

### 奖励如何影响行为

**机制解释：**强化学习研究智能体如何与环境交互，并依据奖励改善策略。即时得分未必等于长期收益，探索新动作也可能牺牲眼前表现。

用迷宫作示意例子：只奖励每一步靠近出口，可能让系统避开暂时远离出口、最终却通向正确路线的通道。奖励设计决定学习方向，也可能埋下偏差。

语言模型中的强化学习，把这个框架用在另一类任务上：候选回答可以获得偏好、正确性或其他评分。这样的应用继承了基本思想，也加入了自己的数据和工程问题。

### 从游戏到推理，不能省去中间条件

有的任务可以自动验证答案，有的任务只能依赖人的判断。奖励可靠程度不同，学习结果也不能简单类比。一个系统在数学测试上进步，不足以证明它在开放社会情境中具有同等可靠的判断。

本章给后文提供一个共同问题：我们说模型“变好”，究竟使用了什么奖励？奖励是否与真正关心的目标一致？

## 第八章　黄仁勋与工程团队：算力怎样成为研究条件

### 餐馆、工程学位与芯片公司的学徒期

黄仁勋年轻时在Denny’s做过洗碗、收桌和服务工作。多年后，NVIDIA在回访餐馆的官方报道中重新讲述这段经历。它属于本人及公司的回顾，应当以这个身份阅读。[S54]

他的工程路径则可以从公司历史披露中追踪：在俄勒冈州立大学获得电气工程学士、在斯坦福获得硕士，先后在AMD与LSI Logic工作，再于1993年参与创办NVIDIA。[S55]

餐馆细节让人物变得可接近，工程履历解释了专业经验的积累。二者都不应变成“吃过苦所以必然成功”的公式。创业后来能走到哪里，还依赖合作者、产品判断与时代条件。

### 算法需要能够运行

模型训练需要大量计算，但计算能力不会自动变成可使用的科研工具。硬件、编程接口、编译工具、数值库和开发者经验必须接上。

NVIDIA官方时间线记录了黄仁勋、Chris Malachowsky与Curtis Priem于1993年共同创办公司，并将2006年列为CUDA架构公开的重要年份。[S12]

黄仁勋在这本人物志里代表企业与平台建设，不应被写成神经网络算法的发明者。Ian Buck等工程研究者的工作，则提醒我们注意平台背后的具体技术劳动。[S13]

### GPU为什么适合许多训练任务

**机制解释：**神经网络训练包含大量矩阵及张量运算，其中许多计算可以并行进行。适配的软件体系帮助研究者使用硬件资源，同时减少反复从低层重写程序的成本。

但训练速度还受内存、数据传输、通信和调度影响。一群设备如果多数时间在等待数据，标称计算能力就不能代表实际训练效率。

### 供给也会塑造研究方向

**作者解读：**一种实验越容易运行，研究者越可能持续尝试它；一种工具积累越多，后来者迁移的成本也可能越高。硬件平台由此参与塑造研究生态。

这不意味着模型能力可以完全由采购数量解释。效率设计、数据质量和组织经验同样重要。下一部分的人物故事，正发生在这些条件的交汇处。

## 第九章　OpenAI：奥尔特曼、苏茨克维与大众入口

### 一位学习者与一位创业者的来路

多伦多大学的人物介绍记载，苏茨克维生于俄罗斯，在以色列成长，少年时随家人移居加拿大。他在2005年获得多伦多大学数学学士学位，随后继续完成计算机科学硕士和博士训练，博士导师是辛顿。学校的回顾也谈到他早年对计算机与学习问题的兴趣。[S56]

这条研究者路径，与奥尔特曼的创业经历不同。奥尔特曼在公开访谈中回顾，早期公司Loopt经营了七年。[S57] 在AI之前，他已经经历了一段持续经营创业公司的时期。我们可以据此理解他并非从模型论文直接走向组织领导，却不能仅靠创业回忆评价其后所有管理选择。

两条来路在OpenAI相遇：一条持续追问学习系统的可能性，另一条积累创业组织经验。这是本书依据公开经历作出的叙事安排，并非对任何一次内部决策的还原。

### 同一个组织中的不同工作

OpenAI于2015年发布的创立介绍，将Sam Altman与Elon Musk列为共同主席，将Ilya Sutskever列为研究负责人。那是当时的组织记录，并非本书编写时的现职表。[S14]

把OpenAI写成奥尔特曼一个人的故事，会漏掉研究方法、工程实现和产品建设。反过来，只写科学家，也难以解释研究如何获得长期资源并形成服务。

### 苏茨克维的技术来路

2014年，Sutskever、Oriol Vinyals和Quoc V. Le发表序列到序列学习论文，研究用神经网络把输入序列映射为输出序列的方法。[S15]

这项工作与后来产品之间存在技术史上的联系，却不是从某篇论文到ChatGPT的直接、单线继承。其间还有架构变化、预训练扩展、数据处理与后训练等多条研究路线。

### 从会续写到能响应要求

2022年的InstructGPT论文研究通过人类反馈，让语言模型更好地遵循指令。论文第一作者为Long Ouyang，作者群包括多位研究者。[S16]

**机制解释：**示范告诉模型怎样回答；偏好比较提供哪些回答更被认可的信号；进一步优化改变模型的输出倾向。这个过程把“文本是否像训练材料”与“回答是否符合使用者要求”的差异变得可操作。

它也带来一个持续问题：谁来判断好回答？训练反馈可以改善体验，却不能保证每种使用场景都获得真实、充分和公正的答案。

### 一个产品入口的意义

**作者解读：**大众对话界面缩短了使用模型的路径。普通人可以用自然语言试验能力，不必先掌握专门的软件接口。正因为入口变得容易，人们更需要辨认回答的依据。

GPT-4技术报告明确讨论了模型局限，也未公开全部训练与架构细节。外部作者必须承认这些信息边界，不能把推测写成内部事实。[S17]

OpenAI这一章的核心，是研究、资源和交互如何汇合。奥尔特曼与苏茨克维分别帮助读者看见其中不同的工作位置，团队的贡献则贯穿始终。

## 第十章　Anthropic：阿莫代伊兄妹与可控性的组织实验

### 兄妹的不同专业背景

Dario在斯坦福完成本科学习，2011年在普林斯顿获得物理学博士学位，研究侧重生物物理，导师包括Michael Berry和William Bialek。此后他进入科技公司，逐渐转向大规模AI研究。[S58]

Daniela的起点则是人文学科。斯坦福创业课程的演讲介绍记载，她在加州大学圣克鲁兹分校接受英语文学、政治和音乐方面的教育；进入AI机构前，她在Stripe早期团队从事招聘，后来负责风险运营。[S59]

把这两段经历并排放置，Anthropic便不只是“又一家由科学家创办的实验室”。它的创立者带来了不同种类的专业经验。专业不同如何影响具体决策，需要更多证据；但读者至少能够看到，AI组织中的重要工作并不全部从计算机专业出发。

### 把可靠性写进研究议程

Anthropic在2021年的官方介绍中，把Dario Amodei与Daniela Amodei列为领导者，并将构建更可靠的通用AI系统作为方向。[S18]

这是公司对自身目标的陈述。人物志可以据此说明其公开研究议程，却不能仅凭愿景证明公司已经解决安全问题。

Dario也参与了2020年语言模型缩放规律研究。那项论文把模型规模、数据和计算投入与损失变化联系起来，是理解大模型投入方式的一份重要材料。[S19]

### 原则如何进入训练

2022年的Constitutional AI论文由Yuntao Bai等研究者署名，探讨依据一组原则，让AI参与批评、修订与反馈的训练方法。[S20]

**机制解释：**如果每个反馈都依靠人工，收集成本会很高。原则约束与模型生成反馈提供了另一条路径；不过，选择什么原则、如何解释冲突，仍然包含人的判断。

“宪法式AI”是研究方法名称，不能与国家法律效力混淆。方法名称也不等于系统已经具备稳定、完整的道德推理。

### 研究与组织要同时成立

**作者解读：**Daniela在创立记录中的位置提醒我们，研究机构还需要组织与运营。人才如何合作、产品如何交付、风险问题如何被带到决策桌上，都影响研究目标能否延续。

Claude的产品表现与Anthropic的研究主张应当分别评估。用户愿意使用一款产品，不能替代安全论证；一份安全论文，也不能替代具体任务中的测试。

本章留下的开放问题是：当能力、商业需求与审慎要求发生冲突时，组织能否把公开原则落实为实际选择？仅靠人物承诺，无法替读者完成判断。

## 第十一章　Gemini：哈萨比斯、迪恩与跨团队协作

### 棋盘、游戏和分布式系统

哈萨比斯的早期生活里，棋与游戏占据了显眼位置。英国皇家学会简介记载，他少年时已展现国际象棋才能，17岁时参与编写经典游戏《Theme Park》。[S60] 后来在UCL从事神经科学研究的经历，又把他的路径从游戏设计接到认知研究。[S61]

这种跨界足以构成一个值得理解的人物轮廓，无须再虚构他面对某盘棋时的心理。游戏提供规则、目标和试验环境；对人怎样学习的研究则提供另一组问题。它们与后来AI工作的联系，可以作为研究线索继续追踪。

迪恩走的是另一条路径。他在明尼苏达大学学习计算机科学与经济学，1996年在华盛顿大学获得计算机科学博士学位，随后在DEC研究机构工作，1999年加入Google。学校2014年的资料已经记录了他对抓取、索引、查询与大规模计算基础设施的贡献。[S62]

一个从游戏与神经科学进入，一个从编译与大规模系统的工程环境进入。同一机构能够汇合不同经历，正是这段组织史值得观察的地方。

### 一个品牌背后不止一座实验室

2023年，Google宣布把DeepMind与Google Brain汇合为Google DeepMind；当时公告说明了Demis Hassabis与Jeff Dean的职责安排。本章使用的是这一历史节点的记录。[S21]

同年Gemini初代技术报告把工作描述为跨Google协作。它因此适合用来观察大规模研究组织：模型的完成，需要多种专业之间持续配合。[S22]

### 多模态意味着增加连接难度

**机制解释：**多模态系统处理文本、图像等不同形式的信息，并学习它们之间的关系。它不只是把几种文件放在一起，而是要让系统在不同信息之间建立可用联系。

以解释图表为示意任务，模型需要读懂标题、数值、图例和问题，还要避免凭视觉印象编造精确数字。输入形式增加，错误也会出现新的来源。

初代报告能够支持对当时设计与实验的讨论，不能替代对后来所有Gemini产品的说明。

### 从科学问题看哈萨比斯

2024年，Hassabis与John Jumper因蛋白质结构预测相关工作分享诺贝尔化学奖的一半，另一半授予David Baker。[S23]

这一记录能说明AI方法对科学研究的贡献，但AlphaFold不是Gemini的另一个名字。把两者区分开，才能看见同一组织中的不同任务、数据和验证标准。

**作者解读：**Hassabis帮助本书呈现问题导向的研究组织；Dean的历史角色帮助呈现系统与研究规模之间的联系。大型机构的优势来自组合能力，也面临协调成本。它们能否合作出成果，要由具体工作检验。

## 第十二章　DeepSeek：梁文锋与效率问题的重新提出

### 硕士论文致谢里的研究训练

浙江大学校方文章确认，梁文锋本科和硕士均毕业于信息与电子工程学院，并转述了其硕士论文致谢：导师项志宇把他带入机器视觉研究，为他安排学习计划，也进行具体的代码指导。这里采用的是学校转述，尚未直接核对论文原件，因而不把其中措辞作为本书的直接引语。[S63]

这段材料比“天才创始人”更能说明研究者如何成长：一个学生进入尚不熟悉的领域，通过课程、代码与实验逐渐获得独立工作的能力。它不能证明后来每项工程设计的来源，却补回了公开成名之前的一段训练过程。

后来备受关注的模型，距离当年机器视觉课程与实验已经很远，但训练研究能力的基本过程仍然具体：读理论、写代码、做实验，再让结果检验判断。梁文锋的早期经历，为理解这类组织怎样建立研究基础提供了一个入口。

### 不把品牌写成单人实验

DeepSeek创始人梁文锋因团队的大模型工作受到关注。关于其创业背景，可以查到美联社的人物报道；本章的技术判断主要依据团队论文。[S24][S25][S26]

梁文锋出现在相关研究署名中，但这并不能用于推断他独自完成某个模块。技术报告的长作者名单，应当与公众人物的高可见度同时保留。

### V3所呈现的系统问题

DeepSeek-V3报告讨论混合专家架构、多头潜在注意力及训练系统设计。[S25]

**机制解释：**混合专家模型让不同输入调用部分专家参数，目标是在总容量与单次计算量之间取得更好的关系。它仍需要处理路由、负载均衡与跨设备通信，不能简单理解成“大部分参数免费”。

注意力中的缓存也会占用资源。降低这类开销可以影响服务效率，但具体收益依赖实现与使用场景。

论文中某项训练成本不等于一家机构的全部研发投入。本书不把单次训练的成本口径扩大为人才、设备、数据、试错和运营的总账。

### R1与学习推理行为

DeepSeek-R1论文研究通过强化学习激励推理能力，并区分R1-Zero与R1等训练路径。[S26]

**机制解释：**能够验证答案的任务，可以提供较清楚的学习信号；长过程本身则不保证正确。模型写出更长解释，可能有帮助，也可能重复或偏离问题。

R1的意义适合放在方法组合中理解：基础模型、奖励、训练过程和推理时计算共同影响表现。它并不证明所有知识和能力都能仅靠奖励从空白产生。

### 开放之后，问题由更多人接手

团队公开模型相关材料，使外部开发者能够进一步试验。[S27] 开放权重、训练数据公开、完整训练流程可复现，是不同层次的事情，需要逐项确认。

**作者解读：**DeepSeek给人物志提供的线索，是在资源约束下重新安排系统。梁文锋的组织角色值得写，工程团队如何把效率问题拆成可以解决的部分，同样值得写。

## 第十三章　Kimi：杨植麟与上下文的长度

### 从博士训练中找到持续的问题

卡内基梅隆大学把杨植麟列入2019年校友记录。该校博士论文目录将他的论文题名列为《Advances in Generative Feature Learning》，导师列为Ruslan Salakhutdinov与William Cohen。[S64][S65]

这比一串创业头衔更接近他的研究起点：如何学习有用的表示，如何组织语言与信息。将这一节点接到Transformer-XL和XLNet，可以看见论文之间存在连续的问题意识，而非只在公司成立以后寻找人物的价值。

从论文到产品，一个持续的困难是怎样组织更多信息。博士研究提供了一组方法问题，创业则加入资源、交付和用户需求。理解杨植麟，需要同时沿着这两条线往下读。

### 先把研究履历落在论文上

讨论杨植麟，能够查到的技术锚点包括2019年的Transformer-XL与XLNet。前者由Zihang Dai、Zhilin Yang等人共同署名，后者由Zhilin Yang、Zihang Dai等人共同署名。[S28][S29]

这些文献可以证明其参与相关研究。它们不能单独证明后来的Kimi直接沿用了相同架构，也不能替代对月之暗面整个团队的介绍。

### 长上下文改变什么

**机制解释：**上下文是模型在一次处理过程中可利用的信息范围。范围扩大，有助于放入更长材料；实际能否找对、理解和综合信息，还要另行测试。

设想把一本长篇人物传记交给模型，这是示意任务。即使全文能放进去，模型仍可能混淆不同年代的职务，或者把书中人物转述的话当成作者意见。容纳、检索、理解与可靠作答，是几个相关但不同的能力。

Transformer-XL围绕固定长度上下文的局限提出研究方法；XLNet则探索自回归预训练目标。杨植麟的研究线索因此连接着“如何使用更多关系信息”这个问题。

### 从材料处理走向任务执行

2025年Kimi K2技术报告以智能体能力为重要主题，署名为Kimi团队。[S30]

**机制解释：**智能体系统需要把语言输出接到工具与环境上。例如查询材料、运行代码、读取结果，再决定下一步。每多一个行动接口，就多出权限、失败恢复和结果检查的问题。

产品品牌会变化，但这一问题具有持续性：一个系统能说出步骤，与它能正确执行步骤，有明显距离。

**作者解读：**Kimi这一章把研究者的长期问题与创业团队的产品问题并置。前者可以从论文追踪，后者必须观察具体系统；不能用创始人的论文资历替整个产品预先背书。

## 第十四章　古德费洛与生成研究者：机器开始制造样本

### 一次告别聚会之前，已有多年的准备

2014年，古德费洛已走到研究生阶段的尾声。Google当年的博士奖学金报道记载，他在蒙特利尔大学即将完成博士训练，此前曾实习参与街景照片中门牌号码的神经网络识别项目。[S82] 他的研究生活同时接触基础方法与实际图像问题。

多年后，在2025年的一次访谈中，他回忆，GAN的初步试验发生在一次同学告别聚会之后。那时他已经提交论文，正投入《Deep Learning》教材写作。与同学的讨论把他重新拉回生成建模问题；已有的程序和工具，使他能够很快试验新想法。他特别强调，参与者此前已有多年积累，后来论文也依靠团队共同完成。[S84]

这段本人回顾保留了发现的偶然性，也解释了试验为什么能够迅速开始：工具已经在手，相关问题已经思考很久，合作者能够继续推进。一次聚会可以成为故事的开头，知识和代码的准备却发生在更早的时候。

古德费洛后来仍把教材入口放在个人主页上。[S66] 对他而言，提出新方法与把已有知识整理给读者，是研究生活中并行的两种工作。

### 从识别到生成

图像识别问“这是什么”，生成建模则试图学习数据规律并产生新样本。2014年，Ian Goodfellow与Jean Pouget-Abadie、Mehdi Mirza等合作者提出生成对抗网络。[S31]

**机制解释：**生成器尝试制造样本，判别器尝试区分真实样本和生成样本，两者在训练中相互影响。对抗提供学习信号，却也带来训练稳定性等困难。

这个设计很容易被写成一段灵光乍现的传奇。本书只保留可核实的研究记录。一个想法如何被提出，与它如何经过实验成为可用方法，是两个都值得认真书写的过程。

### 生成并不是记忆的简单播放

模型可能产生训练材料中没有原样出现的组合，也可能重复已有内容。判断原创性、可靠性或权利问题，需要具体检查，不能仅凭“生成”二字得出结论。

本章也不把GAN当作今天所有图像生成系统的共同内部结构。生成研究包含多条路线，本书在此选择GAN作为人物与机制结合的一个窗口。

### 技术人物为何需要任务边界

**作者解读：**一种方法的历史贡献，不取决于它是否永远占据产品中心。研究可以被替换、吸收或转化，仍然改变后来者思考问题的方式。

人物志因此不能只追逐当前最响亮的品牌。理解古德费洛这一代研究者，有助于理解：今天的能力经过许多尝试才成为可能，其中相当一部分并未以公司名字留在公众记忆里。

## 第十五章　检索与反馈的研究者：让答案有地方核对

### 在大学与工业实验室之间读博士

Patrick Lewis的博士经历跨在UCL与FAIR之间。UCL在2021年介绍这一联合培养模式时，记录了他同时参与两边研究的情况；他的个人主页确认，博士导师为Sebastian Riedel与Pontus Stenetorp。[S67][S68]

对一个需要模型、资料与实验条件共同支持的研究方向而言，合作的连续性本身就是重要条件。Lewis在校方报道中谈到的，正是长期合作相对短期实习的不同。

这段共同培养经历，给需要长期试验的知识与语言研究提供了连续的合作环境。Lewis后来参与的检索增强生成，也可以放回这段研究训练中理解：问题逐渐聚焦到模型如何表示、获得和使用知识。

### 参数里的知识并非可查证书目

一个模型能够生成关于某件事的流畅回答，不意味着它能够指出可靠出处。参数表达的规律与一份可以逐条查验的文献库并不相同。

2020年，Patrick Lewis、Ethan Perez、Aleksandra Piktus等研究者发表检索增强生成论文，把检索机制与生成模型联系起来。[S32]

### 给生成过程接上外部材料

**机制解释：**检索增强生成通常先从外部资料中找出相关内容，再将其提供给生成过程。它有助于引入可更新的材料，但如果检索拿错内容，答案仍可能错误。

用本书研究作示意：查询某人2023年的职务，应当优先找到当时公告，而非随手拿一个没有更新的个人简介。即使材料正确，写作者还要避免把历史职务写成现职。

这同样适用于AI系统。提供材料只是开始，识别时间、来源身份、证据范围与相互矛盾之处，决定了答案是否可靠。

### 把不显眼的人写进历史

后训练、评测、检索和数据管理常被产品叙事省略，但它们直接影响人们能否信任系统。InstructGPT与Constitutional AI的作者群也说明，反馈方法属于共同研究，不能被一位创始人的公众形象替代。[S16][S20]

**作者解读：**AI时代的人物，不只包括提出新架构的人，也包括让错误能够被发现、让答案能够被核对的人。前者扩展能力，后者帮助能力进入有责任的使用。

## 第十六章　姚顺雨：从说出答案到完成行动

### 从清华出发，把语言模型带进行动环境

清华的讲座记录提供了姚顺雨研究生涯中的一个清楚坐标：2023年4月，他回到母校作线上报告，已经是普林斯顿四年级博士生，导师为Karthik Narasimhan，研究语言与强化学习的交叉问题。报告介绍也记录了他从清华姚班毕业，以及在MIT、微软、IBM和Google等机构实习的经历。[S69]

一名学生从课堂走到实验室，需要逐渐学会选择自己的问题。姚顺雨这时选择的问题，可以在报告题目中看见：怎样走向自主的语言智能体。他关注的已经不仅是模型能生成什么，也包括模型能在什么环境中采取行动。

一年后，普林斯顿安排了他的博士公开答辩，时间是2024年5月2日，题目为《Language Agents: From Next-Token Prediction to Digital Automation》。[S70] 从清华的讲座到博士论文，语言、行动和环境持续出现在同一条研究线上。

把这条线与ReAct、思维树、SWE-agent并排阅读，能够看出它逐步展开的方向：让模型接收行动结果，比较不同路径，并通过适合的工具接口完成任务。这里呈现的是公开研究记录之间的联系；具体选择如何形成，仍有待更多本人访谈解释。

### 把研究者放回共同工作中

姚顺雨在个人主页上把研究主题概括为智能体。[S33] 这个简短的自我介绍，与他在博士阶段持续开展的工作相互呼应。

2022年的ReAct由姚顺雨、Jeffrey Zhao、Dian Yu、Nan Du、Izhak Shafran、Karthik Narasimhan和Yuan Cao共同署名。论文尝试把推理与行动交替组织起来。[S34]

这个问题接在本书的产品讨论之后：语言模型可以描述一项工作，但描述本身不能把工作完成。要查询一份材料，就需要接触外部信息；要修改程序，就需要读取文件并检查运行结果。研究者必须让系统获得反馈。

### ReAct与思维树解决不同困难

**机制解释：**ReAct让模型生成的推理过程与任务行动交替出现。行动带回观察结果，后续过程便能够利用新信息，而不必完全依赖最初输入。

例如，查询一本书的出版年份，可以先定位出版社资料，再根据返回内容判断是否找到正确版本。这是示意任务。查询工具失效、材料互相冲突或版本混淆，仍然可能使系统失败；行动循环不等于事实核查已经完成。

2023年，姚顺雨与Dian Yu、Jeffrey Zhao等人发表Tree of Thoughts，探索多个中间思路并进行评估与搜索。[S35] 它关注的是如何比较不同路径，而非把单条输出一味延长。

两项工作可以放在一起理解，但不应合并成一个万能方法。ReAct突出与环境交互；思维树突出候选路径之间的选择。搜索需要额外计算，评估本身也可能出错。

### 工具界面也属于研究

2024年的SWE-agent由John Yang、Carlos E. Jimenez、Alexander Wettig、Kilian Lieret、姚顺雨、Karthik Narasimhan和Ofir Press共同署名，研究面向智能体的计算机接口设计。[S36]

这项工作把一个常被忽略的问题推到前台：能力不只取决于模型，还取决于模型怎样查看文件、编辑代码和执行检查。界面提供的信息太少，系统会误判；返回内容太多，关键结果又可能被淹没。

**作者解读：**姚顺雨的研究线索，是逐步把下一段文字的预测接到可观察的任务过程中。本章同时记住合作者，因为ReAct、思维树和SWE-agent分别是不同团队的共同成果。衡量这类工作的关键，是行动是否有效、反馈是否可信，以及失败之后能否被发现。

## 第十七章　Jason Wei与Denny Zhou：把中间步骤变成研究对象

### 年轻研究者与长期问题的相遇

研究合作实验室对Jason Wei的介绍记载，他于2020年在达特茅斯获得计算机科学学士学位，早期研究涉及语言、少样本数据和医学图像。[S71] 这些线索让他在思维链论文之前已经有了一个更宽的起点。

Wei的个人主页按时间列出文本数据增强、指令微调、思维链与模型能力研究，并记录了Google Brain以及2023年至2025年在OpenAI的工作经历。[S72] 把这些节点连起来，可以看见他不断把“怎样让模型学会或表现出一种能力”变成可实验的问题。

Denny Zhou的个人主页则呈现另一种连续性：思维链之后，仍然围绕自洽性、由易到难的提示、上下文干扰和工具等问题开展合作研究。[S73] 这些相邻的课题不断追问同一件事：模型面对更复杂的问题时，怎样才能更可靠地利用已有能力。

### 答案之前发生什么

2022年，Jason Wei、Xuezhi Wang、Dale Schuurmans、Maarten Bosma、Brian Ichter、Fei Xia、Ed Chi、Quoc Le和Denny Zhou共同发表思维链提示研究。[S37]

论文把一种具体做法变成可比较的实验：在提示中给出包含中间步骤的示例，观察模型在若干推理任务上的表现。其价值应当依据实验条件理解，而不能扩张为“模型只要多想就一定正确”。

### 从提示方式看研究判断

**机制解释：**一个只包含问题与最终答案的示例，与一个展示拆解步骤的示例，向模型提供了不同的生成模式。后者可能帮助模型把复杂任务展开为若干局部计算。

以计算折扣为示意任务，先确定原价，再计算折扣，最后处理附加费用，能够减少直接跳到结论时的一些错误。但如果一开始理解错了折扣规则，清楚的步骤也可能通向错误答案。

输出中的解释还不能自动视为模型内部计算的忠实记录。读者可以检查步骤是否成立，却不应仅凭语言流畅便断言知道了系统的全部工作过程。

### 与姚顺雨一章怎样相接

思维链提供一条展开路径，思维树尝试比较多条路径，ReAct则把过程连接到环境观察。把三者放在相邻章节，可以看见研究如何围绕同一困难逐步分叉。

**作者解读：**Wei与Zhou在本书中的位置，是让读者看见提示和推理过程也可以被严格研究。我们依据论文确认他们的参与，不把一个作者的公众声誉转化成独占贡献，也不根据早期研究推定后来商业模型使用了同样机制。

## 第十八章　John Schulman与Rafael Rafailov：偏好怎样改变模型

### 从折毛巾的机器人到语言模型的偏好

舒尔曼起初学习的是物理。他在加州理工学院做过暑期研究，却逐渐被其他问题吸引。到伯克利读研究生时，他先进入神经科学项目，后来轮转到Pieter Abbeel的实验室。直升机控制和叠毛巾机器人让他投入其中，最终转入电子工程与计算机科学。学校访谈保留了这次转向的来龙去脉。[S74]

他对伯克利的记忆也有一个安静的片段：初次来访后的一天清晨，他跑步到实验室附近，看见路旁的一小群鹿。这是舒尔曼自己的回忆。[S74] 在后来广为人知的强化学习论文之前，他也在寻找适合自己的学科、导师和生活环境。

Rafailov走过的路则经过数学、统计、经济学和金融。他的早期个人主页记载，自己在伯克利完成应用数学、统计与经济学学习，研究生阶段在斯坦福学习统计和计算机科学；读研前还在高盛量化投资策略部门做过初级投资组合经理。[S81]

转向研究后，他关注机器人怎样通过数据与交互形成能力，Chelsea Finn的履历也记录了其博士阶段的师生关系。[S75] 这些经历不能直接解释DPO为何被提出，却让读者看见：一位研究者进入偏好优化之前，已经跨过金融与机器人学习等不同工作环境。

### 学习的步子该迈多大

2017年，John Schulman、Filip Wolski、Prafulla Dhariwal、Alec Radford和Oleg Klimov发表PPO论文，研究策略优化方法。[S38]

强化学习中的策略会随着更新改变，旧策略采集的数据与新策略之间可能出现差距。PPO通过特定目标设计，试图在优化效果、实现复杂度和样本利用之间取得平衡。它属于强化学习方法，不能简单等同于语言模型对齐的全部流程。

本书把Schulman从机构章节中单独写出，正是为了让具体方法不被品牌遮住。一个大众产品背后，可能有多年积累的优化问题。

### 另一条偏好学习路径

2023年的DPO由Rafael Rafailov、Archit Sharma、Eric Mitchell、Stefano Ermon、Christopher D. Manning和Chelsea Finn共同提出。[S39]

**机制解释：**在相应数学设定下，DPO把偏好优化转成直接作用于模型的训练目标，省去传统流程中显式训练奖励模型等环节。它使某类偏好训练更便于实施，但不能概括为任何任务都不再需要奖励模型或交互数据。

PPO与DPO不应被写成单纯的年代替代关系。两者的目标设定与训练流程不同，适用性取决于数据、任务和系统条件。

### 谁提供偏好

假设两份摘要分别更简短和更全面，哪一份更好，取决于读者的用途。这是示意例子。训练数据如果没有呈现这种差异，模型可能只学到一种被普遍奖励的表达风格。

**作者解读：**这组人物把一个社会性问题带进技术内部：我们究竟在优化什么？训练方法可以更高效，却不能替人决定偏好的代表性。模型更讨人喜欢，也不等于它更准确。

## 第十九章　Tri Dao与Albert Gu：效率来自重新安排计算

### 从博士训练走向自己的研究群体

普林斯顿2024年的聘任公告记载，Tri Dao拥有斯坦福本科与博士学位，并于当年9月加入该校任教。[S76] 对一位年轻研究者而言，从完成自己的课题到组织新的研究群体，是另一种职业转折：需要开始帮助学生找到问题。

Albert Gu则出现在Christopher Ré的斯坦福实验室校友名单中，标注为2022年博士毕业。[S77] 这一记录与两人共同署名的Mamba论文放在一起，让读者看见，架构创新背后也存在长期研究训练与合作网络。

我们不能仅凭同属一个研究社区就还原合作中的每次讨论。但可以据此避免一种误解：FlashAttention与Mamba并非凭空出现的产品口号，它们从一批持续研究结构、记忆与计算问题的人手中生长出来。

### 时间花在搬运上

2022年的FlashAttention由Tri Dao、Daniel Y. Fu、Stefano Ermon、Atri Rudra和Christopher Ré共同署名。它强调计算之外的存储读写成本。[S40]

**机制解释：**处理注意力时，中间结果如何在不同层级的GPU存储之间移动，会影响速度与占用。FlashAttention通过分块等方法安排计算，减少昂贵的读写，同时计算精确注意力。

“精确”描述它与相应注意力计算的关系，不表示所有数值实现都没有浮点误差，也不表示模型答案一定正确。它改变的是实现效率层面的问题。

### 如果不沿着同一架构继续走

2023年，Albert Gu与Tri Dao发表Mamba论文，以选择性状态空间模型探索另一种序列处理方式。[S41]

**机制解释：**系统沿序列更新状态，并依据当前输入选择保留或遗忘的信息。它尝试在长序列计算中取得效率与表达能力之间的平衡。

FlashAttention与Mamba代表不同思路：前者改进注意力的执行，后者探索不同的序列建模架构。不能把它们合称为一种“注意力加速算法”。

### 把系统研究写进人物志

**作者解读：**Dao与Gu提醒读者，技术前进既可能来自更好的实现，也可能来自另一种建模方式。二者都需要具体任务和硬件条件的检验。

本章不把某项论文中的吞吐结果扩大为全部场景的速度结论。训练、推理、输入长度和设备条件不同，收益也会变化。效率人物的贡献，值得通过他们拆解瓶颈的方式来理解。

## 第二十章　Edward Hu与LoRA作者群：让适配少改一些参数

### 先在工业实验室研究，再继续追问推理

Edward Hu的公开简介给LoRA之外的经历补上了几个节点。他在读研前曾在微软从事研究；后来在本吉奥指导下完成计算机科学博士训练，博士论文主题为“Building a Reasoning Machine”。他还在简介中回顾了参与OpenAI o1研究的经历。以上属于本人履历陈述，不用于推断未公开的项目分工。[S83]

把这些节点按顺序放在一起，一个人的研究范围便从单一算法名称中展开：减少模型适配开销之后，他继续研究推理。对于使用LoRA的开发者来说，Hu很容易只成为论文上的一个名字；履历则显示，论文只是他持续研究中的一站。

本章仍保留LoRA的完整共同作者名单。本人简介帮助理解职业轨迹，论文署名说明共同成果的归属，两种材料各有用途。[S42]

### 预训练之后还有很多工作

通用模型需要适应特定任务，但完整更新一个大型模型可能需要较多资源。2021年，Edward J. Hu、Yelong Shen、Phillip Wallis、Zeyuan Allen-Zhu、Yuanzhi Li、Shean Wang、Lu Wang和Weizhu Chen共同发表LoRA论文。[S42]

这一完整名单提醒我们，一个广为传播的方法名称背后，存在多个研究位置。人物志可以选择代表人物讲述，却必须保留共同工作的证据。

### 低秩适配意味着什么

**机制解释：**LoRA冻结预训练权重，通过可训练的低秩矩阵表示部分权重更新，从而减少需要训练的参数。它为适配模型提供了一种资源更节省的办法。

“少训练一些参数”不等于不需要基础模型。加载、运行和评估仍然需要资源。具体效果也取决于适配位置、数据质量和任务要求。

以让模型遵循固定报告格式为示意任务，适配可能改变输出习惯；如果报告需要最新事实，单靠这种适配不能保证内容及时。格式学习与知识核对仍然要分开。

### 降低参与门槛之后

**作者解读：**LoRA的价值可以从参与条件理解：一些团队无需重复完整训练，也能试验自己的任务。但门槛降低不会自动消除数据泄漏、过拟合和评测不足。

本章把适配方法接回吴恩达的教育主题。更多人获得工具之后，还需要知道工具改变了哪一部分、没有解决哪一个问题。可参与性与判断力，应当一起增长。

## 第二十一章　Jonathan Ho、Ajay Jain与Pieter Abbeel：从噪声中建立生成路径

### 一个实验室网络里的三个人

伯克利机器人学习实验室的校友记录，将Jonathan Ho列为2020年5月毕业，博士论文围绕深度生成模型、模仿学习、图像合成与压缩。[S78] 这组关键词说明，他的研究路径比“扩散模型作者”更宽。

Ajay Jain的个人主页记载，他在MIT完成计算机科学本科学习，也参与过校园机器智能社群，后来在伯克利研究生成模型。[S79] 从组织学生社群到参与图像与三维生成研究，这是一段可以沿公共资料继续追踪的成长过程。

Abbeel则先在比利时KU Leuven接受电气工程教育，2008年获得斯坦福计算机科学博士学位，其研究横跨机器人与多种机器学习方法。[S80] 将导师与学生的经历放在一起，我们就能理解，扩散论文并不只属于一条孤立的图像技术史，也与学习、控制和机器人研究的社区发生联系。

这里呈现的是公开的教育与研究节点。具体合作中的想法由谁先提出、如何经历试错，需要更直接的访谈与档案，不能从作者排列顺序中推演出来。

### 生成技术有不止一条来路

本书前面以古德费洛及GAN作者群打开生成建模。要理解另一条重要路径，可以阅读Jonathan Ho、Ajay Jain与Pieter Abbeel在2020年发表的去噪扩散概率模型论文。[S43]

这项工作接续了更早的扩散与生成研究，也给后来者提供了继续试验的路径。在Ho、Jain和Abbeel共同工作的这一站上，研究者把逐步去噪变成能够展示图像生成效果的方法。

### 让模型学习逐步恢复

**机制解释：**一种直观理解是，训练过程构造逐步加噪的数据，再学习相反方向的去噪过程。生成时从噪声出发，多步形成样本。这只是理解机制的入口，具体训练目标与采样方法需要结合论文。

它与GAN中的生成器、判别器对抗不同。两类方法都可以生成样本，却通过不同的学习信号工作。也不能从一项图像生成论文直接推断某个视频或商业图像产品的全部实现。

### 逼真与真实之间

画面逼真说明视觉效果，不能证明画面所示事件发生过。把这层区别写清楚，是生成技术通识的一部分。

**作者解读：**Ho、Jain与Abbeel这一章把人物志的范围从语言扩展到图像。这里同样存在贯穿全书的关系：研究者设计学习路径，工程者把路径做成系统，使用者则需要判断输出能够支持什么结论。

理解一个时代，不能只看它会生成什么，还要看人们如何辨认生成物的来源和意义。

## 第二十二章　五条路线之后：怎样读一部仍在发生的人物志

### 产品不同，问题相通

| 观察对象 | 本书代表人物与团队 | 主要观察问题 |
| --- | --- | --- |
| OpenAI与GPT、ChatGPT路线 | 奥尔特曼、苏茨克维及研究和产品团队 | 研究如何汇入大众使用入口 |
| Anthropic与Claude路线 | 阿莫代伊兄妹及反馈、安全研究团队 | 原则如何进入训练与组织选择 |
| Google与Gemini路线 | 哈萨比斯、迪恩及跨团队研究者 | 多模态与大型系统如何协作 |
| DeepSeek路线 | 梁文锋及模型、训练系统团队 | 效率与推理能力如何共同改进 |
| 月之暗面与Kimi路线 | 杨植麟及模型、产品团队 | 上下文如何连接任务执行 |

这张表是本书的观察角度，不是对机构研究范围的排他划分。每一家都涉及多种问题；也没有一家可以仅用一句口号概括。

### 把名声、证据和判断拆开

阅读一则人物报道，可以依次问：人物在什么时间参与了什么工作？证据是论文、公告、访谈还是转述？结论适用于哪个任务？如果把人的名字删去，技术论证本身是否仍然成立？

这些问题也约束本书。我们引用论文确认研究存在，引用机构记录确认其公开安排，再明确提出自己的理解。我们不能凭一份报告知道所有内部决策，更不能替人物填写未经证实的动机。

### 留下普通人的位置

一部人物志容易制造距离：仿佛改变世界的始终是极少数天才，普通读者只能在旁边观看。

回看本书，另一幅图景也很清楚。数据需要组织，概念需要讲授，软件需要实现，结果需要复核。李飞飞与吴恩达之所以放在开篇，也因为他们帮助我们看到能力如何获得公共基础、如何被更多人学习。

**作者结语：**我们不必成为下一位著名创始人，才能认真参与这个时代。理解一项技术的条件，核对一句过于漂亮的宣传，给自己的工作建立可靠的验证方法，都是参与。

AI的历史还在继续。一本值得续写的人物志，需要愿意记住名字，也愿意沿着名字走向共同劳动。

## 附录一　人物与技术阅读索引

| 人物或作者群 | 入口章节 | 关键词 |
| --- | --- | --- |
| 李飞飞、邓嘉及ImageNet作者群 | 第一章 | 数据与分类 |
| 吴恩达、Daphne Koller | 第二章 | 教育、能力传播 |
| 辛顿、Rumelhart、Williams | 第三章 | 反向传播、表示学习 |
| 勒丘恩、何恺明等 | 第四章 | 卷积与残差 |
| 本吉奥、Bahdanau、Cho | 第五章 | 注意力、对齐 |
| Vaswani等八位作者 | 第六章 | Transformer、自注意力 |
| 萨顿、巴托 | 第七章 | 奖励、策略、强化学习 |
| 黄仁勋、Ian Buck等 | 第八章 | GPU、CUDA、工程平台 |
| 奥尔特曼、苏茨克维等 | 第九章 | 组织、序列学习、指令反馈 |
| 阿莫代伊兄妹、Kaplan、Bai等 | 第十章 | 缩放规律、原则反馈 |
| 哈萨比斯、迪恩、Jumper等 | 第十一章 | 多模态与科学AI |
| 梁文锋及DeepSeek团队 | 第十二章 | 混合专家、效率、推理 |
| 杨植麟、Dai及Kimi团队 | 第十三章 | 上下文、预训练、智能体 |
| 古德费洛及合作者 | 第十四章 | GAN |
| Lewis、Perez及合作者 | 第十五章 | 检索增强生成 |
| 姚顺雨及合作者 | 第十六章 | ReAct、思维树、行动接口 |
| Wei、Zhou等 | 第十七章 | 中间步骤、提示、推理 |
| Schulman、Rafailov等 | 第十八章 | PPO、DPO、偏好学习 |
| Tri Dao、Albert Gu及合作者 | 第十九章 | FlashAttention、Mamba、效率 |
| Edward Hu及LoRA作者群 | 第二十章 | 低秩适配 |
| Ho、Jain、Abbeel | 第二十一章 | 去噪扩散、图像生成 |

本索引是阅读导航，不代表完整贡献排名。

## 附录二　成长与研究转折简表

这张表选择若干可核对节点，帮助回看人物如何进入研究；它不构成完整履历，年份含义随事件说明。

| 人物 | 早期训练或工作 | 可辨认的转折 | 继续阅读 |
| --- | --- | --- | --- |
| 李飞飞 | 家庭干洗店；物理学本科 | 博士训练；ImageNet | 第一章；[S44][S45][S01] |
| 辛顿 | 心理学；木工 | 1978年博士；1987年多伦多 | 第三章；[S48] |
| 何恺明 | 清华本科、港中大博士 | 工业实验室视觉研究 | 第四章；[S50] |
| 萨顿 | 心理学转计算机科学 | 1978年开始与巴托合作 | 第七章；[S53] |
| 黄仁勋 | 餐馆、电气工程、芯片公司 | 1993年参与创办NVIDIA | 第八章；[S54][S55] |
| 苏茨克维 | 多伦多数学与计算机 | 辛顿门下；OpenAI | 第九章；[S56][S14] |
| Dario Amodei | 物理与生物物理研究 | 2011年博士；Anthropic | 第十章；[S58][S18] |
| Daniela Amodei | 人文学科教育、招聘与风险运营 | 从组织工作进入AI机构 | 第十章；[S59] |
| 姚顺雨 | 清华姚班；普林斯顿 | 2024年智能体博士答辩 | 第十六章；[S69][S70] |
| Jason Wei | 达特茅斯计算机科学 | 数据增强走向推理 | 第十七章；[S71][S72] |
| John Schulman | 物理转神经科学 | Abbeel实验室；强化学习 | 第十八章；[S74] |
| Rafael Rafailov | 数学、统计、经济与金融 | 斯坦福；机器人学习 | 第十八章；[S81] |
| Edward Hu | 微软研究经历 | 继续博士训练与推理研究 | 第二十章；[S83] |
| Jonathan Ho | 伯克利机器人学习实验室博士训练 | 2020年博士；生成模型 | 第二十一章；[S78] |

## 附录三　参考文献与证据说明

以下资料于2026-11-10进行在线检索。论文摘要页核对不等于全文复现实验；机构自述只用于其明确陈述的研究目标、历史记录或报告内容。完整访问范围与核验状态见项目SOURCES.md。

[S01] Deng等：[ImageNet: A Large-Scale Hierarchical Image Database](https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf)，2009。

[S02] Andrew Ng：[Official Website](https://www.andrewng.org/)，动态页面。

[S03] Coursera：[About Coursera](https://about.coursera.org/About/)，动态页面。

[S04] DeepLearning.AI：[About us](https://www.deeplearning.ai/about)，动态页面。

[S05] Rumelhart、Hinton、Williams：[Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0)，1986。

[S06] ACM：[2018 Turing Award announcement](https://awards.acm.org/binaries/content/assets/press-releases/2019/march/turing-award-2018.pdf)，2019-03-27。

[S07] Nobel Prize：[Physics 2024 summary](https://www.nobelprize.org/prizes/physics/2024/summary/)，2024。

[S08] He、Zhang、Ren、Sun：[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)，2015。

[S09] Bahdanau、Cho、Bengio：[Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)，2014。

[S10] Vaswani等八位作者：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)，2017。

[S11] ACM：[2024 Turing Award announcement](https://awards.acm.org/binaries/content/assets/press-releases/2025/march/turing-award-2024.pdf)，2025。

[S12] NVIDIA：[Corporate Timeline](https://www.nvidia.com/en-us/about-nvidia/corporate-timeline/)，动态页面。

[S13] Stanford EE380：[Ian Buck Abstract/Bio](https://web.stanford.edu/class/ee380/Abstracts/Buck.html.dra)，2006-11-29。

[S14] OpenAI：[Introducing OpenAI](https://openai.com/index/introducing-openai/)，2015-12-11。

[S15] Sutskever、Vinyals、Le：[Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215)，2014。

[S16] Ouyang等：[Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)，2022。

[S17] OpenAI等：[GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)，2023。

[S18] Anthropic：[Anthropic raises $124 million Series A](https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems)，2021-05-28。

[S19] Kaplan等：[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)，2020。

[S20] Bai等：[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)，2022。

[S21] Google：[Google DeepMind: Bringing together two world-class AI teams](https://blog.google/innovation-and-ai/technology/ai/april-ai-update/)，2023。

[S22] Gemini Team：[Gemini: A Family of Highly Capable Multimodal Models](https://deepmind.google/gemini/gemini_1_report.pdf)，2023。

[S23] Nobel Prize：[Chemistry 2024 popular information](https://www.nobelprize.org/prizes/chemistry/2024/popular-information/)，2024。

[S24] Associated Press：[Upstart Chinese AI company DeepSeek’s founder started out as a low-key hedge fund entrepreneur](https://apnews.com/article/0673d5c39d90108189cc31b88d85b9f8)，2025。

[S25] DeepSeek-AI：[DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)，2024。

[S26] DeepSeek-AI：[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)，2025。

[S27] DeepSeek-AI：[DeepSeek-R1 repository](https://github.com/deepseek-ai/DeepSeek-R1)，持续更新。

[S28] Dai、Yang等：[Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context](https://arxiv.org/abs/1901.02860)，2019。

[S29] Yang、Dai等：[XLNet: Generalized Autoregressive Pretraining for Language Understanding](https://arxiv.org/abs/1906.08237)，2019。

[S30] Kimi Team：[Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534)，2025。

[S31] Goodfellow等：[Generative Adversarial Networks](https://arxiv.org/abs/1406.2661)，2014。

[S32] Lewis等：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)，2020。

[S33] 姚顺雨：[About / Selected work](https://ysymyth.github.io/)，动态页面。

[S34] Yao等：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)，2022。

[S35] Yao等：[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)，2023。

[S36] Yang、Jimenez等：[SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793)，2024。

[S37] Wei、Wang等：[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)，2022。

[S38] Schulman等：[Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)，2017。

[S39] Rafailov等：[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)，2023。

[S40] Dao等：[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)，2022。

[S41] Gu、Dao：[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)，2023。

[S42] Hu等：[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)，2021。

[S43] Ho、Jain、Abbeel：[Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)，2020。

[S44] Stanford HAI：[Fei-Fei Li: A Candid Look at a Young Immigrant’s Rise to AI Trailblazer](https://hai.stanford.edu/news/fei-fei-li-candid-look-young-immigrants-rise-ai-trailblazer)，2023-11-07。

[S45] Stanford Profiles：[Fei-Fei Li — Bio](https://profiles.stanford.edu/fei-fei-li)，页面所示或动态页面。

[S46] Andrew Ng：[Official Website — Biography](https://www.andrewng.org/)，页面所示或动态页面。

[S47] Coursera：[Andrew Ng — Board biography](https://investor.coursera.com/governance/board-of-directors/person-details/default.aspx?ItemId=5316ab40-32c9-4030-9884-fcc438d7e1f0)，页面所示或动态页面。

[S48] UCL：[Intelligent futures: Geoffrey Hinton, Godfather turned critic of AI](https://www.ucl.ac.uk/about/search-faces-ucl/intelligent-futures-geoffrey-hinton-godfather-turned-critic-ai)，页面所示或动态页面。

[S49] 法国科学院：[Yann Le Cun — Biography](https://academie-sciences.fr/yann-le-cun)，页面所示或动态页面。

[S50] 何恺明：[Personal homepage — Biography](https://people.csail.mit.edu/kaiming/)，页面所示或动态页面。

[S51] 魁北克首席科学家办公室／Yoshua Bengio：[Parcours de Yoshua Bengio](https://www.scientifique-en-chef.gouv.qc.ca/app/uploads/2023/04/yoshua-bengio_assemblee-nationale-5juin2019.pdf)，2019。

[S52] USC Viterbi：[USC Alumni Paved Path for ChatGPT](https://viterbischool.usc.edu/news/2023/03/attention-is-all-you-need-usc-alumni-paved-path-for-chatgpt/)，2023-03。

[S53] ACM：[2024 Turing Award — Sutton and Barto biographies](https://awards.acm.org/binaries/content/assets/press-releases/2025/march/turing-award-2024.pdf)，2025-03。

[S54] NVIDIA：[Jensen Huang Returns to Denny’s](https://blogs.nvidia.com/blog/nvidia-dennys-trillion/)，2023。

[S55] NVIDIA：[2011 Proxy Statement and Form 10-K — Huang biography](https://s201.q4cdn.com/141608511/files/doc_financials/annual/2011/Letter_to_Stockholders_Proxy_Statement_and_Form_10-K_2011.pdf)，2011。

[S56] University of Toronto：[Ilya Sutskever receives U of T honorary degree](https://www.utoronto.ca/news/ilya-sutskever-leader-ai-and-its-responsible-development-receives-u-t-honorary-degree)，2025。

[S57] Y Combinator：[Uncut Interview with Sam Altman on Masters of Scale](https://www.ycombinator.com/blog/uncut-interview-with-sam-altman-on-masters-of-scale/)，2018。

[S58] Princeton University：[TIME100 AI honors six Princetonians — Dario Amodei](https://www.princeton.edu/index.php/news/2023/09/12/time-magazines-time100-artificial-intelligence-list-honors-six-princetonians)，2023-09-12。

[S59] Stanford eCorner：[Helpful, Honest, Harmless AI — transcript](https://ecorner.stanford.edu/wp-content/uploads/sites/2/2024/02/helpful-honest-harmless-ai-entire-talk-transcript.pdf)，2024-02。

[S60] Royal Society：[Demis Hassabis — Fellow biography](https://royalsociety.org/people/demis-hassabis-13817/)，页面所示或动态页面。

[S61] UCL：[Demis Hassabis — AI and neuroscience trailblazer](https://www.ucl.ac.uk/about/search-faces-ucl/smart-tech-smarter-minds-demis-hassabis-ai-and-neuroscience-trailblazer)，页面所示或动态页面。

[S62] University of Washington：[Jeff Dean / Heidi Hopper Endowed Regental Fellowship](https://lazowska.cs.washington.edu/2014.Luncheon.Booklet.pdf)，2014。

[S63] 浙江大学继续教育学院：[杭州六小龙：浙大基因密码是什么？](https://zdpx.zju.edu.cn/news1.aspx?fl=301&id=52646)，2025-02-14。

[S64] CMU Language Technologies Institute：[Zhilin Yang — Alumni 2019](https://www.lti.cs.cmu.edu/people/alumni/alumni-2019/yang-zhilin.html)，页面所示或动态页面。

[S65] CMU Language Technologies Institute：[PhD Dissertations — Zhilin Yang](https://lti.cmu.edu/research/dissertations/index-allyears-obsolete.html)，页面所示或动态页面。

[S66] Ian Goodfellow：[Research Page](https://www.iangoodfellow.com/)，页面所示或动态页面。

[S67] UCL Faculty of Engineering：[UCL and Facebook AI Research to deliver PhD programme](https://www.ucl.ac.uk/engineering/news/2021/feb/ucl-and-facebook-ai-research-deliver-phd-programme)，2021-02。

[S68] Patrick Lewis：[Personal homepage](https://www.patricklewis.io/)，页面所示或动态页面。

[S69] 清华大学交叉信息研究院：[Towards Autonomous Language Agents — Shunyu Yao](https://iiis.tsinghua.edu.cn/en/info/1044/1726.htm)，2023-04-12。

[S70] Princeton Computer Science：[Shunyu Yao Final Public Oral](https://www.cs.princeton.edu/events/26645)，2024-05-02。

[S71] Levy Lab：[Jason Wei — collaborator biography](https://jlevy44.github.io/levylab/people/CL_Jason_Wei/)，页面所示或动态页面。

[S72] Jason Wei：[Personal homepage — research history](https://www.jasonwei.net/)，页面所示或动态页面。

[S73] Denny Zhou：[Personal homepage — publication chronology](https://dennyzhou.github.io/)，页面所示或动态页面。

[S74] UC Berkeley CDSS：[John Schulman on his journey with AI](https://cdss.berkeley.edu/news/chatgpt-architect-berkeley-alum-john-schulman-his-journey-ai)，页面所示或动态页面。

[S75] Chelsea Finn：[Academic CV — students](https://ai.stanford.edu/~cbfinn/_files/cv.pdf)，页面所示或动态页面。

[S76] Princeton University：[Board approves six faculty appointments — Tri Dao](https://research.princeton.edu/news/board-approves-six-faculty-appointments-1)，2024。

[S77] Christopher Ré：[Alumni — Albert Gu](https://cs.stanford.edu/~chrismre/alumni.html)，页面所示或动态页面。

[S78] UC Berkeley Robot Learning Lab：[People — Jonathan Ho alumni record](https://rll.eecs.berkeley.edu/people.html)，页面所示或动态页面。

[S79] Ajay Jain：[Personal homepage — education and research](https://www.ajayj.com/)，页面所示或动态页面。

[S80] UC Berkeley：[Pieter Abbeel — Faculty biography](https://bcbi.berkeley.edu/people/pieter-abbeel)，页面所示或动态页面。

[S81] Rafael Rafailov：[Personal homepage — early education and research](https://rmrafailov.github.io/)，早期主页，新闻更新至2022年前后。

[S82] Google Research：[2014 Google PhD Fellowships: Supporting the Future of Computer Science](https://research.google/blog/2014-google-phd-fellowships-supporting-the-future-of-computer-science/)，2014-06-18。

[S83] Edward Hu：[About](https://edwardjhu.com/about/)，动态页面。

[S84] Peter Bauman／Ian Goodfellow：[Ian Goodfellow on Inventing GANs — interview](https://www.lerandom.art/editorial/ian-goodfellow-on-inventing-gans)，2025-11-04。

## 若谷书房

内容来自全人类的智慧，感谢AI的高效率整合
