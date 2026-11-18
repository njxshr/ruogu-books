from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parents[1]
ASSETS = PROJECT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

REGULAR = Path("/Users/lizhao/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/fonts/NotoSansSC-Regular.ttf")
BOLD = Path("/Users/lizhao/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/fonts/NotoSansSC-Bold.ttf")
if not REGULAR.exists():
    REGULAR = Path("/System/Library/Fonts/PingFang.ttc")
if not BOLD.exists():
    BOLD = REGULAR

COLORS = {
    "primary": "#8C1D25",
    "secondary": "#6B3034",
    "accent": "#C63D43",
    "ink": "#292326",
    "muted": "#74696B",
    "paper": "#F7F1E8",
    "line": "#DDCFC7",
    "white": "#FFFDFC",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, text_font, fill: str) -> None:
    left, top, right, bottom = box
    bounds = draw.textbbox((0, 0), text, font=text_font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    draw.text(((left + right - width) / 2, (top + bottom - height) / 2 - bounds[1]), text, font=text_font, fill=fill)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 8) -> None:
    draw.line((start, end), fill=color, width=width)
    x, y = end
    draw.polygon(((x, y), (x - 22, y - 15), (x - 22, y + 15)), fill=color)


def base(size: tuple[int, int], title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", size, COLORS["white"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, size[0] - 18, size[1] - 18), radius=28, fill=COLORS["white"], outline=COLORS["line"], width=3)
    draw.text((72, 54), title, font=font(52, True), fill=COLORS["primary"])
    draw.text((74, 126), subtitle, font=font(29), fill=COLORS["muted"])
    draw.line((72, 181, size[0] - 72, 181), fill=COLORS["accent"], width=4)
    return image, draw


def workflow() -> None:
    image, draw = base((1600, 820), "从真实任务到个人工作系统", "每一步都留下可以检查的成果，验收记录再进入下一次任务")
    cards = [
        ("01", "准备材料", ("明确使用场景", "限定目录与版本")),
        ("02", "写清委托", ("目标与业务规则", "交付物和边界")),
        ("03", "观察执行", ("保留中间成果", "记录异常与介入")),
        ("04", "验收交付", ("回查事实与计算", "打开文件查版式")),
        ("05", "沉淀复用", ("保存模板和技能", "再扩展自动执行")),
    ]
    card_w, card_h, gap, left, top = 256, 360, 42, 72, 238
    for index, (number, title, lines) in enumerate(cards):
        x = left + index * (card_w + gap)
        draw.rounded_rectangle((x, top, x + card_w, top + card_h), radius=26, fill=COLORS["paper"], outline=COLORS["line"], width=3)
        draw.ellipse((x + 82, top + 28, x + 174, top + 120), fill=COLORS["primary"] if index < 4 else COLORS["accent"])
        centered(draw, (x + 82, top + 28, x + 174, top + 120), number, font(35, True), "#FFFFFF")
        centered(draw, (x + 14, top + 145, x + card_w - 14, top + 205), title, font(38, True), COLORS["secondary"])
        centered(draw, (x + 12, top + 230, x + card_w - 12, top + 268), lines[0], font(27), COLORS["ink"])
        centered(draw, (x + 12, top + 282, x + card_w - 12, top + 320), lines[1], font(27), COLORS["ink"])
        if index < len(cards) - 1:
            arrow(draw, (x + card_w + 7, top + card_h // 2), (x + card_w + gap - 8, top + card_h // 2), COLORS["accent"], 6)
    draw.rounded_rectangle((72, 652, 1528, 738), radius=22, fill=COLORS["primary"])
    centered(draw, (100, 652, 1500, 738), "反馈回路：缺失、冲突、返工与有效规则都进入项目说明和下一次委托", font(32, True), "#FFFFFF")
    image.save(ASSETS / "diagram-workflow.png", optimize=True)


def system_layers() -> None:
    image, draw = base((1600, 1120), "个人工作系统的五个层次", "从项目现场开始逐层沉淀；任何一层都可以回到真实交付检查价值")
    layers = [
        ("项目层", "材料、主版本、业务规则、交付记录", "工作有清楚现场"),
        ("方法层", "任务模板、技能、验收清单", "稳定做法可以复用"),
        ("连接层", "插件、浏览器流程、外部数据", "材料与工具接得上"),
        ("视图层", "小组件、看板、来源和更新时间", "重要状态持续可见"),
        ("运行层", "目标、定时任务、运行记录和异常处理", "稳定流程持续执行"),
    ]
    top, row_h, gap = 232, 134, 22
    for index, (name, content, value) in enumerate(layers):
        y = top + index * (row_h + gap)
        fill = COLORS["paper"] if index % 2 == 0 else "#FBF7F2"
        draw.rounded_rectangle((72, y, 1528, y + row_h), radius=22, fill=fill, outline=COLORS["line"], width=3)
        draw.rounded_rectangle((92, y + 18, 292, y + row_h - 18), radius=16, fill=COLORS["primary"] if index < 4 else COLORS["accent"])
        centered(draw, (92, y + 18, 292, y + row_h - 18), name, font(36, True), "#FFFFFF")
        draw.text((338, y + 26), content, font=font(32, True), fill=COLORS["ink"])
        draw.text((338, y + 77), value, font=font(27), fill=COLORS["muted"])
        if index < len(layers) - 1:
            draw.line((1445, y + row_h + 2, 1445, y + row_h + gap - 3), fill=COLORS["accent"], width=5)
            draw.polygon(((1445, y + row_h + gap - 3), (1433, y + row_h + gap - 20), (1457, y + row_h + gap - 20)), fill=COLORS["accent"])
    draw.text((74, 1030), "检查顺序：材料是否好找 → 交付是否可查 → 异常是否早见 → 维护是否可持续", font=font(29), fill=COLORS["secondary"])
    image.save(ASSETS / "diagram-system.png", optimize=True)


if __name__ == "__main__":
    workflow()
    system_layers()
    for name in ("diagram-workflow.png", "diagram-system.png"):
        path = ASSETS / name
        print(f"{path} {path.stat().st_size} bytes")
