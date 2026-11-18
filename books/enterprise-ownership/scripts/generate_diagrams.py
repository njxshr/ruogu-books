from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
REGULAR = Path("/Users/lizhao/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/fonts/NotoSansSC-Regular.ttf")
BOLD = Path("/Users/lizhao/Library/Application Support/kimi-desktop/daimon-share/daimon/runtime/python/fonts/NotoSansSC-Bold.ttf")
if not REGULAR.exists():
    REGULAR = Path("/System/Library/Fonts/PingFang.ttc")
if not BOLD.exists():
    BOLD = REGULAR

C = {
    "primary": "#17324D",
    "secondary": "#2F6F73",
    "accent": "#D99A3D",
    "ink": "#1F2937",
    "muted": "#667085",
    "paper": "#F7F3EA",
    "line": "#D8D5CC",
    "white": "#FFFFFF",
}


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def centered(draw, box, text, text_font, fill):
    left, top, right, bottom = box
    bounds = draw.textbbox((0, 0), text, font=text_font)
    w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
    draw.text(((left + right - w) / 2, (top + bottom - h) / 2 - bounds[1]), text, font=text_font, fill=fill)


def base(size, title, subtitle):
    image = Image.new("RGB", size, C["white"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, size[0] - 18, size[1] - 18), radius=28, fill=C["white"], outline=C["line"], width=3)
    draw.text((72, 54), title, font=font(52, True), fill=C["primary"])
    draw.text((74, 126), subtitle, font=font(29), fill=C["muted"])
    draw.line((72, 181, size[0] - 72, 181), fill=C["accent"], width=4)
    return image, draw


def arrow(draw, start, end):
    draw.line((start, end), fill=C["accent"], width=6)
    x, y = end
    draw.polygon(((x, y), (x - 20, y - 14), (x - 20, y + 14)), fill=C["accent"])


def rights_chain():
    image, draw = base((1600, 900), "从企业标签到可检验的制度分析", "沿六个环节逐步核对，保留法人边界、资料时点与证据来源")
    cards = [
        ("01", "主体与任务", ("法人及业务边界", "商业与公共任务")),
        ("02", "出资与控制", ("直接与间接持股", "表决及实际支配")),
        ("03", "决策与授权", ("事项、金额与层级", "信息、异议与追责")),
        ("04", "收益与责任", ("收益如何分配", "后果由谁承担")),
        ("05", "现金与风险", ("回款、债务与担保", "压力情景与退出")),
        ("06", "反证与更新", ("识别推翻证据", "新材料与新时点")),
    ]
    left, top, w, h, gap = 72, 238, 206, 350, 44
    for index, (number, title, lines) in enumerate(cards):
        x = left + index * (w + gap)
        draw.rounded_rectangle((x, top, x + w, top + h), radius=24, fill=C["paper"], outline=C["line"], width=3)
        draw.ellipse((x + 59, top + 26, x + 147, top + 114), fill=C["primary"] if index < 5 else C["secondary"])
        centered(draw, (x + 59, top + 26, x + 147, top + 114), number, font(33, True), C["white"])
        centered(draw, (x + 8, top + 140, x + w - 8, top + 198), title, font(32, True), C["primary"])
        centered(draw, (x + 7, top + 226, x + w - 7, top + 264), lines[0], font(23), C["ink"])
        centered(draw, (x + 7, top + 280, x + w - 7, top + 318), lines[1], font(23), C["ink"])
        if index < len(cards) - 1:
            arrow(draw, (x + w + 7, top + h // 2), (x + w + gap - 8, top + h // 2))
    draw.rounded_rectangle((72, 650, 1528, 802), radius=24, fill=C["primary"])
    centered(draw, (100, 670, 1500, 725), "每次比较都先确认：同一家主体、同一个时点、同一套口径", font(34, True), C["white"])
    centered(draw, (100, 738, 1500, 785), "结论随证据更新；无法取得的材料明确写为“未获得”", font(29), "#E8EEF2")
    image.save(ASSETS / "diagram-analysis-chain.png", optimize=True)


def performance():
    image, draw = base((1600, 920), "五维绩效框架", "用共同的提问纪律组织证据，各类企业按任务确定指标与权重")
    cards = [
        ("商业结果", "收入、利润", "资本回报、现金创造"),
        ("用户与公共结果", "质量、覆盖、可及", "投诉、应急与恢复"),
        ("运营效率", "单位成本、周转", "交付与资源利用"),
        ("长期能力", "技术、人才、数据", "供应链与组织学习"),
        ("风险与责任", "债务、担保、安全", "合规与外部成本"),
    ]
    left, top, w, h, gap = 72, 238, 256, 400, 44
    for index, (title, line1, line2) in enumerate(cards):
        x = left + index * (w + gap)
        draw.rounded_rectangle((x, top, x + w, top + h), radius=24, fill=C["paper"] if index % 2 == 0 else "#F1F6F5", outline=C["line"], width=3)
        draw.rounded_rectangle((x + 22, top + 24, x + w - 22, top + 92), radius=16, fill=C["primary"] if index != 4 else C["secondary"])
        centered(draw, (x + 28, top + 24, x + w - 28, top + 92), f"0{index + 1}", font(32, True), C["white"])
        title_size = 30 if len(title) <= 5 else 27
        centered(draw, (x + 12, top + 126, x + w - 12, top + 195), title, font(title_size, True), C["primary"])
        centered(draw, (x + 12, top + 228, x + w - 12, top + 272), line1, font(25), C["ink"])
        centered(draw, (x + 12, top + 296, x + w - 12, top + 340), line2, font(25), C["ink"])
    draw.rounded_rectangle((72, 694, 1528, 824), radius=24, fill="#EEF3F3", outline=C["secondary"], width=3)
    centered(draw, (100, 710, 1500, 758), "底线指标不能用其他高分抵消；比较前先统一主体、周期与统计口径", font(31, True), C["primary"])
    centered(draw, (100, 770, 1500, 810), "五个维度分别呈现证据，不合成为没有解释力的总分", font(27), C["muted"])
    image.save(ASSETS / "diagram-performance.png", optimize=True)


if __name__ == "__main__":
    rights_chain()
    performance()
    for name in ("diagram-analysis-chain.png", "diagram-performance.png"):
        path = ASSETS / name
        print(f"{path}: {path.stat().st_size} bytes")
