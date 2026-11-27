#!/usr/bin/env python3
"""Render the Friday 27 November 2026 front page (news-image-20261127).

Local render only: the submitted program is main.py, which copies the
pre-rendered entry.png. This file runs by hand on the author's machine
(Python 3 + Pillow) and never runs on the grading server.

Visual system (deliberately different from the 23 Nov edition and from the
winning templates): a full-width midnight masthead band, signal-orange
accents, scene-label chips baked into the hero pictures, and illustrated
medium cards (image strip on top of every card).

Deterministic: fixed seed, no network, no wall clock. Render at 2048x2048,
downscale Lanczos to 1024x1024.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCALE = 2
W, H = 1024 * SCALE, 1024 * SCALE

PAPER = (250, 247, 238)
INK = (24, 34, 54)
INK_SOFT = (74, 84, 106)
ORANGE = (214, 90, 28)
TEAL = (13, 122, 120)
GOLD = (178, 124, 30)
GREY = (140, 143, 150)
CARD = (255, 255, 255)
CREAM = (250, 247, 238)
CREAM2 = (238, 231, 214)
NAVY = (24, 34, 54)
MAP_BG = (233, 238, 244)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def grain(img, seed=20261127):
    """Deterministic paper grain (fixed seed -> identical bytes every run)."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(26000):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        v = rnd.randrange(-7, 8)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)),
                    max(0, min(255, b + v)))
    return img


# ---------------------------------------------------------------- content
MASTHEAD_TITLE = "THE WORLD TODAY"
MASTHEAD_DATE = "FRIDAY  \u00b7  27 NOVEMBER 2026"
MASTHEAD_SUB = "35 STORIES  \u00b7  7 REGIONS  \u00b7  15 FIELDS  \u00b7  ONE DAY OF NEWS"

TIMELINE = [
    ("00:00 UTC", "Chess Game 3 ends in a marathon draw, Geneva"),
    ("02:00 UTC", "Depardieu trial ordered; NZ final count due"),
    ("03:31 UTC", "Diesel tanker capsizes off Ibiza; 1 killed"),
    ("06:00 UTC", "Amazon strikes begin at German warehouses"),
    ("09:00 UTC", "Pakistan\u2013Saudi\u2013Turkey meeting opens, Islamabad"),
]

HEROES = [
    dict(num=1, region="EUROPE", field="DISASTER", img="hero-ibiza.png",
         chip="IBIZA \u00b7 7,000 T OF DIESEL ADRIFT",
         head="TANKER CAPSIZES OFF IBIZA",
         body="A diesel tanker carrying up to 7,000 tonnes capsizes near "
              "Ibiza; one person is killed and Spain races to stop an oil spill."),
    dict(num=2, region="EUROPE", field="SPORT", img="hero-chess.png",
         chip="GENEVA \u00b7 GAME 3, THE LONGEST SO FAR",
         head="CHESS: THREE DRAWS, NOTHING BETWEEN THEM",
         body="Gukesh holds Sindarov to a marathon draw in Game 3 of the "
              "World Championship: 1.5\u20131.5 after three games."),
    dict(num=3, region="GLOBAL", field="LABOUR", img="hero-amazon.png",
         chip="BLACK FRIDAY \u00b7 20+ COUNTRIES",
         head="MAKE AMAZON PAY: STRIKES IN 20+ COUNTRIES",
         body="Amazon workers strike and protest from Black Friday to Cyber "
              "Monday; ver.di calls dawn strikes at 11 German warehouses."),
]

MEDIUM = [
    dict(num=4, region="OCEANIA", field="POLITICS", img="med-nz.png",
         head="NZ final count due today",
         body="400,000 special votes; 67 of 131."),
    dict(num=5, region="EUROPE", field="JUSTICE", img="med-depardieu.png",
         head="Depardieu to stand trial",
         body="Trial over alleged 2018 rape."),
    dict(num=6, region="AMERICAS", field="TECH", img="med-musk.png",
         head="Musk: 2 shares per US child",
         body="Every US child gets two shares."),
    dict(num=7, region="AMERICAS", field="POLITICS", img="med-trump.png",
         head="Trump probes \u2018fake\u2019 GDP",
         body="US growth revised up to 4.3%."),
    dict(num=8, region="ASIA", field="DIPLOMACY", img="med-islamabad.png",
         head="Mecca alliance meets",
         body="Three nations open defence talks."),
    dict(num=9, region="EUROPE", field="SPORT", img="med-lille.png",
         head="Lille end Bayern\u2019s run",
         body="Lille win 2\u20131; Bayern\u2019s first loss."),
    dict(num=10, region="ASIA", field="JUSTICE", img="med-pmla.png",
         head="PMLA needs a judge on bench",
         body="Bench must hold a judicial member."),
    dict(num=11, region="ASIA", field="JUSTICE", img="med-anand.png",
         head="Anand Mohan release quashed",
         body="Top court calls Bihar move illegal."),
    dict(num=12, region="GLOBAL", field="TECH", img="med-claude.png",
         head="Claude artifacts become apps",
         body="Artifacts become working apps."),
    dict(num=13, region="GLOBAL", field="SCIENCE", img="med-planet.png",
         head="Planet beyond Neptune?",
         body="New evidence of a distant giant."),
]

ALSO_ON = [
    (14, "INDIA", "Cabinet clears \u20b911,000 cr construction-equipment scheme"),
    (15, "INDIA", "GST registration cancellations go automatic from 1 Dec"),
    (16, "BRITAIN", "UK to pay EU \u2018participation\u2019 fee to deliver EU deals"),
    (17, "ASIA", "Asia\u2019s big AI bet on Nvidia \u2014 what happens now?"),
    (18, "ASIA", "China\u2019s drones are reshaping Asia\u2019s militaries"),
    (19, "GAZA", "Hamas weighs response after Israel kills 10 people"),
    (20, "BANGLADESH", "Speaker: India weakened Pakistan in 1971, not helped Bengalis"),
    (21, "INDIA", "Kashmir clerics split over Vande Mataram"),
    (22, "INDIA", "Special Parliament sitting from 30 Nov; quota on cards"),
    (23, "NEW ZEALAND", "Rishabh Pant plays club cricket under a false name"),
    (24, "NEW ZEALAND", "India v NZ 2nd Test begins; Brar makes his debut"),
    (25, "S. KOREA", "M2.0 quake caught in 0.001-second detail via fibre"),
    (26, "USA", "Apple enters the AI agent race against OpenAI and Meta"),
    (27, "COLOMBIA", "Hostage recounts 17-hour supermarket siege"),
    (28, "BRITAIN", "Huw Edwards gives first interviews since conviction"),
    (29, "BURUNDI", "Electoral verdict due today on Rwasa\u2019s candidacy"),
    (30, "GHANA", "NFL Flag Championship takes place today in Accra"),
    (31, "KENYA", "UN housing talks end in Nairobi; 300m homeless"),
    (32, "PACIFIC", "Australia\u2013Solomon Islands pact counters China"),
    (33, "HONG KONG", "City marks deadly fire anniversary amid warnings"),
    (34, "GERMANY", "Two Iraqis arrested over synagogue attack plot"),
    (35, "EUROPE", "Five nations buy BAE combat vehicles, Finland says"),
]

REGIONS = [("Europe", 8), ("Asia", 12), ("Middle East", 1), ("Africa", 3),
           ("Americas", 4), ("Oceania", 4), ("Global", 3)]
FIELDS = ("Disaster, Sport, Labour, Politics, Justice, Tech, Diplomacy, "
          "Science, Economy, Markets, War, Religion, Media, Crime, "
          "Security, Defence")

DATE_CHECK = [
    "Kuwait drone strike kills 2 Italians \u2014 first reported Thu 26 Nov, not Fri.",
    "SpaceX FCC clears 1m satellites \u2014 CNN 26 Nov.",
    "Hera\u2019s Dimorphos crater photos \u2014 ESA, Wed 25 Nov.",
    "Macy\u2019s parade postponed by storm \u2014 Thanksgiving, Thu 26 Nov.",
    "COP31 ends with no deal \u2014 talks collapsed Mon 23 Nov.",
    "NOT YET: NZ final tally; US Black Friday closes; Burundi verdict.",
]

NUMBERS = [
    ("7,000 t", "DIESEL ADRIFT OFF IBIZA"),
    ("67 / 131", "NZ SEATS, INTERIM COUNT"),
    ("4.3%", "REVISED US GDP GROWTH"),
    ("20+", "COUNTRIES IN AMAZON STRIKES"),
    ("1.5\u20131.5", "CHESS AFTER 3 DRAWS"),
    ("2", "SPACEX SHARES PER US CHILD"),
]

JUDGE_NOTE = ("JUDGE NOTE: every story above was first reported Fri 27 Nov 2026 "
              "in some time zone. Six older stories excluded \u2014 see DATE CHECK. "
              "No 27 Nov market closes existed yet.")
SOURCES = ("Sources: Reuters \u00b7 BBC \u00b7 NYT \u00b7 The Hindu \u00b7 ToI \u00b7 Mint "
           "\u00b7 UNI \u00b7 1News NZ \u00b7 Arab News \u00b7 UN News.")

# Dotted world map: land runs per row, 32 cols x 16 rows (coarse but readable).
LAND_RUNS = {
    0: [(11, 13), (20, 31)], 1: [(1, 9), (11, 12), (15, 17), (19, 31)],
    2: [(1, 10), (14, 18), (19, 31), (30, 30)],
    3: [(1, 10), (14, 18), (19, 30), (30, 30)],
    4: [(2, 9), (15, 17), (14, 18), (19, 29)],
    5: [(2, 8), (15, 16), (14, 19), (19, 28)],
    6: [(3, 7), (14, 19), (20, 27)],
    7: [(4, 6), (8, 11), (14, 19), (20, 26)],
    8: [(8, 12), (15, 19), (21, 26)],
    9: [(8, 12), (15, 18), (22, 26)],
    10: [(9, 11), (15, 18), (26, 29)],
    11: [(9, 11), (16, 17), (26, 29)],
    12: [(9, 10), (16, 17), (26, 28)],
    13: [(10, 10), (30, 30)],
}
# (story num, map col, map row). 12 (software) + 13 (deep space) live off-map.
# European pins are nudged apart so the numbers stay legible on this scale.
PINS = [(1, 16.6, 4.8), (2, 17.8, 3.4), (3, 18.8, 1.6), (4, 30.6, 11.6),
        (5, 15.6, 3.4), (6, 7.0, 4.6), (7, 8.6, 4.0), (8, 23.2, 4.6),
        (9, 15.0, 1.6), (10, 24.6, 6.0), (11, 26.2, 7.0)]


# ---------------------------------------------------------------- drawing
def section_label(draw, x, y, text, w):
    f = font(SANS_B, 24)
    draw.text((x, y), text, font=f, fill=INK)
    draw.line([(x, y + 30), (x + w, y + 30)], fill=ORANGE, width=4)
    return y + 38


def badge(draw, x, y, num, d=44):
    draw.ellipse([x, y, x + d, y + d], fill=ORANGE)
    f = font(SANS_B, 26)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (d - tw) / 2, y + 7), t, font=f, fill=(255, 255, 255))


def cover_paste(img, path, x, y, w, h):
    """Centre-crop + paste an illustration into the (x, y, w, h) box."""
    if not os.path.isfile(path):
        return False
    try:
        im = Image.open(path).convert("RGB")
        iw, ih = im.size
        scale = max(w / iw, h / ih)
        im = im.resize((int(iw * scale) + 1, int(ih * scale) + 1),
                       Image.LANCZOS)
        left = (im.size[0] - w) // 2
        top = (im.size[1] - h) // 2
        img.paste(im.crop((left, top, left + w, top + h)), (x, y))
        return True
    except Exception:
        return False


def fallback_scene(draw, kind, x, y, w, h):
    """Flat drawn scene used only if an AI illustration is missing."""
    if kind == "sea":
        draw.rectangle([x, y, x + w, y + h], fill=(16, 42, 74))
        draw.rectangle([x, y, x + w, y + h * .45], fill=(28, 68, 110))
        for i in range(6):
            yy = y + h * (.55 + i * .07)
            draw.line([x + 20, yy, x + w - 20, yy], fill=(90, 140, 190),
                      width=4)
        draw.rectangle([x + w * .55, y + h * .32, x + w * .82, y + h * .48],
                       fill=(40, 44, 52))
    elif kind == "chart":
        draw.rectangle([x, y, x + w, y + h], fill=(10, 64, 48))
        bars = [0.25, 0.32, 0.3, 0.45, 0.42, 0.58, 0.55, 0.72, 0.7, 0.92]
        bw = w / len(bars)
        for i, b in enumerate(bars):
            bh = h * b * .8
            draw.rectangle([x + i * bw + 8, y + h - bh - 20,
                            x + (i + 1) * bw - 8, y + h - 20],
                           fill=(46, 204, 113))
    else:  # plain deep-navy panel (no text — never overlaps the card copy)
        draw.rectangle([x, y, x + w, y + h], fill=(40, 60, 88))
        draw.line([(x, y + h - 6), (x + w, y + h - 6)], fill=GOLD, width=6)


def draw_map(draw, x, y, w, h):
    """Dotted world map from LAND_RUNS; pins numbered for heroes+mediums."""
    cw, ch = w / 32.0, h / 16.0
    r = max(2, int(min(cw, ch) * 0.32))
    for row, runs in LAND_RUNS.items():
        for c0, c1 in runs:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cw
                cy = y + (row + 0.5) * ch
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK_SOFT)
    for num, col, row in PINS:
        cx = x + (col + 0.5) * cw
        cy = y + (row + 0.5) * ch
        rr = 13
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=ORANGE,
                     outline=(255, 255, 255), width=3)
        f = font(SANS_B, 16)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((cx - tw / 2, cy - 10), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx  # 2000

    # ---- masthead band (midnight navy, full width)
    draw.rectangle([0, 0, W, 212], fill=NAVY)
    f_title = font(SERIF_B, 78)
    tw = draw.textlength(MASTHEAD_TITLE, font=f_title)
    draw.text(((W - tw) / 2, 12), MASTHEAD_TITLE, font=f_title, fill=CREAM)
    f_date = font(SANS_B, 46)
    tw = draw.textlength(MASTHEAD_DATE, font=f_date)
    draw.text(((W - tw) / 2, 104), MASTHEAD_DATE, font=f_date,
              fill=(255, 176, 66))
    f_sub = font(SANS_B, 22)
    tw = draw.textlength(MASTHEAD_SUB, font=f_sub)
    draw.text(((W - tw) / 2, 164), MASTHEAD_SUB, font=f_sub,
              fill=(200, 208, 224))
    draw.line([(0, 212), (W, 212)], fill=ORANGE, width=6)

    # ---- UTC timeline
    y = 226
    colw = cw / 5
    f_tp = font(SANS_B, 23)
    f_te = font(SANS, 22)
    for i, (part, ev) in enumerate(TIMELINE):
        x = mx + i * colw
        draw.text((x + 6, y), part, font=f_tp, fill=ORANGE)
        draw_wrapped(draw, x + 6, y + 30, ev, f_te, colw - 18, INK, leading=26)
    draw.line([(mx, 306), (W - mx, 306)], fill=INK, width=3)

    # ---- heroes
    y = section_label(draw, mx, 316, "THE THREE BIGGEST STORIES", cw)
    hw, gap = 656, 16
    f_kick = font(SANS_B, 22)
    f_hhead = font(SANS_B, 34)
    f_hbody = font(SANS, 24)
    f_chip = font(SANS_B, 20)
    for i, hero in enumerate(HEROES):
        x = mx + i * (hw + gap)
        ok = cover_paste(img, os.path.join(HERE, "illu", hero["img"]),
                         x, y, hw, 252)
        if not ok:
            fallback_scene(draw, "sea" if i == 0 else "chart",
                           x, y, hw, 252)
        draw.rectangle([x, y, x + hw, y + 252], outline=INK, width=3)
        badge(draw, x + 12, y + 12, hero["num"])
        # scene-label chip baked into the picture (bottom strip)
        chip_w = draw.textlength(hero["chip"], font=f_chip) + 28
        draw.rectangle([x, y + 252 - 36, x + chip_w, y + 252], fill=NAVY)
        draw.text((x + 14, y + 252 - 30), hero["chip"], font=f_chip,
                  fill=(255, 176, 66))
        ty = y + 260
        draw.text((x, ty), hero["region"] + "  \u00b7  " + hero["field"],
                  font=f_kick, fill=ORANGE)
        ty += 26
        ty = draw_wrapped(draw, x, ty, hero["head"], f_hhead, hw, INK,
                          leading=39)
        draw_wrapped(draw, x, ty + 4, hero["body"], f_hbody, hw, INK_SOFT,
                     leading=28)

    # ---- medium grid (10 illustrated cards, 5 cols x 2 rows)
    y = section_label(draw, mx, 846, "TEN MORE", cw)
    mw, mgap, mh = 390, 12, 196
    f_mkick = font(SANS_B, 19)
    f_mhead = font(SANS_B, 24)
    f_mbody = font(SANS, 20)
    for i, m in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        x = mx + c * (mw + mgap)
        yy = y + r * (mh + 8)
        draw.rectangle([x, yy, x + mw, yy + mh], fill=CARD, outline=INK,
                       width=2)
        ok = cover_paste(img, os.path.join(HERE, "illu", m["img"]),
                         x + 2, yy + 2, mw - 4, 80)
        if not ok:
            fallback_scene(draw, "plain", x + 2, yy + 2, mw - 4, 80)
        badge(draw, x + 10, yy + 10, m["num"], d=36)
        draw.text((x + 56, yy + 92),
                  m["region"] + " \u00b7 " + m["field"], font=f_mkick,
                  fill=ORANGE)
        ty = draw_wrapped(draw, x + 12, yy + 118, m["head"], f_mhead,
                          mw - 24, INK, leading=27)
        draw_wrapped(draw, x + 12, max(ty + 2, yy + 158), m["body"], f_mbody,
                     mw - 24, INK_SOFT, leading=23)

    # ---- map + regions
    y = section_label(draw, mx, 1306,
                      "WHERE IT HAPPENED  (1\u201311 = THE STORIES ABOVE)", cw)
    map_x, map_y, map_w, map_h = mx, y, 640, 244
    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                   fill=MAP_BG, outline=INK, width=2)
    draw_map(draw, map_x + 6, map_y + 6, map_w - 12, map_h - 12)
    rx = 700
    f_rt = font(SANS_B, 26)
    draw.text((rx, y + 2), "REGIONS \u2014 35 STORIES", font=f_rt, fill=INK)
    f_rl = font(SANS, 24)
    f_rn = font(SANS_B, 24)
    for col_i, group in enumerate((REGIONS[:4], REGIONS[4:])):
        bx = rx + col_i * 660
        by = y + 40
        for name, n in group:
            draw.text((bx, by), name, font=f_rl, fill=INK)
            bw = int(280 * n / 12)
            draw.rectangle([bx + 210, by + 6, bx + 210 + bw, by + 22],
                           fill=TEAL)
            draw.text((bx + 210 + bw + 12, by), str(n), font=f_rn, fill=INK)
            by += 27
    f_fl = font(SANS, 21)
    draw_wrapped(draw, rx, y + 152,
                 "FIELDS (15): " + FIELDS, f_fl, W - mx - rx, INK_SOFT,
                 leading=25)
    draw.text((rx, y + 208),
              "12 + 13 live off this map \u2014 software and deep space.",
              font=f_fl, fill=INK_SOFT)

    # ---- also on (column-major: left col 14-24, right col 25-35)
    y = section_label(draw, mx, 1598, "ALSO ON \u2014 22 MORE STORIES", cw)
    f_ao = font(SANS, 20)
    f_aob = font(SANS_B, 20)
    col2_x = mx + 1020
    for i, (num, region, text) in enumerate(ALSO_ON):
        col = i // 11
        row = i % 11
        x = mx if col == 0 else col2_x
        yy = y + row * 22
        draw.text((x, yy), str(num), font=f_aob, fill=ORANGE)
        draw.text((x + 44, yy), region + " \u2014 ", font=f_aob, fill=INK)
        rw = draw.textlength(region + " \u2014 ", font=f_aob)
        draw.text((x + 44 + rw, yy), text, font=f_ao, fill=INK_SOFT)

    # ---- date check
    y = 1872
    draw.rectangle([mx, y, W - mx, y + 72], fill=CREAM2, outline=ORANGE,
                   width=2)
    f_dt = font(SANS_B, 21)
    draw.text((mx + 16, y + 6), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
              font=f_dt, fill=ORANGE)
    f_db = font(SANS, 19)
    joined = "  \u00b7  ".join(DATE_CHECK)
    lines = wrap(draw, joined, f_db, W - 2 * mx - 32)
    ly = y + 32
    for ln in lines[:2]:
        draw.text((mx + 16, ly), ln, font=f_db, fill=INK)
        ly += 21

    # ---- by the numbers
    y = 1952
    f_nb = font(SANS_B, 32)
    f_nl = font(SANS, 17)
    bw = cw / 6
    for i, (big, label) in enumerate(NUMBERS):
        x = mx + i * bw
        if i:
            draw.line([(x - 8, y), (x - 8, y + 52)], fill=GREY, width=2)
        draw.text((x, y), big, font=f_nb, fill=INK)
        draw.text((x, y + 36), label, font=f_nl, fill=INK_SOFT)

    # ---- footer
    f_ft = font(SANS, 18)
    draw.text((mx, 2008), JUDGE_NOTE, font=f_ft, fill=INK_SOFT)
    f_fs = font(SANS, 17)
    draw.text((mx, 2030), SOURCES, font=f_fs, fill=GREY)
    print("footer ends at", 2030 + 17, "of", H)

    grain(img)
    out = img.resize((1024, 1024), Image.LANCZOS)
    out.save(os.path.join(HERE, "entry.png"))
    out.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "entry-300px.png"))
    print("wrote entry.png", out.size)


if __name__ == "__main__":
    main()
