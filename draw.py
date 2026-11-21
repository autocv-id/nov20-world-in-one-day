#!/usr/bin/env python3
"""Build entry.png for news-image-20261120 — 'The World In One Day'.

One-page broadsheet: 33 verified stories from Friday 20 November 2026.
13 mains (3 large + 10 medium), 20 one-line briefs, navy pin map,
6-number strip, region bar, timeline, VERDICT, DATE CHECK.
All text, numbers and artwork drawn from this session's own research.
Cream + ink + red. 1024x1024, target <= 350 KB.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                      # side margin
CW = W - 2 * M              # content width = 968

# ---------- palette ----------
CREAM = (247, 242, 231)
CREAM2 = (239, 231, 211)
PANEL = (233, 224, 196)
INK = (26, 26, 26)
MUTED = (107, 99, 85)
RED = (178, 35, 27)
RED_DK = (140, 24, 18)
NAVY = (27, 42, 74)
NAVY_LT = (143, 163, 199)
NAVY_MD = (58, 74, 106)
GOLD = (176, 132, 52)
WHITE = (255, 255, 255)
SKY = (31, 52, 88)
TEAL = (36, 110, 118)
SAND = (214, 196, 150)
GREEN = (74, 110, 68)

# ---------- fonts ----------
FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def F(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"

f_mast = F(SERIF_B, 62)
f_folio = F(SANS_B, 12)
f_kicker = F(SANS_B, 14)
f_strap = F(FN + "NotoSerif-Italic.ttf", 16)
f_time_h = F(SANS_B, 11)
f_time = F(SANS, 12)
f_strip_n = F(SANS_B, 21)
f_strip_l = F(SANS_B, 10)
f_region = F(SANS_B, 10)
f_region_n = F(SANS_B, 13)
f_h1 = F(SERIF_B, 26)
f_d1 = F(SERIF, 14)
f_a1 = F(SANS, 11)
f_label = F(SANS_B, 12)
f_label2 = F(SANS_B, 10)
f_h2 = F(SERIF_B, 17)
f_d2 = F(SANS, 11)
f_a2 = F(SANS, 10)
f_brief = F(SANS, 12)
f_brief_n = F(SANS_B, 12)
f_map_h = F(SANS_B, 11)
f_pin = F(SANS_B, 7)
f_verdict = F(SERIF_B, 15)
f_dc_h = F(SANS_B, 12)
f_dc = F(SANS, 11)
f_dc_note = F(SERIF, 12)
f_scene_n = F(SANS_B, 15)
f_scene_s = F(SANS_B, 10)
f_scene_xs = F(SANS, 9)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


# ---------- helpers ----------
def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, width):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(trial, font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def rule(y, x0=M, x1=W - M, w=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=w)


def banner(x, y, w, text, font=f_label, bg=RED, fg=WHITE, h=19, pad=7):
    """Red label banner with white text, left-aligned."""
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad, y + (h - font.size) // 2 - 1), text, font=font, fill=fg)


def starburst(cx, cy, r, color=RED, n=8):
    """Explosion star: n spikes."""
    import math
    pts = []
    for i in range(n * 2):
        ang = math.pi * i / n - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 220, 80))


def pin_dot(cx, cy, num, r=6):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=WHITE, width=1)
    t = str(num)
    d.text((cx - tw(t, f_pin) / 2, cy - 4), t, font=f_pin, fill=WHITE)


# ================================================================
# TOP OF PAGE
# ================================================================
# folio line
d.text((M, 6), "FRIDAY 20 NOVEMBER 2026", font=f_folio, fill=INK)
fr = "ONE DAY  ·  ONE PAGE  ·  33 STORIES"
d.text((W - M - tw(fr, f_folio), 6), fr, font=f_folio, fill=MUTED)
rule(22, w=1)

# masthead
mast = "THE WORLD IN ONE DAY"
d.text(((W - tw(mast, f_mast)) / 2, 24), mast, font=f_mast, fill=INK)
rule(90, w=3)
rule(93, w=1)

# kicker
kick = "33 STORIES  ·  13 SCENES  ·  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
d.text(((W - tw(kick, f_kicker)) / 2, 98), kick, font=f_kicker, fill=RED_DK)

# strapline (4 stories, italic)
strap = ("Kyiv\u2019s bridges burn  ·  a cyclone spares 300,000  ·  "
         "the AI rout goes global  ·  and the day\u2019s biggest ruling was Thursday\u2019s")
d.text(((W - tw(strap, f_strap)) / 2, 118), strap, font=f_strap, fill=INK)
rule(138, w=1)

# timeline — one line, red prefix + short entries, all UTC
f_time = F(SANS, 11)
tl_pre = "TIMELINE (UTC)   "
tl = ("02:00 AKVAN LANDS  ·  05:30 POLAND BREACH  ·  11:02 SKIFF FIRES  ·  "
      "12:05 FRANCE: UN MEETING  ·  15:00 HORMUZ HIT  ·  "
      "21:00 NASDAQ \u22125.28%")
d.text((M, 143), tl_pre, font=f_time_h, fill=RED_DK)
d.text((M + tw(tl_pre, f_time_h), 143), tl, font=f_time, fill=INK)
rule(162, w=1)

# 6-number strip
strip = [
    ("110+", "MISSILES ON KYIV"),
    ("300,000", "EVACUATED, ODISHA"),
    ("\u22125.28%", "NASDAQ, FRIDAY"),
    ("20,000", "BPD, KENYA OIL"),
    ("$3.79BN", "GTA VI, DAY ONE"),
    ("118", "PHILLIPS, WELLINGTON"),
]
sy, sh = 168, 38
cell = CW / 6
for i, (num, lab) in enumerate(strip):
    x = M + i * cell
    d.rectangle([x, sy, x + 3, sy + sh], fill=RED)
    d.text((x + 10, sy + 1), num, font=f_strip_n, fill=INK)
    d.text((x + 10, sy + 23), lab, font=f_strip_l, fill=MUTED)
rule(sy + sh + 5, w=1)

# region bar — 7 segments, widths proportional to story counts (sum 33)
regions = [("UKRAINE WAR", 7), ("EUROPE", 7), ("ASIA-PACIFIC", 8),
           ("MIDEAST", 3), ("AMERICAS", 4), ("AFRICA", 2), ("GLOBAL", 2)]
ry, rh = 217, 20
x = M
for i, (name, n) in enumerate(regions):
    wseg = CW * n / 33
    shade = CREAM2 if i % 2 == 0 else PANEL
    d.rectangle([x, ry, x + wseg - 1, ry + rh], fill=shade)
    label = "%s %d" % (name, n)
    d.text((x + (wseg - tw(label, f_region)) / 2, ry + 4),
           label, font=f_region, fill=INK)
    x += wseg
rule(ry + rh + 5, w=2)


# ================================================================
# LARGE MAINS — 3 columns, scene 126px + headline + deck + attribution
# ================================================================
LX = [M, 355, 682]
LW = 314
LY = 248
LH = 126


def scene_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # horizon glow
    d.rectangle([x, y + h - 58, x + w, y + h - 52], fill=(214, 120, 60))
    # city silhouette
    import random
    rnd = random.Random(11)
    bx = x + 4
    while bx < x + w - 14:
        bw = rnd.randint(14, 26)
        bh = rnd.randint(18, 46)
        d.rectangle([bx, y + h - 58 - bh, bx + bw, y + h - 58],
                    fill=(72, 90, 124))
        if rnd.random() < 0.7:
            d.rectangle([bx + 3, y + h - 58 - bh + 4, bx + 6,
                         y + h - 58 - bh + 7], fill=GOLD)
        bx += bw + 3
    # river Dnipro — diagonal band
    d.polygon([(x, y + h - 34), (x + w, y + h - 52),
               (x + w, y + h - 18), (x, y + h)], fill=(74, 110, 150))
    # 3 bridges crossing the river, each hit
    for i, by in enumerate((y + h - 44, y + h - 36, y + h - 28)):
        bx0 = x + 18 + i * 86
        d.line([(bx0, by - 8), (bx0 + 52, by - 14)], fill=(220, 220, 220),
               width=3)
        d.line([(bx0, by - 8), (bx0, by + 2)], fill=(220, 220, 220), width=2)
        d.line([(bx0 + 52, by - 14), (bx0 + 52, by - 4)],
               fill=(220, 220, 220), width=2)
        starburst(bx0 + 26, by - 11, 9)
    # data strip
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(10, 14, 26))
    d.text((x + 6, y + h - 16), "110+ MISSILES  ·  400+ DRONES  ·  8 DEAD",
           font=f_scene_s, fill=WHITE)


def scene_akvan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 130, 138))
    # sea bands
    for i in range(5):
        d.rectangle([x, y + 22 + i * 16, x + w, y + 26 + i * 16],
                    fill=(62, 142, 150))
    # coast — landmass lower right
    d.polygon([(x + w * 0.42, y + h), (x + w, y + h - 66),
               (x + w, y + h)], fill=(150, 168, 110))
    d.polygon([(x + w * 0.55, y + h), (x + w, y + h - 40),
               (x + w, y + h)], fill=(110, 138, 84))
    # cyclone spiral — concentric arcs
    cx, cy = x + 118, y + 56
    for r, a0 in ((46, 200), (38, 140), (30, 80), (22, 20), (14, 320)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
              fill=WHITE, width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    # landfall pin + label (dark pill behind text for contrast)
    px, py = x + 232, y + 78
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE,
              width=2)
    d.rectangle([px - 56, py + 6, px + 48, py + 33], fill=(10, 40, 44))
    d.text((px - 52, py + 8), "GOPALPUR", font=f_scene_s, fill=WHITE)
    d.text((px - 52, py + 20), "LANDFALL 07:30 IST", font=f_scene_xs,
           fill=WHITE)
    # data strip
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(10, 40, 44))
    d.text((x + 6, y + h - 16), "WINDS 90 KM/H  ·  300,000 EVACUATED  ·  0 DEAD",
           font=f_scene_s, fill=WHITE)


def scene_ai(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    # grid
    for gy in range(y + 24, y + h - 22, 18):
        d.line([(x + 8, gy), (x + 168, gy)], fill=(210, 196, 164), width=1)
    # falling line — Asia then US
    pts = [(x + 10, y + 26), (x + 34, y + 38), (x + 58, y + 34),
           (x + 82, y + 52), (x + 106, y + 62), (x + 130, y + 84),
           (x + 152, y + 96), (x + 166, y + 100)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts[::2]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED_DK)
    d.text((x + 10, y + h - 38), "ASIA \u2192 WALL ST", font=f_scene_xs,
           fill=MUTED)
    # index table
    tx = x + 176
    d.text((tx, y + 24), "NASDAQ", font=f_scene_s, fill=INK)
    d.text((tx + 74, y + 24), "\u22125.28%", font=f_scene_n, fill=RED)
    d.text((tx, y + 44), "S&P 500", font=f_scene_s, fill=INK)
    d.text((tx + 74, y + 44), "\u22123.70%", font=f_scene_n, fill=RED)
    d.text((tx, y + 64), "NIKKEI", font=f_scene_s, fill=INK)
    d.text((tx + 74, y + 64), "\u22125.06%", font=f_scene_n, fill=RED)
    d.text((tx, y + 84), "TAIEX", font=f_scene_s, fill=INK)
    d.text((tx + 74, y + 84), "\u22126.23%", font=f_scene_n, fill=RED)
    # data strip
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(10, 14, 26))
    d.text((x + 6, y + h - 16), "WORST WEEK SINCE 2020  ·  VIX 40",
           font=f_scene_s, fill=WHITE)


LARGE = [
    (scene_kyiv, "1  ·  KYIV: 3 BRIDGES HIT",
     "3 KYIV BRIDGES HIT IN ONE NIGHT",
     "Overnight barrage cuts power and water across Kyiv; 8 killed, bridges closed.",
     "REUTERS \u00b7 UKRAINE AIR FORCE"),
    (scene_akvan, "2  ·  ODISHA: CYCLONE AKVAN",
     "THE CYCLONE THAT KILLED NO ONE",
     "Akvan lands near Gopalpur at dawn, weakens by afternoon; no deaths reported.",
     "IMD \u00b7 THE HINDU"),
    (scene_ai, "3  ·  MARKETS: AI ROUT GOES GLOBAL",
     "THE AI SELL-OFF GOES GLOBAL",
     "Nasdaq\u2019s 2nd-biggest points drop ever; Asia\u2019s worst week since 1990.",
     "CNBC \u00b7 REUTERS \u00b7 CLOSING PRICES"),
]

WARN = []


def check(cond, msg):
    if not cond:
        WARN.append(msg)


for i, (fn, label, head, deck, attr) in enumerate(LARGE):
    x = LX[i]
    fn(x, LY, LW, LH)
    banner(x, LY, LW, label)
    check(tw(label, f_label) <= LW - 10, "large banner %d too wide" % i)
    hy = LY + LH + 5
    hlines = wrap(head, f_h1, LW)
    check(len(hlines) <= 2, "large headline %d wraps to %d lines" % (i, len(hlines)))
    for j, line in enumerate(hlines):
        d.text((x, hy + j * 28), line, font=f_h1, fill=INK)
    dy = hy + len(hlines) * 28 + 2
    dlines = wrap(deck, f_d1, LW)
    check(len(dlines) <= 2, "large deck %d wraps to %d lines" % (i, len(dlines)))
    for j, line in enumerate(dlines):
        d.text((x, dy + j * 16), line, font=f_d1, fill=INK)
    d.text((x, dy + len(dlines) * 16 + 2), attr, font=f_a1, fill=MUTED)

LARGE_END = LY + LH + 5 + 58 + 30 + 14   # 481
rule(LARGE_END + 4, w=1)


# ================================================================
# MEDIUM MAINS — 5 cols x 2 rows, scene 74px + headline + 1-line deck
# ================================================================
MX = [M, 224, 420, 616, 812]
MW = 184
MROW_Y = [490, 636]
MH = 70


def chip(x, y, text):
    """Small CLAIM/FORECAST chip: white box, red border + red text."""
    wch = tw(text, f_scene_xs) + 8
    d.rectangle([x, y, x + wch, y + 12], fill=WHITE, outline=RED, width=1)
    d.text((x + 4, y + 1), text, font=f_scene_xs, fill=RED_DK)


def scene_poland(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 214, 188))
    # rough Poland blob
    d.polygon([(x + 30, y + 24), (x + 78, y + 20), (x + 120, y + 26),
               (x + 150, y + 34), (x + 158, y + 48), (x + 140, y + 62),
               (x + 96, y + 68), (x + 52, y + 66), (x + 26, y + 52),
               (x + 22, y + 36)], fill=SAND, outline=MUTED)
    d.line([(x + 150, y + 30), (x + 168, y + 28)], fill=RED_DK, width=2)
    d.text((x + 152, y + 30), "UKR", font=f_scene_xs, fill=RED_DK)
    for px, py in ((128, 34), (146, 44), (118, 52)):
        d.ellipse([x + px - 4, y + py - 4, x + px + 4, y + py + 4],
                  fill=RED, outline=WHITE, width=1)
    d.text((x + 6, y + h - 14), "06:30 LOCAL  ·  3 CROSSED", font=f_scene_xs,
           fill=INK)


def scene_iraq(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 200, 140))
    d.ellipse([x + 148, y + 22, x + 170, y + 44], fill=(240, 200, 90))
    # compound walls
    d.rectangle([x + 14, y + 40, x + 120, y + 68], fill=(178, 148, 96))
    d.rectangle([x + 14, y + 34, x + 30, y + 68], fill=(160, 130, 80))
    d.rectangle([x + 104, y + 34, x + 120, y + 68], fill=(160, 130, 80))
    d.rectangle([x + 58, y + 50, x + 76, y + 68], fill=(90, 70, 44))
    d.text((x + 128, y + 50), "12 YRS", font=f_scene_n, fill=RED_DK)
    d.text((x + 6, y + h - 14), "HELD SINCE 2014  ·  NO CLASHES",
           font=f_scene_xs, fill=INK)


def scene_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 96, 140))
    d.polygon([(x, y + 20), (x + 62, y + 20), (x + 52, y + h),
               (x, y + h)], fill=(150, 168, 110))
    d.polygon([(x + w, y + 20), (x + 122, y + 20), (x + 132, y + h),
               (x + w, y + h)], fill=(150, 168, 110))
    # tanker
    d.rectangle([x + 62, y + 44, x + 122, y + 56], fill=(30, 30, 34))
    d.rectangle([x + 106, y + 34, x + 118, y + 44], fill=WHITE)
    d.rectangle([x + 62, y + 56, x + 122, y + 59], fill=RED_DK)
    starburst(x + 70, y + 38, 8)
    chip(x + 96, y + h - 15, "CLAIM: MINE \u2014 IRGC")
    d.text((x + 6, y + h - 14), "15:00 UTC", font=f_scene_xs, fill=WHITE)


def scene_italy(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
    # crowd silhouettes + placards
    for i, cx in enumerate(range(14, 176, 22)):
        cy = y + 58 - (i % 3) * 3
        d.ellipse([x + cx - 5, cy - 12, x + cx + 5, cy - 2], fill=INK)
        d.pieslice([x + cx - 9, cy - 2, x + cx + 9, cy + 16], 180, 360,
                   fill=INK)
    for px, py, txt in ((30, 30, "PAY"), (86, 26, "SCHOOLS"), (140, 30, "1M+")):
        half = tw(txt, f_scene_xs) / 2 + 3
        d.line([(x + px, y + py + 10), (x + px, y + py + 24)], fill=INK,
               width=2)
        d.rectangle([x + px - half, y + py, x + px + half, y + py + 10],
                    fill=WHITE, outline=RED, width=1)
        d.text((x + px - tw(txt, f_scene_xs) / 2, y + py + 1), txt,
               font=f_scene_xs, fill=RED_DK)
    d.text((x + 6, y + h - 14), "ALL SECTORS  ·  100+ CITIES",
           font=f_scene_xs, fill=INK)


def scene_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
    d.rectangle([x + 16, y + 24, x + 108, y + 70], fill=WHITE,
                outline=MUTED)
    for i, ly in enumerate(range(y + 30, y + 66, 7)):
        d.line([(x + 22, ly), (x + 102 - (i % 3) * 12, ly)],
               fill=(180, 180, 180), width=2)
    d.text((x + 118, y + 26), "144\u219280", font=f_scene_n, fill=INK)
    d.text((x + 118, y + 46), "PARAS", font=f_scene_xs, fill=MUTED)
    d.text((x + 6, y + h - 14), "FOSSIL FUELS: CUT FROM TEXT",
           font=f_scene_xs, fill=RED_DK)


def scene_ukeu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    # Union Jack (simplified) + EU flag
    d.rectangle([x + 12, y + 26, x + 82, y + 62], fill=(40, 60, 130))
    d.rectangle([x + 12, y + 41, x + 82, y + 47], fill=WHITE)
    d.rectangle([x + 44, y + 26, x + 50, y + 62], fill=WHITE)
    d.rectangle([x + 12, y + 43, x + 82, y + 45], fill=RED)
    d.rectangle([x + 46, y + 26, x + 48, y + 62], fill=RED)
    d.rectangle([x + 96, y + 26, x + 166, y + 62], fill=(30, 60, 150))
    import math
    for k in range(12):
        a = 2 * math.pi * k / 12
        d.ellipse([x + 131 + 18 * math.cos(a) - 2,
                   y + 44 + 13 * math.sin(a) - 2,
                   x + 131 + 18 * math.cos(a) + 2,
                   y + 44 + 13 * math.sin(a) + 2], fill=(255, 210, 60))
    d.text((x + 6, y + h - 14), "100,000 VISAS/YR EACH WAY",
           font=f_scene_xs, fill=INK)


def scene_japan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    for gy in range(y + 26, y + h - 16, 10):
        d.line([(x + 8, gy), (x + 110, gy)], fill=(210, 196, 164), width=1)
    pts = [(x + 10, y + 58), (x + 34, y + 54), (x + 58, y + 50),
           (x + 82, y + 40), (x + 106, y + 32)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.text((x + 118, y + 26), "+2.3%", font=f_scene_n, fill=RED)
    d.text((x + 118, y + 44), "OCT CPI", font=f_scene_xs, fill=MUTED)
    d.text((x + 6, y + h - 14), "BOJ MEETS 17\u201318 DEC",
           font=f_scene_xs, fill=INK)


def scene_kenya(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 210, 150))
    # pumpjack silhouette
    d.line([(x + 30, y + 62), (x + 52, y + 28)], fill=INK, width=3)
    d.line([(x + 74, y + 62), (x + 52, y + 28)], fill=INK, width=3)
    d.line([(x + 20, y + 30), (x + 92, y + 24)], fill=INK, width=4)
    d.line([(x + 88, y + 24), (x + 88, y + 44)], fill=INK, width=2)
    d.rectangle([x + 84, y + 44, x + 92, y + 52], fill=INK)
    d.rectangle([x + 18, y + 62, x + 96, y + 66], fill=INK)
    d.text((x + 108, y + 26), "1 DEC", font=f_scene_n, fill=RED_DK)
    d.text((x + 108, y + 44), "FIRST OIL", font=f_scene_xs, fill=INK)
    d.text((x + 6, y + h - 14), "20,000 BPD PHASE 1  ·  TURKANA",
           font=f_scene_xs, fill=INK)


def scene_seoul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 214, 188))
    # assembly dome + columns
    d.pieslice([x + 30, y + 22, x + 110, y + 62], 180, 360, fill=(120, 110, 90))
    d.rectangle([x + 24, y + 48, x + 116, y + 66], fill=(120, 110, 90))
    for cx in range(34, 112, 16):
        d.rectangle([x + cx, y + 52, x + cx + 5, y + 66], fill=CREAM)
    d.rectangle([x + 128, y + 30, x + 160, y + 38], fill=INK)
    d.line([(x + 144, y + 38), (x + 144, y + 56)], fill=INK, width=3)
    d.text((x + 126, y + 20), "161/300", font=f_scene_s, fill=RED_DK)
    d.text((x + 6, y + h - 14), "DP ADOPTS IMPEACHMENT POLICY",
           font=f_scene_xs, fill=INK)


def scene_phillips(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 176))
    d.rectangle([x, y + 46, x + w, y + h], fill=(150, 178, 120))
    # stumps + bat + ball
    for sx in (36, 44, 52):
        d.line([(x + sx, y + 40), (x + sx, y + 58)], fill=(220, 180, 60),
               width=3)
    d.polygon([(x + 84, y + 24), (x + 94, y + 28), (x + 78, y + 58),
               (x + 68, y + 54)], fill=(214, 178, 120))
    d.line([(x + 89, y + 26), (x + 100, y + 18)], fill=INK, width=3)
    d.ellipse([x + 120, y + 26, x + 130, y + 36], fill=RED)
    d.text((x + 128, y + 40), "118", font=f_scene_n, fill=INK)
    d.text((x + 6, y + h - 14), "216-RUN STAND  ·  NZ 368",
           font=f_scene_xs, fill=INK)


MEDIUM = [
    (scene_poland, "4  ·  POLAND: NATO BREACH",
     "2 MISSILES HIT POLAND",
     "Tusk: \u2018intentional provocation\u2019", "AP \u00b7 REUTERS"),
    (scene_iraq, "5  ·  IRAQ: TOWN RETAKEN",
     "TROOPS TAKE MILITIA TOWN",
     "Militia to quit within a month", "REUTERS \u00b7 VOA"),
    (scene_hormuz, "6  ·  HORMUZ: TANKER HIT",
     "TANKER HIT, FIRE ON BOARD",
     "No casualties, no spill", "UKMTO \u00b7 REUTERS"),
    (scene_italy, "7  ·  ITALY: GENERAL STRIKE",
     "ITALY STOPS FOR GENERAL STRIKE",
     "Union claims 1m+ marchers", "REUTERS"),
    (scene_cop31, "8  ·  COP31: NO DEAL",
     "CLIMATE TALKS END, NO DEAL",
     "No fossil fuels in the draft", "UN NEWS \u00b7 CARBON BRIEF"),
    (scene_ukeu, "9  ·  UK\u2013EU: RESET SEALED",
     "100,000 VISAS A YEAR, EACH WAY",
     "\u00a317bn boost claimed by 2040", "REUTERS \u00b7 THE TIMES"),
    (scene_japan, "10  ·  JAPAN: CPI +2.3%",
     "INFLATION HITS 12-MONTH HIGH",
     "72% priced for a December hike", "STATISTICS BUREAU"),
    (scene_kenya, "11  ·  KENYA: FIRST OIL",
     "KENYA SWITCHES ON FIRST OIL",
     "Output starts 1 Dec; 20,000 bpd", "CAPITAL FM"),
    (scene_seoul, "12  ·  SEOUL: IMPEACHMENT",
     "SEOUL TO IMPEACH JUDGE",
     "Motion due before year-end", "ASIA DAILY"),
    (scene_phillips, "13  ·  PHILLIPS 118",
     "PHILLIPS\u2019 118 LIFTS NZ",
     "Nicholls 175*; India 159/1", "AP \u00b7 REUTERS"),
]

for i, (fn, label, head, deck, attr) in enumerate(MEDIUM):
    col, row = i % 5, i // 5
    x, y = MX[col], MROW_Y[row]
    fn(x, y, MW, MH)
    banner(x, y, MW, label, font=f_label2)
    check(tw(label, f_label2) <= MW - 10, "medium banner %d too wide" % i)
    hy = y + MH + 3
    hlines = wrap(head, f_h2, MW)
    check(len(hlines) <= 2, "medium headline %d wraps to %d lines: %s"
          % (i, len(hlines), head))
    for j, line in enumerate(hlines):
        d.text((x, hy + j * 18), line, font=f_h2, fill=INK)
    dy2 = hy + len(hlines) * 18 + 2
    check(tw(deck, f_d2) <= MW, "medium deck %d too wide: %s" % (i, deck))
    d.text((x, dy2), deck, font=f_d2, fill=INK)
    d.text((x, dy2 + 13), attr, font=f_a2, fill=MUTED)

MED_END = MROW_Y[1] + MH + 3 + 52 + 12   # 773


# ================================================================
# VERDICT + BOTTOM ROW (map + ALSO) + DATE CHECK
# ================================================================
rule(MED_END + 4, w=1)

# VERDICT strip
vy = MED_END + 9
f_verdict = F(SERIF_B, 14)
verdict = ("VERDICT: WAR ESCALATED, MARKETS\u2019 WORST WEEK SINCE 2020 "
           "\u2014 AND THE CYCLONE KILLED NO ONE.")
check(tw(verdict, f_verdict) <= CW - 14, "verdict too wide")
d.rectangle([M, vy, W - M, vy + 20], fill=PANEL)
d.rectangle([M, vy, M + 3, vy + 20], fill=RED)
d.text((M + 10, vy + 2), verdict, font=f_verdict, fill=INK)

# header row for bottom section
hy2 = vy + 26
d.text((M, hy2), "WHERE IT HAPPENED \u2014 33 PINS", font=f_map_h, fill=RED_DK)
d.text((340, hy2), "ALSO \u2014 IN BRIEF", font=f_map_h, fill=RED_DK)
d.text((W - M - tw("EVERY ITEM DATED 20 NOV 2026", f_scene_xs), hy2 + 1),
       "EVERY ITEM DATED 20 NOV 2026", font=f_scene_xs, fill=MUTED)

# ---- navy pin map (bottom-left) ----
MAP_X, MAP_Y, MAP_W, MAP_H = M, hy2 + 17, 302, 128
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=NAVY)
# land cells: (row, col ranges) on a 48x24 equirectangular grid
# row r covers lat 90-7.5r .. 82.5-7.5r; col c covers lon -180+7.5c .. -172.5+7.5c
LAND = {
    0: [(18, 20)],
    1: [(9, 13), (16, 21), (26, 26), (31, 32), (36, 37)],
    2: [(5, 7), (9, 14), (17, 21), (25, 26), (28, 47)],
    3: [(4, 8), (9, 16), (18, 18), (22, 22), (25, 27), (28, 47)],
    4: [(6, 7), (8, 17), (18, 19), (23, 23), (25, 27), (28, 46)],
    5: [(6, 17), (23, 23), (24, 30), (31, 40), (41, 45)],
    6: [(6, 16), (22, 23), (24, 28), (29, 35), (36, 41), (42, 42)],
    7: [(7, 16), (21, 30), (31, 35), (36, 41), (42, 42)],
    8: [(7, 12), (21, 31), (32, 37), (38, 41)],
    9: [(8, 12), (22, 31), (35, 40), (41, 41)],
    10: [(9, 11), (13, 16), (22, 30), (37, 40), (41, 43)],
    11: [(12, 17), (23, 30), (39, 44)],
    12: [(12, 17), (23, 30), (40, 44)],
    13: [(13, 17), (23, 29), (41, 45)],
    14: [(13, 17), (23, 29), (30, 30), (41, 45)],
    15: [(13, 16), (23, 28), (30, 30), (41, 45)],
    16: [(13, 16), (24, 27), (42, 45)],
    17: [(13, 15), (44, 45), (46, 47)],
    18: [(13, 14)],
    19: [(13, 13)],
    21: [(8, 10), (22, 24), (38, 40)],
}
LAT_TOP, LAT_BOT = 75.0, -55.0   # cropped inhabited band


def project(lat, lon):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return px, py


for r, spans in LAND.items():
    lat_c = 90 - 7.5 * r - 3.75
    if lat_c > LAT_TOP or lat_c < LAT_BOT:
        continue
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            lon_c = -180 + 7.5 * c + 3.75
            px, py = project(lat_c, lon_c)
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                      fill=NAVY_LT)

# pins: (num, lat, lon, dx_px, dy_px) — dx/dy deconflict the Europe cluster
PINS = [
    (1, 50.4, 30.5, -6, -6), (2, 19.3, 84.9, 0, 0), (3, 40.7, -74.0, -8, -8),
    (4, 53.7, 20.4, 4, -6), (5, 32.8, 44.2, 0, 0), (6, 26.2, 56.2, 0, 0),
    (7, 41.9, 12.5, 0, 4), (8, 36.9, 30.7, 0, 0), (9, 50.8, 4.4, -9, -9),
    (10, 35.7, 139.7, 6, 0), (11, 3.5, 35.6, 0, 0), (12, 37.5, 127.0, 6, 0),
    (13, -41.3, 174.8, 0, 0), (14, 39.9, 116.4, -6, 0),
    (15, 22.5, 114.1, 0, 0), (16, 38.9, -77.0, -8, 8),
    (17, 38.9, -77.0, 8, -8), (18, 52.5, 13.4, 0, -9),
    (19, 28.6, 77.2, 0, 0), (20, 50.8, 4.4, 9, -9),
    (21, 51.5, -0.1, -12, -8), (22, 13.5, 30.5, 0, 0),
    (23, 40.7, -74.0, 8, 8), (24, 50.8, 4.4, -9, 9),
    (25, 50.8, 4.4, 9, 9), (26, 54.9, 33.3, 6, 6),
    (27, 14.5, 49.1, 0, 0), (28, 50.1, 8.7, 10, 8),
    (29, 43.9, -1.3, -8, 6), (30, 48.9, 2.3, -10, 10),
    (31, 52.5, 13.4, 9, 0), (32, -15.8, -47.9, 0, 0),
    (33, 19.8, 96.1, 0, 0),
]
for num, lat, lon, dx, dy in PINS:
    px, py = project(lat, lon)
    pin_dot(px + dx, py + dy, num)

# ---- ALSO: 20 briefs, 2 columns x 10 ----
BRIEFS = [
    "CHINA HOLDS RATES 3.00%/3.50%, 18TH MONTH",
    "XI HAILS \u2018TURNAROUND\u2019 WITH AUSTRALIA",
    "US SENTIMENT 51.5, UP FROM 48.0",
    "TRUMP: \u2018VERY GOOD TALKS\u2019 WITH PUTIN",
    "GERMAN PPI +8.1%, FASTEST SINCE 2023",
    "INDIA CORE OUTPUT +10.9%, A RECORD",
    "EU CONFIDENCE \u221216.9, BEATS FORECAST",
    "UK SHOPPING +0.7% ON \u2018BE READY\u2019 FEARS",
    "SUDAN ARMY TAKES RSF HOLDOUT AL-MAZROUB",
    "GTA VI: $3.79BN IN A DAY, TAKE-TWO SAYS",
    "EU APPROVES \u20ac1BN ARMS FOR UKRAINE",
    "EU SENDS RECORD \u20ac7.9BN CASH TO KYIV",
    "DRONES HIT DOROGOBUZH CHEMICAL PLANT",
    "SKIFF FIRES ON BULKER OFF YEMEN; NO HARM",
    "ECB: BOONE + BRUNNERMEIER NOMINATED",
    "BULKER MIRO G AGROUND; 19 AIRLIFTED",
    "FRANCE SEEKS UN MEETING OVER KYIV",
    "MERZ: \u2018RUSSIA WILL NOT WIN THIS WAR\u2019",
    "BOLSONARO, 71, TAKEN TO HOSPITAL",
    "MYANMAR CALLS ICJ RULING \u2018UNFAIR\u2019",
]
f_brief2 = F(SANS, 11)
AY = MAP_Y + 1
for i, text in enumerate(BRIEFS):
    col = i // 10
    row = i % 10
    bx = 340 + col * 330
    by = AY + row * 13
    num = str(14 + i)
    d.text((bx, by), num, font=f_brief_n, fill=RED)
    d.text((bx + tw(num + "  ", f_brief_n), by), text, font=f_brief2,
           fill=INK)

# ---- DATE CHECK ----
DC_Y = MAP_Y + MAP_H + 8
rule(DC_Y, w=1)
d.text((M, DC_Y + 4), "DATE CHECK", font=f_dc_h, fill=RED_DK)
note = "\u2014 NOT SHOWN BECAUSE THEY HAPPENED ON ANOTHER DAY"
d.text((M + tw("DATE CHECK ", f_dc_h), DC_Y + 4), note, font=f_dc_h,
       fill=INK)
d.text((W - M - tw("CHIP: CLAIM = UNVERIFIED CLAIM", f_scene_xs),
        DC_Y + 6), "CHIP: CLAIM = UNVERIFIED CLAIM", font=f_scene_xs,
       fill=MUTED)
DC_ITEMS = [
    "ICJ: MYANMAR GUILTY OF GENOCIDE \u2014 THU",
    "TRUMP\u2013XI\u2013PUTIN TRILATERAL \u2014 THU",
    "ANTHROPIC IPO DEBUT, +17% \u2014 THU",
    "UK PLEDGES 1,000 DRONES \u2014 THU",
    "DENMARK RATIFIES GREENLAND DEAL \u2014 THU",
    "ARGENTINA DISABILITY LAW 71\u20130 \u2014 THU",
    "TRUMP PARDONS PETE ROSE \u2014 THU",
    "US SANCTIONS COMANCHEROS \u2014 THU",
    "HOUTHI STRIKE ON RIYADH TOWER \u2014 THU",
    "IEA: DATA-CENTRE CO2 +70% BY 2030 \u2014 THU",
    "JUDGE: ROLLINS EMAILS UNCONSTITUTIONAL \u2014 THU",
    "BEPICOLOMBO ENTERS MERCURY ORBIT \u2014 SAT",
]
for i, item in enumerate(DC_ITEMS):
    col, row = i // 4, i % 4
    dx = M + col * 323
    dy = DC_Y + 22 + row * 12
    d.text((dx, dy), "\u00d7", font=f_dc, fill=RED)
    d.text((dx + 12, dy), item, font=f_dc, fill=INK)

# ---- validation: every measured element must fit its box ----
check(tw(tl_pre, f_time_h) + tw(tl, f_time) <= CW, "timeline too wide")
check(tw(strap, f_strap) <= CW, "strapline too wide")
check(tw(kick, f_kicker) <= CW, "kicker too wide")
check(tw(mast, f_mast) <= CW, "masthead too wide")
for i, text in enumerate(BRIEFS):
    wline = tw(str(14 + i) + "  ", f_brief_n) + tw(text, f_brief2)
    check(wline <= 322, "brief %d too wide: %s" % (14 + i, text))
for i, item in enumerate(DC_ITEMS):
    check(12 + tw(item, f_dc) <= 318, "date-check %d too wide" % i)
for name, n in regions:
    check(tw("%s %d" % (name, n), f_region) <= CW * n / 33 - 2,
          "region %s too wide" % name)
if WARN:
    print("WARNINGS:")
    for wmsg in WARN:
        print(" -", wmsg)
else:
    print("all width checks passed")

# ---- save ----
img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
