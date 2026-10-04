"""程式與自動化類作品畫面。"""
import math
import random

from .common import *  # noqa: F401,F403


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


