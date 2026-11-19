#!/usr/bin/env python3
"""Compose the 19 November 2026 front page: 1024x1024 PNG, PIL only."""
import math
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (20, 20, 20)
RED = (163, 22, 33)
NAVY = (27, 42, 74)
GREY = (90, 86, 78)
RULE = (60, 58, 52)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF = F + "DejaVuSerif.ttf"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SANS = F + "DejaVuSans.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_hero(base):
    """Night scene over the Gulf: sky, sea, warship, missile arcs.
    Drawn on a separate layer so nothing pokes past the hero frame."""
    x0, y0, x1, y1 = 36, 150, 988, 470
    hw, hh = x1 - x0, y1 - y0
    layer = Image.new("RGB", (hw, hh), (10, 22, 48))
    draw = ImageDraw.Draw(layer)
    ox, oy = -x0, -y0  # translate absolute coords into layer coords
    def L(x, y):
        return (x + ox, y + oy)
    # sky gradient
    top = (10, 22, 48)
    mid = (24, 52, 96)
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        if t < 0.62:
            s = t / 0.62
            c = tuple(int(top[i] + (mid[i] - top[i]) * s) for i in range(3))
        else:
            s = (t - 0.62) / 0.38
            c = tuple(int(mid[i] + ((58, 84, 120)[i] - mid[i]) * s) for i in range(3))
        draw.line([L(x0, y), L(x1, y)], fill=c)
    # stars
    rnd = random.Random(1911)
    for _ in range(90):
        sx = rnd.randint(x0 + 4, x1 - 4)
        sy = rnd.randint(y0 + 4, y0 + 150)
        r = rnd.choice([1, 1, 2])
        draw.ellipse([sx + ox - r, sy + oy - r, sx + ox + r, sy + oy + r], fill=(235, 235, 220))
    # crescent moon
    draw.ellipse([880 + ox, 168 + oy, 940 + ox, 228 + oy], fill=(240, 232, 200))
    draw.ellipse([896 + ox, 162 + oy, 952 + ox, 226 + oy], fill=(24, 52, 96))
    # distant explosion glows on the horizon
    for gx, gr in [(300, 46), (700, 34)]:
        for k in range(gr, 0, -6):
            draw.ellipse([gx + ox - k, 330 + oy - k // 2, gx + ox + k, 330 + oy + k // 3],
                         outline=(255, 140, 55))
    # sea
    draw.rectangle([L(x0, 330), L(x1, y1)], fill=(14, 42, 74))
    for yy in range(336, y1, 14):
        draw.line([L(x0 + 8, yy), L(x1 - 8, yy)], fill=(38, 78, 122), width=2)
    # moon reflection
    for i, yy in enumerate(range(340, y1 - 8, 16)):
        wdt = 26 - i
        draw.line([L(910 - wdt, yy), L(910 + wdt, yy)], fill=(220, 205, 150), width=3)
    # warship silhouette (left)
    draw.polygon([L(*p) for p in [(90, 400), (90, 360), (150, 360), (170, 400), (330, 400),
                  (300, 420), (110, 420)]], fill=(8, 14, 26))
    draw.rectangle([L(150, 330), L(190, 360)], fill=(8, 14, 26))
    draw.line([L(170, 330), L(170, 306)], fill=(8, 14, 26), width=4)
    draw.polygon([L(*p) for p in [(170, 306), (196, 322), (170, 322)]], fill=(8, 14, 26))
    # radar tower (right)
    draw.line([L(850, 400), L(850, 316)], fill=(8, 14, 26), width=5)
    draw.ellipse([L(838, 300), L(866, 328)], fill=(8, 14, 26))
    draw.line([L(850, 314), L(830, 296)], fill=(8, 14, 26), width=3)
    draw.line([L(850, 314), L(872, 292)], fill=(8, 14, 26), width=3)
    # missile arcs with glowing heads
    def arc(cx, cy, rx, ry, a0, a1, col):
        pts = []
        for deg in range(a0, a1 + 1, 4):
            r = math.radians(deg)
            pts.append(L(cx + rx * math.cos(r), cy - ry * math.sin(r)))
        draw.line(pts, fill=col, width=4)
        hx, hy = pts[-1]
        draw.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], fill=(255, 200, 90))
        draw.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(255, 255, 220))
    arc(430, 420, 190, 130, 200, 330, (255, 170, 80))
    arc(620, 420, 150, 105, 210, 340, (255, 190, 110))
    base.paste(layer, (x0, y0))
    d = ImageDraw.Draw(base)
    d.rectangle([x0, y0, x1, y1], outline=(20, 20, 20), width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    # ---- masthead ----
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 26), title, font=f_mast, fill=INK)
    d.line([(mx, 104), (W - mx, 104)], fill=RULE, width=2)
    f_date = font(SANS_B, 21)
    left = "THURSDAY, 19 NOVEMBER 2026"
    right = "WORLD NEWS IN ONE IMAGE"
    d.text((mx, 112), left, font=f_date, fill=INK)
    rw = d.textlength(right, font=f_date)
    d.text((W - mx - rw, 112), right, font=f_date, fill=INK)
    d.line([(mx, 142), (W - mx, 142)], fill=INK, width=4)
    # ---- hero illustration ----
    draw_hero(img)
    # ---- headline band ----
    d.rectangle([mx, 478, W - mx, 606], fill=RED)
    f_head = font(SERIF_B, 50)
    d.text((mx + 18, 486), "GULF WAR WIDENS", font=f_head, fill=(255, 255, 255))
    f_sub = font(SANS, 19)
    sub = ("Iran strikes a U.S. air base in Kuwait and hits Bahrain again — "
           "a day after U.S. jets hit a missile site on Qeshm Island.")
    for i, ln in enumerate(wrap(d, sub, f_sub, W - 2 * mx - 36)):
        d.text((mx + 18, 546 + i * 26), ln, font=f_sub, fill=(255, 240, 235))
    # ---- lead paragraph ----
    f_lead = font(SERIF, 20)
    lead = ("Gulf states said they intercepted missiles and drones from Iran and "
            "its allies on Wednesday. It was the first Iranian attack on Kuwait "
            "since September, and Bahrain faced its third round of attacks this "
            "week in the nine-month-old war.")
    for i, ln in enumerate(wrap(d, lead, f_lead, W - 2 * mx)):
        d.text((mx, 620 + i * 27), ln, font=f_lead, fill=INK)
    # ---- 2x2 story panels ----
    panels = [
        ("2", "SHENZHEN", "Three leaders, one table",
         "Trump, Xi and Putin meet today in Shenzhen — the first-ever "
         "trilateral. Nuclear arms are on the agenda; no deal is expected."),
        ("3", "VICE CITY", "GTA VI is here",
         "After a 13-year wait, Grand Theft Auto VI rolls out worldwide "
         "today. Nearly 1 in 5 U.S. workers plan time off to play."),
        ("4", "BRUSSELS", "€45bn lifeline for Kyiv",
         "The EU proposes a €45bn loan for Ukraine, to be repaid once "
         "Russia pays reparations for the war."),
        ("5", "DEEP SPACE", "Voyager 1, a light-day away",
         "After almost 50 years in space, NASA's Voyager 1 is believed to "
         "have reached one light-day from Earth. NASA confirms today."),
    ]
    pw, ph = 466, 138
    px0, py0 = mx, 706
    gap = 20
    for idx, (num, kick, head, body) in enumerate(panels):
        x = px0 + (idx % 2) * (pw + gap)
        y = py0 + (idx // 2) * (ph + 14)
        d.rectangle([x, y, x + pw, y + ph], outline=RULE, width=2)
        d.rectangle([x, y, x + pw, y + 30], fill=NAVY)
        d.text((x + 12, y + 4), num + "  " + kick, font=font(SANS_B, 17), fill=(255, 255, 255))
        d.text((x + 12, y + 38), head, font=font(SERIF_B, 23), fill=INK)
        f_body = font(SANS, 15)
        for i, ln in enumerate(wrap(d, body, f_body, pw - 24)):
            d.text((x + 12, y + 70 + i * 20), ln, font=f_body, fill=(40, 40, 40))
    # ---- footer ----
    d.line([(mx, 1000), (W - mx, 1000)], fill=RULE, width=2)
    f_foot = font(SANS_B, 14)
    foot = "THURSDAY, 19 NOVEMBER 2026  ·  FIVE STORIES, ONE DAY  ·  THE WORLD IN ONE DAY"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 1006), foot, font=f_foot, fill=GREY)
    out = "/home/hatch/workspace/makefun/news-image-20261119/entry.png"
    img.save(out, "PNG", optimize=True)
    print("saved", out)


if __name__ == "__main__":
    main()
