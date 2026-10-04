"""產生作品展示用的 SVG 示範圖（800x500）。輸出至 images/showcase/。

用法：python tools/gen_showcase.py（僅使用 Python 標準函式庫，無需額外安裝）
"""
import math
import random
from html import escape
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "images" / "showcase"
FONT = "'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif"
MONO = "'JetBrains Mono',Consolas,'Courier New',monospace"
SHADOW = ('<filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
          '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.28"/></filter>')


def svg(body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500" '
            f'font-family="{FONT}"><defs>{SHADOW}{defs}</defs>{body}</svg>\n')


def t(x, y, s, size=12, fill="#111", weight=400, anchor="start", mono=False, extra=""):
    fam = f' font-family="{MONO}"' if mono else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{fam} {extra}>{escape(str(s), quote=False)}</text>')


def r(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def browser_bar(url: str, dark: bool = False) -> str:
    bg, field, txt = ("#1f2937", "#111827", "#9ca3af") if dark else ("#e5e7eb", "#ffffff", "#6b7280")
    return (r(0, 0, 800, 36, bg) + '<circle cx="18" cy="18" r="6" fill="#ff5f57"/>'
            '<circle cx="36" cy="18" r="6" fill="#febc2e"/><circle cx="54" cy="18" r="6" fill="#28c840"/>'
            + r(90, 8, 520, 20, field, 10) + t(106, 22, "🔒 " + url, 11, txt))


# ---------- 1. 咖啡廳形象官網 ----------
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


# ---------- 4. Excel 自動化報表 ----------
def scene_excel() -> str:
    b = [r(0, 0, 800, 500, "#e7ecef"), f'<g filter="url(#sh)">{r(20, 20, 540, 460, "#fff", 8)}</g>',
         r(20, 20, 540, 30, "#217346", 8), r(20, 40, 540, 10, "#217346"),
         t(290, 40, "月報表_2026-09.xlsx - Excel", 12, "#fff", 500, "middle"), r(20, 50, 540, 36, "#f3f3f3")]
    for i, s in enumerate(["常用", "插入", "版面配置", "公式", "資料", "檢視"]):
        b.append(t(36 + i * 62, 73, s, 11, "#217346" if i == 0 else "#444", 700 if i == 0 else 400))
    b += [r(20, 86, 540, 24, "#fff", 0, 'stroke="#ddd"'), t(32, 102, "fx", 11, "#888", 700, mono=True),
          t(56, 102, "=SUMIFS(業績!C:C, 業績!A:A, A3) / C3", 11, "#333", 400, mono=True)]
    cols = [32, 112, 96, 96, 76, 100]
    xs = [20]
    for c in cols:
        xs.append(xs[-1] + c)
    y = 110
    b.append(r(20, y, 512, 22, "#f0f0f0"))
    for i, h in enumerate(["", "A", "B", "C", "D", "E"]):
        b.append(t(xs[i] + cols[i] / 2, y + 15, h, 11, "#666", 400, "middle"))
    data = [("部門", "本月業績", "目標", "達成率", "狀態"),
            ("業務一部", "1,280,000", "1,200,000", "106.7%", "達標"), ("業務二部", "980,000", "1,100,000", "89.1%", "未達"),
            ("業務三部", "1,450,000", "1,300,000", "111.5%", "達標"), ("行銷部", "640,000", "600,000", "106.7%", "達標"),
            ("電商部", "1,920,000", "1,800,000", "106.7%", "達標"), ("通路部", "720,000", "850,000", "84.7%", "未達"),
            ("海外部", "1,060,000", "1,000,000", "106.0%", "達標"), ("企業客戶部", "2,310,000", "2,000,000", "115.5%", "達標"),
            ("新零售部", "430,000", "500,000", "86.0%", "未達"), ("客服加值", "280,000", "250,000", "112.0%", "達標"),
            ("合計", "11,070,000", "10,600,000", "104.4%", "達標")]
    for ri, row in enumerate(data):
        ry = y + 22 + ri * 26
        is_head, is_total = ri == 0, ri == len(data) - 1
        if is_head:
            b.append(r(xs[1], ry, 480, 26, "#217346"))
        elif is_total:
            b.append(r(xs[1], ry, 480, 26, "#e8f3ec"))
        b.append(r(20, ry, 32, 26, "#f0f0f0") + t(36, ry + 17, ri + 1, 10, "#666", 400, "middle"))
        for ci, val in enumerate(row):
            cx = xs[ci + 1]
            if ci == 4 and not is_head:
                ok = val == "達標"
                b.append(r(cx + 2, ry + 3, cols[5] - 4, 20, "#c6efce" if ok else "#ffc7ce", 2))
                b.append(t(cx + cols[5] / 2, ry + 17, val, 11, "#006100" if ok else "#9c0006", 700, "middle"))
                continue
            color = "#fff" if is_head else "#222"
            anchor, tx = ("start", cx + 8) if ci == 0 else ("end", cx + cols[ci + 1] - 8)
            b.append(t(tx, ry + 17, val, 11, color, 700 if is_head or is_total else 400, anchor))
        b.append(f'<line x1="20" y1="{ry+26}" x2="532" y2="{ry+26}" stroke="#e5e5e5"/>')
    for x in xs:
        b.append(f'<line x1="{x}" y1="110" x2="{x}" y2="444" stroke="#e5e5e5"/>')
    b += [r(20, 452, 540, 28, "#f3f3f3", 0)]
    for i, s in enumerate(["總表", "業務部", "行銷部", "圖表"]):
        b.append(r(30 + i * 70, 456, 64, 20, "#fff" if i == 0 else "#f3f3f3", 2) + t(62 + i * 70, 470, s, 10, "#217346" if i == 0 else "#666", 700 if i == 0 else 400, "middle"))
    # 長條圖卡片
    b += [f'<g filter="url(#sh)">{r(578, 24, 202, 214, "#fff", 12)}</g>', t(594, 50, "部門達成率", 13, "#111", 900)]
    bars = [107, 89, 112, 107, 107, 85, 106]
    for i, v in enumerate(bars):
        bh = (v - 60) * 2.6
        bx = 596 + i * 25
        b.append(r(bx, 214 - bh, 16, bh, "#21a366" if v >= 100 else "#f87171", 3))
    b.append('<line x1="590" y1="214" x2="770" y2="214" stroke="#ccc"/><line x1="590" y1="110" x2="770" y2="110" stroke="#f59e0b" stroke-dasharray="4 3"/>')
    b.append(t(592, 104, "--- 目標 100%", 9, "#f59e0b", 700))
    # 終端機
    b += [f'<g filter="url(#sh)">{r(470, 256, 312, 222, "#0c0f1a", 10)}</g>', r(470, 256, 312, 26, "#1b2132", 10), r(470, 270, 312, 12, "#1b2132"),
          t(486, 273, "PowerShell", 11, "#9ca3af")]
    lines = [("PS> python auto_report.py", "#e5e7eb"), ("[1/4] 讀取 ERP 匯出資料 ......... OK", "#93c5fd"),
             ("[2/4] 彙整 10 個部門業績 ....... OK", "#93c5fd"), ("[3/4] 套用格式與產生圖表 ....... OK", "#93c5fd"),
             ("[4/4] 寄送報表給 5 位主管 ....... OK", "#93c5fd"), ("✓ 完成！耗時 8.2 秒", "#4ade80"), ("  （原本人工需 3 小時）", "#4ade80")]
    for i, (s, c) in enumerate(lines):
        b.append(t(484, 306 + i * 22, s, 11, c, 700 if s.startswith("✓") else 400, mono=True))
    return svg("".join(b))


# ---------- 5. 比價爬蟲 ----------
def scene_crawler() -> str:
    b = [r(0, 0, 800, 500, "#0b1020"), f'<g filter="url(#sh)">{r(24, 24, 384, 452, "#0d1117", 10)}</g>',
         r(24, 24, 384, 30, "#161b22", 10), r(24, 44, 384, 10, "#161b22"),
         '<circle cx="42" cy="39" r="5" fill="#ff5f57"/><circle cx="58" cy="39" r="5" fill="#febc2e"/><circle cx="74" cy="39" r="5" fill="#28c840"/>',
         t(216, 44, "price_crawler.py", 11, "#8b949e", 400, "middle", True)]
    lines = [("$ python price_crawler.py --kw 藍牙耳機", "#e6edf3"), ("", ""),
             ("[09:00:01] 排程啟動（每日 09:00）", "#8b949e"), ("[09:00:02] 抓取 平台A ...... 128 筆 ✓", "#58a6ff"),
             ("[09:00:05] 抓取 平台B ...... 96 筆 ✓", "#58a6ff"), ("[09:00:09] 抓取 平台C ...... 143 筆 ✓", "#58a6ff"),
             ("[09:00:10] 清洗資料、去除重複 → 312 筆", "#d2a8ff"), ("[09:00:11] 寫入 Google Sheet ✓", "#3fb950"),
             ("[09:00:11] 寫入 MySQL 資料庫 ✓", "#3fb950"), ("[09:00:12] 偵測降價商品 7 件", "#f0883e"),
             ("[09:00:12] → 已推播 LINE 通知", "#f0883e"), ("", ""), ("完成：3 個平台 / 367 筆 / 11.4 秒", "#3fb950")]
    for i, (s, c) in enumerate(lines):
        if s:
            b.append(t(40, 82 + i * 24, s, 11.5, c, 700 if i in (0, 12) else 400, mono=True))
    b += [r(40, 412, 352, 10, "#21262d", 5), r(40, 412, 352, 10, "#3fb950", 5), t(40, 446, "█ 100%  排程下次執行：明天 09:00", 11, "#8b949e", 400, mono=True)]
    b += [f'<g filter="url(#sh)">{r(424, 24, 352, 258, "#fff", 12)}</g>', t(442, 52, "藍牙耳機 · 三平台比價", 14, "#111827", 900),
          t(758, 52, "更新於 09:00", 10, "#6b7280", 400, "end"), r(436, 64, 328, 26, "#f3f4f6", 6)]
    heads = [("商品", 446), ("平台A", 594), ("平台B", 650), ("平台C", 706), ("最低", 756)]
    for h, x in heads:
        b.append(t(x, 82, h, 11, "#374151", 700, "start" if h == "商品" else "end"))
    rows = [("降噪耳機 Pro", [1990, 2050, 1890]), ("運動耳機 Lite", [890, 860, 920]), ("頭戴式 Studio", [3290, 3190, 3350]),
            ("兒童耳機 Kids", [690, 720, 650]), ("電競耳機 X7", [1590, 1490, 1620]), ("骨傳導 Open", [2480, 2390, 2450])]
    for i, (name, prices) in enumerate(rows):
        y = 112 + i * 28
        lo = min(prices)
        b.append(t(446, y, name, 11.5, "#111827"))
        for j, p in enumerate(prices):
            x = 594 + j * 56
            if p == lo:
                b.append(r(x - 46, y - 14, 50, 19, "#dcfce7", 4))
            b.append(t(x, y, f"{p:,}", 11, "#15803d" if p == lo else "#4b5563", 700 if p == lo else 400, "end"))
        b.append(t(756, y, f"${lo:,}", 11, "#ef4444", 900, "end"))
        b.append(f'<line x1="440" y1="{y+9}" x2="760" y2="{y+9}" stroke="#f1f5f9"/>')
    b += [f'<g filter="url(#sh)">{r(424, 298, 352, 178, "#fff", 12)}</g>', t(442, 324, "近 30 日價格走勢", 13, "#111827", 900)]
    rnd = random.Random(7)
    for col, base in (("#3b82f6", 70), ("#f59e0b", 90), ("#10b981", 110)):
        v, pts = base, []
        for i in range(30):
            v += rnd.uniform(-7, 6)
            pts.append(f"{444 + i * 10.8:.1f},{340 + v:.1f}")
        b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>')
    for i, (lab, col) in enumerate((("平台A", "#3b82f6"), ("平台B", "#f59e0b"), ("平台C", "#10b981"))):
        b += [r(560 + i * 70, 316, 10, 10, col, 2), t(574 + i * 70, 325, lab, 10, "#6b7280")]
    return svg("".join(b))


# ---------- 6. 量化交易回測 ----------
def scene_trading() -> str:
    defs = ('<linearGradient id="eq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22c55e" stop-opacity="0.4"/>'
            '<stop offset="1" stop-color="#22c55e" stop-opacity="0"/></linearGradient>')
    b = [r(0, 0, 800, 500, "#0d1117"), t(24, 36, "策略回測報告", 18, "#e6edf3", 900),
         t(150, 36, "均線突破 + 動能濾網 · 2020/01 – 2026/09", 12, "#8b949e"),
         r(660, 18, 116, 26, "#238636", 13), t(718, 36, "回測完成 ✓", 12, "#fff", 700, "middle"),
         r(24, 56, 524, 280, "#0f141b", 10, 'stroke="#21262d"')]
    rnd = random.Random(11)
    price, candles = 100.0, []
    for i in range(52):
        drift = 0.6 if 8 < i < 30 else (-0.5 if 30 <= i < 38 else 0.45)
        o = price
        c = o + rnd.uniform(-3, 3) + drift * 2
        hi, lo = max(o, c) + rnd.uniform(0.5, 3), min(o, c) - rnd.uniform(0.5, 3)
        candles.append((o, hi, lo, c))
        price = c
    pmin = min(c[2] for c in candles) - 4
    pmax = max(c[1] for c in candles) + 4
    def py(p): return 76 + (pmax - p) / (pmax - pmin) * 240
    for k in range(5):
        y = 76 + k * 60
        b.append(f'<line x1="36" y1="{y}" x2="536" y2="{y}" stroke="#1b222c"/>')
    ma = []
    for i, (o, hi, lo, c) in enumerate(candles):
        x = 44 + i * 9.4
        col = "#26a69a" if c >= o else "#ef5350"
        b.append(f'<line x1="{x:.1f}" y1="{py(hi):.1f}" x2="{x:.1f}" y2="{py(lo):.1f}" stroke="{col}"/>')
        top, bot = py(max(o, c)), py(min(o, c))
        b.append(r(round(x - 3, 1), round(top, 1), 6, round(max(bot - top, 1.5), 1), col, 1))
        window = [cc[3] for cc in candles[max(0, i - 7):i + 1]]
        ma.append(f"{x:.1f},{py(sum(window) / len(window)):.1f}")
    b.append(f'<polyline points="{" ".join(ma)}" fill="none" stroke="#f0b90b" stroke-width="1.8"/>')
    for i, kind in ((9, "buy"), (29, "sell"), (39, "buy")):
        x = 44 + i * 9.4
        if kind == "buy":
            y = py(candles[i][2]) + 12
            b.append(f'<path d="M{x:.1f} {y-6:.1f} l7 11 h-14 z" fill="#22c55e"/>' + t(round(x, 1), round(y + 20, 1), "買進", 10, "#22c55e", 700, "middle"))
        else:
            y = py(candles[i][1]) - 12
            b.append(f'<path d="M{x:.1f} {y+6:.1f} l7 -11 h-14 z" fill="#ef4444"/>' + t(round(x, 1), round(y - 10, 1), "賣出", 10, "#ef4444", 700, "middle"))
    b.append(t(44, 76, "— MA8 移動平均線", 10, "#f0b90b"))
    b += [r(562, 56, 214, 280, "#0f141b", 10, 'stroke="#21262d"'), t(578, 82, "績效指標", 13, "#e6edf3", 900)]
    stats = [("總報酬率", "+186.4%", "#22c55e"), ("年化報酬", "+19.2%", "#22c55e"), ("最大回撤", "-12.8%", "#ef4444"),
             ("夏普比率", "1.74", "#e6edf3"), ("勝率", "58.3%", "#e6edf3"), ("交易次數", "142 筆", "#e6edf3"), ("獲利因子", "2.11", "#e6edf3")]
    for i, (k, v, c) in enumerate(stats):
        y = 114 + i * 32
        b += [t(578, y, k, 12, "#8b949e"), t(760, y, v, 15, c, 900, "end"),
              f'<line x1="578" y1="{y+11}" x2="760" y2="{y+11}" stroke="#1b222c"/>']
    b += [r(24, 350, 752, 128, "#0f141b", 10, 'stroke="#21262d"'), t(40, 372, "資金曲線", 12, "#e6edf3", 700),
          r(110, 363, 10, 10, "#22c55e", 2), t(124, 372, "策略", 10, "#8b949e"), r(160, 363, 10, 10, "#6e7681", 2), t(174, 372, "大盤", 10, "#8b949e")]
    rnd2 = random.Random(5)
    v, bm, pts, bpts = 0.0, 0.0, [], []
    for i in range(80):
        v += rnd2.uniform(-1.2, 2.2)
        bm += rnd2.uniform(-1.5, 1.8)
        x = 40 + i * 9.1
        pts.append(f"{x:.1f},{462 - min(max(v * 2.1, -5), 82):.1f}")
        bpts.append(f"{x:.1f},{462 - min(max(bm * 1.1, -5), 82):.1f}")
    line = " ".join(pts)
    b += [f'<polygon points="40,466 {line} {40+79*9.1:.1f},466" fill="url(#eq)"/>',
          f'<polyline points="{" ".join(bpts)}" fill="none" stroke="#6e7681" stroke-width="1.5" stroke-dasharray="4 3"/>',
          f'<polyline points="{line}" fill="none" stroke="#22c55e" stroke-width="2.2"/>']
    return svg("".join(b), defs)


# ---------- 7. 桌面庫存管理系統 ----------
def scene_inventory() -> str:
    defs = ('<linearGradient id="wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e3a8a"/>'
            '<stop offset="1" stop-color="#0ea5e9"/></linearGradient>')
    b = [r(0, 0, 800, 500, "url(#wall)"), f'<g filter="url(#sh)">{r(36, 26, 728, 448, "#f8fafc", 10)}</g>',
         r(36, 26, 728, 32, "#fff", 10), r(36, 46, 728, 12, "#fff"), r(48, 35, 14, 14, "#2563eb", 3),
         t(70, 47, "庫存管理系統 v2.1", 12, "#111827", 700), t(700, 47, "—   ☐   ✕", 12, "#6b7280"),
         f'<line x1="36" y1="58" x2="764" y2="58" stroke="#e5e7eb"/>', r(36, 58, 150, 392, "#f1f5f9")]
    for i, s in enumerate(["商品清單", "進貨登記", "出貨登記", "盤點作業", "供應商", "報表匯出", "系統設定"]):
        y = 90 + i * 34
        if i == 0:
            b.append(r(46, y - 18, 130, 28, "#dbeafe", 6))
        b.append(t(62, y, s, 12.5, "#1d4ed8" if i == 0 else "#475569", 700 if i == 0 else 400))
    b += [r(200, 70, 92, 28, "#2563eb", 6), t(246, 89, "+ 新增商品", 12, "#fff", 700, "middle"),
          r(300, 70, 92, 28, "#fff", 6, 'stroke="#cbd5e1"'), t(346, 89, "匯入 Excel", 12, "#334155", 500, "middle"),
          r(400, 70, 92, 28, "#fff", 6, 'stroke="#cbd5e1"'), t(446, 89, "列印條碼", 12, "#334155", 500, "middle"),
          r(574, 70, 176, 28, "#fff", 6, 'stroke="#cbd5e1"'), t(588, 89, "搜尋料號 / 品名…", 12, "#94a3b8")]
    chips = [("商品總數", "1,248", "#2563eb"), ("庫存總值", "NT$ 3.2M", "#059669"), ("今日出貨", "86 筆", "#7c3aed"), ("低庫存警示", "6 項", "#dc2626")]
    for i, (k, v, c) in enumerate(chips):
        x = 200 + i * 138
        b += [r(x, 110, 128, 56, "#fff", 8, 'stroke="#e2e8f0"'), r(x, 110, 4, 56, c, 2), t(x + 14, 131, k, 11, "#64748b"), t(x + 14, 155, v, 16, c, 900)]
    b += [r(200, 178, 550, 26, "#e2e8f0", 6)]
    heads = [("料號", 210), ("品名", 300), ("分類", 440), ("庫存", 560), ("安全量", 620), ("狀態", 690)]
    for h, x in heads:
        b.append(t(x, 195, h, 11, "#334155", 700))
    rows = [("A-10021", "不鏽鋼保溫瓶 500ml", "生活用品", 342, 100), ("A-10022", "無線滑鼠 M350", "3C 周邊", 58, 80),
            ("A-10035", "A4 影印紙（箱）", "辦公耗材", 0, 30), ("B-20410", "藍牙鍵盤 K380", "3C 周邊", 126, 50),
            ("B-20418", "USB-C 充電線 1m", "3C 周邊", 24, 60), ("C-30102", "環保購物袋", "生活用品", 890, 200),
            ("C-30115", "抗菌濕紙巾 80 抽", "清潔用品", 412, 150), ("D-40007", "人體工學椅墊", "辦公家具", 37, 20)]
    for i, (code, name, cat, qty, safe) in enumerate(rows):
        y = 228 + i * 28
        if i % 2:
            b.append(r(200, y - 18, 550, 28, "#f1f5f9"))
        if qty == 0:
            st, c, bg = "缺貨", "#dc2626", "#fee2e2"
        elif qty < safe:
            st, c, bg = "偏低", "#d97706", "#fef3c7"
        else:
            st, c, bg = "正常", "#059669", "#d1fae5"
        b += [t(210, y, code, 11, "#475569", 400, mono=True), t(300, y, name, 11.5, "#0f172a"), t(440, y, cat, 11, "#64748b"),
              t(590, y, qty, 11.5, c if qty < safe else "#0f172a", 700, "end"), t(650, y, safe, 11, "#94a3b8", 400, "end"),
              r(684, y - 13, 44, 18, bg, 9), t(706, y, st, 10.5, c, 700, "middle")]
    b += [r(36, 450, 728, 24, "#e2e8f0", 0), '<circle cx="52" cy="462" r="4" fill="#22c55e"/>',
          t(62, 466, "已連線資料庫 · 最後同步 14:32 · 操作人員：倉管-小林", 10.5, "#475569")]
    return svg("".join(b), defs)


# ---------- 8. LINE Bot ----------
def scene_line() -> str:
    defs = ('<linearGradient id="lbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ecfdf3"/>'
            '<stop offset="1" stop-color="#bbf7d0"/></linearGradient>')
    b = [r(0, 0, 800, 500, "url(#lbg)"), f'<g filter="url(#sh)">{r(90, 14, 252, 472, "#111", 34)}</g>',
         r(100, 24, 232, 452, "#9bb5dc", 26), r(100, 24, 232, 50, "#fff", 26), r(100, 50, 232, 24, "#fff"),
         r(178, 30, 76, 8, "#111", 4), t(114, 64, "‹", 18, "#111", 700), t(216, 64, "晨光咖啡", 13, "#111", 700, "middle"),
         r(250, 53, 30, 14, "#06c755", 7), t(265, 63, "官方", 9, "#fff", 700, "middle")]

    def bot(y, lines, w=160):
        h = 14 + len(lines) * 17
        out = ['<circle cx="122" cy="{}" r="11" fill="#8b5e34"/>'.format(y + 10), r(140, y, w, h, "#fff", 12)]
        out += [t(150, y + 19 + i * 17, s, 11, "#111") for i, s in enumerate(lines)]
        return "".join(out), h

    def user(y, s, w):
        return r(318 - w, y, w, 28, "#8de055", 12) + t(318 - w + 10, y + 18, s, 11, "#111"), 28

    seg, h = user(86, "我想預約明天下午兩點，2 位", 168)
    b.append(seg)
    seg, h = bot(124, ["好的！已為您保留座位：", "10/05（日）14:00 · 2 位", "訂位編號 #A1029"])
    b.append(seg)
    b += [r(140, 196, 160, 112, "#fff", 12), r(140, 196, 160, 52, "#c08552", 12), r(140, 236, 160, 12, "#c08552"),
          t(150, 228, "本週限定｜秋季栗子拿鐵", 11, "#fff", 700), t(150, 268, "會員點數 8 / 10", 11, "#111", 700),
          r(150, 276, 140, 8, "#e5e7eb", 4), r(150, 276, 112, 8, "#06c755", 4),
          t(220, 300, "查看菜單 ›", 11, "#06c755", 700, "middle")]
    seg, h = user(318, "謝謝！", 56)
    b.append(seg)
    seg, h = bot(354, ["期待您的光臨，明天見～"], 150)
    b.append(seg)
    b.append(r(100, 392, 232, 84, "#fff", 0))
    b.append(r(100, 456, 232, 20, "#fff", 26))
    menu = ["線上訂位", "看菜單", "會員卡", "最新優惠", "門市資訊", "聯絡客服"]
    for i, s in enumerate(menu):
        cx, cy = 139 + (i % 3) * 77, 410 + (i // 3) * 36
        b += [f'<circle cx="{cx}" cy="{cy}" r="7" fill="#06c755" opacity="0.85"/>', t(cx, cy + 20, s, 9.5, "#374151", 500, "middle")]
    b += [f'<line x1="100" y1="392" x2="332" y2="392" stroke="#e5e7eb"/>']
    b += [t(400, 120, "LINE 官方帳號", 16, "#059669", 700), t(400, 166, "自動客服機器人", 36, "#064e3b", 900),
          t(400, 198, "24 小時自動回覆，客人問、訂、買一次搞定", 14, "#065f46")]
    feats = [("訂位 / 預約自動化", "串接 Google 日曆，自動排程並發送提醒"), ("訂單即時通知", "新訂單、出貨狀態即時推播給店家與客人"),
             ("會員集點與優惠券", "數位會員卡，提升回購率"), ("圖文選單客製化", "依品牌風格設計，常用功能一鍵直達")]
    for i, (k, v) in enumerate(feats):
        y = 250 + i * 56
        b += [f'<circle cx="414" cy="{y-5}" r="13" fill="#06c755"/>', t(414, y, "✓", 13, "#fff", 900, "middle"),
              t(438, y, k, 16, "#064e3b", 900), t(438, y + 20, v, 12, "#047857")]
    return svg("".join(b), defs)


# ---------- 9. Discord 機器人 ----------
def scene_discord() -> str:
    b = [r(0, 0, 800, 500, "#313338"), r(0, 0, 60, 500, "#1e1f22"), r(60, 0, 176, 500, "#2b2d31")]
    for i, c in enumerate(["#5865f2", "#ed4245", "#57f287", "#fee75c", "#eb459e"]):
        b.append(f'<circle cx="30" cy="{34 + i * 56}" r="20" fill="{c}" opacity="{1 if i == 0 else 0.75}"/>')
    b.append(r(0, 22, 4, 24, "#fff", 2))
    b += [t(76, 36, "遊戲社群伺服器", 14, "#f2f3f5", 900), f'<line x1="60" y1="52" x2="236" y2="52" stroke="#1e1f22" stroke-width="2"/>',
          t(76, 80, "文字頻道", 10, "#949ba4", 700)]
    for i, s in enumerate(["公告", "一般聊天", "抽獎活動", "等級排行", "音樂點播", "新手教學"]):
        y = 108 + i * 30
        if i == 2:
            b.append(r(68, y - 18, 160, 26, "#404249", 4))
        b.append(t(80, y, "#  " + s, 13, "#f2f3f5" if i == 2 else "#949ba4", 700 if i == 2 else 400))
    b += [r(60, 452, 176, 48, "#232428"), '<circle cx="84" cy="476" r="14" fill="#f0b232"/>', t(106, 474, "管理員 Sean", 12, "#f2f3f5", 700),
          t(106, 489, "線上", 10, "#949ba4"), r(236, 0, 564, 48, "#313338"), f'<line x1="236" y1="48" x2="800" y2="48" stroke="#26272b" stroke-width="2"/>',
          t(256, 30, "#  抽獎活動", 15, "#f2f3f5", 900), t(370, 30, "| 每週六晚上舉辦，記得按下參加！", 12, "#949ba4")]
    b += ['<circle cx="272" cy="86" r="18" fill="#eb459e"/>', t(300, 80, "小明", 13, "#f2f3f5", 700), t(338, 80, "今天 20:15", 10, "#949ba4"),
          r(300, 88, 336, 22, "#2b2d31", 4), t(308, 103, "/抽獎 開始 獎品:Steam 禮物卡 時間:10m", 11.5, "#dbdee1", 400, mono=True)]
    b += ['<circle cx="272" cy="142" r="18" fill="#5865f2"/>', t(272, 147, "F", 14, "#fff", 900, "middle"),
          t(300, 136, "FutureBot", 13, "#f2f3f5", 700), r(368, 125, 30, 15, "#5865f2", 3), t(383, 136, "BOT", 9, "#fff", 700, "middle"),
          t(406, 136, "今天 20:15", 10, "#949ba4"),
          r(300, 148, 420, 132, "#2b2d31", 6), r(300, 148, 4, 132, "#fee75c", 2),
          t(318, 174, "抽獎活動開始！", 15, "#f2f3f5", 900), t(318, 196, "點擊下方按鈕即可參加，結束時自動抽出得主。", 11.5, "#dbdee1")]
    fields = [("獎品", "Steam 禮物卡 $500"), ("參加人數", "128 人"), ("剩餘時間", "09:42")]
    for i, (k, v) in enumerate(fields):
        x = 318 + i * 136
        b += [t(x, 222, k, 11, "#b5bac1", 700), t(x, 240, v, 12, "#f2f3f5")]
    b += [r(318, 252, 96, 24, "#5865f2", 4), t(366, 268, "參加抽獎", 11.5, "#fff", 700, "middle"),
          r(422, 252, 76, 24, "#4e5058", 4), t(460, 268, "查看規則", 11.5, "#fff", 500, "middle")]
    b += [r(300, 292, 420, 140, "#2b2d31", 6), r(300, 292, 4, 140, "#57f287", 2), t(318, 316, "本週等級排行榜", 14, "#f2f3f5", 900)]
    ranks = [("阿傑", 42, 0.86, "#fee75c"), ("小雨", 39, 0.72, "#c0c0c0"), ("Kevin", 37, 0.55, "#cd7f32"), ("貓貓", 33, 0.41, "#949ba4")]
    for i, (name, lv, p, c) in enumerate(ranks):
        y = 342 + i * 24
        b += [t(318, y, f"{i+1}.", 12, c, 900), t(340, y, name, 12, "#f2f3f5", 700), t(420, y, f"Lv.{lv}", 11.5, "#b5bac1", 400, mono=True),
              r(480, y - 10, 200, 10, "#1e1f22", 5), r(480, y - 10, round(200 * p), 10, "#57f287", 5)]
    b += [r(256, 448, 524, 36, "#383a40", 8), t(274, 471, "傳送訊息到 #抽獎活動", 12.5, "#6d6f78")]
    return svg("".join(b))


# ---------- 10. 2D 平台跳躍遊戲 ----------
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


SCENES = {
    "web-cafe.svg": scene_cafe, "web-shop.svg": scene_shop, "web-dashboard.svg": scene_dashboard,
    "auto-excel.svg": scene_excel, "auto-crawler.svg": scene_crawler, "auto-trading.svg": scene_trading,
    "app-inventory.svg": scene_inventory, "bot-line.svg": scene_line, "bot-discord.svg": scene_discord,
    "game-platformer.svg": scene_platformer, "game-match3.svg": scene_match3, "game-shooter.svg": scene_shooter,
}

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        (OUT_DIR / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
