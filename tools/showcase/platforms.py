"""架站平台類作品：Shopify 品牌電商、WooCommerce 茶行商店、WordPress 室內設計官網。"""
import random

from .common import *  # noqa: F401,F403

# ================= Shopify：LUMI 植萃保養 =================
SAGE, SAGE_DARK, CREAM, SAND = "#5f7a61", "#2f3a2f", "#f6f1e9", "#c9a27e"


def bottle(cx, cy, s=1.0, body=SAND, cap=SAGE_DARK, kind=0):
    """保養品瓶身：0 滴管瓶、1 乳霜罐、2 按壓瓶。(cx, cy) 為瓶身中心。"""
    if kind == 1:
        shape = (r(-40, -12, 80, 20, cap, 6) + r(-44, 6, 88, 50, body, 12) + r(-30, 18, 60, 26, CREAM, 4)
                 + t(0, 36, "LUMI", 10, SAGE_DARK, 900, "middle", extra='letter-spacing="2"'))
    elif kind == 2:
        shape = (path("M-4 -78 h22 v8 h-14 v10 h-8z", cap) + r(-10, -62, 20, 16, cap, 3) + r(-24, -46, 48, 106, body, 12)
                 + r(-18, -6, 36, 40, CREAM, 4) + t(0, 18, "LUMI", 9, SAGE_DARK, 900, "middle", extra='letter-spacing="1.5"'))
    else:
        shape = ('<ellipse cx="0" cy="-62" rx="9" ry="13" fill="' + cap + '"/>' + r(-14, -52, 28, 16, cap, 3) + r(-30, -36, 60, 96, body, 14)
                 + r(-22, -4, 44, 40, CREAM, 4) + t(0, 20, "LUMI", 10, SAGE_DARK, 900, "middle", extra='letter-spacing="2"'))
    return f'<g transform="translate({cx} {cy}) scale({s})">{shape}</g>'


def leaf(cx, cy, rot, s=1.0, color=SAGE):
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            + path("M0 0 q18 -30 0 -64 q-18 34 0 64z", color) + ln(0, 0, 0, -58, "#ffffff", 1.2, 'opacity="0.5"') + "</g>")


def lumi_header(url="lumi.tw"):
    b = [r(0, 36, 800, 464, "#fff"), browser_bar(url), r(0, 36, 800, 24, SAGE_DARK),
         t(400, 52, "全館滿 NT$1,500 免運 · 首購輸入 HELLO 享 9 折", 11, "#f6f1e9", 500, "middle"), r(0, 60, 800, 44, "#fff"),
         t(400, 90, "LUMI", 24, SAGE_DARK, 900, "middle", extra='letter-spacing="8"'), ln(0, 104, 800, 104, "#eee")]
    for i, s in enumerate(["全部商品", "精華液", "乳霜", "禮盒"]):
        b.append(t(32 + i * 70, 87, s, 12, "#444"))
    b += [t(640, 87, "搜尋", 12, "#444"), t(684, 87, "帳戶", 12, "#444"), t(728, 87, "購物車 (2)", 12, SAGE_DARK, 700)]
    return b


def lumi_home_body():
    b = lumi_header()
    b += [r(0, 104, 800, 228, "#efe7da"), t(48, 150, "BOTANICAL SKINCARE", 11, SAND, 700, extra='letter-spacing="3"'),
          t(48, 200, "回歸肌膚", 40, SAGE_DARK, 900), t(48, 248, "本來的光", 40, SAGE_DARK, 900),
          t(48, 278, "100% 植物萃取 · 無香精 · 敏感肌適用", 13, "#6b6b5f"), btn(48, 292, 120, 30, "立即選購", SAGE_DARK, rx=4),
          path("M480 332 v-100 a110 110 0 0 1 220 0 v100z", "#dfe8d8"), leaf(500, 330, -30, 1.2), leaf(690, 330, 28, 1.1, "#7f9a7f"),
          bottle(560, 262, 1.0, SAND, SAGE_DARK, 0), bottle(640, 270, 1.0, "#e8d5c4", SAGE_DARK, 2), bottle(600, 300, 0.75, "#a9bfa5", SAGE_DARK, 1),
          t(40, 364, "本月熱銷", 16, SAGE_DARK, 900), t(760, 364, "查看全部 →", 11, SAGE, 700, "end")]
    prods = [("玫瑰果油精華", "1,280", SAND, 0), ("積雪草修護霜", "980", "#a9bfa5", 1), ("洋甘菊潔顏乳", "620", "#e8d5c4", 2),
             ("植萃保濕禮盒", "2,480", "#d6c3a5", 1)]
    for i, (name, price, col, kind) in enumerate(prods):
        x = 40 + i * 184
        b += [r(x, 376, 170, 76, CREAM, 6), bottle(x + 85, 418, 0.42 if kind != 1 else 0.55, col, SAGE_DARK, kind),
              t(x, 472, name, 12, SAGE_DARK, 700), t(x, 490, "NT$ " + price, 12, "#6b6b5f")]
    return b


def scene_shopify_home():
    return svg("".join(lumi_home_body()))


def scene_shopify_product():
    b = lumi_header() + [t(40, 124, "首頁 / 精華液 / 玫瑰果油精華", 11, "#999")]
    for i, col in enumerate([SAND, "#e8d5c4", "#dfe8d8", "#efe7da"]):
        y = 136 + i * 70
        b += [r(40, y, 58, 62, col, 4, f'stroke="{SAGE_DARK}" stroke-width="1.5"' if i == 0 else ""), bottle(69, y + 36, 0.32, SAND, SAGE_DARK, 0)]
    b += [r(110, 136, 270, 344, CREAM, 6), leaf(150, 470, -24, 1.4), leaf(350, 470, 24, 1.2, "#7f9a7f"), bottle(245, 320, 1.6, SAND, SAGE_DARK, 0),
          t(410, 150, "LUMI 植萃保養", 11, SAND, 700, extra='letter-spacing="2"'), t(410, 182, "玫瑰果油精華 30ml", 24, SAGE_DARK, 900),
          t(410, 206, "★★★★★ 4.9（326 則評論）", 12, "#d4a017"), t(410, 240, "NT$ 1,280", 22, SAGE_DARK, 900),
          r(410, 256, 350, 40, "#fff", 6, 'stroke="#ddd"'), radio(428, 276, False, SAGE_DARK), t(444, 280, "單次購買", 12, "#333"),
          t(746, 280, "NT$ 1,280", 12, "#333", 700, "end"), r(410, 302, 350, 52, "#f3f7f1", 6, f'stroke="{SAGE_DARK}" stroke-width="1.5"'),
          radio(428, 322, True, SAGE_DARK), t(444, 326, "定期配送（每 30 天）享 9 折", 12, SAGE_DARK, 700), t(746, 326, "NT$ 1,152", 12, SAGE_DARK, 900, "end"),
          t(444, 344, "可隨時暫停或取消", 10, "#777"), pill(612, 314, "最划算", SAGE, "#fff", 9),
          r(410, 366, 96, 38, "#fff", 4, 'stroke="#ccc"'), t(428, 390, "－", 13, "#555"), t(458, 390, "1", 13, "#111", 700, "middle"), t(482, 390, "＋", 13, "#555"),
          btn(516, 366, 244, 38, "加入購物車", SAGE_DARK, rx=4, size=13), btn(410, 412, 350, 34, "立即購買", "#111", rx=4)]
    b += [ln(410, 458, 760, 458, "#e5e5e5"), t(410, 478, "主要成分　·　使用方式　·　運送與退換貨", 12, "#444"), t(760, 478, "＋", 14, "#444", 700, "end"),
          ln(410, 490, 760, 490, "#e5e5e5")]
    return svg("".join(b))


def scene_shopify_checkout():
    b = [r(0, 36, 800, 464, "#fff"), browser_bar("lumi.tw/checkouts/cn/7Z3K"), r(470, 36, 330, 464, "#f5f5f5"), ln(470, 36, 470, 500, "#e5e5e5"),
         t(40, 80, "LUMI", 22, SAGE_DARK, 900, extra='letter-spacing="6"'), t(40, 104, "購物車  ›  資訊  ›  運送  ›  付款", 11, "#777"),
         t(40, 136, "聯絡資訊", 14, "#111", 700), t(430, 136, "登入", 11, SAGE, 700, "end"),
         field(40, 140, 390, "", "amber.lin@gmail.com", 32), checkbox(40, 186, True, SAGE_DARK, 13), t(60, 197, "寄送最新消息與優惠給我", 11, "#555"),
         t(40, 228, "運送地址", 14, "#111", 700), field(40, 232, 390, "", "台灣", 32), field(40, 270, 190, "", "名字　怡君", 32, muted=False),
         field(240, 270, 190, "", "姓氏　林", 32), field(40, 308, 390, "", "台中市西區民生路 368 巷 12 號", 32),
         t(40, 372, "運送方式", 14, "#111", 700), r(40, 380, 390, 72, "#fff", 6, 'stroke="#ddd"'), r(40, 380, 390, 36, "#f3f7f1", 6, f'stroke="{SAGE_DARK}"'),
         radio(58, 398, True, SAGE_DARK), t(74, 402, "超商取貨（7-11 / 全家）", 12, "#111", 700), t(416, 402, "NT$ 60", 12, "#111", 700, "end"),
         radio(58, 434, False, SAGE_DARK), t(74, 438, "宅配到府", 12, "#333"), t(416, 438, "NT$ 100", 12, "#333", 400, "end"),
         btn(270, 462, 160, 32, "繼續付款", SAGE_DARK, rx=4), t(40, 482, "‹ 返回購物車", 11, SAGE, 700)]
    items = [("玫瑰果油精華 30ml", "定期配送 · 每 30 天", "1,152", SAND, 0, 1), ("積雪草修護霜 50g", "單次購買", "980", "#a9bfa5", 1, 1),
             ("洋甘菊潔顏乳", "單次購買", "620", "#e8d5c4", 2, 1)]
    for i, (name, sub, price, col, kind, qty) in enumerate(items):
        y = 70 + i * 66
        b += [r(500, y, 54, 54, "#fff", 8, 'stroke="#ddd"'), bottle(527, y + 30, 0.26 if kind != 1 else 0.36, col, SAGE_DARK, kind),
              c(552, y + 2, 9, "#777"), t(552, y + 6, qty, 10, "#fff", 700, "middle"), t(568, y + 24, name, 12, "#111", 700),
              t(568, y + 42, sub, 10, "#777"), t(770, y + 30, "NT$ " + price, 12, "#111", 400, "end")]
    b += [ln(500, 272, 770, 272, "#e0e0e0"), field(500, 278, 190, "", "折扣碼或禮品卡", 34, muted=True),
          r(700, 286, 70, 34, "#e5e5e5", 6), t(735, 307, "套用", 12, "#777", 700, "middle"), ln(500, 336, 770, 336, "#e0e0e0")]
    for i, (k, v) in enumerate([("小計", "NT$ 2,752"), ("首購折扣 HELLO", "- NT$ 275"), ("運費", "NT$ 60")]):
        y = 362 + i * 24
        b += [t(500, y, k, 12, "#555"), t(770, y, v, 12, SAGE if i == 1 else "#111", 700 if i == 1 else 400, "end")]
    b += [ln(500, 426, 770, 426, "#e0e0e0"), t(500, 456, "總計", 16, "#111", 900), t(700, 456, "TWD", 10, "#777", 400, "end"),
          t(770, 458, "NT$ 2,537", 20, "#111", 900, "end"), t(500, 482, "已含稅 · 預估 2–3 個工作天到貨", 10, "#777")]
    return svg("".join(b))


def scene_shopify_admin():
    defs = lin_grad("sa", "#5f7a61", "#5f7a61", True, 0.35, 0)
    b = [r(0, 36, 800, 464, "#f1f1f1"), browser_bar("lumi-tw.myshopify.com/admin/analytics"), r(0, 36, 800, 40, "#1a1a1a"),
         t(20, 61, "LUMI 商店後台", 12, "#fff", 700), r(250, 44, 300, 24, "#303030", 8), t(266, 60, "搜尋", 11, "#a3a3a3"),
         avatar(770, 56, 12, SAND, "LU", 9), r(0, 76, 170, 424, "#ebebeb")]
    nav = ["首頁", "訂單", "商品", "顧客", "內容", "數據分析", "行銷", "折扣"]
    for i, s in enumerate(nav):
        y = 104 + i * 30
        if i == 5:
            b.append(r(8, y - 17, 154, 26, "#fff", 8))
        b.append(t(36, y, s, 12, "#1a1a1a", 700 if i == 5 else 500))
        b.append(r(16, y - 10, 12, 12, "#8a8a8a" if i != 5 else "#1a1a1a", 3))
    b += [pill(120, 120, "12", "#e3e3e3", "#333", 9), t(16, 362, "銷售管道", 11, "#616161", 700), t(36, 388, "線上商店", 12, "#1a1a1a", 500),
          t(36, 414, "POS 門市", 12, "#1a1a1a", 500), r(16, 378, 12, 12, "#8a8a8a", 3), r(16, 404, 12, 12, "#8a8a8a", 3),
          t(190, 106, "數據分析", 18, "#1a1a1a", 900), r(290, 90, 100, 24, "#fff", 8, 'stroke="#d4d4d4"'), t(340, 106, "過去 30 天", 11, "#333", 500, "middle"),
          r(398, 90, 140, 24, "#fff", 8, 'stroke="#d4d4d4"'), t(468, 106, "對比：上一期間", 11, "#333", 500, "middle")]
    kpis = [("總銷售額", "NT$ 486,320", "↑ 18%"), ("工作階段", "18,204", "↑ 9%"), ("轉換率", "3.2%", "↑ 0.4%"), ("平均訂單金額", "NT$ 1,486", "↑ 6%")]
    for i, (k, v, d) in enumerate(kpis):
        x = 190 + i * 147
        b += [r(x, 126, 138, 74, "#fff", 10, 'stroke="#e3e3e3"'), t(x + 12, 146, k, 11, "#616161", 700, extra='text-decoration="underline" text-decoration-style="dotted"'),
              t(x + 12, 172, v, 15, "#1a1a1a", 900), t(x + 12, 190, d, 10, "#0b7a3e", 700),
              sparkline(x + 84, 176, 44, 16, walk(i + 3, 12, 50, 10, 90, -8, 12), SAGE)]
    cur = walk(9, 30, 40, 10, 100, -9, 12)
    prev = walk(17, 30, 35, 10, 90, -9, 9)
    b += [r(190, 212, 380, 270, "#fff", 10, 'stroke="#e3e3e3"'), t(206, 236, "總銷售額隨時間變化", 13, "#1a1a1a", 700),
          t(206, 262, "NT$ 486,320", 20, "#1a1a1a", 900), t(330, 262, "↑ 18%", 11, "#0b7a3e", 700),
          grid_lines(206, 280, 348, 170, 4, "#f0f0f0"), line_chart(206, 280, 348, 170, prev, "#a3b8c9", 1.8, None, 0, 110, dash="5 4"),
          line_chart(206, 280, 348, 170, cur, SAGE, 2.4, "sa", 0, 110),
          r(206, 462, 10, 3, SAGE), t(222, 467, "10/04 前 30 天", 10, "#616161"), r(320, 462, 10, 3, "#a3b8c9"), t(336, 467, "上一期間", 10, "#616161"),
          r(584, 212, 186, 270, "#fff", 10, 'stroke="#e3e3e3"'), t(600, 236, "熱門商品", 13, "#1a1a1a", 700)]
    for i, (name, v) in enumerate([("玫瑰果油精華", 1.0), ("積雪草修護霜", 0.74), ("植萃保濕禮盒", 0.58), ("洋甘菊潔顏乳", 0.41), ("身體乳 200ml", 0.27)]):
        y = 266 + i * 42
        b += [t(600, y, name, 11.5, "#1a1a1a", 500), progress(600, y + 8, 150, 8, v, SAGE, "#eef2ec"), t(754, y, f"{int(v * 412)} 件", 10, "#616161", 400, "end")]
    return svg("".join(b), defs)


def scene_shopify_theme():
    b = [r(0, 0, 800, 500, "#e3e3e3"), r(0, 0, 800, 44, "#1a1a1a"), t(18, 27, "← 結束", 12, "#fff", 500), t(110, 27, "LUMI · 主題自訂", 12, "#fff", 700),
         r(330, 10, 140, 24, "#303030", 6), t(400, 27, "首頁 ▾", 12, "#fff", 500, "middle"), t(620, 27, "□ ▭ ▯", 12, "#a3a3a3"),
         r(680, 10, 50, 24, "#303030", 6), t(705, 27, "預覽", 11, "#fff", 500, "middle"), r(738, 10, 52, 24, "#fff", 6), t(764, 27, "儲存", 11, "#111", 700, "middle"),
         r(0, 44, 210, 456, "#fff"), t(16, 72, "首頁", 14, "#111", 900), t(16, 98, "頁首", 10, "#616161", 700)]
    sections = ["公告列", "頁首", "圖片橫幅", "精選商品系列", "圖文並排", "顧客評價", "電子報"]
    for i, s in enumerate(sections):
        y = 124 + i * 34
        if i == 2:
            b.append(r(8, y - 19, 194, 30, "#f1f1f1", 6))
        b += [r(18, y - 11, 14, 14, "#8a8a8a" if i != 2 else "#1a1a1a", 3), t(42, y, s, 12, "#111", 700 if i == 2 else 400), t(190, y, "◉", 10, "#a3a3a3", 400, "end")]
        if i == 1:
            b.append(t(16, y + 24, "範本", 10, "#616161", 700))
    b += [t(42, 380, "＋ 新增區段", 12, "#2c6ecb", 700), ln(0, 404, 210, 404, "#eee"), t(16, 430, "頁尾", 10, "#616161", 700),
          r(18, 448, 14, 14, "#8a8a8a", 3), t(42, 459, "頁尾", 12, "#111"),
          r(222, 56, 336, 432, "#fff", 4, 'filter="url(#sh)"'),
          f'<g transform="translate(222 40) scale(0.42)">{"".join(lumi_home_body()[2:])}</g>',
          r(222, 84, 336, 96, "none", 0, 'stroke="#2c6ecb" stroke-width="2"'), r(222, 70, 62, 16, "#2c6ecb", 2), t(253, 82, "圖片橫幅", 9, "#fff", 700, "middle"),
          r(570, 44, 230, 456, "#fff"), t(586, 72, "圖片橫幅", 14, "#111", 900), t(586, 100, "圖片", 11, "#616161", 700),
          r(586, 108, 198, 70, "#efe7da", 8), bottle(650, 146, 0.4, SAND, SAGE_DARK, 0), bottle(690, 148, 0.4, "#e8d5c4", SAGE_DARK, 2),
          outline_btn(724, 132, 50, 22, "更換", "#555", 10, 6),
          field(586, 196, 198, "標題", "回歸肌膚本來的光", 30), field(586, 252, 198, "按鈕標籤", "立即選購", 30),
          t(586, 316, "色彩配置", 11, "#475569", 700)]
    for i, col in enumerate([CREAM, "#efe7da", SAGE_DARK, "#fff"]):
        b.append(r(586 + i * 40, 326, 32, 32, col, 6, f'stroke="{"#2c6ecb" if i == 1 else "#ddd"}" stroke-width="{2 if i == 1 else 1}"'))
    b += [t(586, 384, "橫幅高度", 11, "#475569", 700), r(586, 392, 198, 30, "#fff", 6, 'stroke="#cbd5e1"'), t(596, 412, "大", 12, "#111"), t(774, 412, "▾", 11, "#555", 400, "end"),
          t(586, 448, "圖片疊加不透明度", 11, "#475569", 700), t(784, 448, "20%", 11, "#111", 700, "end"),
          ln(590, 468, 780, 468, "#ddd", 4), ln(590, 468, 628, 468, "#1a1a1a", 4), c(628, 468, 7, "#fff", 'stroke="#1a1a1a" stroke-width="2"')]
    return svg("".join(b))


# ================= WooCommerce：山嵐茶行 =================
TEA_GREEN, TEA_GOLD, PAPER, SEAL = "#1f4d3a", "#c8a24a", "#f7f3ea", "#b91c1c"


def tea_can(cx, cy, s=1.0, color=TEA_GREEN, label="烏龍"):
    shape = (r(-30, -40, 60, 86, color, 6) + r(-32, -48, 64, 14, "#0f2a1f", 4) + r(-30, -10, 60, 34, PAPER)
             + t(0, 4, label[0], 13, "#3b3b3b", 900, "middle") + t(0, 20, label[1] if len(label) > 1 else "", 13, "#3b3b3b", 900, "middle")
             + r(18, -8, 6, 30, SEAL, 1))
    return f'<g transform="translate({cx} {cy}) scale({s})">{shape}</g>'


def tea_header(url, active=-1):
    b = [r(0, 36, 800, 464, PAPER), browser_bar(url), r(0, 36, 800, 56, "#fff"), r(32, 46, 36, 36, SEAL, 4),
         t(50, 62, "山", 13, "#fff", 900, "middle"), t(50, 78, "嵐", 13, "#fff", 900, "middle"), t(78, 72, "山嵐茶行", 18, TEA_GREEN, 900)]
    for i, s in enumerate(["首頁", "線上購茶", "茶知識", "關於茶園", "聯絡我們"]):
        x = 330 + i * 72
        b.append(t(x, 70, s, 12.5, TEA_GREEN if i == active else "#555", 700 if i == active else 400))
        if i == active:
            b.append(r(x, 78, tw(s, 12.5), 2, TEA_GOLD))
    b += [r(700, 54, 68, 26, TEA_GREEN, 13), t(734, 71, "購物車 1", 11, "#fff", 700, "middle"), ln(0, 92, 800, 92, "#e7dfcc")]
    return b


def mountains(y0, w=800):
    return (poly([(0, y0 + 120), (120, y0 + 30), (230, y0 + 100), (360, y0 + 10), (500, y0 + 110), (620, y0 + 40), (800, y0 + 120)], "#9fbfa8")
            + poly([(0, y0 + 150), (160, y0 + 70), (300, y0 + 140), (460, y0 + 60), (640, y0 + 150), (800, y0 + 90), (800, y0 + 180), (0, y0 + 180)], "#5d8c6c")
            + poly([(0, y0 + 190), (200, y0 + 120), (420, y0 + 190), (620, y0 + 130), (800, y0 + 200), (800, y0 + 240), (0, y0 + 240)], TEA_GREEN))


def scene_woo_home():
    defs = lin_grad("sky", "#f4ead2", "#e3ecdf")
    b = tea_header("shanlan-tea.tw", 0) + [r(0, 92, 800, 240, "url(#sky)"), c(640, 140, 34, "#f5d48a", 'opacity="0.8"'), mountains(92),
                                          r(0, 232, 800, 22, "#fff", 0, 'opacity="0.35"'), t(48, 160, "高山好茶", 42, TEA_GREEN, 900),
                                          t(48, 196, "產地直送 · 新鮮現焙", 18, "#3f5f4f", 700), btn(48, 212, 120, 34, "線上購茶", TEA_GOLD, size=13, rx=4)]
    b += [t(400, 364, "— 本季推薦 —", 15, TEA_GREEN, 900, "middle")]
    prods = [(("阿里山", "高山烏龍"), "580", "烏龍", TEA_GREEN), (("日月潭", "紅玉紅茶"), "520", "紅玉", "#7f1d1d"),
             (("三峽", "碧螺春"), "450", "綠茶", "#4d7c0f"), (("凍頂", "炭焙烏龍"), "680", "炭焙", "#3f2d20")]
    for i, (name, price, lab, col) in enumerate(prods):
        x = 48 + i * 182
        b += [r(x, 378, 166, 114, "#fff", 6, 'stroke="#e7dfcc"'), tea_can(x + 44, 430, 0.62, col, lab), t(x + 84, 418, name[0], 12, "#333", 700),
              t(x + 84, 434, name[1], 12, "#333", 700), t(x + 84, 458, "NT$ " + price, 13, SEAL, 900), t(x + 84, 478, "加入購物車 ›", 10, TEA_GREEN, 700)]
    return svg("".join(b), defs)


def scene_woo_shop():
    b = tea_header("shanlan-tea.tw/shop", 1) + [r(0, 92, 800, 56, "#efe6d2"), t(32, 128, "線上購茶", 20, TEA_GREEN, 900),
                                               t(768, 126, "首頁 / 商店 / 烏龍茶", 11, "#8a7d5f", 400, "end"),
                                               t(32, 174, "顯示 1–6 筆，共 12 筆結果", 11, "#777"), r(432, 160, 120, 22, "#fff", 4, 'stroke="#d9cfb8"'),
                                               t(442, 175, "依熱銷程度排序 ▾", 10, "#555")]
    prods = [("阿里山高山烏龍", "680", "580", "烏龍", TEA_GREEN, True), ("梨山高冷烏龍", "980", None, "梨山", "#14532d", False),
             ("杉林溪烏龍茶", "620", None, "杉林", "#166534", False), ("凍頂炭焙烏龍", "780", "680", "炭焙", "#3f2d20", True),
             ("東方美人茶", "880", None, "美人", "#92400e", False), ("文山包種茶", "520", None, "包種", "#4d7c0f", False)]
    for i, (name, price, sale, lab, col, on_sale) in enumerate(prods):
        x, y = 32 + (i % 3) * 176, 194 + (i // 3) * 152
        b += [r(x, y, 164, 142, "#fff", 4, 'stroke="#e7dfcc"'), r(x + 8, y + 8, 148, 66, "#f3eddf", 2), tea_can(x + 82, y + 44, 0.52, col, lab),
              t(x + 82, y + 94, name, 12, "#333", 700, "middle")]
        if on_sale:
            b += [c(x + 18, y + 14, 16, TEA_GOLD), t(x + 18, y + 18, "特價", 9, "#fff", 900, "middle"),
                  t(x + 66, y + 114, "$" + price, 11, "#999", 400, "middle", extra='text-decoration="line-through"'), t(x + 104, y + 114, "NT$ " + sale, 12, SEAL, 900, "middle")]
        else:
            b.append(t(x + 82, y + 114, "NT$ " + price, 12, SEAL, 900, "middle"))
        b.append(btn(x + 37, y + 122, 90, 16, "加入購物車", TEA_GREEN, size=9, rx=2))
    b += [r(572, 160, 196, 152, "#fff", 4, 'stroke="#e7dfcc"'), t(588, 184, "商品分類", 13, TEA_GREEN, 900), r(588, 192, 30, 2, TEA_GOLD)]
    for i, (s, n) in enumerate([("烏龍茶", 12), ("紅茶", 8), ("綠茶", 6), ("禮盒組", 5), ("茶具", 9)]):
        y = 216 + i * 21
        b += [t(588, y, "› " + s, 11.5, TEA_GREEN if i == 0 else "#555", 700 if i == 0 else 400), t(752, y, f"({n})", 10.5, "#999", 400, "end")]
    b += [r(572, 322, 196, 84, "#fff", 4, 'stroke="#e7dfcc"'), t(588, 346, "依價格篩選", 13, TEA_GREEN, 900),
          ln(592, 366, 748, 366, "#e7dfcc", 4), ln(612, 366, 712, 366, TEA_GREEN, 4), c(612, 366, 6, TEA_GREEN), c(712, 366, 6, TEA_GREEN),
          t(588, 394, "價格：$400 — $900", 10.5, "#555"), btn(700, 380, 54, 20, "篩選", TEA_GREEN, size=10, rx=2),
          r(572, 416, 196, 74, "#fff", 4, 'stroke="#e7dfcc"'), t(588, 440, "熱門標籤", 13, TEA_GREEN, 900)]
    x = 588
    for tag in ["高山茶", "清香", "送禮", "冷泡"]:
        b.append(pill(x, 452, tag, "#f3eddf", "#6b5b3e", 10))
        x += tw(tag, 10) + 22
    return svg("".join(b))


def scene_woo_product():
    b = tea_header("shanlan-tea.tw/product/alishan-oolong", 1) + [t(32, 116, "首頁 / 烏龍茶 / 阿里山高山烏龍茶", 11, "#8a7d5f"),
                                                                  r(32, 128, 330, 250, "#efe6d2", 6),
                                                                  c(200, 240, 90, "#e3d6b8"), tea_can(197, 254, 1.6, TEA_GREEN, "烏龍"),
                                                                  c(60, 156, 20, TEA_GOLD), t(60, 161, "特價", 11, "#fff", 900, "middle")]
    b += [t(392, 152, "阿里山高山烏龍茶 150g", 22, "#2b2b2b", 900), t(392, 178, "★★★★★ （12 則顧客評價）", 11.5, TEA_GOLD),
          t(392, 214, "$680", 15, "#999", 400, extra='text-decoration="line-through"'), t(440, 216, "NT$ 580", 24, SEAL, 900),
          t(392, 246, "海拔 1,400 公尺手採一心二葉，輕焙火保留花果香，", 12, "#555"),
          t(392, 266, "茶湯金黃透亮，入口甘潤、喉韻悠長。", 12, "#555"),
          t(392, 300, "規格", 12, "#333", 700), r(440, 284, 200, 28, "#fff", 2, 'stroke="#cfc4a8"'), t(452, 303, "150g（半斤）", 12, "#333"), t(628, 303, "▾", 11, "#555", 400, "end"),
          r(392, 326, 70, 36, "#fff", 2, 'stroke="#cfc4a8"'), t(427, 349, "1", 13, "#333", 700, "middle"), btn(472, 326, 168, 36, "加入購物車", TEA_GREEN, size=13, rx=2),
          t(392, 388, "貨號：ALS-150　分類：烏龍茶　標籤：高山茶、清香", 10.5, "#8a7d5f"), ln(32, 404, 768, 404, "#e7dfcc")]
    for i, s in enumerate(["描述", "額外資訊", "評價 (12)"]):
        x = 32 + i * 96
        b += [r(x, 404, 90, 26, "#fff" if i == 0 else "#efe6d2", 0, 'stroke="#e7dfcc"'), t(x + 45, 422, s, 11.5, TEA_GREEN if i == 0 else "#777", 700, "middle")]
    b += [t(32, 452, "風味表現", 12, "#333", 700)]
    for i, (k, v) in enumerate([("花香", 0.85), ("甘醇", 0.9), ("回甘", 0.8), ("焙火", 0.35)]):
        x = 110 + i * 168
        b += [t(x, 452, k, 11, "#555"), progress(x + 32, 444, 110, 8, v, TEA_GOLD, "#efe6d2")]
    b += [t(32, 480, "冲泡建議：95°C 熱水 150ml，茶葉 5g，第一泡 50 秒，可回沖 5–6 次。", 11, "#777")]
    return svg("".join(b))


def scene_woo_checkout():
    b = tea_header("shanlan-tea.tw/checkout") + [t(32, 126, "結帳", 22, TEA_GREEN, 900),
                                                r(32, 138, 736, 28, "#efe6d2", 2), r(32, 138, 3, 28, TEA_GOLD),
                                                t(46, 157, "有優惠券嗎？點此輸入您的優惠代碼", 11.5, "#555"), t(32, 190, "帳單明細", 14, "#2b2b2b", 900)]
    fields = [("名字 *", "怡君", 32, 212, 172), ("姓氏 *", "林", 214, 212, 172), ("地址 *", "台中市西區民生路 368 巷 12 號", 32, 262, 354),
              ("縣市 *", "台中市", 32, 312, 172), ("郵遞區號 *", "403", 214, 312, 172), ("電話 *", "0912-345-678", 32, 362, 172),
              ("電子郵件 *", "amber.lin@gmail.com", 214, 362, 172)]
    for lab, val, x, y, w in fields:
        b.append(field(x, y, w, lab, val, 28, size=11.5))
    b += [t(32, 422, "訂單備註（選填）", 11, "#475569", 700), r(32, 430, 354, 56, "#fff", 6, 'stroke="#cbd5e1"'), t(42, 450, "請於平日白天配送，謝謝。", 11, "#94a3b8"),
          r(408, 180, 360, 310, "#fff", 4, 'stroke="#e7dfcc"'), t(424, 206, "您的訂單", 14, "#2b2b2b", 900)]
    rows = [("阿里山高山烏龍茶 150g × 2", "NT$ 1,160"), ("日月潭紅玉紅茶 75g × 1", "NT$ 520"), ("運費", "NT$ 0（滿千免運）"), ("合計", "NT$ 1,680")]
    for i, (k, v) in enumerate(rows):
        y = 234 + i * 24
        last = i == 3
        b += [t(424, y, k, 11.5, "#2b2b2b" if last else "#555", 900 if last else 400), t(752, y, v, 11.5, SEAL if last else "#333", 900 if last else 400, "end"),
              ln(424, y + 8, 752, y + 8, "#f0e9da")]
    for i, s in enumerate(["信用卡線上刷卡", "ATM 虛擬帳號", "超商代碼繳費", "貨到付款"]):
        y = 344 + i * 22 + (34 if i > 0 else 0)
        b += [radio(432, y - 4, i == 0, TEA_GREEN, 6), t(446, y, s, 11.5, "#333", 700 if i == 0 else 400)]
        if i == 0:
            b += [r(446, y + 6, 306, 26, "#f3eddf", 2), t(456, y + 23, "支援 VISA / Master / JCB，可分 3、6 期零利率", 10, "#6b5b3e")]
    b += [checkbox(424, 452, True, TEA_GREEN, 12), t(442, 462, "我已閱讀並同意網站條款", 10.5, "#555"), btn(632, 448, 120, 32, "下單購買", TEA_GOLD, size=13, rx=2)]
    return svg("".join(b))


def scene_woo_admin():
    defs = lin_grad("wa", "#2271b1", "#2271b1", True, 0.25, 0)
    b = [r(0, 36, 800, 464, "#f0f0f1"), browser_bar("shanlan-tea.tw/wp-admin/admin.php?page=wc-admin"), r(0, 36, 800, 26, "#1d2327"),
         t(12, 53, "⌂ 山嵐茶行", 11, "#f0f0f1", 500), t(100, 53, "＋ 新增", 11, "#f0f0f1", 500), t(788, 53, "你好，Sean", 11, "#f0f0f1", 500, "end"),
         r(0, 62, 150, 438, "#1d2327")]
    menu = ["控制台", "文章", "媒體", "頁面", "留言", "WooCommerce", "商品", "數據分析", "行銷", "外觀", "外掛", "使用者", "設定"]
    for i, s in enumerate(menu):
        y = 84 + i * 30
        if i == 7:
            b.append(r(0, y - 19, 150, 28, "#2271b1"))
        b += [r(12, y - 11, 12, 12, "#a7aaad" if i != 7 else "#fff", 2), t(32, y, s, 11.5, "#fff" if i == 7 else "#c3c4c7", 700 if i in (5, 7) else 400)]
    b += [r(150, 62, 650, 38, "#fff"), t(168, 87, "數據分析 › 總覽", 14, "#1d2327", 700), r(560, 70, 220, 24, "#fff", 2, 'stroke="#8c8f94"'),
          t(570, 86, "本月（9/1 – 9/30）vs 上個月", 10.5, "#1d2327")]
    kpis = [("總銷售額", "NT$ 328,460", "18%"), ("訂單", "412", "9%"), ("售出商品", "1,086", "12%"), ("平均訂單價值", "NT$ 797", "6%")]
    for i, (k, v, d) in enumerate(kpis):
        x = 166 + i * 152
        b += [r(x, 112, 148, 78, "#fff", 0, 'stroke="#dcdcde"'), t(x + 14, 134, k, 11, "#50575e"), t(x + 14, 162, v, 17, "#1d2327", 700),
              r(x + 14, 170, 46, 14, "#edfaef", 2), t(x + 37, 181, "↑ " + d, 9.5, "#00a32a", 700, "middle")]
    cur = walk(23, 30, 40, 10, 100, -10, 12)
    prev = walk(5, 30, 35, 10, 90, -9, 9)
    b += [r(166, 202, 604, 150, "#fff", 0, 'stroke="#dcdcde"'), t(182, 224, "淨銷售額", 12, "#1d2327", 700),
          r(560, 214, 10, 10, "#2271b1"), t(576, 223, "本月", 10, "#50575e"), r(620, 214, 10, 10, "#c3c4c7"), t(636, 223, "上個月", 10, "#50575e"),
          grid_lines(182, 236, 572, 100, 4, "#f0f0f1"), line_chart(182, 236, 572, 100, prev, "#c3c4c7", 1.8, None, 0, 110),
          line_chart(182, 236, 572, 100, cur, "#2271b1", 2.4, "wa", 0, 110),
          r(166, 362, 604, 128, "#fff", 0, 'stroke="#dcdcde"'), t(182, 384, "熱銷商品排行", 12, "#1d2327", 700)]
    rows = [["阿里山高山烏龍茶 150g", "318", "NT$ 184,440"], ["日月潭紅玉紅茶 75g", "206", "NT$ 107,120"],
            ["凍頂炭焙烏龍 150g", "142", "NT$ 96,560"]]
    b.append(table(182, 392, [300, 120, 152], ["商品", "售出件數", "淨銷售額"], rows, 22, 22, "#f6f7f7", "#50575e", "#2271b1",
                   None, "#f0f0f1", 11, ["start", "end", "end"]))
    return svg("".join(b), defs)


# ================= WordPress：木日室內設計 =================
CHAR, TERRA, OFFWHITE, SAND2 = "#222222", "#b5653f", "#f5f2ed", "#d9c7b0"
ROOM_PALETTES = [("#e9e2d6", "#c8b79c", "#7d8b74", "#b5653f"), ("#dfe5e8", "#a9b7bf", "#3d5a6c", "#d9a441"),
                 ("#efe8e1", "#bfa58a", "#5a4636", "#8a9a5b"), ("#e6e1ea", "#b8aec4", "#4b3f63", "#c97b84"),
                 ("#e3ebe1", "#a7b8a0", "#2f4f3f", "#d4a373"), ("#f1ebe3", "#d6c2a8", "#333333", "#b5653f")]


def room(x, y, w, h, palette=0):
    wall, floor, sofa, accent = ROOM_PALETTES[palette % len(ROOM_PALETTES)]
    fy = y + h * 0.68
    out = [f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice">',
           r(0, 0, 400, 240, wall), r(0, 163, 400, 77, floor), ln(0, 163, 400, 163, "#00000022", 2),
           r(230, 26, 120, 100, "#f8fbff", 2, 'stroke="#ffffff" stroke-width="6"'), ln(290, 26, 290, 126, "#ffffff", 4), ln(230, 76, 350, 76, "#ffffff", 4),
           r(60, 40, 70, 50, accent, 2, 'opacity="0.85"'), r(66, 46, 58, 38, "#f5f2ed", 1, 'opacity="0.35"'),
           r(40, 120, 190, 50, sofa, 14), r(30, 104, 210, 34, sofa, 14, 'opacity="0.9"'), r(52, 112, 70, 26, "#ffffff", 8, 'opacity="0.25"'),
           r(48, 168, 8, 14, "#3b3b3b"), r(214, 168, 8, 14, "#3b3b3b"), ln(300, 98, 300, 182, "#3b3b3b", 3), path("M280 98 h40 l-10 -26 h-20z", accent),
           r(355, 150, 26, 30, "#8b5e34", 3), '<ellipse cx="362" cy="134" rx="10" ry="22" fill="#4d7c5a"/>',
           '<ellipse cx="376" cy="138" rx="9" ry="18" fill="#5f9470"/>', '<ellipse cx="130" cy="214" rx="100" ry="14" fill="#00000014"/>',
           r(110, 186, 80, 10, "#6b4f3a", 3), "</svg>"]
    return "".join(out)


def muri_header(url, active=-1, dark=False):
    color = "#fff" if dark else CHAR
    b = [] if dark else [r(0, 36, 800, 52, "#fff"), ln(0, 88, 800, 88, "#eee")]
    b += [t(32, 68, "MURI", 18, color, 900, extra='letter-spacing="4"'), t(98, 68, "木日室內設計", 12, color, 500)]
    for i, s in enumerate(["作品案例", "服務項目", "設計日誌", "關於我們"]):
        x = 420 + i * 72
        b.append(t(x, 67, s, 12, color, 700 if i == active else 400))
        if i == active:
            b.append(r(x, 75, tw(s, 12), 2, TERRA))
    b.append(btn(712, 50, 64, 26, "聯絡", TERRA, size=11, rx=2))
    return b


def scene_wp_home():
    defs = lin_grad("ov", "#000000", "#000000", False, 0.62, 0)
    b = [r(0, 36, 800, 464, OFFWHITE), browser_bar("muri-interior.tw"), room(0, 36, 800, 300, 0), r(0, 36, 800, 300, "url(#ov)")]
    b += muri_header("", -1, True)
    b += [t(40, 170, "讓家，", 34, "#fff", 900), t(40, 214, "成為最想回去的地方", 34, "#fff", 900),
          t(40, 244, "住宅 · 商業空間 · 老屋翻新｜從丈量到完工一站式服務", 13, "#eee"),
          btn(40, 266, 132, 38, "預約免費諮詢", TERRA, size=13, rx=2), outline_btn(184, 266, 100, 38, "看作品", "#fff", 13, 2)]
    stats = [("120+", "完成案例"), ("12 年", "設計經驗"), ("4.9 ★", "客戶評價"), ("100%", "透明報價")]
    for i, (v, k) in enumerate(stats):
        x = 40 + i * 186
        b += [t(x, 386, v, 30, CHAR, 900), t(x, 410, k, 12, "#777"), r(x, 424, 28, 3, TERRA)]
    b += [t(40, 462, "我們相信好的設計，是讓生活自然發生。", 13, "#555"), t(760, 462, "了解我們的設計流程 →", 12, TERRA, 700, "end")]
    return svg("".join(b), defs)


def scene_wp_portfolio():
    b = [r(0, 36, 800, 464, OFFWHITE), browser_bar("muri-interior.tw/projects")] + muri_header("", 0)
    b += [t(40, 128, "作品案例", 24, CHAR, 900), t(150, 128, "PROJECTS", 12, TERRA, 700, extra='letter-spacing="3"')]
    for i, s in enumerate(["全部", "住宅", "商業空間", "老屋翻新", "小坪數"]):
        x = 420 + i * 70
        b.append(btn(x, 110, 62, 24, s, CHAR, size=11, rx=2) if i == 0 else outline_btn(x, 110, 62, 24, s, "#999", 11, 2))
    caps = [("北歐暖木宅", "住宅 · 32 坪 · 台中"), ("湖水藍工作室", "商空 · 18 坪 · 台北"), ("老屋新生", "翻新 · 40 年公寓 · 台南"),
            ("紫藤小宅", "小坪數 · 12 坪 · 新北"), ("森林系民宿", "商空 · 6 間客房 · 南投"), ("極簡灰階宅", "住宅 · 28 坪 · 高雄")]
    for i, (name, meta) in enumerate(caps):
        x, y = 40 + (i % 3) * 244, 150 + (i // 3) * 172
        b += [room(x, y, 232, 120, i), r(x, y + 120, 232, 44, "#fff"), t(x + 12, y + 140, name, 13, CHAR, 900), t(x + 12, y + 157, meta, 10.5, "#888")]
    return svg("".join(b))


def scene_wp_blog():
    b = [r(0, 36, 800, 464, OFFWHITE), browser_bar("muri-interior.tw/blog")] + muri_header("", 2)
    b += [t(40, 128, "設計日誌", 24, CHAR, 900), t(150, 128, "JOURNAL", 12, TERRA, 700, extra='letter-spacing="3"')]
    posts = [("收納技巧", "小坪數也能很寬敞：5 個收納設計重點", "從畸零空間到隱藏式櫃體，讓 12 坪住出 20 坪的感覺。", "2026.09.28 · 閱讀 5 分鐘", 3),
             ("裝修知識", "第一次裝潢就上手：預算怎麼抓才不超支？", "整理 120 個案例的真實花費，教你分配木作、系統櫃與軟裝。", "2026.09.15 · 閱讀 8 分鐘", 2),
             ("風格提案", "2026 居家配色趨勢：大地色的溫柔回歸", "奶茶、陶土與橄欖綠，打造療癒又耐看的空間。", "2026.09.02 · 閱讀 4 分鐘", 4)]
    for i, (cat, title, ex, meta, pal) in enumerate(posts):
        y = 148 + i * 116
        b += [room(40, y, 170, 104, pal), pill(226, y + 4, cat, "#f3e2d8", TERRA, 10), t(226, y + 44, title, 15, CHAR, 900),
              t(226, y + 68, ex, 11.5, "#666"), t(226, y + 94, meta, 10.5, "#999"), ln(40, y + 110, 540, y + 110, "#e6e0d7")]
    b += [r(568, 112, 200, 34, "#fff", 2, 'stroke="#ddd"'), t(580, 134, "搜尋文章…", 11, "#aaa"), t(752, 134, "⌕", 13, "#555", 700, "end"),
          t(568, 176, "分類", 13, CHAR, 900)]
    for i, (s, n) in enumerate([("收納技巧", 18), ("裝修知識", 24), ("風格提案", 15), ("案例分享", 31)]):
        b += [t(568, 200 + i * 22, s, 11.5, "#555"), t(768, 200 + i * 22, n, 11, "#999", 400, "end")]
    b += [t(568, 304, "熱門文章", 13, CHAR, 900)]
    for i, s in enumerate(["系統櫃 vs 木作櫃怎麼選？", "老屋翻新必看的 7 個步驟", "挑高夾層的安全規範"]):
        b += [t(568, 330 + i * 24, f"{i + 1:02d}", 12, TERRA, 900), t(592, 330 + i * 24, s, 11, "#444")]
    b += [r(568, 404, 200, 86, CHAR, 2), t(582, 428, "訂閱電子報", 13, "#fff", 900), t(582, 446, "每月一封設計靈感", 10.5, "#bbb"),
          r(582, 456, 120, 24, "#fff", 2), t(590, 472, "你的 Email", 10, "#aaa"), btn(706, 456, 50, 24, "訂閱", TERRA, size=10, rx=2)]
    return svg("".join(b))


def scene_wp_post():
    b = [r(0, 36, 800, 464, "#fff"), browser_bar("muri-interior.tw/blog/small-space-storage")] + muri_header("", 2)
    b += [t(40, 112, "首頁 / 設計日誌 / 收納技巧", 10.5, "#999"), pill(40, 122, "收納技巧", "#f3e2d8", TERRA, 10),
          t(40, 168, "小坪數也能很寬敞：5 個收納設計重點", 24, CHAR, 900), avatar(54, 192, 12, SAND2, "A", 11, CHAR),
          t(74, 196, "設計師 Amber · 2026.09.28 · 閱讀 5 分鐘", 11, "#777"), room(40, 212, 520, 120, 3),
          t(40, 358, "很多人以為小坪數就只能犧牲收納，其實只要掌握「垂直、隱藏、多功能」", 12.5, "#333"),
          t(40, 380, "三個原則，12 坪也能住得舒適又整齊。以下整理我們最常用的 5 個做法。", 12.5, "#333"),
          t(40, 414, "1. 善用垂直空間", 16, CHAR, 900), r(40, 428, 4, 50, TERRA), r(44, 428, 516, 50, "#faf6f1"),
          t(58, 450, "「天花板到地板的整面高櫃，能比一般櫃體多出 40% 的收納量。」", 12.5, "#5a4636", 700),
          t(58, 468, "— 木日室內設計 Amber", 10.5, "#999"),
          r(588, 112, 180, 198, "#faf6f1", 4), t(604, 138, "本文目錄", 13, CHAR, 900)]
    for i, s in enumerate(["善用垂直空間", "隱藏式收納", "多功能家具", "畸零空間再利用", "定期斷捨離"]):
        y = 166 + i * 26
        if i == 0:
            b.append(r(596, y - 15, 164, 22, "#f3e2d8", 2))
        b.append(t(606, y, f"{i + 1}. {s}", 11.5, TERRA if i == 0 else "#555", 700 if i == 0 else 400))
    b += [t(588, 342, "分享這篇文章", 12, CHAR, 900)]
    for i, (s, col) in enumerate([("f", "#1877f2"), ("L", "#06c755"), ("⧉", "#555")]):
        b += [c(604 + i * 40, 368, 15, col), t(604 + i * 40, 373, s, 13, "#fff", 900, "middle")]
    b += [r(588, 402, 180, 88, CHAR, 4), t(604, 428, "想打造這樣的家？", 13, "#fff", 900), t(604, 448, "免費到府丈量與報價", 10.5, "#bbb"),
          btn(604, 458, 148, 24, "預約諮詢 →", TERRA, size=11, rx=2)]
    return svg("".join(b))


def scene_wp_editor():
    b = [r(0, 0, 800, 500, "#fff"), r(0, 0, 800, 52, "#fff"), ln(0, 52, 800, 52, "#e0e0e0"), r(0, 0, 52, 52, "#1e1e1e"),
         t(26, 33, "W", 18, "#fff", 900, "middle"), r(64, 12, 28, 28, "#3858e9", 2), t(78, 32, "+", 18, "#fff", 700, "middle"),
         t(108, 32, "✎   ↶   ↷   ≡", 14, "#1e1e1e"), r(260, 12, 280, 28, "#f0f0f0", 2), t(400, 31, "小坪數也能很寬敞 · 文章", 11, "#1e1e1e", 500, "middle"),
         t(580, 31, "儲存草稿", 11, "#3858e9", 500), t(656, 31, "預覽", 11, "#1e1e1e", 500), btn(694, 12, 60, 28, "發佈", "#3858e9", size=12, rx=2),
         t(778, 32, "⚙", 15, "#1e1e1e", 400, "middle"), r(0, 52, 560, 448, "#fff"),
         t(80, 108, "小坪數也能很寬敞：5 個收納設計重點", 22, "#1e1e1e", 900),
         t(80, 140, "很多人以為小坪數就只能犧牲收納，其實只要掌握「垂直、隱藏、", 12.5, "#1e1e1e"),
         t(80, 160, "多功能」三個原則，12 坪也能住得舒適又整齊。", 12.5, "#1e1e1e"),
         room(80, 186, 400, 130, 3), r(78, 184, 404, 134, "none", 0, 'stroke="#3858e9" stroke-width="2"'),
         shadow(r(80, 148, 230, 30, "#fff", 2)), r(80, 148, 230, 30, "none", 2, 'stroke="#1e1e1e"'),
         t(96, 168, "▣   ↕   ⬚   ≡   ⧉   ⋮", 12, "#1e1e1e"), t(80, 336, "圖片說明：12 坪北歐小宅的整面收納牆", 10.5, "#757575"),
         t(80, 370, "1. 善用垂直空間", 17, "#1e1e1e", 900), t(80, 398, "天花板到地板的整面高櫃，能比一般櫃體多出 40% 的收納量…", 12.5, "#1e1e1e"),
         shadow(r(300, 402, 220, 92, "#fff", 4)), t(312, 422, "輸入 / 選擇區塊", 10, "#757575")]
    for i, s in enumerate(["段落", "標題", "圖片", "圖庫", "清單", "引言", "按鈕", "表格"]):
        x, y = 312 + (i % 4) * 52, 434 + (i // 4) * 30
        b += [r(x, y, 46, 24, "#f0f0f0" if i else "#e7ecfd", 2), t(x + 23, y + 16, s, 10, "#1e1e1e", 500, "middle")]
    b += [r(560, 52, 240, 448, "#fff"), ln(560, 52, 560, 500, "#e0e0e0"), t(590, 80, "文章", 12, "#1e1e1e", 700), t(650, 80, "區塊", 12, "#757575"),
          r(580, 86, 50, 3, "#3858e9"), ln(560, 92, 800, 92, "#e0e0e0")]
    for i, (k, v) in enumerate([("可見度", "公開"), ("發佈", "立即"), ("範本", "單篇文章"), ("作者", "Amber")]):
        y = 122 + i * 26
        b += [t(580, y, k, 11.5, "#1e1e1e"), t(780, y, v, 11.5, "#3858e9", 500, "end")]
    b += [ln(560, 222, 800, 222, "#e0e0e0"), t(580, 248, "分類", 12, "#1e1e1e", 700)]
    for i, (s, on) in enumerate([("收納技巧", True), ("小坪數", True), ("裝修知識", False), ("風格提案", False)]):
        y = 262 + i * 22
        b += [checkbox(580, y, on, "#1e1e1e", 12), t(600, y + 10, s, 11, "#1e1e1e")]
    b += [ln(560, 358, 800, 358, "#e0e0e0"), t(580, 382, "標籤", 12, "#1e1e1e", 700)]
    x = 580
    for tag in ["收納", "北歐風", "12 坪"]:
        b.append(pill(x, 392, tag, "#f0f0f0", "#1e1e1e", 10))
        x += tw(tag, 10) + 22
    b += [ln(560, 424, 800, 424, "#e0e0e0"), t(580, 446, "精選圖片", 12, "#1e1e1e", 700), room(580, 454, 120, 40, 0)]
    return svg("".join(b))


SCREENS = {
    "platform-shopify": [scene_shopify_home, scene_shopify_product, scene_shopify_checkout, scene_shopify_admin, scene_shopify_theme],
    "platform-woocommerce": [scene_woo_home, scene_woo_shop, scene_woo_product, scene_woo_checkout, scene_woo_admin],
    "platform-wordpress": [scene_wp_home, scene_wp_portfolio, scene_wp_blog, scene_wp_post, scene_wp_editor],
}
