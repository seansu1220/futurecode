"""網頁設計類作品：咖啡廳官網、電商網站、營運後台的其他頁面。"""
import random

from .common import *  # noqa: F401,F403
from .web import product_art, scene_cafe, scene_dashboard, scene_shop

# ================= 咖啡廳官網 =================
CAFE_BROWN, CAFE_DARK, CAFE_MID = "#8b5e34", "#3b2412", "#7c5a3a"


def cafe_frame(active):
    b = [r(0, 36, 800, 464, "url(#bg)"), browser_bar("morningbrew.tw"), c(48, 67, 10, CAFE_BROWN), t(66, 73, "晨光咖啡", 18, CAFE_DARK, 900)]
    for i, s in enumerate(["菜單", "關於我們", "門市據點", "最新消息"]):
        x = 400 + i * 70
        b.append(t(x, 72, s, 13, CAFE_DARK if i == active else CAFE_MID, 700 if i == active else 500))
        if i == active:
            b.append(r(x, 80, tw(s, 13), 3, CAFE_BROWN, 1.5))
    b.append(btn(686, 54, 88, 28, "立即訂位", CAFE_BROWN))
    return diag_grad("bg", "#fdf6ec", "#f3e3cc"), b


def cafe_cup(cx, cy, s=1.0, fill="#fffaf3"):
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            + path("M-36 -20 L36 -20 Q34 16 20 26 L-20 26 Q-34 16 -36 -20Z", fill, 'stroke="#d9c2a3" stroke-width="2"')
            + path("M34 -10 q20 0 18 16 q-3 14 -22 15", "none", f'stroke="{fill}" stroke-width="6"')
            + '<ellipse cx="0" cy="-19" rx="36" ry="7" fill="#6f4518"/></g>')


def scene_cafe_menu():
    defs, b = cafe_frame(0)
    b += [t(40, 130, "菜單 MENU", 30, CAFE_DARK, 900), t(222, 130, "每日 10:00 – 20:00 供應", 12, "#b07a45", 700)]
    for i, s in enumerate(["咖啡", "茶飲", "甜點", "輕食"]):
        b.append(btn(40 + i * 84, 148, 74, 28, s, CAFE_BROWN) if i == 0 else outline_btn(40 + i * 84, 148, 74, 28, s, CAFE_MID))
    items = [("美式咖啡", "衣索比亞淺焙，果香明亮", "90", "#7a4a26"), ("拿鐵", "綿密奶泡 × 雙份濃縮", "120", "#c08552"),
             ("卡布奇諾", "經典義式比例", "120", "#a87444"), ("焦糖瑪奇朵", "自製焦糖醬", "140", "#d19a5b"),
             ("手沖單品", "每週更換產區豆", "160", "#5b3a1e"), ("冰滴咖啡", "12 小時低溫萃取", "150", "#3b2412")]
    for i, (name, desc, price, col) in enumerate(items):
        x, y = 40 + (i % 2) * 262, 192 + (i // 2) * 96
        b += [shadow(r(x, y, 250, 84, "#fff", 12)), c(x + 42, y + 42, 28, col), c(x + 42, y + 42, 18, "#f3e3cc", 'opacity="0.55"'),
              t(x + 84, y + 36, name, 14, CAFE_DARK, 700), t(x + 84, y + 58, desc, 11, "#9b7b5b"), t(x + 236, y + 36, "NT$ " + price, 13, "#b07a45", 900, "end")]
        if i == 1:
            b.append(pill(x + 130, y + 23, "人氣", "#ef4444", "#fff", 9))
    b += [shadow(r(580, 110, 190, 370, "#fff", 16)), r(580, 110, 190, 160, "#ecd3b0", 16), r(580, 250, 190, 20, "#ecd3b0"),
          cafe_cup(675, 196, 1.3), t(596, 296, "今日推薦", 11, "#b07a45", 700), t(596, 322, "秋季栗子拿鐵", 17, CAFE_DARK, 900),
          t(596, 346, "栗子泥 × 焦糖 × 濃縮咖啡", 11, "#9b7b5b"), t(596, 380, "NT$ 150", 22, CAFE_BROWN, 900),
          pill(694, 364, "限量 30 杯", "#fef3c7", "#b45309", 10), btn(596, 400, 158, 34, "加入訂單", CAFE_BROWN),
          t(675, 458, "* 可更換燕麥奶 +NT$20", 10, "#9b7b5b", 400, "middle")]
    return svg("".join(b), defs)


def scene_cafe_booking():
    defs, b = cafe_frame(-1)
    b += [t(40, 128, "線上訂位", 28, CAFE_DARK, 900), t(166, 128, "選擇日期與時段，即時確認座位", 12, "#9b7b5b"),
          shadow(r(40, 146, 440, 336, "#fff", 16)), t(60, 176, "選擇日期", 13, CAFE_DARK, 700), t(200, 176, "‹  2026 年 10 月  ›", 12, CAFE_MID, 700, "middle")]
    for i, d in enumerate("日一二三四五六"):
        b.append(t(78 + i * 36, 204, d, 11, "#9b7b5b", 700, "middle"))
    for day in range(1, 32):
        idx = day + 3
        x, y = 78 + (idx % 7) * 36, 228 + (idx // 7) * 26
        if day == 5:
            b.append(c(x, y - 4, 12, CAFE_BROWN))
        b.append(t(x, y, day, 11, "#fff" if day == 5 else ("#cbb79f" if day < 4 else CAFE_DARK), 700 if day == 5 else 400, "middle"))
    b.append(t(330, 176, "選擇時段", 13, CAFE_DARK, 700))
    for i, (slot, state) in enumerate([("11:00", 0), ("12:30", 0), ("14:00", 1), ("15:30", 0), ("17:00", 2), ("18:30", 0)]):
        y = 190 + i * 36
        if state == 1:
            b.append(btn(330, y, 130, 28, slot + "  ✓", CAFE_BROWN))
        elif state == 2:
            b.append(r(330, y, 130, 28, "#f5f0ea", 14) + t(395, y + 18, slot + "  已額滿", 11, "#cbb79f", 400, "middle"))
        else:
            b.append(outline_btn(330, y, 130, 28, slot, CAFE_MID, 11))
    b += [t(60, 412, "人數", 11, "#475569", 700), r(60, 420, 110, 30, "#fff", 6, 'stroke="#cbd5e1"'),
          t(76, 440, "－", 13, CAFE_MID, 700), t(115, 440, "2 位", 12, CAFE_DARK, 700, "middle"), t(154, 440, "＋", 13, CAFE_MID, 700),
          field(186, 412, 130, "姓名", "林小姐"), field(330, 412, 130, "電話", "0912-345-678")]
    b += [shadow(r(500, 146, 270, 336, "#fff", 16)), t(520, 178, "訂位資訊", 15, CAFE_DARK, 900)]
    for i, (k, v) in enumerate([("門市", "審計店"), ("日期", "10/05（一）"), ("時段", "14:00"), ("人數", "2 位"), ("座位", "靠窗雙人座")]):
        y = 212 + i * 32
        b += [t(520, y, k, 12, "#9b7b5b"), t(750, y, v, 13, CAFE_DARK, 700, "end"), ln(520, y + 12, 750, y + 12, "#f3e3cc")]
    b += [r(520, 372, 230, 30, "#fdf6ec", 8), t(635, 391, "座位將為您保留 15 分鐘", 11, "#b07a45", 700, "middle"),
          btn(520, 414, 230, 40, "確認訂位", CAFE_BROWN, size=14), t(635, 472, "確認後以簡訊與 LINE 通知", 10, "#9b7b5b", 400, "middle")]
    return svg("".join(b), defs)


def mini_map(x, y, w, h, seed):
    rnd = random.Random(seed)
    out = [r(x, y, w, h, "#e8efe0", 10)]
    for _ in range(5):
        out.append(r(x + rnd.randint(5, w - 50), y + rnd.randint(5, h - 30), rnd.randint(24, 46), rnd.randint(14, 24), "#d7e3c8", 3))
    out += [ln(x, y + h * 0.55, x + w, y + h * 0.4, "#fff", 7), ln(x + w * 0.35, y, x + w * 0.5, y + h, "#fff", 6),
            ln(x + w * 0.75, y, x + w * 0.7, y + h, "#fff", 4)]
    px, py = x + w * 0.5, y + h * 0.42
    out.append(path(f"M{px} {py+14} q-12 -14 -12 -22 a12 12 0 0 1 24 0 q0 8 -12 22z", "#ef4444") + c(px, py - 8, 4.5, "#fff"))
    return "".join(out)


def scene_cafe_about():
    defs, b = cafe_frame(2)
    defs += diag_grad("ban", "#5b3a1e", "#a8713f")
    b += [r(40, 98, 720, 150, "url(#ban)", 16), t(72, 158, "我們的故事", 28, "#fff", 900),
          t(72, 188, "從一台二手烘豆機開始，用一杯好咖啡連結人與城市。", 13, "#f3e3cc"),
          t(72, 210, "八年來，我們只做一件事：把每一顆豆子的風味，好好地交到你手上。", 13, "#f3e3cc")]
    rnd = random.Random(4)
    for _ in range(9):
        x, y = rnd.randint(580, 740), rnd.randint(112, 234)
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="8" fill="#3b2412" opacity="0.55" transform="rotate({rnd.randint(0, 180)} {x} {y})"/>')
    b += [t(40, 284, "門市據點", 18, CAFE_DARK, 900), t(128, 284, "共 3 間門市，歡迎來坐坐", 12, "#9b7b5b")]
    stores = [("審計店", "台中市西區民生路 368 巷", "10:00 – 20:00"), ("勤美店", "台中市西區公益路 68 號", "09:00 – 21:00"),
              ("逢甲店", "台中市西屯區文華路 100 號", "11:00 – 22:00")]
    for i, (name, addr, hours) in enumerate(stores):
        x = 40 + i * 245
        b += [shadow(r(x, 298, 230, 184, "#fff", 14)), mini_map(x + 10, 308, 210, 82, i + 1), t(x + 14, 414, name, 15, CAFE_DARK, 900),
              t(x + 14, 434, addr, 11, "#7c5a3a"), t(x + 14, 454, "營業時間 " + hours, 11, "#9b7b5b"), outline_btn(x + 150, 400, 66, 22, "導航", CAFE_BROWN, 10)]
    return svg("".join(b), defs)


def scene_cafe_mobile():
    defs = diag_grad("mbg", "#f3e3cc", "#d6b58d")
    b = [r(0, 0, 800, 500, "url(#mbg)")]

    def header(ox, oy):
        return (t(ox + 16, oy + 24, "9:41", 10, CAFE_DARK, 700) + c(ox + 22, oy + 50, 7, CAFE_BROWN) + t(ox + 34, oy + 55, "晨光咖啡", 12, CAFE_DARK, 900)
                + "".join(ln(ox + 150, oy + 46 + k * 5, ox + 166, oy + 46 + k * 5, CAFE_DARK, 2) for k in range(3)))

    for px in (70, 300, 530):
        b.append(phone(px, 26, 200, 448, "#fdf6ec"))
    ox, oy = 79, 35
    b += [header(ox, oy), c(ox + 91, oy + 150, 62, "#ecd3b0"), cafe_cup(ox + 91, oy + 156, 0.9),
          t(ox + 16, oy + 248, "每一杯，", 20, CAFE_DARK, 900), t(ox + 16, oy + 274, "都是今天的好心情", 16, CAFE_DARK, 900),
          t(ox + 16, oy + 296, "嚴選單品咖啡豆，每日現烘現煮", 10, "#7c5a3a"),
          btn(ox + 16, oy + 316, 150, 34, "查看菜單", CAFE_BROWN), outline_btn(ox + 16, oy + 358, 150, 34, "線上訂位", CAFE_BROWN)]
    ox = 309
    b += [header(ox, oy), t(ox + 16, oy + 96, "菜單", 18, CAFE_DARK, 900)]
    for i, s in enumerate(["咖啡", "茶飲", "甜點"]):
        b.append(btn(ox + 16 + i * 52, oy + 108, 46, 22, s, CAFE_BROWN, size=10) if i == 0 else outline_btn(ox + 16 + i * 52, oy + 108, 46, 22, s, CAFE_MID, 10))
    for i, (name, price, col) in enumerate([("美式咖啡", "90", "#7a4a26"), ("拿鐵", "120", "#c08552"), ("卡布奇諾", "120", "#a87444"),
                                            ("焦糖瑪奇朵", "140", "#d19a5b"), ("手沖單品", "160", "#5b3a1e")]):
        y = oy + 142 + i * 58
        b += [r(ox + 12, y, 158, 50, "#fff", 10), c(ox + 38, y + 25, 16, col), t(ox + 62, y + 22, name, 11, CAFE_DARK, 700),
              t(ox + 62, y + 39, "NT$ " + price, 11, "#b07a45", 900), c(ox + 154, y + 25, 9, CAFE_BROWN), t(ox + 154, y + 29, "+", 12, "#fff", 900, "middle")]
    ox = 539
    b += [header(ox, oy), t(ox + 16, oy + 96, "線上訂位", 18, CAFE_DARK, 900), r(ox + 12, oy + 110, 158, 160, "#fff", 12),
          t(ox + 91, oy + 132, "2026 年 10 月", 11, CAFE_DARK, 700, "middle")]
    for i, d in enumerate("日一二三四五六"):
        b.append(t(ox + 25 + i * 22, oy + 152, d, 9, "#9b7b5b", 700, "middle"))
    for day in range(1, 32):
        idx = day + 3
        x, y = ox + 25 + (idx % 7) * 22, oy + 170 + (idx // 7) * 19
        if day == 5:
            b.append(c(x, y - 3, 8, CAFE_BROWN))
        b.append(t(x, y, day, 9, "#fff" if day == 5 else CAFE_DARK, 700 if day == 5 else 400, "middle"))
    for i, s in enumerate(["11:00", "12:30", "14:00", "15:30", "17:00", "18:30"]):
        x, y = ox + 12 + (i % 3) * 54, oy + 284 + (i // 3) * 32
        b.append(btn(x, y, 50, 24, s, CAFE_BROWN, size=10) if i == 2 else outline_btn(x, y, 50, 24, s, CAFE_MID, 10))
    b.append(btn(ox + 12, oy + 360, 158, 36, "確認訂位", CAFE_BROWN))
    return svg("".join(b), defs)


# ================= 電商網站 =================
SHOP_PINK = "#ff3d77"


def shop_frame():
    return [r(0, 36, 800, 464, "#f5f5f7"), browser_bar("shoply.tw"), r(0, 36, 800, 50, "#fff"),
            t(32, 68, "SHOPLY", 22, SHOP_PINK, 900, extra='letter-spacing="1"'), r(170, 48, 390, 26, "#f3f4f6", 13),
            t(188, 65, "搜尋商品、品牌…", 12, "#9ca3af"), c(545, 61, 10, SHOP_PINK), t(640, 66, "會員中心", 12, "#374151", 500),
            t(716, 66, "購物車", 12, "#374151", 500), c(762, 52, 8, "#ef4444"), t(762, 56, "3", 10, "#fff", 700, "middle")]


def art_scaled(kind, cx, cy, s):
    return f'<g transform="translate({cx} {cy}) scale({s})">{product_art(kind, 0, 0)}</g>'


def scene_shop_list():
    b = shop_frame() + [t(32, 106, "首頁 / 3C 家電 / 耳機與音響", 11, "#6b7280"), shadow(r(32, 118, 170, 364, "#fff", 12)),
                        t(48, 144, "篩選條件", 14, "#111827", 900), t(48, 172, "價格", 12, "#374151", 700),
                        ln(52, 192, 182, 192, "#e5e7eb", 4), ln(76, 192, 150, 192, SHOP_PINK, 4),
                        c(76, 192, 7, "#fff", f'stroke="{SHOP_PINK}" stroke-width="3"'), c(150, 192, 7, "#fff", f'stroke="{SHOP_PINK}" stroke-width="3"'),
                        t(48, 216, "NT$ 500 – 3,000", 11, "#6b7280"), t(48, 246, "品牌", 12, "#374151", 700)]
    for i, (brand, on) in enumerate([("Sonic", True), ("AudioX", False), ("Beat Lab", True), ("Nova", False), ("Pulse", False)]):
        y = 258 + i * 24
        b += [checkbox(48, y, on, SHOP_PINK, 13), t(68, y + 11, brand, 11.5, "#374151")]
    b += [t(48, 396, "評價", 12, "#374151", 700), radio(55, 414, True, SHOP_PINK, 6), t(68, 418, "★★★★ 以上", 11.5, "#f59e0b"),
          t(48, 448, "運送", 12, "#374151", 700), checkbox(48, 458, True, SHOP_PINK, 13), t(68, 469, "24 小時到貨", 11.5, "#374151"),
          r(216, 118, 552, 34, "#fff", 10), t(232, 140, "共 128 件商品", 12, "#374151", 700)]
    for i, s in enumerate(["綜合", "最新", "熱銷", "價格 ↑"]):
        x = 520 + i * 60
        b.append(btn(x, 124, 54, 22, s, SHOP_PINK, size=11) if i == 2 else t(x + 27, 140, s, 11, "#6b7280", 400, "middle"))
    prods = [("headphone", "#ffe4e6", "降噪藍牙耳機 Pro", "1,990"), ("headphone", "#e0f2fe", "頭戴式耳機 Studio", "3,190"),
             ("headphone", "#fef3c7", "運動耳機 Lite", "860"), ("watch", "#ede9fe", "智慧手錶 S2", "3,480"),
             ("headphone", "#dcfce7", "兒童耳機 Kids", "650"), ("watch", "#fee2e2", "運動手環 Band", "1,290")]
    for i, (kind, bg, name, price) in enumerate(prods):
        x, y = 216 + (i % 3) * 186, 164 + (i // 3) * 160
        b += [r(x, y, 176, 150, "#fff", 12, 'stroke="#ececec"'), r(x + 8, y + 8, 160, 76, bg, 8), art_scaled(kind, x + 88, y + 44, 0.8),
              t(x + 12, y + 104, name, 12, "#111827", 700), t(x + 12, y + 126, "NT$ " + price, 14, "#ef4444", 900),
              t(x + 164, y + 126, "★ 4.8", 11, "#f59e0b", 700, "end"), t(x + 12, y + 142, f"已售 {2 + i},{(i * 37) % 9}00", 10, "#9ca3af")]
    return svg("".join(b))


def scene_shop_detail():
    b = shop_frame() + [t(32, 106, "首頁 / 3C 家電 / 耳機 / 降噪藍牙耳機 Pro", 11, "#6b7280"), r(32, 118, 330, 280, "#ffe4e6", 16),
                        art_scaled("headphone", 197, 252, 2.4)]
    for i, bg in enumerate(["#ffe4e6", "#f3f4f6", "#fce7f3", "#e0e7ff"]):
        x = 32 + i * 86
        b += [r(x, 410, 76, 70, bg, 10, f'stroke="{SHOP_PINK}" stroke-width="2"' if i == 0 else ""), art_scaled("headphone", x + 38, 442, 0.7)]
    b += [pill(392, 122, "熱銷 No.1", "#ef4444", "#fff", 10), t(392, 166, "降噪藍牙耳機 Pro", 26, "#111827", 900),
          t(392, 192, "★★★★★ 4.9 · 2,138 則評價 · 已售出 1.2 萬", 12, "#f59e0b"), r(392, 206, 376, 64, "#fff1f2", 12),
          t(408, 248, "NT$ 1,990", 28, "#ef4444", 900), t(560, 248, "$2,690", 13, "#9ca3af", 400, extra='text-decoration="line-through"'),
          pill(612, 234, "省 26%", "#ef4444", "#fff", 10), t(392, 298, "顏色", 12, "#374151", 700)]
    for i, col in enumerate(["#1f2937", "#f9fafb", "#f9a8d4", "#1e3a8a"]):
        x = 452 + i * 36
        b.append(c(x, 294, 12, col, 'stroke="#d1d5db"') + (c(x, 294, 16, "none", f'stroke="{SHOP_PINK}" stroke-width="2"') if i == 0 else ""))
    b += [t(392, 338, "數量", 12, "#374151", 700), r(452, 320, 110, 30, "#fff", 6, 'stroke="#d1d5db"'), t(468, 340, "－", 13, "#374151"),
          t(507, 340, "1", 13, "#111827", 700, "middle"), t(540, 340, "＋", 13, "#374151"), t(576, 340, "庫存 128 件", 11, "#9ca3af"),
          r(392, 366, 180, 44, "#fff1f2", 10, f'stroke="{SHOP_PINK}"'), t(482, 393, "加入購物車", 14, SHOP_PINK, 900, "middle"),
          btn(588, 366, 180, 44, "直接購買", SHOP_PINK, size=14, rx=10),
          t(392, 438, "✓ 24 小時快速到貨    ✓ 7 天鑑賞期    ✓ 一年保固", 11.5, "#059669", 700),
          t(392, 462, "付款方式：信用卡 / LINE Pay / 超商取貨付款 / ATM 轉帳", 11, "#6b7280")]
    return svg("".join(b))


def scene_shop_cart():
    b = shop_frame()
    steps = ["購物車", "付款與運送", "確認訂單", "完成"]
    for i in range(3):
        x = 220 + i * 120
        b.append(ln(x, 108, x + 120, 108, SHOP_PINK if i == 0 else "#e5e7eb", 3))
    for i, s in enumerate(steps):
        x = 220 + i * 120
        done, cur = i == 0, i == 1
        b += [c(x, 108, 11, SHOP_PINK if (done or cur) else "#e5e7eb"), t(x, 112, "✓" if done else i + 1, 11, "#fff" if (done or cur) else "#9ca3af", 900, "middle"),
              t(x, 134, s, 11, "#111827" if cur else "#6b7280", 700 if cur else 400, "middle")]
    b += [shadow(r(32, 150, 470, 330, "#fff", 14)), t(50, 180, "購物車（3 件商品）", 15, "#111827", 900)]
    items = [("headphone", "#ffe4e6", "降噪藍牙耳機 Pro", "顏色：黑", "1,990", 1), ("watch", "#e0f2fe", "智慧運動手錶 S2", "錶帶：灰", "3,480", 1),
             ("plant", "#dcfce7", "療癒桌上型盆栽", "款式：圓盆", "390", 2)]
    for i, (kind, bg, name, spec, price, qty) in enumerate(items):
        y = 198 + i * 74
        b += [r(50, y, 60, 60, bg, 8), art_scaled(kind, 80, y + 30, 0.55), t(124, y + 22, name, 13, "#111827", 700), t(124, y + 42, spec, 11, "#9ca3af"),
              r(300, y + 16, 84, 26, "#fff", 6, 'stroke="#e5e7eb"'), t(314, y + 34, "－", 12, "#6b7280"), t(342, y + 34, qty, 12, "#111827", 700, "middle"),
              t(366, y + 34, "＋", 12, "#6b7280"), t(470, y + 34, "NT$ " + price, 13, "#ef4444", 900, "end"), t(488, y + 34, "✕", 11, "#d1d5db", 400, "middle"),
              ln(50, y + 68, 484, y + 68, "#f3f4f6")]
    b += [t(50, 446, "優惠券", 12, "#374151", 700), r(106, 428, 150, 26, "#f9fafb", 6, 'stroke="#e5e7eb"'), t(116, 446, "DOUBLE11", 12, "#111827", 700, mono=True),
          pill(268, 432, "已折抵 NT$100", "#dcfce7", "#15803d", 10),
          shadow(r(518, 150, 250, 330, "#fff", 14)), t(536, 180, "付款方式", 15, "#111827", 900)]
    for i, s in enumerate(["信用卡（一次付清）", "LINE Pay", "超商取貨付款", "ATM 轉帳"]):
        y = 206 + i * 28
        b += [radio(544, y, i == 0, SHOP_PINK), t(558, y + 4, s, 12, "#374151")]
    for i, (k, v) in enumerate([("小計", "NT$ 6,250"), ("運費", "免運"), ("折扣", "- NT$ 100")]):
        y = 334 + i * 24
        b += [t(536, y, k, 12, "#6b7280"), t(750, y, v, 12, "#15803d" if i else "#111827", 700, "end")]
    b += [ln(536, 398, 750, 398, "#e5e7eb"), t(536, 424, "總計", 13, "#111827", 900), t(750, 426, "NT$ 6,150", 20, "#ef4444", 900, "end"),
          btn(536, 438, 214, 34, "前往結帳", SHOP_PINK, rx=8)]
    return svg("".join(b))


def scene_shop_member():
    b = shop_frame() + [shadow(r(32, 102, 180, 380, "#fff", 14)), avatar(122, 146, 26, "#fbcfe8", "林", 20, "#be185d"),
                        t(122, 192, "林○婷", 14, "#111827", 900, "middle"), pill(88, 202, "金卡會員", "#fef3c7", "#b45309", 10)]
    b.append(side_nav(32, 256, 180, ["我的訂單", "收藏清單", "優惠券（5）", "購物金 NT$320", "個人資料", "登出"], 0, 34, "#4b5563", SHOP_PINK, "#fff1f2"))
    b += [t(230, 128, "我的訂單", 20, "#111827", 900)]
    for i, s in enumerate(["全部", "待付款", "待出貨", "配送中", "已完成"]):
        x = 330 + i * 86
        b.append(btn(x, 110, 76, 26, s, SHOP_PINK, size=11) if i == 3 else outline_btn(x, 110, 76, 26, s, "#9ca3af", 11, fill="#fff"))
    b += [shadow(r(230, 150, 538, 176, "#fff", 14)), t(248, 176, "訂單 #20260930-117", 12, "#111827", 700, mono=True), t(750, 176, "2026/09/30 下單", 11, "#9ca3af", 400, "end"),
          r(248, 188, 54, 54, "#e0f2fe", 8), art_scaled("watch", 275, 215, 0.5), t(314, 210, "智慧運動手錶 S2 × 1", 13, "#111827", 700),
          t(314, 230, "NT$ 3,480", 12, "#ef4444", 900)]
    nodes = [("已付款", "09/30 21:04"), ("已出貨", "10/01 10:22"), ("配送中", "10/02 08:15"), ("已送達", "預計 10/03")]
    for i in range(3):
        b.append(ln(290 + i * 140, 270, 430 + i * 140, 270, SHOP_PINK if i < 2 else "#e5e7eb", 3))
    for i, (s, tm) in enumerate(nodes):
        x = 290 + i * 140
        on = i < 3
        b += [c(x, 270, 16, SHOP_PINK, 'opacity="0.2"') if i == 2 else "", c(x, 270, 10 if i == 2 else 8, SHOP_PINK if on else "#e5e7eb"),
              t(x, 296, s, 11.5, "#111827" if on else "#9ca3af", 700, "middle"), t(x, 312, tm, 10, "#9ca3af", 400, "middle")]
    b += [outline_btn(672, 200, 80, 26, "查看物流", SHOP_PINK, 11),
          shadow(r(230, 340, 538, 140, "#fff", 14)), t(248, 366, "訂單 #20260912-052", 12, "#111827", 700, mono=True), pill(690, 352, "已完成", "#dcfce7", "#15803d", 10),
          r(248, 380, 54, 54, "#ffe4e6", 8), art_scaled("headphone", 275, 407, 0.5), t(314, 402, "降噪藍牙耳機 Pro × 1", 13, "#111827", 700),
          t(314, 422, "NT$ 1,990", 12, "#ef4444", 900), outline_btn(556, 438, 90, 28, "再買一次", "#6b7280", 11), btn(658, 438, 92, 28, "評價商品", SHOP_PINK, size=11)]
    return svg("".join(b))


# ================= 營運後台 =================
DASH_NAV = ["總覽", "訂單管理", "商品管理", "會員分析", "行銷活動", "報表匯出", "系統設定"]


def dash_frame(active, title, url_path):
    return [r(0, 36, 800, 464, "#0b1220"), browser_bar("admin.yourbrand.tw/" + url_path, True), r(0, 36, 160, 464, "#0f172a"),
            c(28, 66, 10, "#22d3ee"), t(46, 71, "營運後台", 15, "#f1f5f9", 900),
            side_nav(4, 106, 152, DASH_NAV, active, 36, "#64748b", "#f1f5f9", "#1e293b", 13, "#22d3ee"),
            t(180, 74, title, 18, "#f1f5f9", 900)]


def dark_pill(x, y, label, color):
    w = tw(label, 10) + 16
    return r(x, y, w, 18, color, 9, 'opacity="0.18"') + t(x + w / 2, y + 13, label, 10, color, 700, "middle")


def scene_dash_orders():
    b = dash_frame(1, "訂單管理", "orders")
    for i, (s, n) in enumerate([("全部", "3,429"), ("待出貨", "48"), ("已出貨", "3,317"), ("退貨", "6")]):
        x = 180 + i * 104
        on = i == 1
        b += [r(x, 88, 96, 28, "#22d3ee" if on else "#111a2e", 14, "" if on else 'stroke="#1e293b"'),
              t(x + 48, 107, f"{s} {n}", 11, "#0b1220" if on else "#94a3b8", 700, "middle")]
    b += [r(610, 88, 72, 28, "#111a2e", 6, 'stroke="#334155"'), t(646, 107, "匯出 CSV", 11, "#cbd5e1", 500, "middle"),
          btn(690, 88, 80, 28, "批次出貨", "#22d3ee", "#0b1220", 11, 6)]
    names = ["王○明", "林○婷", "陳○豪", "張○芳", "李○宇", "黃○琪", "吳○翰", "劉○萱", "蔡○廷", "楊○涵"]
    pays = ["信用卡", "LINE Pay", "超商取貨", "ATM", "信用卡", "信用卡", "LINE Pay", "超商取貨", "信用卡", "ATM"]
    rows = [["", f"#20261004-{120 - i:03d}", names[i], f"10/04 {14 - i // 2:02d}:{(i * 7) % 60:02d}",
             f"NT$ {(i * 731 + 890) % 5000 + 390:,}", pays[i], ""] for i in range(10)]
    checked = {0, 1, 3}

    def cell(ri, ci, val, x, base, w):
        if ci == 0:
            return checkbox(x + 9, base - 11, ri in checked, "#22d3ee", 13)
        if ci == 6:
            st, col = ("待出貨", "#fbbf24") if ri < 6 else ("揀貨中", "#a78bfa")
            return dark_pill(x + 8, base - 13, st, col)
        return None

    b.append(table(180, 128, [32, 130, 82, 100, 92, 82, 72], ["", "訂單編號", "客戶", "下單時間", "金額", "付款", "狀態"], rows, 32, 28,
                   "#111a2e", "#94a3b8", "#e2e8f0", None, "#1e293b", 11, cell=cell, mono_cols=(1,)))
    b.append(r(180, 156, 590, 64, "#22d3ee", 0, 'opacity="0.06"'))
    return svg("".join(b))


def scene_dash_products():
    b = dash_frame(2, "商品管理", "products") + [btn(560, 58, 96, 28, "+ 新增商品", "#22d3ee", "#0b1220", 11, 6),
                                                  r(664, 58, 106, 28, "#111a2e", 6, 'stroke="#334155"'), t(676, 76, "全部分類 ▾", 11, "#cbd5e1")]
    prods = [("降噪藍牙耳機 Pro", "HP-001", "1,990", 128, True, "#f472b6"), ("智慧運動手錶 S2", "WT-002", "3,480", 42, True, "#38bdf8"),
             ("輕量慢跑鞋 AirFlow", "SH-014", "1,680", 9, True, "#a78bfa"), ("療癒桌上型盆栽", "PL-031", "390", 260, True, "#4ade80"),
             ("頭戴式耳機 Studio", "HP-007", "3,190", 0, False, "#fb923c"), ("無線充電盤", "AC-120", "690", 75, True, "#facc15"),
             ("保溫隨行杯", "LF-210", "520", 18, True, "#2dd4bf"), ("藍牙喇叭 Mini", "SP-033", "1,290", 56, False, "#f87171")]
    rows = [["", n, sku, "NT$ " + p, "", "", ""] for n, sku, p, st, on, col in prods]

    def cell(ri, ci, val, x, base, w):
        n, sku, p, st, on, col = prods[ri]
        if ci == 0:
            return r(x + 8, base - 20, 30, 30, col, 6, 'opacity="0.85"')
        if ci == 4:
            color = "#f87171" if st < 20 else "#22d3ee"
            return t(x + 10, base, st, 11, color, 700) + progress(x + 44, base - 6, 50, 5, min(st / 150, 1), color, "#1e293b")
        if ci == 5:
            return toggle(x + 10, base - 13, on, "#22d3ee")
        if ci == 6:
            return t(x + 8, base, "編輯", 11, "#22d3ee", 700)
        return None

    b.append(table(180, 100, [48, 170, 80, 84, 110, 54, 44], ["", "商品名稱", "料號", "售價", "庫存", "上架", ""], rows, 44, 28,
                   "#111a2e", "#94a3b8", "#e2e8f0", None, "#1e293b", 11.5, cell=cell, mono_cols=(2,)))
    return svg("".join(b))


def scene_dash_members():
    b = dash_frame(3, "會員分析", "members")
    b += [r(180, 92, 380, 180, "#111a2e", 10, 'stroke="#1e293b"'), t(196, 114, "每月新增會員", 12, "#e2e8f0", 700),
          grid_lines(200, 130, 344, 120, 4, "#1e293b"),
          bar_chart(200, 130, 344, 120, [320, 410, 380, 460, 520, 490, 610, 580, 660, 720, 790, 862], ["#22d3ee"] * 11 + ["#a78bfa"], 0.4)]
    for i, m in enumerate(["1", "3", "5", "7", "9", "11"]):
        b.append(t(214 + i * 57.3, 266, m + "月", 9, "#64748b", 400, "middle"))
    b += [r(574, 92, 196, 180, "#111a2e", 10, 'stroke="#1e293b"'), t(590, 114, "會員等級", 12, "#e2e8f0", 700),
          donut(634, 190, 40, [(0.58, "#64748b"), (0.27, "#22d3ee"), (0.11, "#fbbf24"), (0.04, "#f472b6")], 16),
          t(634, 195, "8,214", 12, "#f1f5f9", 900, "middle")]
    for i, (name, pct, col) in enumerate([("一般", "58%", "#64748b"), ("銀卡", "27%", "#22d3ee"), ("金卡", "11%", "#fbbf24"), ("VIP", "4%", "#f472b6")]):
        y = 146 + i * 26
        b += [r(690, y - 8, 8, 8, col, 2), t(704, y, name, 10, "#94a3b8"), t(704, y + 12, pct, 10, "#f1f5f9", 700)]
    b += [r(180, 286, 380, 196, "#111a2e", 10, 'stroke="#1e293b"'), t(196, 308, "回購留存率（同期群分析）", 12, "#e2e8f0", 700)]
    for j in range(6):
        b.append(t(280 + j * 44, 328, f"M{j}", 9, "#64748b", 700, "middle"))
    for i in range(6):
        b.append(t(196, 350 + i * 22, f"2026/0{i + 3}", 9, "#94a3b8", 400, mono=True))
        for j in range(6 - i):
            v = 1.0 if j == 0 else max(0.12, 0.62 - j * 0.09 + (i % 3) * 0.03)
            b += [r(260 + j * 44, 337 + i * 22, 40, 18, "#22d3ee", 3, f'opacity="{0.15 + v * 0.8:.2f}"'),
                  t(280 + j * 44, 350 + i * 22, f"{int(v * 100)}%", 9, "#0b1220" if v > 0.5 else "#e2e8f0", 700, "middle")]
    b += [r(574, 286, 196, 196, "#111a2e", 10, 'stroke="#1e293b"'), t(590, 308, "會員地區分布", 12, "#e2e8f0", 700)]
    for i, (city, v) in enumerate([("台北市", 0.32), ("新北市", 0.24), ("台中市", 0.18), ("高雄市", 0.12), ("其他", 0.14)]):
        y = 336 + i * 28
        b += [t(590, y, city, 11, "#cbd5e1"), progress(640, y - 9, 86, 10, v / 0.32, "#a78bfa", "#1e293b"), t(758, y, f"{int(v * 100)}%", 10, "#f1f5f9", 700, "end")]
    return svg("".join(b))


def scene_dash_login():
    defs = diag_grad("lg", "#0b1220", "#1e1b4b") + rad_grad("orb", "#22d3ee", "#22d3ee", 0.35, 0) + lin_grad("lgbtn", "#22d3ee", "#a78bfa", False)
    b = [r(0, 36, 800, 464, "url(#lg)"), browser_bar("admin.yourbrand.tw/login", True), c(160, 380, 180, "url(#orb)"), c(700, 120, 120, "url(#orb)"),
         c(56, 112, 14, "#22d3ee"), t(80, 118, "營運後台", 20, "#f1f5f9", 900), t(56, 190, "數據驅動", 36, "#f1f5f9", 900),
         t(56, 236, "每一個經營決策", 36, "#22d3ee", 900)]
    for i, s in enumerate(["即時營收與訂單監控", "會員分群與行銷成效追蹤", "多層級帳號權限管理", "一鍵匯出報表"]):
        y = 284 + i * 32
        b += [c(64, y - 4, 9, "#22d3ee", 'opacity="0.2"'), t(64, y, "✓", 11, "#22d3ee", 900, "middle"), t(84, y, s, 14, "#cbd5e1")]
    b += [shadow(r(470, 82, 290, 384, "#111a2e", 16)), r(470, 82, 290, 384, "none", 16, 'stroke="#334155"'),
          t(615, 124, "登入管理後台", 18, "#f1f5f9", 900, "middle"), t(615, 146, "請使用公司帳號登入", 11, "#64748b", 400, "middle"),
          field(494, 170, 242, "帳號", "admin@yourbrand.tw", 34, True), field(494, 230, 242, "密碼", "••••••••••", 34, True),
          t(494, 290, "兩步驟驗證碼", 11, "#94a3b8", 700)]
    for i, d in enumerate("48291 "):
        x = 494 + i * 41
        b += [r(x, 298, 35, 38, "#0f172a", 6, f'stroke="{"#22d3ee" if i == 5 else "#334155"}"'), t(x + 17.5, 323, d.strip(), 16, "#f1f5f9", 900, "middle")]
    b += [checkbox(494, 352, True, "#22d3ee", 13), t(514, 363, "記住我", 11, "#94a3b8"), t(736, 363, "忘記密碼？", 11, "#22d3ee", 700, "end"),
          r(494, 380, 242, 40, "url(#lgbtn)", 8), t(615, 405, "登入", 14, "#0b1220", 900, "middle"),
          t(615, 448, "© 2026 YourBrand · 連線已加密", 10, "#475569", 400, "middle")]
    return svg("".join(b), defs)


SCREENS = {
    "web-cafe": [scene_cafe, scene_cafe_menu, scene_cafe_booking, scene_cafe_about, scene_cafe_mobile],
    "web-shop": [scene_shop, scene_shop_list, scene_shop_detail, scene_shop_cart, scene_shop_member],
    "web-dashboard": [scene_dashboard, scene_dash_orders, scene_dash_products, scene_dash_members, scene_dash_login],
}
