"""進階遊戲類作品：台灣 16 張麻將、集換式卡牌對戰、戰棋策略 RPG。"""
import math
import random

from .common import *  # noqa: F401,F403

# ================= 麻將：雀神大亨 =================
NUM_CN = "一二三四五六七八九"
GOLD, MJ_RED, MJ_DARK = "#fbbf24", "#b91c1c", "#450a0a"
DOT_LAYOUT = {
    1: [(.5, .5)], 2: [(.5, .27), (.5, .73)], 3: [(.27, .22), (.5, .5), (.73, .78)],
    4: [(.3, .27), (.7, .27), (.3, .73), (.7, .73)], 5: [(.28, .22), (.72, .22), (.5, .5), (.28, .78), (.72, .78)],
    6: [(.3, .2), (.7, .2), (.3, .5), (.7, .5), (.3, .8), (.7, .8)],
    7: [(.22, .15), (.5, .27), (.78, .39), (.3, .62), (.7, .62), (.3, .85), (.7, .85)],
    8: [(.3, .14), (.7, .14), (.3, .38), (.7, .38), (.3, .62), (.7, .62), (.3, .86), (.7, .86)],
    9: [(.22, .18), (.5, .18), (.78, .18), (.22, .5), (.5, .5), (.78, .5), (.22, .82), (.5, .82), (.78, .82)],
}


def mj_face(face, w, h):
    suit, val = face
    if suit == "m":
        return t(w / 2, h * 0.44, NUM_CN[val - 1], round(h * 0.36, 1), "#1e3a8a", 900, "middle") + t(w / 2, h * 0.86, "萬", round(h * 0.36, 1), MJ_RED, 900, "middle")
    if suit == "z":
        if val == "白":
            return r(w * 0.2, h * 0.18, w * 0.6, h * 0.64, "none", 2, 'stroke="#2563eb" stroke-width="2"')
        col = MJ_RED if val == "中" else ("#15803d" if val == "發" else "#1e293b")
        return t(w / 2, h * 0.68, val, round(h * 0.52, 1), col, 900, "middle")
    out = []
    pts = DOT_LAYOUT[val]
    for i, (px, py) in enumerate(pts):
        x, y = w * 0.08 + px * w * 0.84, h * 0.06 + py * h * 0.88
        if suit == "p":
            rad = w * 0.3 if val == 1 else (w * 0.13 if val < 7 else w * 0.11)
            col = ["#1d4ed8", "#15803d", MJ_RED][i % 3] if val > 1 else MJ_RED
            out.append(c(round(x, 1), round(y, 1), round(rad, 1), col) + c(round(x, 1), round(y, 1), round(rad * 0.45, 1), "#fbf7ea"))
        else:
            if val == 1:
                out.append(f'<ellipse cx="{w / 2}" cy="{h / 2}" rx="{w * 0.26}" ry="{h * 0.3}" fill="#15803d"/>' + c(w / 2, h * 0.36, w * 0.08, MJ_RED))
                break
            sw, sh = w * 0.12, h * (0.2 if val < 7 else 0.16)
            col = MJ_RED if (val in (5, 7, 9) and (px, py) == (.5, .5)) or (val == 7 and i == 0) else "#15803d"
            out.append(r(round(x - sw / 2, 1), round(y - sh / 2, 1), round(sw, 1), round(sh, 1), col, 1.5))
    return "".join(out)


def mj_tile(x, y, face=None, w=30, h=40, rot=0, lift=0, glow=False):
    """麻將牌；face=None 代表牌背。"""
    side = r(0, 4, w, h, "#15803d" if face else "#14532d", 4)
    if face is None:
        body = r(0, 0, w, h, "#22a060", 4, 'stroke="#14532d"') + r(3, 3, w - 6, h - 6, "none", 3, 'stroke="#86efac" opacity="0.45"')
    else:
        body = r(0, 0, w, h, "#fbf7ea", 4, f'stroke="{GOLD if glow else "#c8bfa5"}" stroke-width="{3 if glow else 1}"') + mj_face(face, w, h)
    tf = f"translate({x} {y - lift})" + (f" rotate({rot} {w / 2} {h / 2})" if rot else "")
    return f'<g transform="{tf}">{side}{body}</g>'


def mj_tile_back_side(x, y, w=26, h=16):
    return r(x, y + 3, w, h, "#14532d", 3) + r(x, y, w, h, "#22a060", 3, 'stroke="#14532d"')


WIN_HAND = [("m", 1), ("m", 2), ("m", 3), ("m", 7), ("m", 8), ("m", 9), ("p", 3), ("p", 4), ("p", 5),
            ("s", 2), ("s", 3), ("s", 4), ("z", "東"), ("z", "東"), ("z", "東"), ("p", 6)]


def felt_bg():
    defs = rad_grad("felt", "#15803d", "#064e3b", 1, 1, "0.5", "0.45", "0.75")
    return defs, [r(0, 0, 800, 500, "#3f1d0b"), r(10, 10, 780, 480, "url(#felt)", 24, 'stroke="#78350f" stroke-width="6"')]


def mj_player(x, y, name, wind, pts, color, anchor="start"):
    out = [c(x, y, 22, color, f'stroke="{GOLD}" stroke-width="3"'), t(x, y + 6, name[0], 16, "#fff", 900, "middle")]
    tx = x + 30 if anchor == "start" else x - 30
    out += [t(tx, y - 4, f"{name} · {wind}", 12, "#fff", 900, anchor), t(tx, y + 14, pts, 11, GOLD, 700, anchor, True)]
    return "".join(out)


def scene_mj_lobby():
    defs = diag_grad("lob", "#450a0a", "#b91c1c") + rad_grad("lg", "#fde68a", "#b91c1c", 0.5, 0)
    b = [r(0, 0, 800, 500, "url(#lob)"), c(400, 120, 220, "url(#lg)")]
    for i in range(12):
        b.append(c(40 + i * 70, 470, 40, "#7f1d1d", 'opacity="0.35"'))
    b += [r(0, 0, 800, 52, "#000000", 0, 'opacity="0.35"'), c(32, 26, 18, "#f97316", f'stroke="{GOLD}" stroke-width="3"'), t(32, 32, "林", 15, "#fff", 900, "middle"),
          t(58, 22, "雀神小林", 13, "#fff", 900), pill(58, 30, "雀聖 III", GOLD, MJ_DARK, 9), r(470, 13, 150, 26, "#000", 13, 'opacity="0.4"'),
          c(486, 26, 9, GOLD), t(500, 31, "1,286,400", 12, "#fff", 900, mono=True), r(630, 13, 100, 26, "#000", 13, 'opacity="0.4"'),
          path("M646 18 l8 8 l-8 8 l-8 -8z", "#38bdf8"), t(660, 31, "520", 12, "#fff", 900, mono=True), t(770, 32, "⚙", 18, "#fff", 400, "middle"),
          outline_text(400, 112, "雀神大亨", 54, GOLD, MJ_DARK, 10), t(400, 138, "台灣 16 張麻將 · 線上對戰", 13, "#fde68a", 700, "middle")]
    modes = [("快速配對", "隨機配對真人玩家", "#dc2626", "#7f1d1d", "線上 3,842 人"), ("好友房", "自訂規則、邀請好友", "#ea580c", "#7c2d12", "輸入房號加入"),
             ("錦標賽", "獎金池 500 萬金幣", "#ca8a04", "#713f12", "20:00 開賽"), ("練習模式", "與 AI 對戰練功", "#0f766e", "#134e4a", "三種難度")]
    for i, (name, desc, c1, c2, tag) in enumerate(modes):
        x = 34 + i * 186
        gid = f"m{i}"
        defs += diag_grad(gid, c1, c2)
        b += [shadow(r(x, 160, 172, 250, f"url(#{gid})", 16)), r(x, 160, 172, 250, "none", 16, f'stroke="{GOLD}" stroke-width="2"'),
              mj_tile(x + 40, 196, [("z", "中"), ("p", 5), ("m", 8), ("s", 9)][i], 40, 54, -12), mj_tile(x + 92, 192, [("z", "發"), ("s", 1), ("z", "東"), ("p", 1)][i], 40, 54, 10),
              t(x + 86, 300, name, 22, "#fff", 900, "middle"), t(x + 86, 324, desc, 11.5, "#fde68a", 400, "middle"),
              r(x + 30, 340, 112, 22, "#000", 11, 'opacity="0.3"'), t(x + 86, 355, tag, 10.5, "#fff", 700, "middle"),
              btn(x + 30, 370, 112, 28, "進入", GOLD, MJ_DARK, 13, 14)]
    for i, s in enumerate(["商城", "任務", "排行", "背包", "公會", "設定"]):
        x = 120 + i * 112
        b += [c(x, 448, 20, "#000", 'opacity="0.35"'), c(x, 448, 14, GOLD, 'opacity="0.85"'), t(x, 484, s, 11.5, "#fff", 700, "middle")]
    b += [c(232, 432, 7, "#ef4444"), t(232, 435, "3", 8, "#fff", 900, "middle")]
    return svg("".join(b), defs)


def scene_mj_table():
    defs, b = felt_bg()
    for i in range(16):
        b.append(mj_tile(232 + i * 21, 26, None, 20, 28))
    for i in range(16):
        b.append(mj_tile_back_side(36, 88 + i * 18))
        b.append(mj_tile_back_side(738, 88 + i * 18))
    b += [r(300, 150, 200, 150, "#064e3b", 14, 'stroke="#fbbf24" stroke-opacity="0.5" stroke-width="2"'), c(400, 225, 38, "#022c22", f'stroke="{GOLD}" stroke-width="2"'),
          t(400, 234, "東", 26, GOLD, 900, "middle"), t(400, 176, "西", 12, "#a7f3d0", 700, "middle"), t(400, 284, "東", 12, GOLD, 900, "middle"),
          t(326, 230, "北", 12, "#a7f3d0", 700, "middle"), t(474, 230, "南", 12, "#a7f3d0", 700, "middle"), t(430, 168, "剩 48 張", 10, "#a7f3d0", 700),
          t(312, 168, "東風東局", 10, "#a7f3d0", 700)]
    rnd = random.Random(6)
    pool = [("m", n) for n in range(1, 10)] + [("p", n) for n in range(1, 10)] + [("s", n) for n in range(1, 10)] + [("z", z) for z in "南西北白發"]
    for i in range(10):
        b.append(mj_tile(310 + (i % 8) * 23, 308 + (i // 8) * 32, rnd.choice(pool), 22, 30))
    for i in range(9):
        b.append(mj_tile(310 + (i % 8) * 23, 112 - (i // 8) * 32, rnd.choice(pool), 22, 30, 180))
    for i in range(8):
        b.append(mj_tile(244 - (i // 6) * 32, 152 + (i % 6) * 23, rnd.choice(pool), 22, 30, 90))
        b.append(mj_tile(534 + (i // 6) * 32, 152 + (i % 6) * 23, rnd.choice(pool), 22, 30, -90))
    last = (334 + 1 * 23, 340)
    b.append(path(f"M{last[0] + 11} {last[1] + 8} l-6 -8 h12z", GOLD))
    b += [mj_player(130, 64, "阿明", "西", "48,200", "#2563eb"), mj_player(610, 64, "老王", "南", "49,600", "#7c3aed"),
          mj_player(96, 420 - 50, "小美", "北", "49,400", "#db2777")]
    hand_x = 92
    for i, face in enumerate(WIN_HAND):
        b.append(mj_tile(hand_x + i * 37, 424, face, 36, 50))
    b += [mj_tile(hand_x + 16 * 37 + 14, 424, ("p", 6), 36, 50, lift=14, glow=True), c(56, 450, 22, "#f97316", f'stroke="{GOLD}" stroke-width="3"'),
          t(56, 456, "你", 15, "#fff", 900, "middle"), pill(32, 476, "莊 · 52,800", "#000000", GOLD, 9),
          c(744, 318, 20, "#000", 'opacity="0.4"'), t(744, 324, "08", 15, "#fff", 900, "middle", True),
          f'<g filter="url(#glow)">{c(628, 372, 34, GOLD)}</g>', c(628, 372, 30, "#f59e0b", f'stroke="#fff" stroke-width="3"'), t(628, 383, "胡", 28, "#7c2d12", 900, "middle"),
          c(690, 380, 22, "#475569", 'stroke="#fff" stroke-width="2"'), t(690, 387, "過", 17, "#fff", 900, "middle"),
          outline_text(560, 392, "自摸！", 18, "#fde047", "#7c2d12", 5)]
    return svg("".join(b), defs)


def scene_mj_win():
    defs, b = felt_bg()
    defs += rad_grad("burst", "#fde68a", "#f59e0b", 0.9, 0)
    b += [r(0, 0, 800, 500, "#000", 0, 'opacity="0.55"'), c(400, 70, 160, "url(#burst)")]
    for k in range(16):
        a = k / 16 * math.tau
        b.append(ln(400, 70, round(400 + math.cos(a) * 190, 1), round(70 + math.sin(a) * 120, 1), "#fde68a", 3, 'opacity="0.35"'))
    b += [outline_text(400, 96, "自 摸", 60, "#fde047", "#7c2d12", 12), shadow(r(70, 120, 660, 360, "#3f0d0d", 18)),
          r(70, 120, 660, 360, "none", 18, f'stroke="{GOLD}" stroke-width="3"')]
    for i, face in enumerate(WIN_HAND + [("p", 6)]):
        extra = sum(8 for k in (3, 6, 9, 12, 15) if i >= k)
        b.append(mj_tile(92 + i * 33 + extra, 140, face, 31, 42, glow=(i == 16)))
    b += [t(96, 220, "台數明細", 15, GOLD, 900), ln(96, 230, 410, 230, "#7f1d1d", 2)]
    fan = [("莊家", 1), ("自摸", 1), ("門清", 1), ("東風刻（圈風 + 門風）", 2), ("三暗刻", 2), ("連莊 1 · 拉莊", 2)]
    for i, (k, v) in enumerate(fan):
        y = 254 + i * 28
        b += [t(96, y, k, 13.5, "#fde68a"), t(406, y, f"{v} 台", 13.5, "#fff", 900, "end")]
    b += [ln(96, 422, 410, 422, "#7f1d1d", 2), t(96, 450, "合計", 16, GOLD, 900), outline_text(406, 452, "9 台", 26, "#fde047", "#7c2d12", 5, "end")]
    players = [("你", "莊家 · 自摸", "+5,400", "#f97316", True), ("阿明", "西", "-1,800", "#2563eb", False), ("老王", "南", "-1,800", "#7c3aed", False),
               ("小美", "北", "-1,800", "#db2777", False)]
    for i, (name, role, delta, col, me) in enumerate(players):
        y = 236 + i * 46
        if me:
            b.append(r(436, y - 18, 274, 40, GOLD, 10, 'opacity="0.15"'))
        b += [c(460, y + 2, 15, col, f'stroke="{GOLD}" stroke-width="2"'), t(460, y + 7, name[0], 13, "#fff", 900, "middle"), t(484, y, name, 13, "#fff", 900),
              t(484, y + 16, role, 10.5, "#fca5a5"), t(700, y + 8, delta, 17, "#fde047" if me else "#94a3b8", 900, "end", True)]
    b += [btn(452, 424, 120, 36, "分享戰績", "#7f1d1d", "#fde68a", 13, 18), btn(586, 424, 124, 36, "下一局 ▶", GOLD, MJ_DARK, 14, 18)]
    return svg("".join(b), defs)


def scene_mj_room():
    defs = diag_grad("lob", "#450a0a", "#991b1b")
    b = [r(0, 0, 800, 500, "url(#lob)"), outline_text(400, 50, "建立好友房", 28, GOLD, MJ_DARK, 7), shadow(r(30, 72, 470, 408, "#2a0a0a", 16)),
         r(30, 72, 470, 408, "none", 16, f'stroke="{GOLD}" stroke-opacity="0.6" stroke-width="2"')]

    def options(y, label, opts, sel):
        out = [t(54, y + 18, label, 13, "#fde68a", 700)]
        for i, s in enumerate(opts):
            x = 150 + i * 112
            out.append(btn(x, y, 102, 28, s, GOLD if i == sel else "#4a1010", MJ_DARK if i == sel else "#fca5a5", 12, 14))
        return "".join(out)

    b += [options(92, "局數", ["1 圈", "4 圈", "8 圈"], 1), options(134, "底 / 台", ["100 / 20", "300 / 100", "500 / 200"], 1),
          options(176, "思考時間", ["10 秒", "15 秒", "20 秒"], 1), t(54, 238, "規則設定", 13, "#fde68a", 700)]
    rules = [("花牌", True), ("吃牌", True), ("搶槓胡", True), ("連莊拉莊", True), ("一炮多響", False), ("相公", True)]
    for i, (s, on) in enumerate(rules):
        x, y = 150 + (i % 2) * 168, 228 + (i // 2) * 36
        b += [t(x, y + 14, s, 12.5, "#fff"), toggle(x + 96, y + 1, on, "#f59e0b")]
    b += [field(54, 352, 210, "房間密碼（選填）", "••••", 32, True), t(290, 360, "觀戰", 11, "#94a3b8", 700), toggle(290, 372, False, "#f59e0b"),
          t(54, 424, "建立房間需消耗 房卡 × 1（剩餘 12 張）", 11, "#fca5a5"), btn(300, 432, 180, 36, "建立房間", GOLD, MJ_DARK, 15, 18),
          shadow(r(520, 72, 250, 408, "#2a0a0a", 16)), r(520, 72, 250, 408, "none", 16, f'stroke="{GOLD}" stroke-opacity="0.6" stroke-width="2"'),
          t(645, 104, "房號", 12, "#fca5a5", 700, "middle"), outline_text(645, 140, "482 913", 32, GOLD, MJ_DARK, 5, mono=True),
          t(645, 164, "4 圈 · 300/100 · 15 秒", 11, "#fde68a", 400, "middle")]
    seats = [("東", "你（房主）", "#f97316"), ("南", "阿明", "#2563eb"), ("西", "等待加入…", None), ("北", "等待加入…", None)]
    for i, (wind, name, col) in enumerate(seats):
        y = 184 + i * 54
        b += [r(540, y, 210, 44, "#4a1010", 10), t(560, y + 28, wind, 16, GOLD, 900, "middle")]
        if col:
            b += [c(600, y + 22, 14, col), t(600, y + 27, name[0], 11, "#fff", 900, "middle"), t(622, y + 27, name, 12.5, "#fff", 700)]
        else:
            b += [c(600, y + 22, 14, "none", 'stroke="#fca5a5" stroke-dasharray="3 3"'), t(622, y + 27, name, 12, "#fca5a5")]
    b += [btn(540, 412, 210, 36, "邀請 LINE 好友", "#06c755", "#fff", 13, 18), t(645, 466, "或分享房號給朋友", 10.5, "#fca5a5", 400, "middle")]
    return svg("".join(b), defs)


def scene_mj_profile():
    defs = diag_grad("lob", "#1c0a0a", "#450a0a")
    b = [r(0, 0, 800, 500, "url(#lob)"), shadow(r(24, 24, 300, 452, "#2a0a0a", 16)), r(24, 24, 300, 452, "none", 16, f'stroke="{GOLD}" stroke-opacity="0.5"'),
         portrait(174, 108, 0.95, "#f6d2b3", "#1f2937", "#b91c1c", 0, GOLD), t(174, 196, "雀神小林", 20, "#fff", 900, "middle"),
         pill(132, 206, "雀聖 III ★★☆", GOLD, MJ_DARK, 11), progress(64, 240, 220, 8, 0.66, GOLD, "#4a1010"), t(174, 264, "升段還差 340 分", 10.5, "#fca5a5", 400, "middle")]
    stats = [("總場次", "1,286"), ("胡牌率", "31.4%"), ("自摸率", "12.8%"), ("放槍率", "9.6%"), ("最大台數", "18 台"), ("最長連莊", "7 次")]
    for i, (k, v) in enumerate(stats):
        x, y = 48 + (i % 2) * 140, 296 + (i // 2) * 48
        b += [r(x, y, 130, 40, "#4a1010", 8), t(x + 10, y + 16, k, 10.5, "#fca5a5"), t(x + 120, y + 32, v, 15, "#fff", 900, "end")]
    b += [t(48, 460, "近 10 場", 10.5, "#fca5a5", 700)]
    for i, res in enumerate("WLWWLWLWWW"):
        b.append(c(110 + i * 20, 456, 7, GOLD if res == "W" else "#64748b"))
    b += [shadow(r(340, 24, 436, 452, "#2a0a0a", 16)), r(340, 24, 436, 452, "none", 16, f'stroke="{GOLD}" stroke-opacity="0.5"'),
          t(364, 60, "本週排行榜", 18, GOLD, 900)]
    for i, s in enumerate(["積分", "胡牌數", "最大台數"]):
        b.append(btn(560 + i * 70, 42, 64, 24, s, GOLD if i == 0 else "#4a1010", MJ_DARK if i == 0 else "#fca5a5", 11, 12))
    board = [("牌桌之王", "雀神 I", 98420), ("東風不敗", "雀神 II", 91380), ("清一色控", "雀神 III", 87250), ("小八", "雀聖 I", 80110),
             ("雀神小林", "雀聖 III", 76540), ("阿明", "雀聖 III", 74300), ("老王", "雀豪 I", 70980), ("胡很大", "雀豪 I", 69020)]
    cols = ["#f97316", "#2563eb", "#7c3aed", "#db2777", "#0d9488", "#ca8a04"]
    for i, (name, rank, pts) in enumerate(board):
        y = 100 + i * 46
        me = name == "雀神小林"
        b.append(r(356, y - 4, 404, 40, GOLD if me else "#4a1010", 10, f'opacity="{0.25 if me else 1}"'))
        medal = [GOLD, "#e5e7eb", "#d97706"][i] if i < 3 else "#7f1d1d"
        b += [c(382, y + 16, 13, medal), t(382, y + 21, i + 1, 12, MJ_DARK if i < 3 else "#fff", 900, "middle"), c(418, y + 16, 14, cols[i % len(cols)]),
              t(418, y + 21, name[0], 11, "#fff", 900, "middle"), t(442, y + 13, name, 13, "#fff", 900), t(442, y + 29, rank, 10, "#fca5a5"),
              t(744, y + 22, f"{pts:,}", 15, GOLD, 900, "end", True)]
    return svg("".join(b), defs)


# ================= 卡牌對戰：幻境對決 =================
RARITY = {"common": "#9ca3af", "rare": "#3b82f6", "epic": "#a855f7", "legend": "#f59e0b"}
ART = {
    "flame": "M50 20 q22 22 10 44 q-4 -14 -12 -16 q4 12 -8 22 q-14 -10 -6 -28 q4 -12 16 -22z",
    "shield": "M50 18 l22 8 v18 q0 18 -22 28 q-22 -10 -22 -28 v-18z",
    "leaf": "M30 66 q0 -40 44 -46 q2 44 -44 46z",
    "skull": "M34 40 a16 16 0 0 1 32 0 v10 h-6 v8 h-20 v-8 h-6z",
    "star": "M50 16 l8 18 l20 2 l-15 13 l5 19 l-18 -10 l-18 10 l5 -19 l-15 -13 l20 -2z",
    "wave": "M22 52 q14 -20 28 0 q14 20 28 0 v14 h-56z",
    "dragon": "M24 62 q8 -34 34 -40 l-4 10 l16 -4 l-6 12 q14 4 12 22 q-14 -10 -26 -2 q-10 8 -26 2z",
    "sword": "M47 16 h6 v34 h10 v5 h-10 v10 h-6 v-10 h-10 v-5 h10z",
}


def tcg_card(x, y, s=1.0, name="", cost=3, atk=None, hp=None, color="#7c3aed", rarity="common", art="star", rot=0, glow=False):
    """集換式卡牌（原始尺寸 100×140），(x, y) 為左上角。"""
    rc = RARITY[rarity]
    body = [r(0, 0, 100, 140, rc, 10), r(4, 4, 92, 132, "#1c1917", 8), r(8, 10, 84, 64, color, 6),
            path(ART[art], "#ffffff", 'opacity="0.85"'), r(6, 76, 88, 18, "#44403c", 4, f'stroke="{rc}"'),
            t(50, 89, name, 9.5, "#fff", 700, "middle"), r(16, 102, 68, 3.5, "#57534e", 2), r(16, 110, 52, 3.5, "#57534e", 2),
            c(12, 12, 12, "#2563eb", 'stroke="#fff" stroke-width="2"'), t(12, 17, cost, 13, "#fff", 900, "middle")]
    if atk is not None:
        body += [c(12, 128, 12, "#f59e0b", 'stroke="#fff" stroke-width="2"'), t(12, 133, atk, 13, "#fff", 900, "middle"),
                 c(88, 128, 12, "#dc2626", 'stroke="#fff" stroke-width="2"'), t(88, 133, hp, 13, "#fff", 900, "middle")]
    if rarity in ("epic", "legend"):
        body.append(c(50, 96, 4, rc))
    tf = f"translate({x} {y}) scale({s})" + (f" rotate({rot} 50 140)" if rot else "")
    inner = "".join(body)
    if glow:
        halo = r(-4, -4, 108, 148, rc, 14, 'opacity="0.7"')
        inner = f'<g filter="url(#glow)">{halo}</g>' + inner
    return f'<g transform="{tf}">{inner}</g>'


def card_back(x, y, s=1.0, rot=0):
    tf = f"translate({x} {y}) scale({s})" + (f" rotate({rot} 50 140)" if rot else "")
    return (f'<g transform="{tf}">' + r(0, 0, 100, 140, "#1e1b4b", 10, 'stroke="#a78bfa" stroke-width="3"') + r(10, 10, 80, 120, "none", 6, 'stroke="#6d28d9" stroke-width="2"')
            + c(50, 70, 22, "#4c1d95", 'stroke="#c4b5fd" stroke-width="2"') + path("M50 54 l6 12 l12 4 l-12 4 l-6 12 l-6 -12 l-12 -4 l12 -4z", "#c4b5fd") + "</g>")


def fantasy_bg():
    defs = diag_grad("fbg", "#0c0a1d", "#3b0764") + rad_grad("rune", "#a855f7", "#3b0764", 0.55, 0)
    return defs, [r(0, 0, 800, 500, "url(#fbg)"), stars(77, 50, color="#e9d5ff")]


def minion(cx, cy, atk, hp, color, art, taunt=False, dmg=None):
    out = []
    if taunt:
        out.append(path(f"M{cx} {cy - 50} l36 12 v34 q0 30 -36 46 q-36 -16 -36 -46 v-34z", "#a8a29e", 'stroke="#57534e" stroke-width="3"'))
    out += [f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="38" fill="{color}" stroke="#fde68a" stroke-width="3"/>',
            f'<g transform="translate({cx - 30} {cy - 36}) scale(0.6)">{path(ART[art], "#fff", 'opacity="0.85"')}</g>',
            c(cx - 24, cy + 28, 12, "#f59e0b", 'stroke="#fff" stroke-width="2"'), t(cx - 24, cy + 33, atk, 13, "#fff", 900, "middle"),
            c(cx + 24, cy + 28, 12, "#dc2626", 'stroke="#fff" stroke-width="2"'), t(cx + 24, cy + 33, hp, 13, "#fff", 900, "middle")]
    if dmg:
        out.append(outline_text(cx, cy + 6, dmg, 24, "#fef08a", "#991b1b", 5))
    return "".join(out)


def scene_tcg_menu():
    defs, b = fantasy_bg()
    b += [c(250, 260, 210, "url(#rune)"), c(250, 260, 170, "none", 'stroke="#c4b5fd" stroke-width="2" stroke-dasharray="4 10" opacity="0.6"'),
          c(250, 260, 130, "none", 'stroke="#f0abfc" stroke-width="1.5" opacity="0.5"'),
          tcg_card(110, 150, 1.45, "暗影刺客", 3, 4, 2, "#4c1d95", "epic", "skull", -16),
          tcg_card(250, 140, 1.45, "聖光守衛", 4, 3, 6, "#ca8a04", "rare", "shield", 14),
          tcg_card(175, 110, 1.6, "遠古炎龍", 8, 8, 8, "#b91c1c", "legend", "dragon", 0, True),
          outline_text(600, 120, "幻境對決", 52, "#fde68a", "#3b0764", 10), outline_text(600, 154, "MYTHIC DUEL", 18, "#e9d5ff", "#3b0764", 5, mono=True)]
    for i, s in enumerate(["對戰", "冒險模式", "我的牌組", "卡包商店", "設定"]):
        y = 186 + i * 54
        on = i == 0
        b += [path(f"M490 {y} h220 l14 20 l-14 20 h-220 l-14 -20z", "#f59e0b" if on else "#2e1065", f'stroke="{"#fde68a" if on else "#7c3aed"}" stroke-width="2"'),
              t(600, y + 26, s, 16, "#3b0764" if on else "#e9d5ff", 900, "middle")]
    b += [c(496, 186 + 3 * 54 + 6, 8, "#ef4444"), t(496, 186 + 3 * 54 + 10, "2", 9, "#fff", 900, "middle"),
          t(24, 484, "伺服器：亞洲 · 線上 12,804 人", 10.5, "#c4b5fd"), t(776, 484, "v2.4.0", 10, "#a78bfa", 700, "end")]
    return svg("".join(b), defs)


def scene_tcg_battle():
    defs = lin_grad("board", "#78350f", "#451a03") + rad_grad("mid", "#d6b98c", "#a16207", 1, 1, "0.5", "0.5", "0.6")
    b = [r(0, 0, 800, 500, "url(#board)"), r(40, 60, 720, 380, "url(#mid)", 40, 'stroke="#422006" stroke-width="6"'),
         ln(70, 250, 730, 250, "#78350f", 2, 'opacity="0.5" stroke-dasharray="10 8"')]
    for i in range(5):
        b.append(card_back(290 + i * 46, -70, 0.7, (i - 2) * 6))
    b += [c(400, 108, 42, "#7f1d1d", 'stroke="#fde68a" stroke-width="4"'), portrait(400, 108, 0.62, "#e7c0a0", "#111827", "#7f1d1d", 2, "#a855f7"),
          c(436, 138, 14, "#dc2626", 'stroke="#fff" stroke-width="2"'), t(436, 143, "22", 13, "#fff", 900, "middle"), outline_text(470, 104, "-6", 26, "#fef08a", "#991b1b", 5),
          minion(250, 196, 3, 2, "#4c1d95", "skull"), minion(330, 196, 2, 5, "#57534e", "shield", True), minion(470, 196, 5, 4, "#065f46", "leaf"),
          minion(240, 304, 4, 3, "#b91c1c", "flame"), minion(320, 304, 8, 8, "#991b1b", "dragon"), minion(400, 304, 2, 2, "#1d4ed8", "wave"),
          minion(480, 304, 3, 6, "#ca8a04", "shield", True), minion(560, 304, 1, 1, "#7c3aed", "star"),
          path("M320 270 Q370 170 430 138", "none", 'stroke="#ef4444" stroke-width="7" stroke-dasharray="14 8" stroke-linecap="round"'),
          path("M436 132 l-20 -2 l10 16z", "#ef4444"), c(400, 392, 42, "#1e3a8a", 'stroke="#fde68a" stroke-width="4"'),
          portrait(400, 392, 0.62, "#f6d2b3", "#b45309", "#1e3a8a", 0, "#fbbf24"), c(436, 422, 14, "#dc2626", 'stroke="#fff" stroke-width="2"'),
          t(436, 427, "27", 13, "#fff", 900, "middle"), c(364, 422, 13, "#64748b", 'stroke="#fff" stroke-width="2"'), t(364, 427, "3", 12, "#fff", 900, "middle")]
    hand = [("火球術", 4, None, None, "#b91c1c", "rare", "flame"), ("森林守護者", 5, 4, 6, "#065f46", "common", "leaf"),
            ("寒冰箭", 2, None, None, "#1d4ed8", "common", "wave"), ("聖騎士", 6, 5, 5, "#ca8a04", "epic", "sword"),
            ("星辰法師", 3, 2, 4, "#6d28d9", "rare", "star")]
    for i, (name, cost, atk, hp, col, rar, art) in enumerate(hand):
        lift = 26 if i == 3 else 0
        b.append(tcg_card(230 + i * 62, 418 - lift, 0.78, name, cost, atk, hp, col, rar, art, (i - 2) * 7, glow=(i == 3)))
    b += [r(640, 226, 120, 48, "#ca8a04", 24, 'stroke="#fde68a" stroke-width="3"'), t(700, 256, "結束回合", 15, "#3b0764", 900, "middle"),
          t(640, 470, "法力", 11, "#fde68a", 700)]
    for i in range(10):
        full = i < 7
        x = 672 + (i % 5) * 20
        y = 458 + (i // 5) * 18
        b.append(path(f"M{x} {y - 8} l7 8 l-7 8 l-7 -8z", "#38bdf8" if full else ("#334155" if i < 8 else "none"), 'stroke="#bae6fd" stroke-width="1"' if i < 8 else ""))
    b += [t(776, 470, "7/8", 14, "#fff", 900, "end", True), r(640, 286, 120, 6, "#422006", 3), r(640, 286, 74, 6, "#f59e0b", 3), t(700, 306, "剩餘 42 秒", 10, "#fde68a", 700, "middle"),
          t(40, 40, "對手：暗夜術士", 12, "#fde68a", 900), t(40, 488, "牌庫 18", 11, "#fde68a", 700)]
    return svg("".join(b), defs)


def scene_tcg_deck():
    defs, b = fantasy_bg()
    b += [t(24, 40, "我的收藏", 20, "#fde68a", 900), r(140, 22, 180, 28, "#1e1b4b", 14, 'stroke="#6d28d9"'), t(156, 41, "搜尋卡牌…", 11.5, "#a78bfa")]
    fx = 332
    for i, (s, col) in enumerate([("火", "#ef4444"), ("水", "#3b82f6"), ("自然", "#22c55e"), ("暗", "#a855f7"), ("光", "#f59e0b")]):
        w = 26 if len(s) == 1 else 40
        b.append(btn(fx, 24, w, 24, s, col if i == 0 else "#1e1b4b", "#fff", 11, 12))
        fx += w + 6
    for k in range(8):
        on = k == 4
        b += [c(36 + k * 30, 70, 12, "#2563eb" if on else "#1e1b4b", 'stroke="#60a5fa"'), t(36 + k * 30, 75, "7+" if k == 7 else k, 11, "#fff", 900, "middle")]
    coll = [("遠古炎龍", 8, 8, 8, "#b91c1c", "legend", "dragon"), ("火焰元素", 4, 5, 3, "#c2410c", "common", "flame"), ("熔岩巨人", 7, 6, 8, "#7f1d1d", "epic", "shield"),
            ("烈焰射手", 2, 3, 1, "#dc2626", "common", "flame"), ("火球術", 4, None, None, "#b91c1c", "rare", "flame"), ("燃燒之劍", 3, None, None, "#9a3412", "rare", "sword"),
            ("鳳凰", 6, 5, 4, "#ea580c", "epic", "star"), ("龍之怒吼", 5, None, None, "#991b1b", "rare", "dragon")]
    for i, (name, cost, atk, hp, col, rar, art) in enumerate(coll):
        x, y = 24 + (i % 4) * 116, 96 + (i // 4) * 196
        b.append(tcg_card(x, y, 1.05, name, cost, atk, hp, col, rar, art))
        b += [r(x + 30, y + 154, 46, 18, "#1e1b4b", 9), t(x + 53, y + 167, "× 2" if rar != "legend" else "× 1", 10.5, "#e9d5ff", 700, "middle")]
    b += [shadow(r(500, 16, 280, 468, "#1e1b4b", 14)), r(500, 16, 280, 468, "none", 14, 'stroke="#7c3aed"'), t(516, 44, "烈焰龍族", 16, "#fde68a", 900),
          t(764, 44, "30 / 30", 13, "#22c55e", 900, "end", True)]
    deck = [(1, "火花", 2, "common"), (2, "烈焰射手", 2, "common"), (2, "灼熱之觸", 2, "common"), (3, "燃燒之劍", 2, "rare"), (3, "幼龍", 2, "common"),
            (4, "火焰元素", 2, "common"), (4, "火球術", 2, "rare"), (5, "龍之怒吼", 2, "rare"), (6, "鳳凰", 1, "epic"), (7, "熔岩巨人", 1, "epic"),
            (8, "遠古炎龍", 1, "legend")]
    for i, (cost, name, n, rar) in enumerate(deck):
        y = 58 + i * 26
        b += [r(512, y, 256, 22, "#2e1065", 4), r(512, y, 4, 22, RARITY[rar], 2), c(530, y + 11, 9, "#2563eb"), t(530, y + 15, cost, 10, "#fff", 900, "middle"),
              t(546, y + 15, name, 11.5, "#fff", 700), t(758, y + 15, f"× {n}", 10.5, RARITY[rar], 900, "end")]
    b += [t(516, 362, "法力曲線", 12, "#e9d5ff", 700), bar_chart(516, 372, 248, 70, [2, 6, 4, 4, 2, 1, 1, 1], "#7c3aed", 0.3)]
    for k in range(8):
        b.append(t(round(516 + k * 31 + 15.5, 1), 456, "7+" if k == 7 else k + 1, 10, "#a78bfa", 700, "middle"))
    b.append(btn(516, 462, 248, 18, "儲存牌組", "#22c55e", size=11, rx=9))
    return svg("".join(b), defs)


def scene_tcg_pack():
    defs, b = fantasy_bg()
    defs += rad_grad("ray", "#fde68a", "#f59e0b", 0.85, 0)
    b += [c(400, 250, 260, "url(#ray)")]
    for k in range(18):
        a = k / 18 * math.tau
        b.append(path(f"M400 250 L{400 + math.cos(a) * 420:.0f} {250 + math.sin(a) * 420:.0f} L{400 + math.cos(a + 0.08) * 420:.0f} {250 + math.sin(a + 0.08) * 420:.0f}Z",
                      "#fde68a", 'opacity="0.12"'))
    cards = [(80, 150, -14, ("寒冰箭", 2, None, None, "#1d4ed8", "common", "wave")), (200, 120, -7, ("森林守護者", 5, 4, 6, "#065f46", "rare", "leaf")),
             (316, 70, 0, ("遠古炎龍", 8, 8, 8, "#b91c1c", "legend", "dragon")), (470, 120, 7, ("暗影刺客", 3, 4, 2, "#4c1d95", "epic", "skull")),
             (590, 150, 14, ("星辰法師", 3, 2, 4, "#6d28d9", "common", "star"))]
    for x, y, rot, (name, cost, atk, hp, col, rar, art) in cards:
        s = 1.7 if rar == "legend" else 1.3
        b.append(tcg_card(x, y, s, name, cost, atk, hp, col, rar, art, rot, glow=rar in ("legend", "epic")))
    b += [outline_text(400, 50, "傳 說 卡 牌 ！", 34, "#fde047", "#7c2d12", 8), t(400, 430, "遠古炎龍 · 戰吼：對所有敵人造成 3 點傷害", 14, "#fde68a", 700, "middle"),
          btn(290, 448, 220, 36, "再開一包（剩 3 包）", "#f59e0b", "#3b0764", 14, 18), t(776, 484, "點擊卡片查看詳情", 10.5, "#c4b5fd", 400, "end")]
    return svg("".join(b), defs)


def scene_tcg_heroes():
    defs, b = fantasy_bg()
    b += [outline_text(400, 54, "選擇你的英雄", 30, "#fde68a", "#3b0764", 7)]
    heroes = [("烈焰法師", "火球術：造成 2 點傷害", "#b91c1c", "#f6d2b3", "#7f1d1d", 3), ("聖光騎士", "聖盾：獲得 2 點護甲", "#ca8a04", "#f6d2b3", "#b45309", 0),
              ("暗影刺客", "淬毒：武器 +1 攻擊", "#4c1d95", "#e7c0a0", "#111827", 2), ("自然德魯伊", "變形：+1 攻擊與 +1 護甲", "#065f46", "#f1c9a5", "#365314", 1)]
    for i, (name, power, col, skin, hair, style) in enumerate(heroes):
        x = 32 + i * 188
        sel = i == 1
        gid = f"h{i}"
        defs += lin_grad(gid, col, "#0c0a1d")
        b += [r(x, 82, 172, 336, f"url(#{gid})", 16, f'stroke="{"#fde68a" if sel else "#6d28d9"}" stroke-width="{4 if sel else 2}"'),
              c(x + 86, 186, 66, "#000", 'opacity="0.25"'), portrait(x + 86, 180, 1.15, skin, hair, col, style, "#fde68a"),
              r(x + 12, 276, 148, 30, "#000", 8, 'opacity="0.35"'), t(x + 86, 297, name, 17, "#fff", 900, "middle"),
              t(x + 86, 330, "英雄技能", 10.5, "#fde68a", 700, "middle"), t(x + 86, 350, power, 11, "#f5f3ff", 400, "middle")]
        for k, (lab, v) in enumerate(zip(["攻擊", "防禦", "難度"], [(0.9, 0.4, 0.6), (0.6, 0.9, 0.3), (0.8, 0.3, 0.9), (0.6, 0.7, 0.5)][i])):
            yy = 368 + k * 16
            b += [t(x + 18, yy + 7, lab, 9.5, "#e9d5ff", 700), progress(x + 50, yy, 104, 7, v, "#fde68a" if sel else "#a78bfa", "#1e1b4b")]
        if sel:
            frame = r(x, 82, 172, 336, "none", 16, 'stroke="#fde68a" stroke-width="2"')
            b.append(f'<g filter="url(#glow)">{frame}</g>')
    b += [btn(300, 438, 200, 40, "確認選擇", "#f59e0b", "#3b0764", 16, 20)]
    return svg("".join(b), defs)


# ================= 戰棋：鐵血戰紀 =================
TILE = 50
TERRAIN_MAP = [
    "GGGFFGGGRGGMMMCC",
    "GFFFGGGGRGGMMGCC",
    "GGFGGWWGRRGGGGGG",
    "GGGGWWGGGRGGFFGG",
    "VVGWWGGFGRRGFFGG",
    "VVGWGGFFGGRGGGMM",
    "GGGWGGGFGGRRGGMM",
    "GGWWGGGGGGGRGFFG",
    "GWWGGFFGGGGRGGFG",
    "WWGGGFGGGGGRRGGG",
]
TERRAIN_INFO = {"G": ("草原", "#7cb05a"), "F": ("森林", "#5f9147"), "M": ("山地", "#9ca3af"), "W": ("河流", "#3b82f6"),
                "R": ("道路", "#d6b98c"), "C": ("城堡", "#78716c"), "V": ("村莊", "#c9a46b")}


def terrain_tile(col, row, kind, seed):
    x, y = col * TILE, row * TILE
    base = TERRAIN_INFO[kind][1]
    out = [r(x, y, TILE, TILE, base), r(x, y, TILE, TILE, "none", 0, 'stroke="#000" stroke-opacity="0.08"')]
    if kind == "F":
        out += [path(f"M{x + 10} {y + 34} l10 -22 l10 22z", "#2f5d2a"), path(f"M{x + 24} {y + 42} l11 -24 l11 24z", "#3b6e33")]
    elif kind == "M":
        out += [path(f"M{x + 4} {y + 44} l20 -34 l20 34z", "#6b7280"), path(f"M{x + 18} {y + 20} l6 -10 l6 10 l-6 -2z", "#f3f4f6")]
    elif kind == "W":
        out += [path(f"M{x + 6} {y + 18} q8 -6 16 0 q8 6 16 0", "none", 'stroke="#bfdbfe" stroke-width="2"'),
                path(f"M{x + 12} {y + 34} q8 -6 16 0 q8 6 16 0", "none", 'stroke="#bfdbfe" stroke-width="2"')]
    elif kind == "C":
        out += [r(x + 6, y + 14, 38, 32, "#57534e", 2), r(x + 6, y + 8, 8, 8, "#57534e"), r(x + 21, y + 8, 8, 8, "#57534e"), r(x + 36, y + 8, 8, 8, "#57534e"),
                r(x + 20, y + 30, 10, 16, "#292524", 4)]
    elif kind == "V":
        out += [r(x + 12, y + 24, 26, 18, "#fef3c7"), path(f"M{x + 8} {y + 26} l17 -14 l17 14z", "#b91c1c"), r(x + 22, y + 32, 6, 10, "#78350f")]
    elif kind == "G" and seed % 3 == 0:
        out.append(path(f"M{x + 14} {y + 30} l2 -6 l2 6 M{x + 32} {y + 20} l2 -6 l2 6", "none", 'stroke="#5c8f3e" stroke-width="1.5"'))
    return "".join(out)


def unit(col, row, letter, team, hp=1.0, done=False):
    cx, cy = col * TILE + 25, row * TILE + 23
    fill = "#2563eb" if team == "blue" else ("#dc2626" if team == "red" else "#a16207")
    out = [f'<ellipse cx="{cx}" cy="{cy + 20}" rx="16" ry="5" fill="#000" opacity="0.25"/>',
           c(cx, cy, 17, fill, f'stroke="#fff" stroke-width="2.5" opacity="{0.55 if done else 1}"'), t(cx, cy + 6, letter, 15, "#fff", 900, "middle"),
           r(cx - 15, cy + 20, 30, 4, "#111827", 2), r(cx - 15, cy + 20, round(30 * hp, 1), 4, "#22c55e" if hp > 0.5 else "#f59e0b", 2)]
    return "".join(out)


def scene_tactics_title():
    defs = lin_grad("night", "#0f172a", "#7c2d12") + rad_grad("moon", "#fef3c7", "#fef3c7", 0.9, 0)
    b = [r(0, 0, 800, 500, "url(#night)"), stars(88, 90), c(620, 110, 90, "url(#moon)"), c(620, 110, 46, "#fef3c7"),
         path("M0 400 L80 400 L80 330 L100 330 L100 300 L120 330 L140 330 L140 280 L160 260 L180 280 L180 330 L240 330 L240 360 L300 360 L300 300 "
              "L320 270 L340 300 L340 360 L420 360 L420 320 L460 320 L460 380 L560 380 L560 340 L600 300 L640 340 L640 390 L800 390 L800 500 L0 500 Z", "#0b0f1a"),
         path("M0 460 Q200 420 400 450 T800 440 V500 H0Z", "#020617")]
    for x in (160, 320, 600):
        b += [ln(x, 260 if x == 160 else (270 if x == 320 else 300), x, 220 if x == 160 else (230 if x == 320 else 262), "#0b0f1a", 3),
              path(f"M{x} {220 if x == 160 else (230 if x == 320 else 262)} l22 8 l-22 8z", "#991b1b")]
    b += [ln(330, 60, 470, 200, "#cbd5e1", 8, 'stroke-linecap="round"'), ln(470, 60, 330, 200, "#cbd5e1", 8, 'stroke-linecap="round"'),
          r(320, 52, 24, 10, "#a16207", 3, 'transform="rotate(45 332 57)"'), r(456, 52, 24, 10, "#a16207", 3, 'transform="rotate(-45 468 57)"'),
          outline_text(400, 168, "鐵血戰紀", 64, "#e5e7eb", "#450a0a", 10), outline_text(400, 202, "IRON  CHRONICLE", 18, "#fca5a5", "#1c1917", 5, mono=True)]
    for i, s in enumerate(["新的旅程", "繼續遊戲", "讀取紀錄", "設定"]):
        y = 250 + i * 40
        on = i == 1
        b += [r(310, y, 180, 30, "#7f1d1d" if on else "#000", 4, f'opacity="{0.9 if on else 0.4}" stroke="#fca5a5" stroke-opacity="{0.9 if on else 0.3}"'),
              t(400, y + 21, s, 14, "#fef2f2" if on else "#e5e7eb", 900 if on else 500, "middle")]
        if on:
            b.append(t(296, y + 21, "▶", 12, "#fca5a5", 900, "middle"))
    b += [t(400, 486, "第 4 章 · 北境要塞　遊戲時間 12:48", 11, "#94a3b8", 400, "middle")]
    return svg("".join(b), defs)


def scene_tactics_map():
    b = []
    for row, line in enumerate(TERRAIN_MAP):
        for col, kind in enumerate(line):
            b.append(terrain_tile(col, row, kind, row * 16 + col))
    sel = (5, 6)
    for row, line in enumerate(TERRAIN_MAP):
        for col, kind in enumerate(line):
            d = abs(col - sel[0]) + abs(row - sel[1])
            if kind in "WM":
                continue
            if 0 < d <= 3:
                b.append(r(col * TILE + 3, row * TILE + 3, TILE - 6, TILE - 6, "#93c5fd", 4, 'opacity="0.55" stroke="#eff6ff" stroke-width="2"'))
            elif d == 4:
                b.append(r(col * TILE + 3, row * TILE + 3, TILE - 6, TILE - 6, "#fca5a5", 4, 'opacity="0.55" stroke="#fef2f2" stroke-width="2"'))
    b += [path("M275 325 H325 V275 H425", "none", 'stroke="#fef08a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"'),
          path("M420 263 l18 12 l-18 12z", "#fef08a"), r(452, 252, 46, 46, "none", 4, 'stroke="#fff" stroke-width="3"')]
    blues = [(5, 6, "劍", 0.84), (3, 7, "槍", 1.0), (6, 8, "弓", 0.7), (2, 5, "法", 1.0), (7, 7, "騎", 0.6, True)]
    reds = [(9, 5, "斧", 0.5), (10, 3, "弓", 1.0), (11, 6, "槍", 0.9), (13, 4, "法", 1.0), (14, 0, "將", 1.0)]
    for u in blues:
        b.append(unit(u[0], u[1], u[2], "blue", u[3], len(u) > 4))
    for u in reds:
        b.append(unit(u[0], u[1], u[2], "red", u[3]))
    b += [r(280, 8, 240, 34, "#0f172a", 17, 'opacity="0.85" stroke="#60a5fa"'), t(400, 30, "第 3 回合 · 我方行動", 14, "#bfdbfe", 900, "middle"),
          shadow(r(8, 8, 230, 84, "#0f172a", 10)), r(8, 8, 230, 84, "none", 10, 'stroke="#60a5fa"'), c(46, 50, 28, "#1e3a8a"),
          portrait(46, 46, 0.38, "#f6d2b3", "#b45309", "#1e40af", 0, "#fbbf24"), t(84, 32, "艾倫", 14, "#fff", 900), t(126, 32, "聖騎士 Lv.12", 10.5, "#93c5fd", 700),
          t(84, 54, "HP", 10.5, "#94a3b8", 700), progress(106, 46, 100, 8, 0.84, "#22c55e", "#1e293b"), t(230, 54, "32/38", 10, "#e2e8f0", 700, "end", True),
          t(84, 76, "移動 5　武器：銀之劍", 10.5, "#cbd5e1"), shadow(r(632, 404, 160, 88, "#0f172a", 10)), r(632, 404, 160, 88, "none", 10, 'stroke="#60a5fa"'),
          t(646, 428, "地形：森林", 12.5, "#fff", 900), t(646, 450, "防禦 +1　迴避 +20%", 11, "#86efac"), t(646, 470, "移動消耗 2", 11, "#cbd5e1"),
          r(8, 456, 270, 36, "#0f172a", 8, 'opacity="0.85"'), t(20, 479, "勝利條件：擊敗敵將「葛雷格」", 12, "#fde68a", 700)]
    return svg("".join(b))


def soldier(x, y, s, armor, weapon="sword", facing=1, helm="#9ca3af"):
    parts = [r(-14, 20, 10, 34, "#374151", 3), r(4, 20, 10, 34, "#374151", 3), r(-18, -18, 36, 42, armor, 8), r(-18, 4, 36, 8, "#78350f"),
             c(0, -34, 16, "#f1c9a5"), path("M-17 -36 q0 -22 17 -22 q17 0 17 22 h-6 v-6 h-22 v6z", helm), r(-6, -36, 4, 4, "#1f2937")]
    if weapon == "sword":
        parts += [r(14, -4, 10, 10, "#f1c9a5", 3), r(20, -70, 5, 70, "#e5e7eb", 2), r(12, -6, 21, 5, "#a16207", 2),
                  f'<ellipse cx="-22" cy="2" rx="12" ry="20" fill="#1d4ed8" stroke="#fbbf24" stroke-width="3"/>']
    else:
        parts += [r(14, -4, 10, 10, "#f1c9a5", 3), r(18, -60, 5, 72, "#78350f", 2), path("M23 -60 q24 6 18 30 q-12 -6 -18 -10z", "#d1d5db", 'stroke="#4b5563" stroke-width="2"')]
    tf = f"translate({x} {y}) scale({s * facing} {s})"
    return f'<g transform="{tf}">{"".join(parts)}</g>'


def scene_tactics_battle():
    defs = lin_grad("bsky", "#7dd3fc", "#e0f2fe")
    b = [r(0, 0, 800, 300, "url(#bsky)"), cloud_shape(150, 70), cloud_shape(600, 50), path("M0 220 Q200 150 400 210 T800 190 V300 H0Z", "#86c06c"),
         r(0, 250, 800, 50, "#6aa84f"), path("M560 210 l14 -40 l14 40z M600 214 l12 -34 l12 34z", "#2f5d2a"),
         soldier(250, 216, 1.5, "#2563eb", "sword", 1), soldier(560, 216, 1.5, "#991b1b", "axe", -1, "#57534e"),
         path("M450 120 q40 40 10 110", "none", 'stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.9"'),
         path("M440 130 q30 30 8 92", "none", 'stroke="#fde68a" stroke-width="4" stroke-linecap="round"'), outline_text(590, 120, "14", 40, "#fff", "#7f1d1d", 7),
         outline_text(590, 150, "必殺！", 16, "#fde047", "#7f1d1d", 4)]
    b += [r(0, 300, 800, 200, "#0f172a"), ln(400, 316, 400, 484, "#334155", 2)]

    def side(x0, name, cls, col, weapon, hp, hpmax, hp_after, stats, adv, anchor_right=False):
        out = [r(x0, 314, 380, 34, col, 6, 'opacity="0.9"'), t(x0 + 14, 337, name, 15, "#fff", 900), t(x0 + 366, 337, cls, 11.5, "#e2e8f0", 700, "end"),
               t(x0 + 14, 372, "HP", 11, "#94a3b8", 700), progress(x0 + 40, 364, 220, 10, hp_after / hpmax, "#22c55e" if hp_after / hpmax > 0.4 else "#ef4444", "#1e293b"),
               r(round(x0 + 40 + 220 * hp_after / hpmax, 1), 364, round(220 * (hp - hp_after) / hpmax, 1), 10, "#fca5a5", 0),
               t(x0 + 366, 373, f"{hp} → {hp_after}", 12, "#fff", 900, "end", True), t(x0 + 14, 402, "武器", 11, "#94a3b8", 700),
               t(x0 + 50, 402, weapon, 12, "#fde68a", 700), t(x0 + 160, 402, adv, 12, "#22c55e" if adv.startswith("▲") else "#ef4444", 900)]
        for i, (k, v) in enumerate(stats):
            x = x0 + 14 + i * 92
            out += [r(x, 416, 84, 54, "#1e293b", 8), t(x + 42, 436, k, 10.5, "#94a3b8", 700, "middle"), t(x + 42, 460, v, 17, "#fff", 900, "middle")]
        return "".join(out)

    b += [side(10, "艾倫", "聖騎士 Lv.12", "#1d4ed8", "銀之劍", 32, 38, 32, [("威力", "18"), ("命中", "85%"), ("必殺", "6%"), ("攻擊", "×2")], "▲ 劍剋斧"),
          side(410, "山賊頭目", "狂戰士 Lv.10", "#991b1b", "鐵斧", 40, 40, 12, [("威力", "9"), ("命中", "52%"), ("必殺", "2%"), ("攻擊", "×1")], "▼ 斧被劍剋")]
    return svg("".join(b), defs)


def cloud_shape(cx, cy):
    return (f'<g fill="#fff" opacity="0.9"><ellipse cx="{cx}" cy="{cy}" rx="44" ry="16"/><circle cx="{cx - 16}" cy="{cy - 10}" r="16"/>'
            f'<circle cx="{cx + 12}" cy="{cy - 14}" r="20"/></g>')


def radar(cx, cy, rad, values, labels, color):
    n = len(values)
    out = []
    for ring in (0.25, 0.5, 0.75, 1.0):
        pts = [(cx + math.cos(-math.pi / 2 + k * math.tau / n) * rad * ring, cy + math.sin(-math.pi / 2 + k * math.tau / n) * rad * ring) for k in range(n)]
        out.append(poly(pts, "none", 'stroke="#475569" stroke-width="1"'))
    for k in range(n):
        a = -math.pi / 2 + k * math.tau / n
        out.append(ln(cx, cy, round(cx + math.cos(a) * rad, 1), round(cy + math.sin(a) * rad, 1), "#475569"))
        out.append(t(round(cx + math.cos(a) * (rad + 18), 1), round(cy + math.sin(a) * (rad + 18) + 4, 1), labels[k], 11, "#cbd5e1", 700, "middle"))
    pts = [(cx + math.cos(-math.pi / 2 + k * math.tau / n) * rad * v, cy + math.sin(-math.pi / 2 + k * math.tau / n) * rad * v) for k, v in enumerate(values)]
    out.append(poly(pts, color, f'opacity="0.45" stroke="{color}" stroke-width="2"'))
    return "".join(out)


def scene_tactics_status():
    defs = lin_grad("st", "#0f172a", "#1e293b") + lin_grad("ban", "#1d4ed8", "#0f172a")
    b = [r(0, 0, 800, 500, "url(#st)"), r(20, 20, 250, 460, "url(#ban)", 14, 'stroke="#60a5fa"'), c(145, 150, 92, "#93c5fd", 'opacity="0.15"'),
         portrait(145, 150, 1.55, "#f6d2b3", "#b45309", "#1e40af", 0, "#fbbf24"), r(20, 280, 250, 200, "#0f172a", 0, 'opacity="0.55"'),
         t(40, 312, "艾倫", 26, "#fff", 900), t(112, 312, "聖騎士", 13, "#93c5fd", 700), t(40, 340, "Lv.12", 15, "#fde68a", 900, mono=True),
         t(250, 340, "EXP 68 / 100", 11, "#94a3b8", 400, "end", True), progress(40, 350, 210, 8, 0.68, "#fde68a", "#1e293b"),
         t(40, 384, "HP", 12, "#94a3b8", 700), t(250, 384, "32 / 38", 13, "#fff", 900, "end", True), progress(40, 392, 210, 8, 0.84, "#22c55e", "#1e293b"),
         t(40, 426, "「為了守護王國，", 12, "#e2e8f0"), t(40, 446, "　我的劍永不退縮。」", 12, "#e2e8f0"), t(40, 470, "出身：南方騎士團", 10.5, "#94a3b8"),
         r(286, 20, 250, 300, "#0f172a", 14, 'stroke="#334155"'), t(302, 46, "能力值", 14, "#fff", 900),
         radar(411, 178, 92, [0.72, 0.3, 0.66, 0.58, 0.45, 0.8, 0.4], ["力量", "魔力", "技巧", "速度", "幸運", "防禦", "魔防"], "#3b82f6")]
    b += [r(286, 332, 250, 148, "#0f172a", 14, 'stroke="#334155"'), t(302, 358, "技能", 14, "#fff", 900)]
    for i, (s, desc, col) in enumerate([("連續攻擊", "速度高時追擊", "#f59e0b"), ("護衛", "相鄰友軍防禦 +2", "#22c55e"), ("騎士之魂", "HP 低於 50% 時攻擊 +5", "#ef4444")]):
        y = 386 + i * 32
        b += [r(302, y - 16, 218, 26, "#1e293b", 6), c(316, y - 3, 7, col), t(330, y + 1, s, 12, "#fff", 900), t(512, y + 1, desc, 10, "#94a3b8", 400, "end")]
    b += [r(552, 20, 228, 460, "#0f172a", 14, 'stroke="#334155"'), t(568, 46, "裝備", 14, "#fff", 900)]
    equips = [("武器", "銀之劍", "威力 13　命中 80", "#e5e7eb"), ("副手", "騎士盾", "防禦 +3", "#3b82f6"), ("防具", "鋼鐵鎧甲", "防禦 +5　速度 -1", "#9ca3af"),
              ("飾品", "力量之戒", "力量 +2", "#f59e0b"), ("道具", "傷藥 × 3", "回復 HP 10", "#22c55e")]
    for i, (slot, name, desc, col) in enumerate(equips):
        y = 64 + i * 62
        b += [r(568, y, 196, 52, "#1e293b", 8), r(578, y + 8, 36, 36, "#0f172a", 6, f'stroke="{col}" stroke-width="2"'), c(596, y + 26, 8, col),
              t(624, y + 20, slot, 10, "#94a3b8", 700), t(624, y + 38, name, 13, "#fff", 900), t(756, y + 38, desc.split("　")[0], 9.5, "#93c5fd", 400, "end")]
    b += [t(568, 394, "轉職路線", 12, "#fde68a", 900)]
    for i, (s, done) in enumerate([("見習騎士", True), ("聖騎士", True), ("聖殿守護者", False)]):
        x = 568 + i * 70
        b += [r(x, 404, 62, 26, "#1d4ed8" if done else "#1e293b", 6, '' if done else 'stroke="#475569" stroke-dasharray="3 3"'),
              t(x + 31, 421, s, 9.5, "#fff" if done else "#94a3b8", 700, "middle")]
        if i < 2:
            b.append(t(x + 66, 421, "›", 12, "#94a3b8", 900, "middle"))
    b += [t(568, 456, "Lv.20 可轉職為上級職業", 10.5, "#94a3b8")]
    return svg("".join(b), defs)


def scene_tactics_story():
    defs = lin_grad("hall", "#451a03", "#1c0a03") + lin_grad("light", "#fef3c7", "#fef3c7", True, 0.55, 0)
    b = [r(0, 0, 800, 500, "url(#hall)")]
    for x in (120, 330, 470, 680):
        b += [r(x - 22, 40, 44, 320, "#78350f"), r(x - 28, 40, 56, 16, "#92400e"), r(x - 28, 344, 56, 16, "#92400e")]
    for x in (225, 575):
        b += [path(f"M{x - 40} 230 V110 a40 40 0 0 1 80 0 V230z", "#fde68a", 'opacity="0.75"'), path(f"M{x - 40} 230 L{x - 80} 360 H{x + 80} L{x + 40} 230z", "url(#light)")]
    b += [path("M340 360 L460 360 L560 500 L240 500Z", "#991b1b"), path("M352 360 L448 360 L530 500 L270 500Z", "none", 'stroke="#fbbf24" stroke-width="3"'),
          r(370, 200, 60, 90, "#a16207", 6), r(360, 186, 80, 22, "#ca8a04", 6), r(0, 0, 800, 500, "#000", 0, 'opacity="0.15"'),
          f'<g opacity="0.55">{portrait(170, 250, 2.3, "#f6d2b3", "#b45309", "#1e40af", 0, "#fbbf24")}</g>',
          portrait(630, 240, 2.4, "#fbe2cf", "#f8e7a8", "#9d174d", 1, "#fbbf24"),
          path("M606 140 l8 -18 l8 12 l8 -16 l8 16 l8 -12 l8 18z", "#fbbf24", 'transform="translate(-6 -14)"'),
          r(0, 0, 800, 36, "#000", 0, 'opacity="0.35"'), t(776, 24, "自動　快進　紀錄　選單", 11.5, "#e5e7eb", 700, "end"),
          shadow(r(30, 352, 740, 132, "#0b1120", 14)), r(30, 352, 740, 132, "none", 14, 'stroke="#fbbf24" stroke-width="2" stroke-opacity="0.7"'),
          r(52, 334, 120, 32, "#9d174d", 8, 'stroke="#fbbf24" stroke-width="2"'), t(112, 356, "莉雅公主", 15, "#fff", 900, "middle"),
          t(60, 400, "艾倫，北方的要塞已經失守了……", 17, "#f8fafc", 500), t(60, 432, "我們必須在敵軍抵達王都之前，找到傳說中的聖劍。", 17, "#f8fafc", 500),
          t(746, 468, "▼", 14, "#fbbf24", 900, "end")]
    for i, s in enumerate(["「交給我吧，公主。我一定會找到它。」", "「這太危險了，請讓我先派人偵查。」"]):
        y = 230 + i * 50
        on = i == 0
        b += [r(410, y, 360, 40, "#0b1120" if not on else "#1e3a8a", 8, f'opacity="0.92" stroke="{"#fbbf24" if on else "#475569"}" stroke-width="2"'),
              t(590, y + 26, s, 13, "#fff" if on else "#cbd5e1", 700 if on else 400, "middle")]
    return svg("".join(b), defs)


SCREENS = {
    "game-mahjong": [scene_mj_lobby, scene_mj_table, scene_mj_win, scene_mj_room, scene_mj_profile],
    "game-cardbattle": [scene_tcg_menu, scene_tcg_battle, scene_tcg_deck, scene_tcg_pack, scene_tcg_heroes],
    "game-tactics": [scene_tactics_title, scene_tactics_map, scene_tactics_battle, scene_tactics_status, scene_tactics_story],
}
