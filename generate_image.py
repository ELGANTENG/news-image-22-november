#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Deterministic: fixed coordinates, fixed sizes, no timestamps, no
randomness, no network, no external images. Output: entry.png, 1024x1024.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (25, 25, 25)
PAPER = (248, 244, 234)
RED = (164, 31, 31)
BLUE = (31, 78, 121)
GREEN = (46, 125, 50)
GOLD = (201, 162, 39)
MUTED = (85, 85, 85)
LIGHT_BLUE = (47, 111, 178)
PURPLE = (110, 60, 140)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAGLINE = font("DejaVuSans.ttf", 17)
F_KICKER = font("DejaVuSans-Bold.ttf", 16)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_HERO_BODY = font("DejaVuSans.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 23)
F_BODY = font("DejaVuSans.ttf", 16)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_FOOT = font("DejaVuSans.ttf", 14)


def wrap(d, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def draw_lines(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
# Every icon fits inside cy-46 .. cy+44 (the panel icon band).

def icon_globe(d, cx, cy, r):
    """Hero scene: globe, sun, leaves, flags."""
    sx, sy, sr = cx + r + 38, cy - r - 6, 30
    for k in range(8):
        a = k * math.pi / 4
        x1 = sx + int((sr + 4) * math.cos(a))
        y1 = sy + int((sr + 4) * math.sin(a))
        x2 = sx + int((sr + 16) * math.cos(a))
        y2 = sy + int((sr + 16) * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=4)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 196, 66),
              outline=(200, 150, 20), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIGHT_BLUE,
              outline=INK, width=3)
    d.ellipse([cx - r + 18, cy - r + 26, cx - 8, cy - 6], fill=GREEN)
    d.ellipse([cx - 6, cy + 8, cx + r - 22, cy + r - 30], fill=GREEN)
    d.ellipse([cx + 6, cy - r + 14, cx + r - 34, cy - r + 52], fill=GREEN)
    for w in (30, 55, 80):
        d.ellipse([cx - w, cy - r, cx + w, cy + r], outline=(255, 255, 255),
                  width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    for lx in (cx - 70, cx - 20, cx + 30):
        d.ellipse([lx - 16, cy + r - 14, lx + 16, cy + r + 6], fill=GREEN)
    for fx, col in ((cx - 118, RED), (cx + 118, BLUE), (cx + 150, GREEN)):
        d.line([(fx, cy + r - 34), (fx, cy + r + 26)], fill=INK, width=2)
        d.polygon([(fx, cy + r - 34), (fx + 26, cy + r - 26),
                   (fx, cy + r - 18)], fill=col)


def icon_mountains(d, cx, cy):
    """Nepal: Himalayas and a red pennant flag."""
    d.polygon([(cx - 120, cy + 42), (cx - 45, cy - 46), (cx + 10, cy + 42)],
              fill=(120, 130, 145))
    d.polygon([(cx - 60, cy + 42), (cx + 15, cy - 46), (cx + 90, cy + 42)],
              fill=(90, 100, 118))
    d.polygon([(cx + 30, cy + 42), (cx + 78, cy - 18), (cx + 122, cy + 42)],
              fill=(120, 130, 145))
    d.polygon([(cx - 45, cy - 46), (cx - 58, cy - 26), (cx - 32, cy - 26)],
              fill=(255, 255, 255))
    d.polygon([(cx + 15, cy - 46), (cx - 2, cy - 24), (cx + 32, cy - 24)],
              fill=(255, 255, 255))
    d.polygon([(cx + 78, cy - 18), (cx + 68, cy - 6), (cx + 88, cy - 6)],
              fill=(255, 255, 255))
    px = cx + 132
    d.line([(px, cy - 46), (px, cy + 42)], fill=INK, width=3)
    d.polygon([(px, cy - 46), (px + 32, cy - 36), (px, cy - 26)], fill=RED)
    d.polygon([(px, cy - 24), (px + 28, cy - 15), (px, cy - 6)], fill=RED)


def icon_cricket(d, cx, cy):
    """Cricket: stumps, bat and ball."""
    for sx in (cx - 52, cx - 38, cx - 24):
        d.rectangle([sx, cy - 28, sx + 9, cy + 42], fill=(214, 178, 94),
                    outline=INK, width=1)
    d.rectangle([cx - 52, cy - 36, cx - 15, cy - 29], fill=(214, 178, 94),
                outline=INK, width=1)
    d.polygon([(cx + 18, cy - 40), (cx + 46, cy - 32), (cx + 8, cy + 42),
               (cx - 14, cy + 34)], fill=(176, 124, 72), outline=INK)
    d.rectangle([cx + 26, cy - 46, cx + 34, cy - 38], fill=(120, 84, 48),
                outline=INK, width=1)
    bx, by = cx + 96, cy - 30
    d.ellipse([bx - 15, by - 15, bx + 15, by + 15], fill=RED, outline=INK,
              width=2)
    d.arc([bx - 15, by - 15, bx + 15, by + 15], start=200, end=340,
          fill=(255, 255, 255), width=2)


def icon_ship(d, cx, cy):
    """Baltic ship: hull, containers, flames, smoke."""
    for sx, sy, sr in ((cx - 78, cy - 38, 11), (cx - 62, cy - 44, 13),
                       (cx - 46, cy - 38, 10)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150))
    fx, fy = cx - 30, cy - 30
    d.polygon([(fx - 24, fy + 22), (fx - 13, fy - 18), (fx - 2, fy + 6),
               (fx + 9, fy - 24), (fx + 20, fy + 2), (fx + 28, fy + 22)],
              fill=(230, 120, 20))
    d.polygon([(fx - 11, fy + 22), (fx - 4, fy - 4), (fx + 5, fy + 8),
               (fx + 12, fy - 10), (fx + 16, fy + 22)], fill=(240, 196, 66))
    for jx, col in ((cx - 96, (200, 60, 60)), (cx - 66, (60, 120, 200)),
                    (cx - 36, (60, 160, 90))):
        d.rectangle([jx, cy - 8, jx + 28, cy + 12], fill=col, outline=INK,
                    width=1)
    d.polygon([(cx - 118, cy + 12), (cx + 118, cy + 12), (cx + 92, cy + 42),
               (cx - 92, cy + 42)], fill=(40, 48, 60))
    d.rectangle([cx - 118, cy + 12, cx + 118, cy + 19], fill=(200, 60, 60))


def icon_ballot(d, cx, cy):
    """South Africa: skyline and ballot box."""
    for bx, bw, bh in ((cx - 122, 26, 34), (cx - 90, 20, 44),
                       (cx - 64, 30, 28), (cx + 34, 22, 40),
                       (cx + 62, 28, 30), (cx + 96, 22, 46)):
        d.rectangle([bx, cy + 42 - bh, bx + bw, cy + 42], fill=(150, 155, 165),
                    outline=INK, width=1)
    d.rectangle([cx - 34, cy - 20, cx + 34, cy + 42], fill=BLUE, outline=INK,
                width=2)
    d.rectangle([cx - 44, cy - 30, cx + 44, cy - 20], fill=(25, 60, 95),
                outline=INK, width=2)
    d.rectangle([cx - 14, cy - 30, cx + 14, cy - 25], fill=INK)
    d.polygon([(cx - 12, cy - 46), (cx + 12, cy - 46), (cx + 8, cy - 30),
               (cx - 16, cy - 30)], fill=(255, 255, 255), outline=INK)
    d.line([(cx - 8, cy - 40), (cx + 6, cy - 40)], fill=RED, width=3)
    d.line([(cx - 8, cy - 35), (cx + 4, cy - 35)], fill=INK, width=2)


def icon_eu(d, cx, cy):
    """Britain / EU: circle of stars with a gear."""
    d.ellipse([cx - 58, cy - 46, cx + 58, cy + 46], fill=(20, 50, 120),
              outline=INK, width=2)
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx = cx + int(36 * math.cos(a))
        sy = cy + int(36 * math.sin(a))
        star(d, sx, sy, 7, GOLD)
    gx, gy = cx + 62, cy + 26
    d.ellipse([gx - 15, gy - 15, gx + 15, gy + 15], fill=(120, 120, 120),
              outline=INK, width=2)
    d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=PAPER, outline=INK,
              width=2)
    for k in range(6):
        a = k * math.pi / 3
        x1 = gx + int(15 * math.cos(a))
        y1 = gy + int(15 * math.sin(a))
        x2 = gx + int(21 * math.cos(a))
        y2 = gy + int(21 * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=(120, 120, 120), width=6)


def icon_maths(d, cx, cy):
    """Riemann: a chip and the primes."""
    d.rectangle([cx - 42, cy - 40, cx + 42, cy + 28], fill=(30, 34, 44),
                outline=INK, width=2)
    for k in range(4):
        x = cx - 27 + k * 18
        d.line([(x, cy - 40), (x, cy - 46)], fill=INK, width=3)
        d.line([(x, cy + 28), (x, cy + 34)], fill=INK, width=3)
        y = cy - 22 + k * 18
        d.line([(cx - 42, y), (cx - 48, y)], fill=INK, width=3)
        d.line([(cx + 42, y), (cx + 48, y)], fill=INK, width=3)
    d.text((cx, cy - 10), "\u03b6", font=font("DejaVuSans-Bold.ttf", 30),
           fill=(255, 255, 255), anchor="mm")
    d.text((cx, cy + 14), "= 0?", font=font("DejaVuSans-Bold.ttf", 14),
           fill=(240, 196, 66), anchor="mm")
    d.text((cx, cy + 40), "2  3  5  7  11  13",
           font=font("DejaVuSans-Bold.ttf", 16), fill=INK, anchor="mm")


# ---------------------------------------------------------------- page
def main():
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26  # margin

    # masthead
    draw_centered(d, W // 2, 18, "THE WORLD TODAY", F_TITLE, INK)
    d.line([(M, 96), (W - M, 96)], fill=INK, width=3)
    d.line([(M, 101), (W - M, 101)], fill=INK, width=1)
    draw_centered(d, W // 2, 112, "SUNDAY 22 NOVEMBER 2026", F_DATE, RED)
    draw_centered(d, W // 2, 146,
                  "Seven stories from one day, around the world",
                  F_TAGLINE, MUTED)

    # ---------------- hero: COP31
    hx0, hy0, hx1, hy1 = M, 178, W - M, 452
    d.rectangle([hx0, hy0, hx1, hy1], outline=INK, width=3)
    d.rectangle([hx0 + 3, hy0 + 3, hx1 - 3, hy1 - 3], outline=INK, width=1)
    icon_globe(d, hx0 + 185, hy0 + 145, 92)
    tx = hx0 + 380
    ty = hy0 + 26
    d.text((tx, ty), "CLIMATE  \u2022  ANTALYA, TURKEY", font=F_KICKER,
           fill=RED)
    ty += 30
    head = wrap(d, "COP31 CLOSE TO A DEAL AT LAST", F_HERO_HEAD,
                hx1 - tx - 24)
    ty = draw_lines(d, tx, ty, head, F_HERO_HEAD, INK, 46)
    ty += 10
    body = wrap(
        d,
        "After two days of overtime, a new climate package goes to "
        "nearly 200 nations for approval on Sunday morning, ending a "
        "bitter fight over fossil fuels and finance.",
        F_HERO_BODY, hx1 - tx - 24)
    draw_lines(d, tx, ty, body, F_HERO_BODY, (50, 50, 50), 26)

    # ---------------- six panels
    panels = [
        ("ASIA  \u2022  DIPLOMACY", "NEPAL'S PM LANDS IN DELHI",
         "Balendra Shah begins his first foreign trip since taking "
         "office in March. Talks with Modi on Monday.",
         icon_mountains, RED),
        ("SPORT  \u2022  CRICKET", "PANT'S 128 PUTS INDIA PAST 600",
         "Rishabh Pant's century powers India to 629 for 6 at lunch on "
         "day four, a lead of 261.",
         icon_cricket, BLUE),
        ("EUROPE  \u2022  BALTIC SEA", "BALTIC SHIP FIRE BURNS ON",
         "The sanctioned Russian cargo ship Sparta II is still ablaze "
         "after a suspected drone strike.",
         icon_ship, RED),
        ("AFRICA  \u2022  POLITICS", "BIG-CITY DEALS STILL UNSIGNED",
         "Two weeks after the local elections, Johannesburg, Tshwane "
         "and Durban still have no deal.",
         icon_ballot, GREEN),
        ("BRITAIN  \u2022  EUROPE", "BLAIR: REJOIN EU ONLY ON TECH TERMS",
         "Tony Blair says Britain should rejoin the EU only if the bloc "
         "moves the right way on tech.",
         icon_eu, BLUE),
        ("SCIENCE  \u2022  MATHEMATICS", "AI 'SOLVES' MATHS' HARDEST PROBLEM",
         "Mathematicians verify an AI-assisted proof of the Riemann "
         "Hypothesis, unsolved since 1859.",
         icon_maths, PURPLE),
    ]

    gx0, gy0 = M, 464
    pw, ph, gap = 316, 250, 12
    for i, (kicker, head, body, icon, col) in enumerate(panels):
        col_i = i % 3
        row_i = i // 3
        x0 = gx0 + col_i * (pw + gap)
        y0 = gy0 + row_i * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
        d.text((x0 + 12, y0 + 10), kicker, font=F_TAG, fill=col)
        d.line([(x0 + 12, y0 + 32), (x1 - 12, y0 + 32)], fill=(180, 175, 160),
               width=1)
        icon(d, x0 + pw // 2, y0 + 82)
        hy = y0 + 136
        hl = wrap(d, head, F_HEAD, pw - 24)
        if len(hl) > 2:
            raise ValueError("headline wraps to %d lines: %r" % (len(hl), head))
        hy = draw_lines(d, x0 + 12, hy, hl, F_HEAD, INK, 26)
        bl = wrap(d, body, F_BODY, pw - 24)
        if len(bl) > 3:
            raise ValueError("body wraps to %d lines: %r" % (len(bl), body))
        draw_lines(d, x0 + 12, hy + 4, bl, F_BODY, (50, 50, 50), 19)

    # footer
    fy = 988
    d.line([(M, fy - 6), (W - M, fy - 6)], fill=INK, width=1)
    draw_centered(d, W // 2, fy + 2,
                  "Sources: Reuters  \u2022  BBC  \u2022  ESPNcricinfo  "
                  "\u2022  CNN  \u2022  AFP",
                  F_FOOT, MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
