#!/usr/bin/env python3
"""news-23 b145 numbers-led: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Numbers-led: BIG number grid first, then masthead content, 3 hero scenes, 10 cards,
map + ALSO, DATE CHECK, footer. Output 1024x1024 PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------- palette ----------
PAPER = (250, 247, 238)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (16, 32, 64)
GOLD = (176, 141, 30)
GREEN = (24, 90, 52)
GREY = (110, 110, 105)
LIGHT = (232, 228, 218)
MAPGREEN = (198, 224, 178)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28  # margin

# ============ MASTHEAD ============
d.text((MX, 6), "THE WORLD TODAY", font=SERIF_B(52), fill=INK)
d.text((W - MX - text_w(d, "MONDAY 23 NOVEMBER 2026", SANS_B(15)), 30),
       "MONDAY 23 NOVEMBER 2026", font=SANS_B(15), fill=GOLD)
d.line([(MX, 74), (W - MX, 74)], fill=GOLD, width=3)

# ============ KICKER (red strip) ============
d.rectangle([0, 80, W, 102], fill=RED)
kick = "AI rout hits Asia   ·   UN chief urges AI rules   ·   US lead over China at record low   ·   Anthropic IPO $107.3B"
d.text((MX, 85), kick, font=SANS_B(14), fill=(255, 255, 255))

# ============ BIG NUMBER GRID (2 rows x 5 cols) ============
nums = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
grid_y0, grid_y1 = 108, 216
cell_w = (W - 2 * MX) / 5
for i, (val, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x0 = MX + col * cell_w
    y0 = grid_y0 + row * 54
    if col:
        d.line([(x0 - 6, y0 + 4), (x0 - 6, y0 + 48)], fill=(200, 196, 186), width=1)
    vf = SANS_B(27) if len(val) <= 7 else SANS_B(23)
    d.text((x0, y0), val, font=vf, fill=INK)
    d.text((x0, y0 + 30), lab, font=SANS_B(10), fill=GREY)
d.line([(MX, grid_y1), (W - MX, grid_y1)], fill=INK, width=2)

# ============ REGION BAR ============
regions = [("ASIA-PACIFIC", 7, NAVY), ("AMERICAS", 8, DARKRED), ("MIDDLE EAST", 6, (90, 60, 20)),
           ("EUROPE", 5, (40, 70, 110)), ("AFRICA", 3, (110, 90, 20)), ("WORLD", 2, (70, 70, 70))]
rx, ry = MX, 222
for name, n, col in regions:
    label = f"{name} {n}"
    w = text_w(d, label, SANS_B(12)) + 16
    d.rectangle([rx, ry, rx + w, ry + 20], fill=col)
    d.text((rx + 8, ry + 3), label, font=SANS_B(12), fill=(255, 255, 255))
    rx += w + 6

# ============ THE DAY IN UTC ============
d.text((MX, 248), "THE DAY IN UTC", font=SANS_B(11), fill=INK)
d.text((MX + 130, 248), "~00:00 Kospi dives    ~05:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles",
       font=SANS(11), fill=GREY)
d.text((W - MX - text_w(d, "~ APPROX", SANS(10)), 248), "~ APPROX", font=SANS(10), fill=GREY)
d.line([(MX, 266), (W - MX, 266)], fill=INK, width=1)

# ============ HERO SCENES ============
hero_y0, hero_y1 = 272, 500
hw = (W - 2 * MX - 2 * 12) / 3
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", "KOSPI 4,708.54  ·  -161 PTS  ·  SAMSUNG -3.1%  ·  HYNIX -2.5%"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED", "BRIDGETOWN SUMMIT, BARBADOS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", "ASIA POWER INDEX 2026  ·  LOWY INSTITUTE"),
]

for i, (head, body, src, chip, cap) in enumerate(heroes):
    x0 = MX + i * (hw + 12)
    x1 = x0 + hw
    # scene box
    sy0, sy1 = hero_y0, hero_y0 + 128
    if i == 0:  # Kospi skyline + falling chart
        d.rectangle([x0, sy0, x1, sy1], fill=NAVY)
        import random
        random.seed(145)
        bx = x0 + 6
        while bx < x1 - 14:
            bw, bh = random.randint(14, 26), random.randint(28, 58)
            d.rectangle([bx, sy1 - bh, bx + bw, sy1], fill=(30, 52, 96))
            for wy in range(int(sy1 - bh + 5), int(sy1 - 5), 9):
                for wx in range(int(bx + 3), int(bx + bw - 3), 7):
                    if random.random() < 0.55:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
            bx += bw + 4
        # chart line, starts right of the big number text
        pts = [(x0 + 118, sy0 + 78), (x0 + 160, sy0 + 62), (x0 + 200, sy0 + 70),
               (x0 + 240, sy0 + 48), (x0 + 280, sy0 + 58), (x1 - 8, sy0 + 92)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.text((x0 + 10, sy0 + 8), "-3.3%", font=SANS_B(40), fill=(255, 255, 255))
    elif i == 1:  # Guterres globe
        d.rectangle([x0, sy0, x1, sy1], fill=GREEN)
        cx, cy, r = x0 + hw - 62, sy0 + 64, 46
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 235, 200))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 140, 100), width=2)
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(90, 140, 100), width=1)
        d.line([(cx - r, cy), (cx + r, cy)], fill=(90, 140, 100), width=1)
        d.line([(cx - r * 0.8, cy - r * 0.55), (cx + r * 0.8, cy - r * 0.55)], fill=(90, 140, 100), width=1)
        d.line([(cx - r * 0.8, cy + r * 0.55), (cx + r * 0.8, cy + r * 0.55)], fill=(90, 140, 100), width=1)
        d.text((x0 + 10, sy0 + 10), "150", font=SANS_B(46), fill=(255, 215, 90))
        d.text((x0 + 10, sy0 + 62), "DELEGATES BACK A", font=SANS_B(15), fill=(255, 215, 90))
        d.text((x0 + 10, sy0 + 82), "RISK FRAMEWORK", font=SANS_B(15), fill=(255, 215, 90))
    else:  # Power Index bars
        d.rectangle([x0, sy0, x1, sy1], fill=(245, 242, 234))
        d.text((x0 + 10, sy0 + 6), "NARROWEST SINCE 2018", font=SANS_B(12), fill=INK)
        d.text((x1 - 62, sy0 + 6), "GAP 5.3", font=SANS_B(12), fill=RED)
        bars = [("78.9", "US", NAVY, 0.789), ("73.6", "CHINA", DARKRED, 0.736), ("40.5", "INDIA", GOLD, 0.405)]
        by = sy0 + 30
        for val, lab, col, frac in bars:
            d.text((x0 + 10, by), val, font=SANS_B(14), fill=INK)
            bar_end = x0 + 62 + (hw - 130) * frac
            d.rectangle([x0 + 62, by + 2, bar_end, by + 16], fill=col)
            labf = SANS_B(12)
            lx = bar_end - text_w(d, lab, labf) - 6
            d.text((lx, by + 2), lab, font=labf,
                   fill=(255, 255, 255) if col != GOLD else (40, 40, 40))
            by += 28
    # black caption strip at bottom of scene
    d.rectangle([x0, sy1 - 18, x1, sy1], fill=INK)
    capf = SANS_B(9)
    capw = text_w(d, cap, capf)
    if capw > hw - 8:
        cap = cap.replace("  ·  ", " · ")
        capw = text_w(d, cap, capf)
    d.text((x0 + 4, sy1 - 15), cap, font=capf, fill=(255, 255, 255))
    # headline below scene (clear gap from black strip)
    hy = sy1 + 8
    hl = wrap(d, head, SERIF_B(17), hw)
    for ln in hl[:2]:
        d.text((x0, hy), ln, font=SERIF_B(17), fill=INK)
        hy += 21
    bl = wrap(d, body, SANS(11), hw)
    for ln in bl[:2]:
        d.text((x0, hy), ln, font=SANS(11), fill=(40, 40, 40))
        hy += 14
    # source + chip on their own row
    sy_ = hero_y1 - 16
    d.text((x0, sy_), src, font=SANS(9), fill=GREY)
    cw = text_w(d, chip, SANS_B(9)) + 12
    d.rectangle([x1 - cw, sy_ - 2, x1, sy_ + 12], fill=NAVY)
    d.text((x1 - cw + 6, sy_), chip, font=SANS_B(9), fill=(255, 255, 255))

d.line([(MX, 508), (W - MX, 508)], fill=INK, width=2)

# ============ 10 CARDS ============
d.rectangle([0, 514, W, 536], fill=INK)
d.text((MX, 519), "MORE OF THE DAY  —  10 STORIES", font=SANS_B(13), fill=(255, 255, 255))
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83, closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
cw = (W - 2 * MX - 4 * 10) / 5
cy0, cy1 = 540, 668
for i, (num, reg, head, body, src, chip) in enumerate(cards):
    col, row = i % 5, i // 5
    x0 = MX + col * (cw + 10)
    y0 = cy0 + row * 64
    d.text((x0, y0), num, font=SANS_B(13), fill=RED)
    d.text((x0 + text_w(d, num, SANS_B(13)) + 5, y0 + 1), reg, font=SANS_B(9), fill=RED)
    hl = wrap(d, head, SANS_B(11), cw)
    hy = y0 + 15
    for ln in hl[:2]:
        d.text((x0, hy), ln, font=SANS_B(11), fill=INK)
        hy += 13
    d.text((x0, hy), body, font=SANS(10), fill=(60, 60, 60))
    sy_ = y0 + 52
    d.text((x0, sy_), src, font=SANS(9), fill=GREY)
    chipw = text_w(d, chip, SANS_B(9)) + 10
    d.rectangle([x0 + cw - chipw, sy_ - 2, x0 + cw, sy_ + 11],
                fill=NAVY if chip == "REPORTED" else RED)
    d.text((x0 + cw - chipw + 5, sy_), chip, font=SANS_B(9), fill=(255, 255, 255))

d.line([(MX, 668), (W - MX, 668)], fill=INK, width=2)

# ============ MAP + ALSO ============
d.rectangle([0, 674, W, 696], fill=INK)
d.text((MX, 679), "WHERE IT HAPPENED", font=SANS_B(13), fill=(255, 255, 255))
map_x0, map_y0 = MX, 702
map_w, map_h = 380, 150
# blobs: Americas (left), Eurasia+Africa (middle), Asia-Pacific (right)
d.polygon([(map_x0 + 10, map_y0 + 10), (map_x0 + 90, map_y0 + 6), (map_x0 + 110, map_y0 + 60),
           (map_x0 + 80, map_y0 + 130), (map_x0 + 30, map_y0 + 140), (map_x0 + 5, map_y0 + 70)],
          fill=MAPGREEN)
d.polygon([(map_x0 + 150, map_y0 + 8), (map_x0 + 300, map_y0 + 4), (map_x0 + 340, map_y0 + 55),
           (map_x0 + 300, map_y0 + 120), (map_x0 + 200, map_y0 + 140), (map_x0 + 150, map_y0 + 80)],
          fill=MAPGREEN)
d.polygon([(map_x0 + 320, map_y0 + 30), (map_x0 + 378, map_y0 + 25), (map_x0 + 375, map_y0 + 95),
           (map_x0 + 335, map_y0 + 110), (map_x0 + 318, map_y0 + 70)], fill=MAPGREEN)
pins = [(44, 62), (78, 128), (368, 62), (60, 30), (85, 95), (250, 100), (280, 60),
        (300, 42), (265, 70), (238, 58), (180, 110), (300, 95), (250, 118)]
for n, (px, py) in enumerate(pins, 1):
    px += map_x0
    py += map_y0
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    t = str(n)
    d.text((px - text_w(d, t, SANS_B(9)) / 2, py - 6), t, font=SANS_B(9), fill=(255, 255, 255))
legend = ["Pins 1-13:  1 Seoul   2 Bridgetown   3 Beijing   4 Washington   5 New York   6 Kyiv",
          "7 Paris   8 London   9 Warsaw   10 Manchester   11 Beirut   12 Gaza   13 Khartoum"]
ly = map_y0 + map_h + 4
for ln in legend:
    d.text((map_x0, ly), ln, font=SANS(9), fill=INK)
    ly += 12

also_x = MX + 400
d.text((also_x, 702), "ALSO ON MONDAY", font=SANS_B(12), fill=INK)
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over AI exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
ay = 719
for ln in also:
    d.text((also_x, ay), ln, font=SANS(10), fill=INK)
    ay += 9.2

# ============ DATE CHECK ============
dc_y0, dc_y1 = 884, 968
d.rectangle([MX, dc_y0, W - MX, dc_y1], outline=RED, width=2)
d.text((MX + 8, dc_y0 + 6), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  STORIES DATED 23 NOV ONLY",
       font=SANS_B(11), fill=RED)
d.text((MX + 8, dc_y0 + 26),
       "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
       font=SANS(11), fill=INK)
d.text((MX + 8, dc_y0 + 42),
       "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
       font=SANS(11), fill=INK)
d.text((MX + 8, dc_y0 + 62),
       "NOT YET —  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=SANS(11), fill=INK)

# ============ FOOTER ============
d.text((MX, 978), "Sources: Reuters  ·  AP  ·  Bloomberg  ·  AFP  ·  Yonhap  ·  BBC  ·  WSJ  ·  ESPN  ·  Lowy Institute (Asia Power Index 2026).",
       font=SANS(10), fill=GREY)
d.text((MX, 992), "CHIPS: REPORTED = confirmed by wires  ·  CLAIM = one side's claim, independently unconfirmed  ·  ONGOING = still developing.",
       font=SANS(10), fill=GREY)
d.text((MX, 1006), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=SANS(10), fill=GREY)

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
