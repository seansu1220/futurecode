"""休閒遊戲類作品：2D 平台跳躍、寶石消除、太空射擊的其他畫面。"""
import math
import random

from .common import *  # noqa: F401,F403
from .games_casual import brick_platform, cloud, coin, enemy_ship, gem, scene_match3, scene_platformer, scene_shooter

HUD_STROKE = "#1b1b3a"


# ================= 2D 平台跳躍：像素大冒險 =================
def hero(hx, hy, s=1.0, cap="#e53935", shirt="#e53935", pants="#1e40af", skin="#ffcc99", hat=None):
    """像素風主角，(hx, hy) 為腳底中心。hat：None 帽子、'wizard' 法師帽、'ninja' 頭巾、'crown' 皇冠。"""
    parts = [r(-12, -46, 24, 20, skin, 4), c(5, -38, 2.5, "#222"), r(-14, -26, 28, 22, shirt, 4), r(-14, -14, 28, 8, pants, 2),
             r(-14, -6, 11, 6, pants, 2), r(3, -6, 11, 6, pants, 2), r(14, -24, 9, 8, skin, 3)]
    if hat == "wizard":
        parts.append(path("M-16 -44 L0 -78 L16 -44 Z", cap) + r(-18, -48, 36, 6, cap, 3) + c(0, -60, 3, "#fde047"))
    elif hat == "ninja":
        parts.append(r(-13, -48, 26, 10, cap, 3) + path("M-13 -44 l-12 -6 l2 8z", cap) + r(-12, -36, 24, 6, cap))
    elif hat == "crown":
        parts.append(path("M-12 -46 l0 -12 l6 6 l6 -10 l6 10 l6 -6 l0 12z", "#fbbf24") + r(-14, -48, 6, 22, cap, 3) + r(8, -48, 6, 22, cap, 3))
    else:
        parts.append(r(-14, -52, 30, 10, cap, 3))
    return f'<g transform="translate({hx} {hy}) scale({s})">{"".join(parts)}</g>'


def slime(cx, by, s=1.0, color="#7b2ff7"):
    return (f'<g transform="translate({cx} {by}) scale({s})">' + path("M-22 0 q0 -36 22 -36 q22 0 22 36 z", color)
            + c(-7, -16, 5, "#fff") + c(7, -16, 5, "#fff") + c(-6, -15, 2.5, "#111") + c(8, -15, 2.5, "#111") + "</g>")


def sky_scene(defs_id="sky"):
    defs = lin_grad(defs_id, "#4cb8ff", "#d4f3ff")
    b = [r(0, 0, 800, 500, f"url(#{defs_id})"), cloud(140, 110), cloud(620, 90, 1.2), cloud(420, 170, 0.8),
         '<path d="M0 420 Q120 300 240 420 Z" fill="#7fd39b"/><path d="M180 420 Q340 260 500 420 Z" fill="#69c48a"/><path d="M460 420 Q620 320 800 420 Z" fill="#7fd39b"/>',
         r(0, 420, 800, 80, "#c47a3a"), r(0, 412, 800, 16, "#5cc84a")]
    for x in range(0, 800, 40):
        b.append(ln(x, 428, x, 500, "#a5612a", 2))
    b.append(ln(0, 464, 800, 464, "#a5612a", 2))
    return defs, b


def scene_platformer_title():
    defs, b = sky_scene()
    b += [outline_text(400, 150, "PIXEL QUEST", 66, "#ffd23f", HUD_STROKE, 10, mono=True), outline_text(400, 196, "像素大冒險", 30, "#fff", HUD_STROKE, 7)]
    for i, s in enumerate(["開始遊戲", "繼續冒險", "角色選擇", "遊戲設定"]):
        y = 232 + i * 44
        on = i == 0
        b += [r(310, y, 180, 36, "#ffd23f" if on else "#ffffff", 8, f'stroke="{HUD_STROKE}" stroke-width="3"'),
              t(400, y + 24, s, 15, HUD_STROKE, 900, "middle")]
        if on:
            b.append(path(f"M286 {y + 8} l14 10 l-14 10z", "#ffd23f", f'stroke="{HUD_STROKE}" stroke-width="2"'))
    b += [hero(150, 412, 2.0), slime(650, 412, 1.4), coin(560, 360), coin(590, 350), coin(620, 360),
          outline_text(400, 484, "PRESS START", 16, "#fff", HUD_STROKE, 4, mono=True), t(780, 490, "v1.0.3", 10, "#fff", 700, "end")]
    return svg("".join(b), defs)


def scene_platformer_map():
    defs = lin_grad("sea", "#38bdf8", "#0369a1")
    b = [r(0, 0, 800, 500, "url(#sea)")]
    rnd = random.Random(5)
    for _ in range(26):
        x, y = rnd.randint(0, 780), rnd.randint(40, 490)
        b.append(path(f"M{x} {y} q6 -5 12 0 q6 5 12 0", "none", 'stroke="#e0f2fe" stroke-width="2" opacity="0.5"'))
    b += ['<ellipse cx="230" cy="300" rx="210" ry="150" fill="#fde68a"/>', '<ellipse cx="230" cy="296" rx="196" ry="138" fill="#86efac"/>',
          '<ellipse cx="600" cy="230" rx="170" ry="130" fill="#fde68a"/>', '<ellipse cx="600" cy="226" rx="156" ry="118" fill="#4ade80"/>',
          '<ellipse cx="660" cy="420" rx="90" ry="50" fill="#fde68a"/>', '<ellipse cx="660" cy="416" rx="80" ry="42" fill="#a3a3a3"/>']
    for x, y in ((120, 230), (330, 360), (520, 160), (700, 280), (180, 380)):
        b.append(path(f"M{x} {y} l14 -28 l14 28z", "#15803d") + r(x + 12, y, 4, 8, "#78350f"))
    nodes = [(110, 330), (200, 260), (300, 300), (380, 210), (470, 250), (560, 180), (650, 260), (660, 400)]
    pts = " ".join(f"{x},{y}" for x, y in nodes)
    b.append(f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="2 10" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(nodes):
        done, cur, boss = i < 4, i == 4, i == 7
        col = "#22c55e" if done else ("#ffd23f" if cur else "#9ca3af")
        if boss:
            b += [r(x - 26, y - 34, 52, 40, "#57534e", 3, f'stroke="{HUD_STROKE}" stroke-width="3"'),
                  "".join(r(x - 26 + k * 13, y - 44, 9, 12, "#57534e", 1, f'stroke="{HUD_STROKE}" stroke-width="2"') for k in range(4)),
                  r(x - 7, y - 14, 14, 20, HUD_STROKE, 6), outline_text(x, y + 26, "BOSS", 13, "#f87171", HUD_STROKE, 4, mono=True)]
            continue
        b += [c(x, y, 20 if cur else 17, col, f'stroke="{HUD_STROKE}" stroke-width="3"'), t(x, y + 5, f"1-{i + 1}", 11, HUD_STROKE, 900, "middle", True)]
        if done:
            b.append(t(x, y - 24, "★★★" if i != 2 else "★★☆", 12, "#facc15", 900, "middle", extra=f'stroke="{HUD_STROKE}" stroke-width="2" paint-order="stroke"'))
        if i > 4:
            b.append(r(x - 6, y - 4, 12, 10, HUD_STROKE, 2) + path(f"M{x - 4} {y - 4} v-4 a4 4 0 0 1 8 0 v4", "none", f'stroke="{HUD_STROKE}" stroke-width="2"'))
    b += [c(470, 250, 30, "#ffd23f", 'opacity="0.35"'), hero(470, 230, 0.9),
          r(16, 16, 230, 56, "#ffffff", 12, f'stroke="{HUD_STROKE}" stroke-width="3"'), t(32, 40, "世界 1", 13, "#64748b", 900), t(32, 62, "青草平原", 18, HUD_STROKE, 900),
          t(232, 52, "★ 11 / 21", 14, "#ca8a04", 900, "end"), r(552, 16, 232, 40, "#ffffff", 12, f'stroke="{HUD_STROKE}" stroke-width="3"'),
          coin(574, 36), t(592, 42, "× 128", 15, HUD_STROKE, 900, mono=True), t(768, 42, "♥ × 3", 15, "#ef4444", 900, "end", True),
          shadow(r(16, 380, 260, 104, "#ffffff", 14)), t(32, 406, "1-5 雲端之路", 16, HUD_STROKE, 900), t(32, 428, "最佳時間：--:--　收集金幣：0 / 30", 11, "#64748b"),
          t(32, 448, "提示：踩在雲朵上可以跳得更高！", 11, "#0369a1"), btn(176, 452, 88, 26, "開始 ▶", "#22c55e", size=13, rx=8)]
    return svg("".join(b), defs)


def scene_platformer_select():
    defs = diag_grad("sel", "#1e1b4b", "#4338ca")
    b = [r(0, 0, 800, 500, "url(#sel)"), stars(3, 60), outline_text(400, 58, "選擇你的角色", 30, "#fff", HUD_STROKE, 6)]
    chars = [("勇者", "#e53935", "#e53935", None, (0.6, 0.6, 0.8), "均衡型，適合新手"), ("法師", "#7c3aed", "#7c3aed", "wizard", (0.5, 0.5, 0.9), "可發射火球攻擊"),
             ("忍者", "#1f2937", "#374151", "ninja", (0.95, 0.8, 0.5), "速度最快，可二段跳"), ("？？？", "#ec4899", "#f9a8d4", "crown", (0.6, 0.9, 0.4), "通過世界 2 解鎖")]
    for i, (name, cap, shirt, hat, st, desc) in enumerate(chars):
        x = 40 + i * 184
        sel = i == 2
        b += [r(x, 90, 168, 340, "#312e81" if not sel else "#4c1d95", 16, f'stroke="{"#fde047" if sel else "#6366f1"}" stroke-width="{4 if sel else 2}"'),
              c(x + 84, 190, 56, "#ffffff", 'opacity="0.08"'), hero(x + 84, 240, 2.2, cap, shirt, "#111827" if hat == "ninja" else "#1e40af", hat=hat),
              t(x + 84, 280, name, 20, "#fff", 900, "middle"), t(x + 84, 300, desc, 10.5, "#c7d2fe", 400, "middle")]
        for k, (lab, v) in enumerate(zip(["速度", "跳躍", "力量"], st)):
            y = 330 + k * 26
            b += [t(x + 16, y + 9, lab, 11, "#e0e7ff", 700), progress(x + 52, y, 100, 10, v, "#fde047" if sel else "#818cf8", "#1e1b4b")]
        if sel:
            b += [r(x + 44, 400, 80, 22, "#fde047", 11), t(x + 84, 415, "已選擇", 11, HUD_STROKE, 900, "middle")]
        if i == 3:
            b += [r(x, 90, 168, 340, "#000000", 16, 'opacity="0.45"'), r(x + 70, 236, 28, 22, "#fff", 4) + path(f"M{x + 76} 236 v-8 a8 8 0 0 1 16 0 v8", "none", 'stroke="#fff" stroke-width="4"')]
    b += [btn(320, 448, 160, 38, "確定出發 ▶", "#22c55e", size=15, rx=10), t(40, 474, "◀ ▶ 切換角色　Enter 確認", 11, "#a5b4fc")]
    return svg("".join(b), defs)


def scene_platformer_boss():
    defs = lin_grad("cast", "#1c1917", "#44403c") + lin_grad("lava", "#fb923c", "#b91c1c") + rad_grad("fire", "#fef08a", "#f97316", 1, 0.2)
    b = [r(0, 0, 800, 500, "url(#cast)")]
    for row in range(10):
        for col in range(14):
            x = col * 60 + (30 if row % 2 else 0) - 30
            b.append(r(x, row * 36, 58, 34, "#292524", 2, 'opacity="0.6"'))
    b += [r(80, 120, 26, 40, "#78350f", 3), path("M93 120 q-10 -16 0 -30 q10 14 0 30z", "#f97316"), r(690, 120, 26, 40, "#78350f", 3),
          path("M703 120 q-10 -16 0 -30 q10 14 0 30z", "#f97316"), r(0, 430, 800, 70, "url(#lava)")]
    for x in (60, 210, 380, 560, 720):
        b.append(c(x, 440, 8, "#fde047", 'opacity="0.7"'))
    b += [r(40, 360, 260, 24, "#78716c", 3, 'stroke="#292524" stroke-width="3"'), r(500, 330, 260, 24, "#78716c", 3, 'stroke="#292524" stroke-width="3"'),
          r(320, 270, 120, 20, "#78716c", 3, 'stroke="#292524" stroke-width="3"')]
    # 火龍王
    b += ['<g transform="translate(610 250)">', '<ellipse cx="0" cy="40" rx="90" ry="46" fill="#15803d" stroke="#052e16" stroke-width="4"/>',
          path("M-30 10 q-60 -80 -40 -120 q30 30 20 80z", "#166534", 'stroke="#052e16" stroke-width="3"'),
          path("M30 0 q40 -90 90 -100 q-20 40 -50 100z", "#166534", 'stroke="#052e16" stroke-width="3"'),
          '<ellipse cx="-70" cy="-10" rx="46" ry="34" fill="#16a34a" stroke="#052e16" stroke-width="4"/>',
          path("M-60 -40 l-6 -28 l16 22z M-90 -38 l-14 -24 l20 16z", "#fde68a"), c(-82, -16, 7, "#fef08a"), c(-82, -16, 3, "#111"),
          path("M-112 0 q10 8 26 2", "none", 'stroke="#052e16" stroke-width="3"'), r(-40, 74, 22, 16, "#14532d", 4), r(30, 74, 22, 16, "#14532d", 4), "</g>",
          path("M508 248 Q420 230 330 290 Q420 260 508 262 Z", "url(#fire)"), c(350, 284, 18, "url(#fire)"),
          hero(160, 360, 1.5), r(178, 300, 6, 40, "#e5e7eb", 2, 'transform="rotate(30 181 320)"'),
          outline_text(400, 36, "火龍王 · 第 2 階段", 16, "#fca5a5", HUD_STROKE, 4), r(220, 46, 360, 16, "#450a0a", 8, 'stroke="#fca5a5" stroke-width="2"'),
          r(220, 46, 150, 16, "#ef4444", 8), outline_text(470, 160, "-120", 26, "#fde047", "#7c2d12", 5)]
    for i in range(3):
        x = 24 + i * 34
        b.append(path(f"M{x + 12} 450 c-8 -12 -24 -2 -12 10 l12 12 l12 -12 c12 -12 -4 -22 -12 -10z", "#ef4444" if i < 2 else "#57534e", f'stroke="{HUD_STROKE}" stroke-width="2.5"'))
    b += [outline_text(24, 40, "WORLD 1-BOSS", 14, "#fff", HUD_STROKE, 4, "start", mono=True), outline_text(776, 40, "TIME 142", 14, "#fff", HUD_STROKE, 4, "end", mono=True)]
    return svg("".join(b), defs)


# ================= 寶石消除：寶石傳說 =================
def match_bg():
    defs = diag_grad("mbg", "#1e1052", "#7b2ff7")
    return defs, [r(0, 0, 800, 500, "url(#mbg)"), stars(21, 40)]


def gold_panel(x, y, w, h):
    return shadow(r(x, y, w, h, "#2a1766", 18, 'stroke="#a78bfa" stroke-width="3"'))


def scene_match3_title():
    defs, b = match_bg()
    defs += rad_grad("halo", "#f0abfc", "#7b2ff7", 0.7, 0)
    b += [c(400, 190, 200, "url(#halo)")]
    rnd = random.Random(9)
    for i in range(14):
        ang = i / 14 * math.tau
        x, y = 400 + math.cos(ang) * 230, 190 + math.sin(ang) * 120
        b.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({rnd.uniform(1.1, 1.8):.2f})">{gem(i % 5, 0, 0)}</g>')
    b += [outline_text(400, 182, "寶石傳說", 64, "#fde047", "#7c2d12", 12), outline_text(400, 224, "JEWEL LEGEND", 20, "#fff", "#4c1d95", 6, mono=True),
          c(400, 330, 54, "#22c55e", 'stroke="#fff" stroke-width="6"'), path("M386 306 L424 330 L386 354 Z", "#fff"),
          outline_text(400, 412, "開始遊戲", 22, "#fff", "#14532d", 6)]
    for i, (s, col) in enumerate([("每日獎勵", "#f97316"), ("商店", "#ec4899"), ("設定", "#6366f1")]):
        x = 60 + i * 90 if i < 1 else 600 + (i - 1) * 90
        b += [c(x + 30, 448, 26, col, 'stroke="#fff" stroke-width="3"'), t(x + 30, 453, s[:2], 11, "#fff", 900, "middle"), t(x + 30, 490, s, 11, "#e9d5ff", 700, "middle")]
    b += [c(108, 426, 10, "#ef4444"), t(108, 430, "1", 10, "#fff", 900, "middle")]
    return svg("".join(b), defs)


def scene_match3_map():
    defs = lin_grad("land", "#f9a8d4", "#7c3aed")
    b = [r(0, 0, 800, 500, "url(#land)")]
    for x, y, rr, col in ((100, 160, 90, "#f472b6"), (700, 120, 110, "#c084fc"), (650, 420, 120, "#a855f7"), (140, 440, 100, "#e879f9")):
        b.append(c(x, y, rr, col, 'opacity="0.45"'))
    nodes = [(400, 470), (300, 420), (250, 350), (330, 290), (450, 270), (530, 210), (470, 140), (360, 110), (280, 60)]
    d = "M" + " ".join(f"{x} {y}" for x, y in nodes)
    b.append(path(d, "none", 'stroke="#fdf4ff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"'))
    for i, (x, y) in enumerate(nodes):
        lvl = 8 + i
        done, cur = lvl < 12, lvl == 12
        col = "#ec4899" if done else ("#fde047" if cur else "#a78bfa")
        b += [c(x, y, 24 if cur else 20, col, 'stroke="#fff" stroke-width="4"'), t(x, y + 6, lvl, 15, "#fff" if not cur else "#7c2d12", 900, "middle")]
        if done:
            b.append(t(x, y - 26, "★★★" if lvl != 10 else "★★☆", 12, "#fde047", 900, "middle", extra='stroke="#7c2d12" stroke-width="2" paint-order="stroke"'))
        if cur:
            b += [c(x + 34, y - 24, 16, "#fbbf24", 'stroke="#fff" stroke-width="3"'), t(x + 34, y - 19, "你", 12, "#7c2d12", 900, "middle")]
    b += [r(0, 0, 800, 48, "#2a1766", 0, 'opacity="0.85"'), t(24, 31, "♥ 5", 16, "#f43f5e", 900), t(70, 31, "滿", 11, "#fda4af", 700),
          r(320, 10, 120, 28, "#1e1052", 14), c(338, 24, 9, "#fde047"), t(356, 30, "2,480", 13, "#fff", 900),
          r(456, 10, 100, 28, "#1e1052", 14), f'<g transform="translate(474 24) scale(0.6)">{gem(1, 0, 0)}</g>', t(492, 30, "36", 13, "#fff", 900)]
    for i, (s, col) in enumerate([("每日任務", "#f97316"), ("道具商店", "#ec4899"), ("好友排行", "#22d3ee")]):
        y = 100 + i * 80
        b += [c(720, y, 28, col, 'stroke="#fff" stroke-width="3"'), t(720, y + 44, s, 11, "#fff", 900, "middle")]
    b += [shadow(r(560, 360, 220, 120, "#fff", 18)), t(580, 390, "第 12 關", 18, "#4c1d95", 900), t(580, 412, "目標：收集 20 顆紅寶石", 12, "#6d28d9"),
          t(580, 432, "步數限制：30 步", 12, "#6d28d9"), btn(580, 442, 180, 30, "開始 ▶", "#22c55e", size=14, rx=15)]
    return svg("".join(b), defs)


def scene_match3_shop():
    defs, b = match_bg()
    b += [gold_panel(60, 30, 680, 440), outline_text(400, 74, "道具商店", 28, "#fde047", "#7c2d12", 6), r(560, 46, 160, 30, "#1e1052", 15),
          c(580, 61, 10, "#fde047"), t(598, 67, "2,480", 14, "#fff", 900)]
    for i, s in enumerate(["道具", "金幣", "超值禮包"]):
        x = 210 + i * 130
        b.append(btn(x, 92, 120, 30, s, "#ec4899" if i == 0 else "#3b2386", "#fff", 13, 15))
    items = [("炸彈 × 3", "消除周圍 3×3", "100", "#f97316", "爆"), ("彩虹球", "消除同色所有寶石", "180", "#ec4899", "虹"),
             ("重洗棋盤", "重新排列全部寶石", "60", "#22d3ee", "洗"), ("+5 步數", "步數用完時救急", "120", "#22c55e", "+5"),
             ("生命 × 5", "立即補滿生命", "200", "#ef4444", "♥"), ("新手禮包", "金幣 ×3000 + 道具組", "NT$ 90", "#fbbf24", "禮")]
    for i, (name, desc, price, col, icon) in enumerate(items):
        x, y = 88 + (i % 3) * 212, 140 + (i // 3) * 160
        hot = i == 5
        b += [r(x, y, 196, 148, "#3b2386", 14, f'stroke="{"#fde047" if hot else "#6d28d9"}" stroke-width="{3 if hot else 1.5}"'),
              c(x + 98, y + 46, 30, col, 'stroke="#fff" stroke-width="3"'), t(x + 98, y + 53, icon, 18, "#fff", 900, "middle"),
              t(x + 98, y + 94, name, 14, "#fff", 900, "middle"), t(x + 98, y + 112, desc, 10.5, "#c4b5fd", 400, "middle"),
              btn(x + 38, y + 120, 120, 22, ("● " + price) if not hot else price, "#22c55e" if not hot else "#f97316", size=11.5, rx=11)]
        if hot:
            b += [r(x + 126, y - 10, 70, 22, "#ef4444", 11), t(x + 161, y + 5, "人氣 No.1", 10, "#fff", 900, "middle")]
    b += [c(728, 42, 18, "#ef4444", 'stroke="#fff" stroke-width="3"'), t(728, 48, "✕", 14, "#fff", 900, "middle")]
    return svg("".join(b), defs)


def scene_match3_result():
    defs, b = match_bg()
    rnd = random.Random(14)
    for _ in range(60):
        x, y = rnd.randint(0, 800), rnd.randint(0, 500)
        col = rnd.choice(["#fde047", "#f472b6", "#22d3ee", "#4ade80", "#fb923c"])
        b.append(r(x, y, 8, 4, col, 1, f'transform="rotate({rnd.randint(0, 180)} {x} {y})"'))
    b += [gold_panel(200, 60, 400, 400), path("M170 70 h460 l-24 24 l24 24 h-460 l24 -24z", "#ec4899", 'stroke="#fff" stroke-width="3"'),
          outline_text(400, 104, "過關！", 28, "#fff", "#831843", 6)]
    for i, (dx, dy, s) in enumerate(((-90, 190, 1.2), (0, 170, 1.6), (90, 190, 1.2))):
        pts = []
        for k in range(10):
            a = math.radians(-90 + k * 36)
            rad = 26 if k % 2 == 0 else 12
            pts.append((400 + dx + rad * s * math.cos(a), dy + rad * s * math.sin(a)))
        b.append(poly(pts, "#fde047", 'stroke="#b45309" stroke-width="3"'))
    b += [t(400, 250, "分數", 13, "#c4b5fd", 700, "middle"), outline_text(400, 290, "24,860", 38, "#fde047", "#7c2d12", 6),
          pill(352, 300, "新紀錄！", "#ef4444", "#fff", 11), t(400, 346, "獎勵", 13, "#c4b5fd", 700, "middle"),
          r(270, 356, 120, 40, "#1e1052", 12), c(296, 376, 11, "#fde047"), t(316, 382, "+120", 15, "#fff", 900),
          r(410, 356, 120, 40, "#1e1052", 12), f'<g transform="translate(436 376) scale(0.75)">{gem(1, 0, 0)}</g>', t(456, 382, "+2", 15, "#fff", 900),
          btn(232, 412, 150, 36, "↻ 重玩", "#6366f1", size=14, rx=18), btn(418, 412, 150, 36, "下一關 ▶", "#22c55e", size=14, rx=18)]
    return svg("".join(b), defs)


# ================= 太空射擊：星際突擊 =================
def space_bg():
    defs = (rad_grad("neb1", "#7c3aed", "#7c3aed", 0.55, 0, "0.3", "0.3") + rad_grad("neb2", "#0ea5e9", "#0ea5e9", 0.4, 0, "0.8", "0.7"))
    return defs, [r(0, 0, 800, 500, "#050816"), r(0, 0, 800, 500, "url(#neb1)"), r(0, 0, 800, 500, "url(#neb2)"), stars(42, 120)]


def player_ship(cx, cy, s=1.0, body="#e0f2fe", trim="#22d3ee", wing=None):
    wing = wing or trim
    shape = (path("M-40 30 L-14 4 L-14 30 Z M40 30 L14 4 L14 30 Z", wing, 'opacity="0.85"') + path("M0 -44 L24 30 L0 20 L-24 30 Z", body, f'stroke="{trim}" stroke-width="2.5"')
             + path("M0 -22 L8 6 L0 3 L-8 6 Z", "#0ea5e9") + path("M-10 26 L0 62 L10 26 Z", "#fb923c", 'opacity="0.9"') + path("M-5 26 L0 46 L5 26 Z", "#fde047"))
    return f'<g transform="translate({cx} {cy}) scale({s})">{shape}</g>'


def scene_shooter_title():
    defs, b = space_bg()
    b += ['<circle cx="640" cy="380" r="150" fill="#1e3a8a"/><circle cx="610" cy="350" r="150" fill="#050816" opacity="0.35"/>',
          '<ellipse cx="640" cy="380" rx="230" ry="30" fill="none" stroke="#93c5fd" stroke-width="4" opacity="0.45" transform="rotate(-14 640 380)"/>',
          outline_text(400, 124, "STAR STRIKER", 60, "#22d3ee", "#082f49", 10, mono=True), outline_text(400, 168, "星 際 突 擊", 26, "#fff", "#082f49", 6),
          player_ship(400, 260, 1.5)]
    for i, s in enumerate(["開始任務", "機庫", "排行榜", "設定"]):
        y = 340 + i * 36
        on = i == 0
        b += [r(320, y, 160, 28, "#22d3ee" if on else "#0f172a", 4, f'stroke="#22d3ee" stroke-width="1.5" opacity="{1 if on else 0.85}"'),
              t(400, y + 19, s, 13, "#082f49" if on else "#e0f2fe", 900, "middle")]
    b += [t(24, 484, "最高分 0,384,200", 11, "#94a3b8", 700, mono=True), t(776, 484, "© FUTURE CODE GAMES", 10, "#64748b", 700, "end", True)]
    return svg("".join(b), defs)


def scene_shooter_hangar():
    defs, b = space_bg()
    b += [outline_text(400, 54, "機庫 · 選擇機體", 26, "#fff", "#082f49", 6)]
    ships = [("疾風號", "#e0f2fe", "#22d3ee", (0.5, 0.95, 0.4), "高速閃避型"), ("雷霆號", "#fef3c7", "#f59e0b", (0.9, 0.6, 0.6), "重火力攻擊型"),
             ("堡壘號", "#dcfce7", "#22c55e", (0.6, 0.4, 0.95), "高護盾防禦型")]
    for i, (name, body, trim, st, role) in enumerate(ships):
        x = 140 + i * 260
        sel = i == 1
        b += [f'<ellipse cx="{x}" cy="300" rx="90" ry="20" fill="{trim}" opacity="{0.45 if sel else 0.2}"/>',
              f'<ellipse cx="{x}" cy="300" rx="70" ry="13" fill="none" stroke="{trim}" stroke-width="2"/>',
              player_ship(x, 230, 1.9 if sel else 1.4, body, trim), t(x, 344, name, 20 if sel else 16, "#fff", 900, "middle"),
              t(x, 364, role, 11, trim, 700, "middle")]
        for k, (lab, v) in enumerate(zip(["火力", "速度", "護盾"], st)):
            y = 384 + k * 22
            b += [t(x - 80, y + 9, lab, 11, "#cbd5e1", 700), progress(x - 46, y, 126, 9, v, trim, "#1e293b")]
        if sel:
            b.append(r(x - 110, 80, 220, 400, "none", 16, f'stroke="{trim}" stroke-width="2" stroke-dasharray="8 6"'))
    b += [btn(330, 452, 140, 34, "出擊 ▶", "#f59e0b", "#1c1917", 15, 6), t(24, 30, "◀  Q", 12, "#64748b", 700, mono=True), t(776, 30, "E  ▶", 12, "#64748b", 700, "end", True)]
    return svg("".join(b), defs)


def scene_shooter_upgrade():
    defs, b = space_bg()
    b += [r(0, 0, 800, 500, "#050816", 0, 'opacity="0.55"'), outline_text(40, 54, "武器研發", 26, "#fff", "#082f49", 6, "start"),
          r(600, 30, 176, 32, "#0f172a", 16, 'stroke="#a78bfa"'), path("M622 38 l8 8 l-8 8 l-8 -8z", "#a78bfa"), t(640, 52, "能量晶體 1,860", 12, "#e9d5ff", 900)]
    nodes = {"主砲": (120, 250, 3, 5, "#22d3ee", True), "散射砲": (300, 150, 2, 5, "#22d3ee", True), "雷射": (300, 350, 1, 5, "#f472b6", True),
             "追蹤導彈": (480, 110, 0, 3, "#f59e0b", False), "穿透彈": (480, 220, 2, 3, "#22d3ee", True), "護盾": (480, 330, 1, 5, "#22c55e", True),
             "僚機": (480, 430, 0, 3, "#a78bfa", False), "終極砲": (640, 250, 0, 1, "#ef4444", False)}
    links = [("主砲", "散射砲"), ("主砲", "雷射"), ("散射砲", "追蹤導彈"), ("散射砲", "穿透彈"), ("雷射", "護盾"), ("雷射", "僚機"), ("穿透彈", "終極砲"), ("護盾", "終極砲")]
    for a, z in links:
        (x1, y1, *_), (x2, y2, *_) = nodes[a], nodes[z]
        unlocked = nodes[z][5]
        b.append(ln(x1, y1, x2, y2, "#22d3ee" if unlocked else "#334155", 3, '' if unlocked else 'stroke-dasharray="6 5"'))
    for name, (x, y, lv, mx, col, unlocked) in nodes.items():
        sel = name == "穿透彈"
        b += [c(x, y, 34 if sel else 28, "#0f172a", f'stroke="{col if unlocked else "#334155"}" stroke-width="{4 if sel else 3}"'),
              t(x, y + 5, name[:2], 13, col if unlocked else "#475569", 900, "middle"), t(x, y + 50, name, 11.5, "#e2e8f0" if unlocked else "#64748b", 700, "middle")]
        for k in range(mx):
            b.append(r(x - mx * 5 + k * 10, y + 58, 8, 5, col if k < lv else "#1e293b", 1))
        if sel:
            b.append(c(x, y, 44, col, 'opacity="0.15"'))
    b += [shadow(r(560, 330, 216, 150, "#0f172a", 12)), r(560, 330, 216, 150, "none", 12, 'stroke="#22d3ee"'),
          t(576, 356, "穿透彈 Lv.2 → Lv.3", 13, "#e0f2fe", 900), t(576, 378, "子彈可貫穿 3 個敵人", 11, "#94a3b8"),
          t(576, 398, "傷害 +15%　射速 +5%", 11, "#22d3ee", 700), btn(576, 430, 184, 32, "升級　◆ 480", "#a78bfa", "#1e1b4b", 13, 6)]
    return svg("".join(b), defs)


def scene_shooter_result():
    defs, b = space_bg()
    b += [r(0, 0, 800, 500, "#050816", 0, 'opacity="0.5"'), outline_text(400, 66, "MISSION COMPLETE", 40, "#22d3ee", "#082f49", 8, mono=True),
          t(400, 92, "第 5 關 · 深淵戰艦 已擊破", 13, "#e0f2fe", 700, "middle"), shadow(r(60, 116, 330, 340, "#0f172a", 14)),
          r(60, 116, 330, 340, "none", 14, 'stroke="#22d3ee"'), t(84, 150, "戰績", 15, "#e0f2fe", 900)]
    for i, (k, v) in enumerate([("分數", "0,384,200"), ("擊墜數", "248"), ("命中率", "87.4%"), ("最大連擊", "× 96"), ("受到傷害", "2 次")]):
        y = 186 + i * 36
        b += [t(84, y, k, 12.5, "#94a3b8"), t(366, y, v, 16, "#fff", 900, "end", True), ln(84, y + 12, 366, y + 12, "#1e293b")]
    b += [t(84, 384, "評價", 12.5, "#94a3b8"), outline_text(330, 420, "S", 56, "#fde047", "#7c2d12", 6), btn(84, 404, 150, 32, "繼續 ▶", "#22d3ee", "#082f49", 13, 6),
          shadow(r(410, 116, 330, 340, "#0f172a", 14)), r(410, 116, 330, 340, "none", 14, 'stroke="#a78bfa"'), t(434, 150, "全球排行榜", 15, "#e9d5ff", 900),
          t(716, 150, "本週", 11, "#a78bfa", 700, "end")]
    board = [("NovaAce", "0,512,880"), ("小隼", "0,498,120"), ("CometX", "0,431,600"), ("你", "0,384,200"), ("阿翔", "0,377,050"), ("PixelPilot", "0,352,900")]
    for i, (name, sc) in enumerate(board):
        y = 186 + i * 40
        me = name == "你"
        if me:
            b.append(r(422, y - 22, 306, 34, "#a78bfa", 8, 'opacity="0.25"'))
        medal = ["#fde047", "#e5e7eb", "#d97706"][i] if i < 3 else "#475569"
        b += [c(446, y - 5, 12, medal), t(446, y, i + 1, 11, "#0f172a", 900, "middle"), t(470, y, name, 13, "#fff" if me else "#cbd5e1", 900 if me else 500),
              t(716, y, sc, 13, "#fde047" if me else "#e2e8f0", 900, "end", True)]
    return svg("".join(b), defs)


SCREENS = {
    "game-platformer": [scene_platformer_title, scene_platformer_map, scene_platformer, scene_platformer_select, scene_platformer_boss],
    "game-match3": [scene_match3_title, scene_match3_map, scene_match3, scene_match3_shop, scene_match3_result],
    "game-shooter": [scene_shooter_title, scene_shooter_hangar, scene_shooter, scene_shooter_upgrade, scene_shooter_result],
}
