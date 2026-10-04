"""休閒遊戲類作品畫面（平台跳躍、消除、射擊）。"""
import math
import random

from .common import *  # noqa: F401,F403


def cloud(cx, cy, s=1.0):
    return (f'<g fill="#fff" opacity="0.92"><ellipse cx="{cx}" cy="{cy}" rx="{40*s}" ry="{16*s}"/>'
            f'<circle cx="{cx-14*s}" cy="{cy-10*s}" r="{16*s}"/><circle cx="{cx+12*s}" cy="{cy-14*s}" r="{20*s}"/></g>')


def coin(cx, cy):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="11" fill="#ffd23f" stroke="#e09b00" stroke-width="2.5"/>'
            f'<rect x="{cx-2}" y="{cy-6}" width="4" height="12" rx="2" fill="#e09b00"/>')


def brick_platform(x, y, n):
    out = [r(x, y, n * 32, 26, "#d9733b", 3, 'stroke="#7c3a14" stroke-width="2"')]
    for i in range(1, n):
        out.append(f'<line x1="{x+i*32}" y1="{y}" x2="{x+i*32}" y2="{y+26}" stroke="#7c3a14" stroke-width="2"/>')
    out.append(f'<line x1="{x}" y1="{y+13}" x2="{x+n*32}" y2="{y+13}" stroke="#7c3a14" stroke-width="1.5"/>')
    return "".join(out)


def scene_platformer() -> str:
    defs = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4cb8ff"/>'
            '<stop offset="1" stop-color="#d4f3ff"/></linearGradient>')
    b = [r(0, 0, 800, 500, "url(#sky)"), '<circle cx="690" cy="86" r="38" fill="#fff3a6"/><circle cx="690" cy="86" r="52" fill="#fff3a6" opacity="0.35"/>',
         cloud(140, 110), cloud(420, 80, 1.2), cloud(600, 170, 0.8),
         '<path d="M0 420 Q120 300 240 420 Z" fill="#7fd39b"/><path d="M180 420 Q340 260 500 420 Z" fill="#69c48a"/><path d="M460 420 Q620 320 800 420 Z" fill="#7fd39b"/>',
         r(0, 420, 800, 80, "#c47a3a"), r(0, 412, 800, 16, "#5cc84a")]
    for x in range(0, 800, 40):
        b.append(f'<line x1="{x}" y1="428" x2="{x}" y2="500" stroke="#a5612a" stroke-width="2"/>')
    b.append('<line x1="0" y1="464" x2="800" y2="464" stroke="#a5612a" stroke-width="2"/>')
    b += [brick_platform(380, 300, 5), brick_platform(560, 220, 3), brick_platform(120, 260, 3)]
    b += [r(412, 180, 34, 34, "#f5b000", 4, 'stroke="#8a5600" stroke-width="2.5"'), t(429, 205, "?", 22, "#fff", 900, "middle")]
    for cx, cy in ((412, 270), (444, 262), (476, 270), (582, 190), (614, 182), (646, 190), (152, 230), (184, 222)):
        b.append(coin(cx, cy))
    # 主角（跳躍中）
    hx, hy = 290, 300
    b += [f'<g transform="translate({hx} {hy})">', r(-14, -40, 30, 10, "#e53935", 3), r(-12, -32, 24, 20, "#ffcc99", 4),
          '<circle cx="5" cy="-24" r="2.5" fill="#222"/>', r(-14, -12, 28, 24, "#e53935", 4), r(-14, -4, 28, 10, "#1e40af", 2),
          r(-16, 12, 12, 12, "#1e40af", 3), r(4, 8, 12, 12, "#1e40af", 3), r(14, -14, 10, 8, "#ffcc99", 3), '</g>',
          '<path d="M250 320 q-20 10 -40 4" stroke="#fff" stroke-width="3" fill="none" opacity="0.7"/>']
    # 敵人史萊姆
    for ex in (520, 680):
        b += [f'<path d="M{ex-22} 414 q0 -36 22 -36 q22 0 22 36 z" fill="#7b2ff7"/>',
              f'<circle cx="{ex-7}" cy="398" r="5" fill="#fff"/><circle cx="{ex+7}" cy="398" r="5" fill="#fff"/>',
              f'<circle cx="{ex-6}" cy="399" r="2.5" fill="#111"/><circle cx="{ex+8}" cy="399" r="2.5" fill="#111"/>']
    b += ['<rect x="752" y="170" width="6" height="244" fill="#e5e7eb"/><circle cx="755" cy="166" r="7" fill="#ffd23f"/>',
          '<path d="M752 178 l-46 18 l46 18 z" fill="#22c55e"/>', r(738, 404, 34, 12, "#6b7280", 2)]
    hud = 'stroke="#1b1b3a" stroke-width="5" paint-order="stroke" letter-spacing="1"'
    b += [t(24, 40, "SCORE", 14, "#fff", 900, mono=True, extra=hud), t(24, 64, "012450", 20, "#fff", 900, mono=True, extra=hud),
          coin(214, 50), t(232, 58, "× 23", 20, "#fff", 900, mono=True, extra=hud),
          t(400, 40, "WORLD", 14, "#fff", 900, "middle", True, hud), t(400, 64, "1-3", 20, "#fff", 900, "middle", True, hud),
          t(560, 40, "TIME", 14, "#fff", 900, mono=True, extra=hud), t(560, 64, "287", 20, "#fff", 900, mono=True, extra=hud)]
    for i in range(3):
        x = 660 + i * 34
        b.append(f'<path d="M{x} 44 c-8 -12 -24 -2 -12 10 l12 12 l12 -12 c12 -12 -4 -22 -12 -10z" fill="#ef4444" stroke="#1b1b3a" stroke-width="2.5"/>')
    return svg("".join(b), defs)


# ---------- 11. 消除益智遊戲 ----------
def gem(kind, cx, cy, rr=15):
    if kind == 0:
        return f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/><circle cx="{cx-5}" cy="{cy-5}" r="4" fill="#fff" opacity="0.6"/>'
    if kind == 1:
        return f'<path d="M{cx} {cy-rr-2} L{cx+rr} {cy} L{cx} {cy+rr+2} L{cx-rr} {cy} Z" fill="#3b82f6" stroke="#1e3a8a" stroke-width="2"/><path d="M{cx} {cy-rr+4} L{cx+7} {cy} L{cx} {cy-2} Z" fill="#fff" opacity="0.55"/>'
    if kind == 2:
        return r(cx - rr + 1, cy - rr + 1, 2 * rr - 2, 2 * rr - 2, "#22c55e", 7, 'stroke="#14532d" stroke-width="2"') + r(cx - 8, cy - 9, 7, 7, "#fff", 2, 'opacity="0.55"')
    if kind == 3:
        pts = []
        for i in range(10):
            a = math.radians(-90 + i * 36)
            rad = rr + 2 if i % 2 == 0 else (rr + 2) * 0.48
            pts.append(f"{cx + rad*math.cos(a):.1f},{cy + rad*math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="#facc15" stroke="#854d0e" stroke-width="2"/>'
    pts = " ".join(f"{cx + rr*math.cos(math.radians(60*i)):.1f},{cy + rr*math.sin(math.radians(60*i)):.1f}" for i in range(6))
    return f'<polygon points="{pts}" fill="#c084fc" stroke="#581c87" stroke-width="2"/><circle cx="{cx-4}" cy="{cy-4}" r="3.5" fill="#fff" opacity="0.55"/>'


def scene_match3() -> str:
    defs = ('<linearGradient id="mbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e1052"/>'
            '<stop offset="1" stop-color="#7b2ff7"/></linearGradient>'
            '<radialGradient id="glow"><stop offset="0" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    b = [r(0, 0, 800, 500, "url(#mbg)")]
    rnd = random.Random(21)
    for _ in range(40):
        b.append(f'<circle cx="{rnd.randint(0,800)}" cy="{rnd.randint(0,500)}" r="{rnd.uniform(0.8,2.2):.1f}" fill="#fff" opacity="{rnd.uniform(0.2,0.7):.2f}"/>')
    bx, by, cell, n = 254, 96, 42, 7
    board = r(bx - 12, by - 12, cell * n + 24, cell * n + 24, "#2a1766", 18, 'stroke="#a78bfa" stroke-width="3"')
    b += [f'<g filter="url(#sh)">{board}</g>']
    for i in range(n):
        for j in range(n):
            b.append(r(bx + j * cell + 2, by + i * cell + 2, cell - 4, cell - 4, "#3b2386" if (i + j) % 2 else "#33207a", 8))
    match_row = 3
    b.append(r(bx + 2 * cell, by + match_row * cell, cell * 3, cell, "url(#glow)", 12))
    for i in range(n):
        for j in range(n):
            kind = 0 if (i == match_row and 2 <= j <= 4) else rnd.randint(0, 4)
            if i == match_row and j in (1, 5) and kind == 0:
                kind = 2
            b.append(gem(kind, bx + j * cell + cell // 2, by + i * cell + cell // 2))
    b += [t(bx + 3.5 * cell, by + match_row * cell - 8, "+300", 22, "#fde047", 900, "middle", extra='stroke="#7c2d12" stroke-width="4" paint-order="stroke"'),
          t(400, 60, "COMBO × 3！", 30, "#fde047", 900, "middle", extra='stroke="#7c2d12" stroke-width="6" paint-order="stroke"')]
    b += [r(24, 96, 196, 300, "#2a1766", 16, 'opacity="0.92" stroke="#6d28d9"'), t(122, 128, "第 12 關", 20, "#fff", 900, "middle"),
          t(122, 162, "分數", 12, "#c4b5fd", 400, "middle"), t(122, 192, "24,860", 26, "#fde047", 900, "middle"),
          r(44, 206, 156, 12, "#1e1052", 6), r(44, 206, 118, 12, "#fde047", 6), t(122, 238, "★ ★ ☆", 22, "#fde047", 900, "middle"),
          t(122, 280, "剩餘步數", 12, "#c4b5fd", 400, "middle"), t(122, 326, "18", 44, "#fff", 900, "middle"),
          t(122, 370, "再消除 4 次可過關", 11, "#c4b5fd", 400, "middle")]
    b += [r(580, 96, 196, 300, "#2a1766", 16, 'opacity="0.92" stroke="#6d28d9"'), t(678, 128, "收集目標", 16, "#fff", 900, "middle")]
    goals = [(0, "12 / 20", 0.6), (1, "15 / 15", 1.0), (3, "6 / 10", 0.6)]
    for i, (kind, txt, p) in enumerate(goals):
        y = 168 + i * 50
        b += [gem(kind, 614, y), t(640, y - 2, txt, 14, "#fff", 900), r(640, y + 6, 116, 8, "#1e1052", 4), r(640, y + 6, round(116 * p), 8, "#4ade80" if p >= 1 else "#a78bfa", 4)]
    b += [t(678, 330, "道具", 13, "#c4b5fd", 700, "middle")]
    for i, (lab, c) in enumerate((("炸彈", "#f97316"), ("彩虹", "#ec4899"), ("重洗", "#22d3ee"))):
        x = 612 + i * 66
        b += [f'<circle cx="{x}" cy="360" r="18" fill="{c}" stroke="#fff" stroke-width="2"/>', t(x, 365, lab, 10, "#fff", 900, "middle")]
    return svg("".join(b), defs)


# ---------- 12. 太空射擊遊戲 ----------
def enemy_ship(cx, cy, col):
    return (f'<path d="M{cx} {cy+16} L{cx+18} {cy-8} L{cx+8} {cy-4} L{cx} {cy-14} L{cx-8} {cy-4} L{cx-18} {cy-8} Z" fill="{col}" stroke="#fff" stroke-width="1" stroke-opacity="0.4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="#fde047"/>')


def scene_shooter() -> str:
    defs = ('<radialGradient id="neb1" cx="0.3" cy="0.3" r="0.5"><stop offset="0" stop-color="#7c3aed" stop-opacity="0.55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="neb2" cx="0.8" cy="0.7" r="0.45"><stop offset="0" stop-color="#0ea5e9" stop-opacity="0.4"/><stop offset="1" stop-color="#0ea5e9" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="boom"><stop offset="0" stop-color="#fff7ad"/><stop offset="0.45" stop-color="#fb923c"/><stop offset="1" stop-color="#dc2626" stop-opacity="0"/></radialGradient>')
    b = [r(0, 0, 800, 500, "#050816"), r(0, 0, 800, 500, "url(#neb1)"), r(0, 0, 800, 500, "url(#neb2)")]
    rnd = random.Random(42)
    for _ in range(120):
        b.append(f'<circle cx="{rnd.randint(0,800)}" cy="{rnd.randint(0,500)}" r="{rnd.uniform(0.5,1.8):.1f}" fill="#fff" opacity="{rnd.uniform(0.3,1):.2f}"/>')
    b += ['<circle cx="690" cy="400" r="70" fill="#1e3a8a"/><circle cx="672" cy="384" r="70" fill="#050816" opacity="0.35"/>',
          '<ellipse cx="690" cy="400" rx="110" ry="16" fill="none" stroke="#93c5fd" stroke-width="3" opacity="0.5" transform="rotate(-15 690 400)"/>']
    # Boss
    b += ['<path d="M400 160 L470 110 L520 120 L480 80 L430 92 L400 60 L370 92 L320 80 L280 120 L330 110 Z" fill="#9f1239" stroke="#fda4af" stroke-width="2"/>',
          '<circle cx="400" cy="112" r="16" fill="#fde047" stroke="#f97316" stroke-width="4"/>', '<circle cx="340" cy="104" r="6" fill="#fb7185"/><circle cx="460" cy="104" r="6" fill="#fb7185"/>']
    for x, y in ((350, 176), (400, 190), (450, 176), (380, 214), (420, 214)):
        b.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#f472b6"/><circle cx="{x}" cy="{y}" r="9" fill="#f472b6" opacity="0.3"/>')
    for i, (x, y) in enumerate(((150, 150), (200, 120), (250, 150), (550, 150), (600, 120), (650, 150), (180, 210), (620, 210))):
        b.append(enemy_ship(x, y, "#f97316" if i % 2 else "#ef4444"))
    b += ['<circle cx="250" cy="260" r="34" fill="url(#boom)"/><circle cx="560" cy="230" r="24" fill="url(#boom)"/>']
    for x, y in ((392, 320), (408, 320), (392, 270), (408, 270), (392, 222), (408, 222)):
        b.append(r(x - 2, y, 4, 22, "#22d3ee", 2) + r(x - 4, y, 8, 22, "#22d3ee", 4, 'opacity="0.3"'))
    b += ['<path d="M400 350 L430 430 L400 418 L370 430 Z" fill="#e0f2fe" stroke="#22d3ee" stroke-width="2.5"/>',
          '<path d="M400 372 L410 404 L400 400 L390 404 Z" fill="#0ea5e9"/>',
          '<path d="M386 424 L400 470 L414 424 Z" fill="#fb923c" opacity="0.9"/><path d="M393 424 L400 452 L407 424 Z" fill="#fde047"/>',
          '<circle cx="400" cy="398" r="58" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.35" stroke-dasharray="6 6"/>']
    b += [t(400, 30, "BOSS · 深淵戰艦", 13, "#fda4af", 900, "middle"), r(250, 38, 300, 12, "#3f0d1b", 6, 'stroke="#fda4af"'), r(250, 38, 196, 12, "#e11d48", 6),
          t(24, 34, "SCORE", 12, "#94a3b8", 900, mono=True), t(24, 60, "0384200", 22, "#fff", 900, mono=True),
          t(776, 34, "STAGE 5", 14, "#fde047", 900, "end", True), t(776, 58, "POWER ▮▮▮▮▯", 13, "#22d3ee", 900, "end", True)]
    for i in range(3):
        x = 32 + i * 30
        b.append(f'<path d="M{x} 456 L{x+11} 484 L{x} 479 L{x-11} 484 Z" fill="#e0f2fe" stroke="#22d3ee" stroke-width="1.5"/>')
    b.append(t(24, 446, "LIVES", 11, "#94a3b8", 900, mono=True))
    return svg("".join(b), defs)

