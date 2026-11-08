from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, sys, shutil, json
P=Path(__file__).resolve().parents[1]
FONT='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
LATIN='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
PAPER='#F5F2EB'; INK='#142B3B'; TEAL='#146C64'; ORANGE='#D7793F'; MUTED='#64747A'; LINE='#CBD5D0'; WHITE='#FFFFFF'
W,H=1600,1000

def f(s,b=False): return ImageFont.truetype(LATIN if b else FONT,s)
def text(d,xy,s,size=42,color=INK,anchor=None): d.text(xy,s,font=f(size),fill=color,anchor=anchor,spacing=16)
def center(d,box,s,size=42,color=INK):
 x0,y0,x1,y1=box; lines=s.split('\n'); step=size+19
 for i,line in enumerate(lines): text(d,((x0+x1)/2,(y0+y1)/2+(i-(len(lines)-1)/2)*step),line,size,color,'mm')
def card(d,box,s,color=TEAL,fill=WHITE,size=42):
 d.rounded_rectangle(box,radius=16,fill=fill,outline=color,width=4); center(d,box,s,size,color)
def arrow(d,a,b,color=TEAL,width=5):
 d.line([a,b],fill=color,width=width); angle=math.atan2(b[1]-a[1],b[0]-a[0]); n=17
 pts=[b,(b[0]-n*math.cos(angle-.5),b[1]-n*math.sin(angle-.5)),(b[0]-n*math.cos(angle+.5),b[1]-n*math.sin(angle+.5))];d.polygon(pts,fill=color)
def canvas(num,title,subtitle):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 text(d,(76,55),f'NEO LAB  /  图 {num:02d}',28,TEAL)
 text(d,(72,115),title,61)
 text(d,(76,201),subtitle,35,MUTED)
 d.line((76,263,1524,263),fill=LINE,width=2)
 return im,d

def save(im,name):
 p=P/'assets/masters'/name; im.save(p,optimize=True); shutil.copy2(p,P/'assets/illustrations'/name)

def fig01():
 im,d=canvas(1,'组织单位的改变','减少信息中转，同时保留明确的责任与验收。')
 text(d,(335,308),'逐层转交',43,INK,'mm');text(d,(1150,308),'围绕成果协作',43,TEAL,'mm')
 for box,s in [((205,355,465,445),'管理中心'),((125,505,355,595),'部门甲'),((395,505,625,595),'部门乙'),((105,685,335,775),'执行岗位'),((405,685,635,775),'执行岗位')]:card(d,box,s,INK,size=39)
 arrow(d,(335,445),(240,505),INK);arrow(d,(335,445),(510,505),INK);arrow(d,(240,595),(220,685),INK);arrow(d,(510,595),(520,685),INK)
 d.line((750,320,750,825),fill=LINE,width=3)
 card(d,(980,365,1340,448),'人类责任',INK,size=42)
 card(d,(1010,566,1320,670),'可验证成果',ORANGE,size=44)
 for box,s in [((815,477,1030,555),'任务 A'),((1290,477,1505,555),'任务 B'),((815,730,1030,808),'任务 C'),((1290,730,1505,808),'任务 D')]:card(d,box,s,TEAL,size=40)
 for a,b in [((1000,555),(1060,566)),((1320,555),(1280,566)),((1010,730),(1080,670)),((1320,730),(1260,670))]:arrow(d,a,b,TEAL)
 arrow(d,(1160,448),(1160,566),INK)
 center(d,(140,858,1460,960),'组织更灵活，不等于权力和责任自动消失。',39,INK)
 return im

def fig02():
 im,d=canvas(2,'组织形式为何出现','以下是解释框架，不是单线演化或完全替代的时间表。')
 labels=[('早期行政','跨地域征收\n与秩序维持'),('现代官僚制','规则化任职\n与可预期程序'),('工业企业','规模生产\n与跨部门协调'),('数字网络','远程协作\n与知识复用')]
 for i,(title,desc) in enumerate(labels):
  x=76+i*371
  d.ellipse((x+135,357,x+175,397),fill=ORANGE)
  # The four historical lenses are deliberately not joined by progress arrows.
  card(d,(x,440,x+335,550),title,INK,size=42)
  center(d,(x,580,x+335,755),desc,40,TEAL)
 d.line((90,825,1510,825),fill=TEAL,width=7)
 center(d,(110,847,1490,960),'不同形式长期共存；技术、制度与权力共同塑造选择。',39)
 return im

def fig05():
 im,d=canvas(3,'成本下降，也会发生迁移','评估从需求进入到成果被接受的完整过程。')
 data=[('认知成本','检索、比较、生成','部分环节可能下降',TEAL),('协调成本','交接、排期、整合','流程重组才有收益',TEAL),('验证成本','检查、纠错、验收','可能成为新瓶颈',ORANGE),('责任成本','承诺、补救、争议','不会由模型承担',ORANGE)]
 for i,(a,b,c,col) in enumerate(data):
  x=76+i*371;card(d,(x,340,x+335,715),'',col)
  center(d,(x+15,375,x+320,455),a,47,col);center(d,(x+10,490,x+325,555),b,39);center(d,(x+10,604,x+325,675),c,39,col)
 card(d,(100,801,1500,925),'完整成本 = 执行 + 协调 + 验证 + 失败补救 + 持续维护',INK,fill='#E8EDE9',size=37)
 return im

def fig07():
 im,d=canvas(4,'机会判断的两个门槛','高价值需求，还需要成本可承受的验收方式。')
 x0,y0,x1,y1=235,365,1495,847;xm=(x0+x1)//2;ym=(y0+y1)//2
 d.rectangle((xm,y0,x1,ym),fill='#E1EEE7');d.rectangle((x0,y0,x1,y1),outline=LINE,width=3);d.line((xm,y0,xm,y1),fill=LINE,width=3);d.line((x0,ym,x1,ym),fill=LINE,width=3)
 center(d,(x0,y0,xm,ym),'先解决验证难题\n谨慎承诺结果',43,ORANGE)
 center(d,(xm,y0,x1,ym),'优先试验\n真实需求 × 可验收成果',43,TEAL)
 center(d,(x0,ym,xm,y1),'暂不优先\n价值与证据都弱',43,MUTED)
 center(d,(xm,ym,x1,y1),'容易做，但未必值得做\n先确认付费意愿',39,INK)
 arrow(d,(210,865),(210,325),INK,4);arrow(d,(218,866),(1520,866),INK,4)
 text(d,(140,360),'高',36,INK);text(d,(140,795),'低',36,INK);text(d,(80,490),'需求',37,INK);text(d,(80,545),'价值',37,INK)
 text(d,(240,895),'低',34);text(d,(1435,895),'高',34);text(d,(855,921),'结果可验证性',40,INK,'mm')
 return im

def fig09():
 im,d=canvas(5,'一项任务怎样形成闭环','智能体可参与执行；任务契约、验收与反馈决定可靠性。')
 labels=['需求','任务契约','执行','独立验证','交付']
 for i,s in enumerate(labels):
  x=75+i*300;card(d,(x,451,x+247,571),s,ORANGE if i==3 else TEAL,size=43)
  if i<4:arrow(d,(x+250,511),(x+293,511))
 card(d,(378,325,1178,395),'具名责任人：承诺、授权与异常处置',INK,size=37)
 d.line((1123,581,1123,721,488,721),fill=ORANGE,width=5);arrow(d,(488,721),(488,581),ORANGE,5)
 text(d,(790,676),'不通过：纠正输入或执行',37,ORANGE,'mm')
 card(d,(183,814,1417,926),'知识记录：来源 → 判断 → 结果 → 后续改进',INK,fill='#E8EDE9',size=41)
 return im

def fig11():
 im,d=canvas(6,'让权限与后果相匹配','以下是组织设计示意；具体阈值由实际业务确定。')
 rows=[(330,'低影响 · 可撤销','限定范围内自动处理',TEAL),(490,'中等影响 · 可补救','明确额度与人工抽查',TEAL),(650,'高影响 · 难撤销','执行前由有权人员确认',ORANGE)]
 for y,a,b,col in rows:
  card(d,(96,y,667,y+120),a,col,size=43);arrow(d,(685,y+60),(760,y+60),col);card(d,(780,y,1504,y+120),b,col,size=43)
 center(d,(125,824,1475,955),'异常处理：暂停 → 复核 → 补救 → 确认后恢复',42,INK)
 return im

def fig14():
 im,d=canvas(7,'成熟组织的双轨试验','试验获得证据，再决定如何进入正式服务。')
 text(d,(105,380),'主业务',43,INK);text(d,(105,705),'试验轨',43,TEAL)
 for x,label in [(320,'稳定服务'),(775,'共同接口'),(1210,'逐步扩展')]:card(d,(x,345,x+270,465),label,INK,size=42)
 arrow(d,(590,405),(775,405),INK,6);arrow(d,(1045,405),(1210,405),INK,6)
 for x,label in [(320,'限定任务'),(775,'比较与复盘'),(1210,'停止或修订')]:card(d,(x,680,x+270,800),label,TEAL,size=39)
 arrow(d,(590,740),(775,740),TEAL,6)
 card(d,(780,520,1045,610),'证据门',ORANGE,size=43)
 arrow(d,(910,680),(910,610),ORANGE,6);arrow(d,(910,520),(910,465),ORANGE,6)
 text(d,(810,482),'通过',31,ORANGE)
 d.line((1045,565,1345,565),fill=ORANGE,width=5);arrow(d,(1345,565),(1345,680),ORANGE,5)
 text(d,(1100,516),'未通过',36,ORANGE)
 center(d,(100,856,1500,966),'质量、成本、责任与可重复性，共同决定扩大。',42)
 return im

def fig16():
 im,d=canvas(8,'四种未来，可以同时存在','这是情景框架，不是预测概率。')
 x0,y0,x1,y1=275,367,1495,844;xm=(x0+x1)//2;ym=(y0+y1)//2
 d.rectangle((xm,y0,x1,ym),fill='#E1EEE7');d.rectangle((x0,y0,x1,y1),outline=LINE,width=3);d.line((xm,y0,xm,y1),fill=LINE,width=3);d.line((x0,ym,x1,ym),fill=LINE,width=3)
 center(d,(x0,y0,xm,ym),'碎片化服务市场\n容易进入，难辨质量',42,MUTED)
 center(d,(xm,y0,x1,ym),'实验室网络\n可组合，也可自主退出',42,TEAL)
 center(d,(x0,ym,xm,y1),'AI 加固的科层\n集中判断与过程监控',42,INK)
 center(d,(xm,ym,x1,y1),'平台依附的高效团队\n高效交付，入口集中',40,ORANGE)
 arrow(d,(251,866),(251,325),INK,4);arrow(d,(260,866),(1520,866),INK,4)
 text(d,(181,364),'高',34);text(d,(181,796),'低',34);text(d,(78,485),'基础设施',40);text(d,(78,545),'可替代性',40)
 text(d,(277,895),'低',34);text(d,(1438,895),'高',34);text(d,(885,922),'能力可验证性',40,INK,'mm')
 return im

def cover():
 cfg=json.loads((P/'book.json').read_text())
 im=Image.new('RGB',(1600,2268),PAPER);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1600,32),fill=TEAL)
 text(d,(120,150),'组织的下一种可能',42,TEAL)
 d.text((105,280),'NEO LAB',font=f(184,True),fill=INK)
 text(d,(120,555),'AI 原生组织的崛起',91,INK)
 d.line((120,720,1460,720),fill=ORANGE,width=8)
 text(d,(120,775),'从科层制的历史',53,MUTED);text(d,(120,855),'到人机协作的新秩序',53,MUTED)
 # The hierarchy gradually opens into a network; all geometry is original.
 pts={0:(355,1150),1:(225,1340),2:(505,1340),3:(155,1585),4:(370,1585),5:(650,1585),6:(905,1300),7:(1210,1150),8:(1410,1435),9:(1190,1705),10:(865,1770)}
 edges=[(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(2,6),(5,6),(5,10),(6,7),(6,8),(6,9),(6,10),(7,8),(8,9),(9,10),(5,9)]
 for a,b in edges:d.line((pts[a],pts[b]),fill=LINE if a<3 and b<6 else '#A6BEB5',width=5)
 for k,(x,y) in pts.items():
  r=26 if k!=6 else 48;d.ellipse((x-r,y-r,x+r,y+r),fill=ORANGE if k==6 else INK if k<6 else TEAL)
 text(d,(120,2000),cfg['author']+' 著',40,INK)
 text(d,(120,2073),'2026.09.23',33,MUTED)
 text(d,(1455,2088),cfg['publisher'],37,TEAL,'rm')
 save(im,'cover.png')

if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 funcs={1:fig01,2:fig02,5:fig05,7:fig07,9:fig09,11:fig11,14:fig14,16:fig16}
 if mode=='cover':cover()
 elif mode=='anchor':save(fig01(),'fig-01.png')
 else:
  for n,func in funcs.items():save(func(),f'fig-{n:02d}.png')
  cover()
  cfg=json.loads((P/'book.json').read_text());cfg.update({'output_basename':'Neo_Lab_AI原生组织','cover_image':'assets/illustrations/cover.png','font_regular':FONT,'font_bold':FONT,'theme':{'primary':INK,'secondary':TEAL,'accent':ORANGE,'ink':INK,'muted':MUTED,'paper':PAPER},'quality_contract':{'chapter_heading_pattern':'^第[0-9]{2}章','expected_chapters':16,'required_sections':['本章结论与行动']},'cover_label':'NEO LAB','edition':'第一版 · 2026年9月','copyright':'正文含AI辅助创作与研究核验；示意案例和原创方法已作区分。引用资料权利归原权利人。'})
  (P/'book.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
 print('created',mode)
