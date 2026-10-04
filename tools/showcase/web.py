"""網頁設計類作品畫面。"""
import math
import random

from .common import *  # noqa: F401,F403


def scene_cafe() -> str:
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fdf6ec"/>'
            '<stop offset="1" stop-color="#f3e3cc"/></linearGradient>')
    b = [r(0, 36, 800, 464, "url(#bg)"),
         '<circle cx="590" cy="205" r="140" fill="#ecd3b0"/><circle cx="590" cy="205" r="108" fill="#e2bd8c" opacity="0.6"/>',
         browser_bar("morningbrew.tw")]
    b += ['<circle cx="48" cy="67" r="10" fill="#8b5e34"/>', t(66, 73, "晨光咖啡", 18, "#3b2412", 900)]
    for i, s in enumerate(["菜單", "關於我們", "門市據點", "最新消息"]):
        b.append(t(400 + i * 70, 72, s, 13, "#7c5a3a", 500))
    b += [r(686, 54, 88, 28, "#8b5e34", 14), t(730, 73, "立即訂位", 12, "#fff", 700, "middle")]
    b += [t(40, 132, "SINCE 2018 · 台中審計新村", 12, "#b07a45", 700, extra='letter-spacing="2"'),
          t(40, 184, "每一杯，", 42, "#3b2412", 900), t(40, 234, "都是今天的好心情", 36, "#3b2412", 900),
          t(40, 268, "嚴選單品咖啡豆，每日現烘現煮", 14, "#7c5a3a"),
          t(40, 290, "手作甜點 × 安靜角落，陪你度過美好午後", 14, "#7c5a3a"),
          r(40, 310, 124, 40, "#8b5e34", 20), t(102, 335, "查看菜單", 14, "#fff", 700, "middle"),
          r(176, 310, 124, 40, "none", 20, 'stroke="#8b5e34" stroke-width="2"'),
          t(238, 335, "線上訂位", 14, "#8b5e34", 700, "middle")]
    b += ['<ellipse cx="590" cy="292" rx="118" ry="20" fill="#fffaf3" stroke="#d9c2a3" stroke-width="2"/>',
          '<path d="M658 214 q40 0 36 32 q-5 28 -44 30" stroke="#fffaf3" stroke-width="12" fill="none"/>',
          '<path d="M518 196 L662 196 Q658 266 626 288 L554 288 Q522 266 518 196 Z" fill="#fffaf3" stroke="#d9c2a3" stroke-width="2"/>',
          '<ellipse cx="590" cy="198" rx="72" ry="13" fill="#6f4518"/>',
          '<path d="M590 206 c-10 -8 -22 -4 -18 -12 c3 -6 12 -4 18 2 c6 -6 15 -8 18 -2 c4 8 -8 4 -18 12z" fill="#f3e3cc"/>']
    for dx in (-24, 0, 24):
        b.append(f'<path d="M{590+dx} 170 q-12 -18 0 -34 q12 -16 0 -34" stroke="#b07a45" stroke-width="4" '
                 f'fill="none" opacity="0.45" stroke-linecap="round"/>')
    items = [("拿鐵 Latte", "NT$ 120", "#c08552"), ("手沖單品・耶加雪菲", "NT$ 160", "#7a4a26"),
             ("巴斯克乳酪蛋糕", "NT$ 140", "#e9b872")]
    for i, (name, price, color) in enumerate(items):
        x = 40 + i * 248
        b += [r(x, 378, 226, 96, "#fff", 14, 'filter="url(#sh)"'), r(x + 14, 391, 70, 70, color, 12),
              f'<circle cx="{x+49}" cy="426" r="18" fill="#fff" opacity="0.35"/>',
              t(x + 98, 418, name, 14, "#3b2412", 700), t(x + 98, 444, price, 15, "#b07a45", 900),
              t(x + 98, 462, "★ 4.9 · 本週熱銷", 11, "#9b7b5b")]
    return svg("".join(b), defs)


# ---------- 2. 電商購物網站 ----------
def product_art(kind: str, cx: int, cy: int) -> str:
    if kind == "headphone":
        return (f'<path d="M{cx-34} {cy+10} v-12 a34 34 0 0 1 68 0 v12" stroke="#1f2937" stroke-width="8" fill="none"/>'
                + r(cx - 44, cy, 20, 34, "#ff5a5f", 8) + r(cx + 24, cy, 20, 34, "#ff5a5f", 8))
    if kind == "watch":
        return (r(cx - 14, cy - 44, 28, 88, "#334155", 8) + f'<circle cx="{cx}" cy="{cy}" r="28" fill="#0f172a" stroke="#94a3b8" stroke-width="4"/>'
                + f'<path d="M{cx} {cy} v-16 M{cx} {cy} h12" stroke="#22d3ee" stroke-width="3" stroke-linecap="round"/>')
    if kind == "shoe":
        return (f'<path d="M{cx-52} {cy+20} q0 -30 18 -34 q20 8 34 -6 q30 18 52 22 q8 8 0 18 z" fill="#6366f1"/>'
                + r(cx - 54, cy + 18, 108, 10, "#e5e7eb", 5))
    return (f'<path d="M{cx-22} {cy+8} h44 l-6 34 h-32 z" fill="#c2410c"/>'
            f'<ellipse cx="{cx-14}" cy="{cy-14}" rx="10" ry="24" fill="#16a34a" transform="rotate(-25 {cx-14} {cy-14})"/>'
            f'<ellipse cx="{cx+14}" cy="{cy-14}" rx="10" ry="24" fill="#22c55e" transform="rotate(25 {cx+14} {cy-14})"/>'
            f'<ellipse cx="{cx}" cy="{cy-24}" rx="9" ry="22" fill="#15803d"/>')


def scene_shop() -> str:
    defs = ('<linearGradient id="ban" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff7a59"/>'
            '<stop offset="1" stop-color="#ff3d77"/></linearGradient>')
    b = [r(0, 36, 800, 464, "#f5f5f7"), browser_bar("shoply.tw"), r(0, 36, 800, 50, "#fff"),
         t(32, 68, "SHOPLY", 22, "#ff3d77", 900, extra='letter-spacing="1"'),
         r(170, 48, 390, 26, "#f3f4f6", 13), t(188, 65, "搜尋商品、品牌…", 12, "#9ca3af"),
         '<circle cx="545" cy="61" r="10" fill="#ff3d77"/>',
         t(640, 66, "會員中心", 12, "#374151", 500), t(716, 66, "購物車", 12, "#374151", 500),
         '<circle cx="762" cy="52" r="8" fill="#ef4444"/>', t(762, 56, "3", 10, "#fff", 700, "middle"),
         r(0, 86, 800, 28, "#fafafa")]
    for i, s in enumerate(["新品上市", "3C 家電", "居家生活", "美妝保養", "運動戶外", "限時特賣"]):
        b.append(t(32 + i * 92, 105, s, 12, "#ef4444" if i == 5 else "#4b5563", 700 if i == 5 else 400))
    b += [r(32, 124, 736, 128, "url(#ban)", 16),
          '<circle cx="660" cy="150" r="70" fill="#fff" opacity="0.12"/><circle cx="730" cy="230" r="50" fill="#fff" opacity="0.1"/>',
          t(64, 176, "雙 11 限時狂歡", 32, "#fff", 900), t(64, 204, "全館滿千折百 · 指定商品免運到府", 14, "#ffe4ec"),
          r(64, 218, 104, 26, "#fff", 13), t(116, 236, "立即搶購", 12, "#ff3d77", 700, "middle"),
          r(560, 162, 166, 60, "#fff", 12, 'opacity="0.95"'), t(643, 182, "活動倒數", 11, "#ff3d77", 700, "middle"),
          t(643, 210, "02 : 15 : 39", 22, "#111827", 900, "middle", True)]
    prods = [("headphone", "#ffe4e6", "降噪藍牙耳機 Pro", "1,990", "2,690"),
             ("watch", "#e0f2fe", "智慧運動手錶 S2", "3,480", "4,200"),
             ("shoe", "#ede9fe", "輕量慢跑鞋 AirFlow", "1,680", "2,280"),
             ("plant", "#dcfce7", "療癒桌上型盆栽", "390", "520")]
    for i, (kind, bg, name, price, orig) in enumerate(prods):
        x = 32 + i * 186
        b += [r(x, 266, 172, 214, "#fff", 14, 'stroke="#ececec"'), r(x + 10, 276, 152, 104, bg, 10),
              product_art(kind, x + 86, 324), t(x + 12, 402, name, 13, "#111827", 700),
              t(x + 12, 426, "NT$ " + price, 16, "#ef4444", 900),
              t(x + 100, 426, "$" + orig, 11, "#9ca3af", 400, extra='text-decoration="line-through"'),
              t(x + 12, 446, "★★★★★ 4.9（2.1k）", 11, "#f59e0b"),
              r(x + 12, 454, 148, 20, "#fff1f2", 10), t(x + 86, 468, "加入購物車", 11, "#ff3d77", 700, "middle")]
        if i < 2:
            b += [r(x + 16, 282, 40, 18, "#ef4444", 9), t(x + 36, 295, "熱銷", 10, "#fff", 700, "middle")]
    return svg("".join(b), defs)


# ---------- 3. 營運數據後台 ----------
def scene_dashboard() -> str:
    defs = ('<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity="0.45"/>'
            '<stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></linearGradient>')
    b = [r(0, 36, 800, 464, "#0b1220"), browser_bar("admin.yourbrand.tw/dashboard", True), r(0, 36, 160, 464, "#0f172a"),
         '<circle cx="28" cy="66" r="10" fill="#22d3ee"/>', t(46, 71, "營運後台", 15, "#f1f5f9", 900)]
    for i, s in enumerate(["總覽", "訂單管理", "商品管理", "會員分析", "行銷活動", "報表匯出", "系統設定"]):
        y = 106 + i * 36
        if i == 0:
            b.append(r(12, y - 18, 136, 28, "#1e293b", 8) + r(12, y - 18, 3, 28, "#22d3ee"))
        b.append(t(32, y, s, 13, "#f1f5f9" if i == 0 else "#64748b", 700 if i == 0 else 400))
    b += [t(180, 74, "總覽 Dashboard", 18, "#f1f5f9", 900), r(600, 56, 170, 26, "#1e293b", 13),
          t(685, 73, "2026/09/01 – 09/30", 11, "#94a3b8", 400, "middle")]
    kpis = [("本月營收", "NT$ 1,284,500", "▲ 12.4%", "#34d399"), ("訂單數", "3,429", "▲ 8.1%", "#34d399"),
            ("新會員", "862", "▲ 21.3%", "#34d399"), ("轉換率", "3.8%", "▼ 0.4%", "#f87171")]
    for i, (label, val, delta, c) in enumerate(kpis):
        x = 180 + i * 150
        b += [r(x, 94, 140, 76, "#111a2e", 10, 'stroke="#1e293b"'), t(x + 14, 116, label, 11, "#94a3b8"),
              t(x + 14, 142, val, 17 if len(val) < 10 else 15, "#f1f5f9", 900), t(x + 14, 160, delta + " 較上月", 10, c, 700)]
    # 折線圖
    b += [r(180, 184, 380, 182, "#111a2e", 10, 'stroke="#1e293b"'), t(196, 206, "營收趨勢（近 30 天）", 12, "#e2e8f0", 700)]
    x0, y0, w, h = 200, 226, 344, 120
    for k in range(5):
        y = y0 + k * h / 4
        b.append(f'<line x1="{x0}" y1="{y}" x2="{x0+w}" y2="{y}" stroke="#1e293b"/>')
    rnd = random.Random(3)
    vals, v = [], 40
    for i in range(30):
        v += rnd.uniform(-6, 9)
        v = max(15, min(100, v))
        vals.append(v)
    pts = [(x0 + i * w / 29, y0 + h - vals[i] / 100 * h) for i in range(30)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    b += [f'<polygon points="{x0},{y0+h} {line} {x0+w},{y0+h}" fill="url(#area)"/>',
          f'<polyline points="{line}" fill="none" stroke="#22d3ee" stroke-width="2.5" stroke-linejoin="round"/>',
          f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="#22d3ee" stroke="#0b1220" stroke-width="2"/>']
    # 甜甜圈圖
    b += [r(574, 184, 196, 182, "#111a2e", 10, 'stroke="#1e293b"'), t(590, 206, "流量來源", 12, "#e2e8f0", 700)]
    circ = 2 * math.pi * 40
    off = 0
    segs = [(0.45, "#22d3ee", "自然搜尋"), (0.30, "#a78bfa", "社群媒體"), (0.15, "#f472b6", "廣告投放"), (0.10, "#fbbf24", "直接造訪")]
    for frac, col, _ in segs:
        b.append(f'<circle cx="634" cy="282" r="40" fill="none" stroke="{col}" stroke-width="16" '
                 f'stroke-dasharray="{frac*circ:.1f} {circ:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 634 282)"/>')
        off += frac * circ
    b.append(t(634, 287, "12.8k", 13, "#f1f5f9", 900, "middle"))
    for i, (frac, col, name) in enumerate(segs):
        y = 236 + i * 26
        b += [r(690, y - 8, 8, 8, col, 2), t(704, y, name, 10, "#94a3b8"), t(704, y + 12, f"{int(frac*100)}%", 10, "#f1f5f9", 700)]
    # 訂單表格
    b += [r(180, 380, 590, 104, "#111a2e", 10, 'stroke="#1e293b"'), t(196, 401, "最新訂單", 12, "#e2e8f0", 700)]
    rows = [("#20260930-118", "王○明", "NT$ 2,380", "已出貨", "#34d399"), ("#20260930-117", "林○婷", "NT$ 1,190", "處理中", "#fbbf24"),
            ("#20260930-116", "陳○豪", "NT$ 5,640", "已出貨", "#34d399")]
    for i, (oid, name, amt, st, c) in enumerate(rows):
        y = 424 + i * 22
        b += [t(196, y, oid, 11, "#94a3b8", 400, mono=True), t(340, y, name, 11, "#e2e8f0"), t(460, y, amt, 11, "#e2e8f0", 700),
              r(620, y - 12, 56, 17, c, 8, 'opacity="0.18"'), t(648, y, st, 10, c, 700, "middle")]
    return svg("".join(b), defs)


