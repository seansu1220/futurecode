"""程式與自動化類作品：Excel 報表、比價爬蟲、量化回測、庫存系統的其他畫面。"""
import math
import random

from .common import *  # noqa: F401,F403
from .automation import scene_crawler, scene_excel, scene_inventory, scene_trading

XL_GREEN = "#217346"


# ================= Excel 自動化 =================
def excel_window(x, y, w, h, title, tabs, active_tab):
    b = [shadow(r(x, y, w, h, "#fff", 8)), r(x, y, w, 30, XL_GREEN, 8), r(x, y + 20, w, 10, XL_GREEN),
         t(x + w / 2, y + 20, title, 12, "#fff", 500, "middle"), r(x, y + 30, w, 30, "#f3f3f3")]
    for i, s in enumerate(["常用", "插入", "版面配置", "公式", "資料", "檢視"]):
        b.append(t(x + 16 + i * 58, y + 50, s, 11, XL_GREEN if i == 0 else "#444", 700 if i == 0 else 400))
    b.append(r(x, y + h - 26, w, 26, "#f3f3f3", 0))
    for i, s in enumerate(tabs):
        on = i == active_tab
        b.append(r(x + 10 + i * 74, y + h - 23, 68, 20, "#fff" if on else "#f3f3f3", 2)
                 + t(x + 44 + i * 74, y + h - 9, s, 10, XL_GREEN if on else "#666", 700 if on else 400, "middle"))
    return b


def file_card(x, y, name, kind="xlsx"):
    col = XL_GREEN if kind == "xlsx" else "#2563eb"
    return (shadow(r(x, y, 168, 40, "#fff", 8)) + r(x + 8, y + 8, 24, 24, col, 4) + t(x + 20, y + 25, "X" if kind == "xlsx" else "C", 12, "#fff", 900, "middle")
            + t(x + 40, y + 19, name, 11, "#111", 700) + t(x + 40, y + 33, "2026/09/30 匯出", 9, "#888"))


def scene_excel_raw():
    b = [r(0, 0, 800, 500, "#e7ecef"), t(24, 40, "來源檔案", 14, "#111", 900), t(100, 40, "12 個部門檔案", 11, "#666")]
    for i, (name, kind) in enumerate([("業務一部_09.xlsx", "xlsx"), ("業務二部_09.xlsx", "xlsx"), ("行銷部_09.csv", "csv"),
                                      ("電商部_09.xlsx", "xlsx"), ("ERP_export.csv", "csv"), ("通路部_09.xlsx", "xlsx")]):
        b.append(file_card(24, 58 + i * 52, name, kind))
    b += [t(108, 388, "⋯ 另外 6 個檔案", 11, "#666", 700, "middle"), path("M200 230 h26 v-10 l18 18 l-18 18 v-10 h-26z", XL_GREEN),
          shadow(r(20, 410, 220, 70, XL_GREEN, 10)), t(36, 436, "自動合併完成", 14, "#fff", 900), t(36, 458, "12 個檔案 → 4,382 筆資料", 11, "#d1fae5"),
          t(36, 474, "空白列、重複單號已自動清除", 10, "#a7f3d0")]
    b += excel_window(250, 16, 532, 468, "原始資料_彙整.xlsx - Excel", ["原始資料", "清洗紀錄", "樞紐分析"], 0)
    cols = [30, 74, 102, 64, 70, 70, 40, 82]
    heads = ["", "日期", "單號", "部門", "客戶", "品項", "數量", "金額"]
    xs = [250]
    for w in cols:
        xs.append(xs[-1] + w)
    b.append(r(250, 76, 532, 22, "#f0f0f0"))
    for i, h in enumerate(heads):
        b.append(t(xs[i] + cols[i] / 2, 91, h, 10.5, "#444", 700, "middle"))
    rnd = random.Random(8)
    depts = ["業務一部", "業務二部", "行銷部", "電商部", "通路部"]
    clients = ["宏達", "大成", "光華", "永豐", "新興", "東元", "台實"]
    goods = ["A4 紙", "碳粉匣", "螢幕", "鍵盤", "滑鼠", "印表機"]
    for ri in range(14):
        y = 98 + ri * 25
        fixed = ri in (3, 9)
        if fixed:
            b.append(r(280, y, 502, 25, "#fff4ce"))
        qty = rnd.randint(2, 60)
        row = [str(ri + 2), f"2026/09/{ri + 1:02d}", f"SO-0926{ri + 41:03d}", rnd.choice(depts), rnd.choice(clients) + "企業",
               rnd.choice(goods), str(qty), f"{qty * rnd.randint(180, 2400):,}"]
        for ci, v in enumerate(row):
            if ci == 0:
                b.append(r(250, y, 30, 25, "#f0f0f0") + t(265, y + 17, v, 9.5, "#666", 400, "middle"))
            else:
                anchor = "end" if ci >= 6 else "start"
                tx = xs[ci + 1] - 6 if anchor == "end" else xs[ci] + 6
                b.append(t(tx, y + 17, v, 10, "#222", 400, anchor, ci == 2))
        b.append(ln(250, y + 25, 782, y + 25, "#e8e8e8"))
    for x in xs:
        b.append(ln(x, 76, x, 448, "#e8e8e8"))
    b += [shadow(r(560, 172, 200, 48, "#111827", 8)), t(574, 192, "日期格式已統一", 11, "#fde68a", 700),
          t(574, 210, "「9/4」→「2026/09/04」", 10, "#e5e7eb", 400, mono=True), path("M600 220 l10 10 l10 -10z", "#111827")]
    return svg("".join(b))


def scene_excel_dashboard():
    b = [r(0, 0, 800, 500, "#e7ecef")] + excel_window(16, 16, 768, 468, "月報表_2026-09.xlsx - Excel", ["總表", "業務部", "行銷部", "圖表"], 3)
    b.append(r(16, 76, 768, 382, "#f7f7f7"))
    kpis = [("本月總業績", "11,070,000", XL_GREEN), ("整體達成率", "104.4%", "#2563eb"), ("年成長率", "+8.2%", "#7c3aed"), ("達標部門", "7 / 10", "#d97706")]
    for i, (k, v, col) in enumerate(kpis):
        x = 32 + i * 186
        b += [r(x, 88, 176, 64, "#fff", 4, 'stroke="#d9d9d9"'), r(x, 88, 4, 64, col), t(x + 16, 110, k, 11, "#666"), t(x + 16, 138, v, 20, col, 900)]
    months = [820, 860, 910, 880, 950, 990, 1010, 970, 1060, 1107]
    b += [r(32, 164, 440, 282, "#fff", 4, 'stroke="#d9d9d9"'), t(48, 188, "月業績趨勢（萬元）", 12, "#222", 700),
          grid_lines(64, 204, 392, 200, 4, "#eee"), line_chart(64, 204, 392, 200, months, XL_GREEN, 2.5, None, 700, 1150, dots=True),
          line_chart(64, 204, 392, 200, [780, 800, 820, 840, 860, 880, 900, 920, 940, 960], "#f59e0b", 1.8, None, 700, 1150, dash="5 4")]
    for i in range(10):
        b.append(t(round(64 + i * 392 / 9, 1), 424, f"{i + 1}月", 9, "#888", 400, "middle"))
    b += [r(64, 432, 10, 3, XL_GREEN), t(80, 437, "實際", 9.5, "#666"), r(120, 432, 10, 3, "#f59e0b"), t(136, 437, "目標", 9.5, "#666"),
          r(488, 164, 280, 136, "#fff", 4, 'stroke="#d9d9d9"'), t(504, 188, "業績佔比", 12, "#222", 700),
          donut(560, 240, 36, [(0.31, XL_GREEN), (0.22, "#2563eb"), (0.18, "#7c3aed"), (0.15, "#f59e0b"), (0.14, "#94a3b8")], 18)]
    for i, (k, v, col) in enumerate([("業務部", "31%", XL_GREEN), ("電商部", "22%", "#2563eb"), ("企業客戶", "18%", "#7c3aed"),
                                     ("行銷部", "15%", "#f59e0b"), ("其他", "14%", "#94a3b8")]):
        y = 206 + i * 18
        b += [r(620, y - 8, 8, 8, col, 1), t(634, y, k, 10, "#444"), t(752, y, v, 10, "#222", 700, "end")]
    b += [r(488, 312, 280, 134, "#fff", 4, 'stroke="#d9d9d9"'), t(504, 334, "部門達成率", 12, "#222", 700)]
    for i, (k, v) in enumerate([("企業客戶", 1.155), ("業務三部", 1.115), ("客服加值", 1.12), ("業務二部", 0.891), ("通路部", 0.847)]):
        y = 356 + i * 18
        col = XL_GREEN if v >= 1 else "#ef4444"
        b += [t(504, y, k, 10, "#444"), r(566, y - 9, round((v - 0.6) * 230, 1), 11, col, 2), t(752, y, f"{v * 100:.1f}%", 10, col, 700, "end")]
    return svg("".join(b))


def scene_excel_email():
    b = [r(0, 0, 800, 500, "#f3f4f6"), r(0, 0, 800, 40, "#0f6cbd"), t(20, 26, "信箱", 14, "#fff", 900), r(200, 8, 360, 24, "#ffffff", 12, 'opacity="0.9"'),
         t(216, 25, "搜尋郵件", 11, "#6b7280"), avatar(776, 20, 12, "#fff", "S", 11, "#0f6cbd"), r(0, 40, 140, 460, "#eef2f7")]
    for i, (s, n) in enumerate([("收件匣", "3"), ("已寄出", ""), ("草稿", ""), ("自動報表", "12"), ("封存", "")]):
        y = 74 + i * 30
        if i == 3:
            b.append(r(8, y - 18, 124, 26, "#dbe7f7", 6))
        b += [t(22, y, s, 12, "#0f172a", 700 if i == 3 else 400), t(126, y, n, 10.5, "#0f6cbd", 700, "end")]
    b += [r(140, 40, 230, 460, "#fff"), ln(370, 40, 370, 500, "#e5e7eb"), t(156, 66, "自動報表", 13, "#0f172a", 900)]
    for i, m in enumerate(["9", "8", "7", "6", "5", "4"]):
        y = 82 + i * 64
        if i == 0:
            b.append(r(140, y, 230, 64, "#e8f0fb") + r(140, y, 3, 64, "#0f6cbd"))
        b += [t(156, y + 22, "報表機器人", 11.5, "#0f172a", 900 if i == 0 else 500), t(356, y + 22, f"{10 - i if i else 10}/01", 10, "#6b7280", 400, "end"),
              t(156, y + 40, f"【自動報表】2026 年 {m} 月業績月報", 11, "#0f172a" if i == 0 else "#374151", 700 if i == 0 else 400),
              t(156, y + 56, "各位主管好，以下為本月部門業績摘要…", 10, "#6b7280"), ln(140, y + 64, 370, y + 64, "#f1f5f9")]
    b += [r(370, 40, 430, 460, "#fff"), t(392, 76, "【自動報表】2026 年 9 月部門業績月報", 15, "#0f172a", 900),
          avatar(406, 106, 14, XL_GREEN, "報", 12), t(428, 102, "報表機器人 <report-bot@company.com>", 11, "#0f172a", 700),
          t(428, 118, "收件者：業務主管群組（5 人）　2026/10/01 08:00", 10, "#6b7280"), ln(392, 132, 780, 132, "#e5e7eb"),
          t(392, 158, "各位主管好，", 12, "#111"), t(392, 180, "以下為 2026 年 9 月部門業績摘要，整體達成率 104.4%：", 12, "#111")]
    rows = [["業務一部", "1,280,000", "106.7%"], ["業務二部", "980,000", "89.1%"], ["電商部", "1,920,000", "106.7%"], ["企業客戶部", "2,310,000", "115.5%"]]

    def cell(ri, ci, val, x, base, w):
        if ci == 2:
            col = "#006100" if float(val[:-1]) >= 100 else "#9c0006"
            return t(x + w - 10, base, val, 11, col, 700, "end")
        return None

    b += [table(392, 194, [150, 120, 100], ["部門", "本月業績", "達成率"], rows, 24, 24, "#e8f3ec", XL_GREEN, "#111", None, "#eee", 11,
                ["start", "end", "end"], cell),
          t(392, 342, "完整報表與圖表請見附件。如有疑問請洽財務部。", 12, "#111"), t(392, 368, "— 此信由自動化報表系統寄出", 10.5, "#6b7280"),
          t(392, 404, "附件（2）", 11, "#374151", 700)]
    for i, (name, size, col, letter) in enumerate([("月報表_2026-09.xlsx", "248 KB", XL_GREEN, "X"), ("業績圖表_2026-09.pdf", "1.2 MB", "#dc2626", "P")]):
        x = 392 + i * 196
        b += [r(x, 414, 186, 46, "#fff", 8, 'stroke="#e5e7eb"'), r(x + 8, 422, 30, 30, col, 6), t(x + 23, 442, letter, 13, "#fff", 900, "middle"),
              t(x + 46, 434, name, 10.5, "#0f172a", 700), t(x + 46, 450, size, 9.5, "#6b7280")]
    return svg("".join(b))


def scene_excel_settings():
    defs = diag_grad("wall", "#065f46", "#0ea5e9")
    b = [r(0, 0, 800, 500, "url(#wall)"), app_window(40, 24, 720, 452, "報表小幫手 v1.3", "#f8fafc"),
         t(64, 86, "自動報表設定", 17, "#0f172a", 900), t(64, 106, "設定一次，每月自動完成報表與寄送", 11, "#64748b"),
         field(64, 126, 300, "資料來源資料夾", "D:\\業績資料\\2026-09", 30), btn(372, 134, 56, 30, "瀏覽", "#e2e8f0", "#0f172a", 11, 6),
         field(64, 180, 300, "輸出位置", "D:\\報表輸出", 30), btn(372, 188, 56, 30, "瀏覽", "#e2e8f0", "#0f172a", 11, 6),
         field(64, 234, 364, "報表範本", "部門業績月報.xlsx", 30), t(418, 262, "▾", 11, "#475569", 400, "end"), t(64, 292, "收件人", 11, "#475569", 700),
         r(64, 300, 364, 58, "#fff", 6, 'stroke="#cbd5e1"')]
    x, y = 72, 308
    for name in ["王經理", "林協理", "陳副總", "張主任", "李主管"]:
        w = tw(name, 10) + 30
        if x + w > 420:
            x, y = 72, y + 24
        b += [r(x, y, w, 20, "#dcfce7", 10), t(x + 10, y + 14, name, 10, "#166534", 700), t(x + w - 10, y + 14, "×", 10, "#166534", 700, "middle")]
        x += w + 6
    b += [t(64, 384, "排程", 11, "#475569", 700), toggle(64, 394, True, XL_GREEN), t(106, 407, "啟用自動排程", 12, "#0f172a", 700),
          r(210, 392, 218, 24, "#fff", 6, 'stroke="#cbd5e1"'), t(220, 409, "每月 1 日 08:00 執行", 11, "#0f172a"),
          btn(64, 432, 150, 34, "▶ 立即執行", XL_GREEN, size=13, rx=6), btn(224, 432, 100, 34, "儲存設定", "#e2e8f0", "#0f172a", 12, 6),
          r(452, 70, 290, 396, "#0f172a", 8), t(468, 96, "執行紀錄", 13, "#e2e8f0", 700), pill(680, 82, "運作中", "#14532d", "#4ade80", 10)]
    logs = [("10/01 08:00", "9 月報表完成，已寄 5 人", True), ("09/01 08:00", "8 月報表完成，已寄 5 人", True),
            ("08/01 08:00", "7 月報表完成，已寄 5 人", True), ("07/01 08:00", "缺少通路部檔案，已通知承辦", False),
            ("07/01 10:12", "補件後重新執行完成", True), ("06/01 08:00", "5 月報表完成，已寄 4 人", True),
            ("05/01 08:00", "4 月報表完成，已寄 4 人", True)]
    for i, (tm, msg, ok) in enumerate(logs):
        yy = 126 + i * 46
        b += [c(476, yy - 4, 7, "#22c55e" if ok else "#f59e0b"), t(476, yy - 1, "✓" if ok else "!", 9, "#0f172a", 900, "middle"),
              t(492, yy, tm, 10.5, "#94a3b8", 400, mono=True), t(492, yy + 18, msg, 11.5, "#e2e8f0"), ln(468, yy + 30, 726, yy + 30, "#1e293b")]
    return svg("".join(b), defs)


# ================= 比價爬蟲 =================
def scene_crawler_config():
    b = [r(0, 0, 800, 500, "#1e1e1e"), r(0, 0, 800, 30, "#323233"), t(400, 20, "config.yaml — price_crawler", 11, "#cccccc", 400, "middle"),
         r(0, 30, 44, 470, "#2c2c2c")]
    for i in range(5):
        b.append(r(12, 46 + i * 44, 20, 20, "#858585" if i else "#ffffff", 3, 'opacity="0.8"'))
    b += [r(44, 30, 186, 470, "#252526"), t(58, 52, "檔案總管", 10, "#bbbbbb", 700), t(58, 76, "▾ PRICE_CRAWLER", 10.5, "#cccccc", 700)]
    tree = [("config.yaml", 1, True), ("crawler.py", 1, False), ("scheduler.py", 1, False), ("notify.py", 1, False), ("▾ parsers", 1, False),
            ("platform_a.py", 2, False), ("platform_b.py", 2, False), ("platform_c.py", 2, False), ("▾ tests", 1, False),
            ("test_parsers.py", 2, False), ("requirements.txt", 1, False), (".env", 1, False)]
    for i, (name, depth, active) in enumerate(tree):
        y = 100 + i * 22
        if active:
            b.append(r(44, y - 15, 186, 22, "#37373d"))
        col = "#e5c07b" if name.endswith(".yaml") else ("#61afef" if name.endswith(".py") else "#cccccc")
        b.append(t(58 + depth * 12, y, name, 11, col if not name.startswith("▾") else "#cccccc"))
    b += [r(230, 30, 570, 30, "#2d2d2d"), r(230, 30, 130, 30, "#1e1e1e"), t(246, 50, "config.yaml", 11, "#e5c07b"), t(376, 50, "crawler.py", 11, "#8a8a8a")]
    code = [("# 比價爬蟲設定檔", "c"), ("keywords:", "k"), ("  - 藍牙耳機", "s"), ("  - 智慧手錶", "s"), ("  - 行動電源", "s"), ("platforms:", "k"),
            ("  - name: 平台A", "kv"), ("    enabled: true", "kb"), ("  - name: 平台B", "kv"), ("    enabled: true", "kb"),
            ('schedule: "0 9 * * *"   # 每天 09:00', "kv"), ("output:", "k"), ("  google_sheet: 比價追蹤表", "kv"),
            ("  database: mysql://crawler@db/prices", "kv"), ("notify:", "k"), ("  line_token: ${LINE_TOKEN}", "kv"),
            ("  drop_threshold: 5%    # 降價超過 5% 才通知", "kv")]
    for i, (line, kind) in enumerate(code):
        y = 82 + i * 19
        b.append(t(262, y, i + 1, 11, "#6e7681", 400, "end", True))
        if kind == "c":
            b.append(t(276, y, line, 11.5, "#6a9955", 400, mono=True))
        elif kind == "k":
            b.append(t(276, y, line, 11.5, "#e06c75", 400, mono=True))
        elif kind == "s":
            b.append(t(276, y, "  - ", 11.5, "#cccccc", 400, mono=True) + t(312, y, line[4:], 11.5, "#98c379", 400, mono=True))
        else:
            key, _, val = line.partition(":")
            comment = ""
            if "#" in val:
                val, _, comment = val.partition("#")
            kx = 276
            b.append(t(kx, y, key + ":", 11.5, "#e06c75", 400, mono=True))
            vx = kx + len(key + ": ") * 7.0
            b.append(t(round(vx, 1), y, val.strip(), 11.5, "#d19a66" if kind == "kb" else "#98c379", 400, mono=True))
            if comment:
                b.append(t(round(vx + len(val.strip()) * 7.0 + 30, 1), y, "# " + comment.strip(), 11.5, "#6a9955", 400, mono=True))
    b += [r(230, 404, 570, 96, "#181818"), ln(230, 404, 800, 404, "#3c3c3c"), t(246, 424, "終端機", 10.5, "#cccccc", 700),
          t(246, 448, "$ python crawler.py --dry-run", 11, "#cccccc", 400, mono=True), t(246, 468, "✓ 設定檔驗證通過：3 個關鍵字、3 個平台", 11, "#4ec9b0", 400, mono=True),
          t(246, 488, "✓ 測試抓取 9 筆成功，未寫入資料庫（試跑模式）", 11, "#4ec9b0", 400, mono=True)]
    return svg("".join(b))


def scene_crawler_sheet():
    b = [r(0, 0, 800, 500, "#fff"), r(16, 12, 26, 32, "#0f9d58", 3), r(22, 22, 14, 14, "#fff", 1), t(52, 30, "比價追蹤表", 15, "#202124", 500),
         t(52, 46, "檔案　編輯　檢視　插入　格式　資料　工具　擴充功能", 10.5, "#444"), btn(694, 16, 88, 30, "共用", "#c2e7ff", "#001d35", 12, 15),
         r(12, 56, 776, 30, "#edf2fa", 15), t(30, 76, "↶  ↷  🖶   100% ▾   $  %  .0   預設 ▾   10 ▾   B  I  S  A", 11, "#444"),
         r(0, 92, 800, 22, "#fff"), t(12, 107, "F2", 10.5, "#444", 700), t(60, 107, "fx  =IFERROR((D2-E2)/E2, \"\")", 10.5, "#444", 400, mono=True),
         ln(0, 114, 800, 114, "#e0e0e0")]
    widths = [36, 86, 64, 170, 86, 86, 86, 186]
    heads = ["", "日期", "平台", "商品", "價格", "前次價格", "漲跌", "連結"]
    xs = [0]
    for w in widths:
        xs.append(xs[-1] + w)
    b.append(r(0, 114, 800, 22, "#f8f9fa"))
    for i, h in enumerate(["", "A", "B", "C", "D", "E", "F", "G"]):
        b.append(t(xs[i] + widths[i] / 2, 129, h, 10, "#5f6368", 400, "middle"))
    rnd = random.Random(12)
    prods = ["降噪耳機 Pro", "運動耳機 Lite", "頭戴式 Studio", "智慧手錶 S2", "行動電源 20000", "電競耳機 X7", "骨傳導 Open"]
    for ri in range(14):
        y = 136 + ri * 24
        b.append(r(0, y, 36, 24, "#f8f9fa") + t(18, y + 16, ri + 1, 10, "#5f6368", 400, "middle"))
        if ri == 0:
            b.append(r(36, y, 764, 24, "#e8f0fe"))
            vals = heads[1:]
        else:
            prev = rnd.randint(6, 40) * 100 - 10
            change = rnd.choice([-0.078, -0.052, -0.031, 0, 0, 0.02, 0.045, -0.12])
            cur = int(prev * (1 + change))
            vals = ["10/04", rnd.choice(["平台A", "平台B", "平台C"]), rnd.choice(prods), f"{cur:,}", f"{prev:,}",
                    "—" if change == 0 else f"{'▼' if change < 0 else '▲'} {abs(change) * 100:.1f}%", f"https://shop-{ri}.example/item"]
        for ci, v in enumerate(vals):
            x0 = xs[ci + 1]
            col, weight = "#202124", 700 if ri == 0 else 400
            if ci == 5 and ri > 0 and v != "—":
                down = v.startswith("▼")
                b.append(r(x0 + 1, y + 1, widths[ci + 1] - 2, 22, "#e6f4ea" if down else "#fce8e6"))
                col = "#137333" if down else "#c5221f"
            if ci == 6 and ri > 0:
                col = "#1a73e8"
            anchor = "end" if ci in (3, 4, 5) and ri > 0 else "start"
            tx = x0 + widths[ci + 1] - 8 if anchor == "end" else x0 + 8
            b.append(t(tx, y + 16, v, 10.5, col, weight, anchor, ci == 6))
        b.append(ln(0, y + 24, 800, y + 24, "#e2e2e2"))
    for x in xs:
        b.append(ln(x, 114, x, 472, "#e2e2e2"))
    b += [r(0, 472, 800, 28, "#f8f9fa"), t(16, 491, "＋  ≡", 12, "#5f6368")]
    for i, s in enumerate(["每日價格", "降價紀錄", "統計"]):
        b.append(r(70 + i * 90, 474, 84, 24, "#e1e9f7" if i == 0 else "#f8f9fa", 4) + t(112 + i * 90, 490, s, 10.5, "#0b57d0" if i == 0 else "#444", 700 if i == 0 else 400, "middle"))
    return svg("".join(b))


def scene_crawler_line():
    defs = diag_grad("cbg", "#eef2ff", "#c7d2fe")
    b = [r(0, 0, 800, 500, "url(#cbg)"), phone(470, 14, 252, 472, "#8fb0d9"), r(479, 23, 234, 48, "#fff", 22), r(479, 47, 234, 24, "#fff"),
         t(493, 60, "‹", 18, "#111", 700), t(596, 60, "比價小幫手", 13, "#111", 700, "middle")]

    def drop_card(y, name, old, new, pct, platform, col):
        return (c(500, y + 10, 11, "#3b82f6") + r(518, y, 180, 130, "#fff", 12) + r(518, y, 180, 28, "#16a34a", 12) + r(518, y + 16, 180, 12, "#16a34a")
                + t(530, y + 19, f"降價提醒 ▼ {pct}", 11, "#fff", 900) + r(530, y + 36, 40, 40, col, 8) + t(580, y + 52, name, 11, "#111", 700)
                + t(580, y + 70, platform, 10, "#6b7280") + t(530, y + 96, f"NT$ {old}", 10.5, "#9ca3af", 400, extra='text-decoration="line-through"')
                + t(600, y + 96, f"→ NT$ {new}", 13, "#16a34a", 900) + ln(518, y + 106, 698, y + 106, "#f1f5f9") + t(608, y + 123, "前往購買 ›", 11, "#2563eb", 700, "middle"))

    b += [r(518, 84, 180, 46, "#fff", 12), t(528, 103, "早安！今日追蹤 367 項商品，", 10.5, "#111"), t(528, 121, "共 7 項降價，摘要如下：", 10.5, "#111"),
          drop_card(140, "降噪耳機 Pro", "2,050", "1,890", "7.8%", "平台B", "#f472b6"),
          drop_card(282, "智慧手錶 S2", "3,680", "3,390", "7.9%", "平台A", "#60a5fa"),
          r(479, 424, 234, 53, "#fff", 0), r(479, 450, 234, 27, "#fff", 22), r(490, 434, 180, 28, "#f3f4f6", 14), t(502, 452, "輸入訊息", 11, "#9ca3af"),
          c(692, 448, 13, "#06c755"), t(692, 453, "↑", 12, "#fff", 900, "middle")]
    b += [t(48, 128, "爬蟲 × LINE 通知", 16, "#4338ca", 700), t(48, 172, "降價第一時間", 36, "#1e1b4b", 900), t(48, 214, "推播到你手機", 36, "#1e1b4b", 900)]
    feats = [("自訂降價門檻", "例如降超過 5% 或低於指定價格才通知"), ("每日摘要報告", "早上 9 點彙整昨日價格變化"), ("一鍵前往購買", "卡片按鈕直接開啟商品頁"),
             ("多人訂閱", "群組、個人皆可加入通知名單")]
    for i, (k, v) in enumerate(feats):
        y = 262 + i * 54
        b += [c(62, y - 5, 13, "#4f46e5"), t(62, y, "✓", 13, "#fff", 900, "middle"), t(86, y, k, 16, "#1e1b4b", 900), t(86, y + 20, v, 12, "#4338ca")]
    return svg("".join(b), defs)


def scene_crawler_dashboard():
    defs = lin_grad("pa", "#2563eb", "#2563eb", True, 0.2, 0)
    b = [r(0, 36, 800, 464, "#f8fafc"), browser_bar("price-tracker.local/item/hp-001"), r(0, 36, 800, 48, "#fff"), ln(0, 84, 800, 84, "#e5e7eb"),
         c(30, 60, 10, "#2563eb"), t(48, 65, "價格追蹤儀表板", 14, "#0f172a", 900), r(220, 47, 260, 26, "#f1f5f9", 13), t(236, 64, "搜尋追蹤商品…", 11, "#94a3b8"),
         t(760, 65, "追蹤中 367 項", 11, "#475569", 700, "end"), t(24, 116, "降噪耳機 Pro", 20, "#0f172a", 900), pill(160, 102, "藍牙耳機", "#dbeafe", "#1d4ed8", 10),
         r(24, 130, 520, 230, "#fff", 12, 'stroke="#e5e7eb"'), t(40, 154, "近 90 日價格走勢", 12, "#0f172a", 700)]
    for i, s in enumerate(["30 天", "90 天", "1 年"]):
        b.append(btn(394 + i * 48, 140, 44, 22, s, "#2563eb" if i == 1 else "#f1f5f9", "#fff" if i == 1 else "#475569", 10, 6))
    a = walk(31, 60, 2100, 1780, 2300, -45, 40)
    bb = walk(32, 60, 2150, 1800, 2350, -40, 38)
    cc = walk(33, 60, 2200, 1850, 2400, -38, 36)
    b += [grid_lines(56, 176, 472, 160, 4, "#f1f5f9")]
    for k, v in enumerate(["2,400", "2,200", "2,000", "1,800"]):
        b.append(t(48, 180 + k * 53, v, 9, "#94a3b8", 400, "end"))
    b += [line_chart(56, 176, 472, 160, cc, "#10b981", 1.6, None, 1750, 2420), line_chart(56, 176, 472, 160, a, "#f59e0b", 1.6, None, 1750, 2420),
          line_chart(56, 176, 472, 160, bb, "#2563eb", 2.4, "pa", 1750, 2420)]
    lo_i = min(range(60), key=lambda i: bb[i])
    lx, ly = 56 + lo_i * 472 / 59, 176 + 160 - (bb[lo_i] - 1750) / 670 * 160
    b += [c(round(lx, 1), round(ly, 1), 5, "#ef4444", 'stroke="#fff" stroke-width="2"'), r(round(lx - 46, 1), round(ly + 8, 1), 92, 20, "#ef4444", 4),
          t(round(lx, 1), round(ly + 22, 1), f"史低 NT${bb[lo_i]:,.0f}", 10, "#fff", 700, "middle")]
    for i, (lab, col) in enumerate([("平台A", "#f59e0b"), ("平台B", "#2563eb"), ("平台C", "#10b981")]):
        b += [r(200 + i * 70, 148, 10, 10, col, 2), t(214 + i * 70, 157, lab, 10, "#475569")]
    cards = [("目前最低價", "NT$ 1,890", "平台B", "#2563eb"), ("史上最低價", f"NT$ {bb[lo_i]:,.0f}", "2026/08/12", "#ef4444"),
             ("90 日均價", "NT$ 2,012", "三平台平均", "#475569")]
    for i, (k, v, sub, col) in enumerate(cards):
        y = 130 + i * 62
        b += [r(560, y, 216, 54, "#fff", 12, 'stroke="#e5e7eb"'), t(576, y + 20, k, 10.5, "#64748b"), t(576, y + 42, v, 17, col, 900), t(760, y + 42, sub, 10, "#94a3b8", 400, "end")]
    b += [r(560, 316, 216, 44, "#dcfce7", 12), t(576, 336, "建議：低於均價 6%", 12, "#166534", 900), t(576, 352, "可考慮入手", 10.5, "#166534"),
          r(24, 374, 752, 116, "#fff", 12, 'stroke="#e5e7eb"'), t(40, 396, "其他追蹤商品", 12, "#0f172a", 700)]
    items = [("智慧手錶 S2", "3,390", "▼ 7.9%", True), ("行動電源 20000", "990", "▲ 2.1%", False), ("電競耳機 X7", "1,490", "▼ 3.2%", True)]
    for i, (name, price, ch, down) in enumerate(items):
        y = 422 + i * 22
        col = "#16a34a" if down else "#dc2626"
        b += [t(40, y, name, 11.5, "#0f172a"), t(300, y, "NT$ " + price, 11.5, "#0f172a", 700, "end"), t(380, y, ch, 11, col, 700, "end"),
              sparkline(420, y - 12, 140, 14, walk(40 + i, 20, 50, 0, 100, -12 if down else -8, 8 if down else 12), col),
              t(760, y, "查看 ›", 11, "#2563eb", 700, "end")]
    return svg("".join(b), defs)


# ================= 量化交易 =================
GH_BG, GH_PANEL, GH_LINE, GH_TEXT, GH_MUTED = "#0d1117", "#0f141b", "#21262d", "#e6edf3", "#8b949e"


def heat_color(v):
    """0~1 對應 紅→黃→綠。"""
    stops = [(0.0, (127, 29, 29)), (0.5, (245, 158, 11)), (1.0, (22, 163, 74))]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            k = (v - p0) / (p1 - p0)
            rgb = [round(a + (b2 - a) * k) for a, b2 in zip(c0, c1)]
            return "#%02x%02x%02x" % tuple(rgb)
    return "#16a34a"


def scene_trading_heatmap():
    b = [r(0, 0, 800, 500, GH_BG), t(24, 36, "參數最佳化", 18, GH_TEXT, 900), t(130, 36, "夏普比率熱力圖 · 均線突破策略", 12, GH_MUTED),
         r(24, 56, 524, 420, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(286, 466, "短均線週期", 11, GH_MUTED, 700, "middle"),
         t(40, 260, "長均線週期", 11, GH_MUTED, 700, "middle", extra='transform="rotate(-90 40 260)"')]
    cols, rows = 10, 8
    cw, ch = 44, 44
    x0, y0 = 70, 74
    best = None
    for ri in range(rows):
        for ci in range(cols):
            fast, slow = 5 + ci * 5, 20 + ri * 20
            v = math.exp(-((fast - 20) ** 2) / 260 - ((slow - 60) ** 2) / 3800) * 0.95 + 0.05 * math.sin(ci * 1.7 + ri)
            v = max(0.0, min(1.0, v))
            if fast >= slow:
                v = 0.0
            sharpe = round(-0.4 + v * 2.15, 2)
            if best is None or sharpe > best[0]:
                best = (sharpe, ci, ri, fast, slow)
            b += [r(x0 + ci * cw, y0 + ri * ch, cw - 3, ch - 3, heat_color(v) if fast < slow else "#161b22", 3),
                  t(x0 + ci * cw + (cw - 3) / 2, y0 + ri * ch + 26, f"{sharpe:.2f}" if fast < slow else "—", 9.5, "#fff" if fast < slow else "#30363d", 700, "middle")]
    for ci in range(cols):
        b.append(t(x0 + ci * cw + 20, 440, 5 + ci * 5, 10, GH_MUTED, 400, "middle"))
    for ri in range(rows):
        b.append(t(62, y0 + ri * ch + 26, 20 + ri * 20, 10, GH_MUTED, 400, "end"))
    _, bc, br, bf, bs = best
    b += [r(x0 + bc * cw - 2, y0 + br * ch - 2, cw + 1, ch + 1, "none", 4, 'stroke="#fff" stroke-width="2.5"'),
          r(564, 56, 212, 230, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(580, 82, "最佳參數組合", 13, GH_TEXT, 900)]
    stats = [("短均線", f"{bf} 日"), ("長均線", f"{bs} 日"), ("夏普比率", f"{best[0]:.2f}"), ("年化報酬", "+19.2%"), ("最大回撤", "-12.8%")]
    for i, (k, v) in enumerate(stats):
        y = 114 + i * 32
        b += [t(580, y, k, 12, GH_MUTED), t(760, y, v, 15, "#22c55e" if i in (2, 3) else ("#ef4444" if i == 4 else GH_TEXT), 900, "end"),
              ln(580, y + 11, 760, y + 11, GH_LINE)]
    b += [r(564, 298, 212, 82, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(580, 322, "色階", 12, GH_TEXT, 700)]
    for k in range(20):
        b.append(r(580 + k * 9, 334, 9, 14, heat_color(k / 19)))
    b += [t(580, 366, "-0.40", 10, GH_MUTED), t(760, 366, "1.75", 10, GH_MUTED, 400, "end"),
          r(564, 392, 212, 84, "#0f2a1a", 10, 'stroke="#238636"'), t(580, 418, "✓ 樣本外驗證通過", 13, "#3fb950", 900),
          t(580, 440, "2025–2026 夏普 1.52，表現穩定", 11, "#7ee787"), t(580, 460, "共測試 80 組參數 · 耗時 42 秒", 10.5, GH_MUTED)]
    return svg("".join(b))


def scene_trading_trades():
    b = [r(0, 0, 800, 500, GH_BG), t(24, 36, "交易明細", 18, GH_TEXT, 900), t(112, 36, "共 142 筆 · 2020/01 – 2026/09", 12, GH_MUTED)]
    chips = [("獲利 83 筆", "#22c55e"), ("虧損 59 筆", "#ef4444"), ("平均獲利 +4.8%", "#22c55e"), ("平均虧損 -2.1%", "#ef4444")]
    x = 24
    for s, col in chips:
        w = tw(s, 11) + 20
        b += [r(x, 52, w, 24, col, 12, 'opacity="0.15"'), t(x + w / 2, 68, s, 11, col, 700, "middle")]
        x += w + 8
    rnd = random.Random(19)
    rows = []
    for i in range(13):
        ret = rnd.choice([1, 1, 1, -1]) * round(rnd.uniform(0.6, 9.5), 1)
        entry = rnd.randint(14000, 23000)
        days = rnd.randint(2, 38)
        rows.append([str(142 - i), f"2026/{9 - i // 2:02d}/{rnd.randint(1, 28):02d}", f"{days} 天", "多" if rnd.random() > 0.3 else "空",
                     f"{entry:,}", f"{int(entry * (1 + ret / 100)):,}", f"{'+' if ret > 0 else ''}{ret}%"])

    def cell(ri, ci, val, x, base, w):
        if ci == 6:
            return t(x + w - 10, base, val, 11, "#22c55e" if val.startswith("+") else "#ef4444", 700, "end")
        if ci == 3:
            col = "#58a6ff" if val == "多" else "#d2a8ff"
            return r(x + 10, base - 12, 22, 16, col, 4, 'opacity="0.2"') + t(x + 21, base, val, 10.5, col, 700, "middle")
        return None

    b += [r(24, 88, 500, 390, GH_PANEL, 10, f'stroke="{GH_LINE}"'),
          table(32, 96, [40, 92, 64, 50, 76, 76, 86], ["#", "進場日期", "持有", "方向", "進場價", "出場價", "損益"], rows, 27, 26,
                "#161b22", GH_MUTED, GH_TEXT, None, GH_LINE, 11, ["start", "start", "start", "start", "end", "end", "end"], cell, (4, 5)),
          r(540, 88, 236, 250, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(556, 112, "報酬分布", 13, GH_TEXT, 900)]
    hist = [2, 5, 9, 14, 18, 11, 16, 21, 17, 12, 8, 5, 3, 1]
    for i, v in enumerate(hist):
        col = "#ef4444" if i < 5 else "#22c55e"
        b.append(r(560 + i * 14.5, 312 - v * 8, 12, v * 8, col, 2))
    b += [ln(556, 314, 760, 314, GH_LINE), t(560, 330, "-6%", 9.5, GH_MUTED), t(633, 330, "0%", 9.5, GH_MUTED, 400, "middle"), t(760, 330, "+12%", 9.5, GH_MUTED, 400, "end"),
          r(540, 350, 236, 128, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(556, 374, "持倉統計", 13, GH_TEXT, 900)]
    for i, (k, v) in enumerate([("平均持有天數", "11.4 天"), ("最長連勝", "9 次"), ("最長連敗", "4 次"), ("多 / 空比例", "72% / 28%")]):
        y = 400 + i * 22
        b += [t(556, y, k, 11, GH_MUTED), t(760, y, v, 12, GH_TEXT, 700, "end")]
    return svg("".join(b))


def scene_trading_live():
    defs = lin_grad("lv", "#58a6ff", "#58a6ff", True, 0.3, 0)
    b = [r(0, 0, 800, 500, GH_BG), t(24, 34, "即時監控", 18, GH_TEXT, 900), c(120, 29, 5, "#3fb950"), t(130, 34, "策略運行中 · 13:05:42", 11, "#3fb950", 700),
         r(640, 16, 136, 26, "#21262d", 13), t(708, 33, "模擬 / 實盤：模擬", 10.5, GH_MUTED, 700, "middle"),
         r(24, 54, 220, 270, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(40, 78, "觀察清單", 12, GH_TEXT, 700)]
    watch = [("台指期 TX", "23,182", "+0.82%", True), ("小台指 MTX", "23,180", "+0.81%", True), ("電子期 TE", "1,284.5", "+1.12%", True),
             ("金融期 TF", "2,036.4", "-0.21%", False), ("加權指數", "23,145", "+0.76%", True), ("櫃買指數", "268.42", "-0.35%", False)]
    for i, (name, px, ch, up) in enumerate(watch):
        y = 108 + i * 36
        col = "#ef4444" if up else "#22c55e"
        if i == 0:
            b.append(r(32, y - 18, 204, 32, "#161b22", 6))
        b += [t(40, y - 2, name, 11, GH_TEXT, 700), t(40, y + 12, px, 10.5, GH_MUTED, 400, mono=True), t(228, y + 12, ch, 10.5, col, 700, "end"),
              sparkline(150, y - 12, 76, 14, walk(50 + i, 20, 50, 0, 100, -10 if not up else -8, 8 if not up else 11), col)]
    prices = walk(77, 80, 40, 10, 95, -3, 3.4)
    b += [r(256, 54, 520, 270, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(272, 78, "台指期 TX · 1 分 K", 12, GH_TEXT, 700),
          t(760, 78, "23,182  ▲ 188", 12, "#ef4444", 900, "end"), grid_lines(272, 92, 488, 160, 4, "#161b22"),
          line_chart(272, 92, 488, 160, prices, "#58a6ff", 2, "lv", 0, 100)]
    vol = walk(78, 80, 40, 5, 100, -25, 25)
    for i, v in enumerate(vol):
        b.append(r(round(272 + i * 6.1, 1), round(310 - v * 0.5, 1), 4, round(v * 0.5, 1), "#30363d"))
    sig_i = 52
    sx, sy = 272 + sig_i * 488 / 79, 92 + 160 - prices[sig_i] / 100 * 160
    b += [c(round(sx, 1), round(sy, 1), 6, "#ef4444", 'stroke="#fff" stroke-width="2"'), r(round(sx - 52, 1), round(sy - 34, 1), 104, 22, "#ef4444", 4),
          t(round(sx, 1), round(sy - 19, 1), "多單進場 23,150", 10.5, "#fff", 700, "middle"),
          r(24, 336, 360, 142, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(40, 360, "目前持倉", 12, GH_TEXT, 700)]
    b.append(table(40, 372, [80, 50, 80, 70, 64], ["商品", "方向", "均價", "口數", "損益"],
               [["台指期 TX", "多", "23,150", "2", "+6,400"], ["電子期 TE", "多", "1,276.0", "1", "+3,400"], ["金融期 TF", "空", "2,041.0", "1", "+1,840"]],
               28, 24, "#161b22", GH_MUTED, GH_TEXT, None, GH_LINE, 11, ["start", "start", "end", "end", "end"],
               lambda ri, ci, v, x, base, w: t(x + w - 10, base, v, 11, "#ef4444", 700, "end") if ci == 4 else None))
    b += [r(396, 336, 380, 142, GH_PANEL, 10, f'stroke="{GH_LINE}"'), t(412, 360, "訊號紀錄", 12, GH_TEXT, 700), t(760, 360, "今日損益 +NT$ 11,640", 11.5, "#ef4444", 900, "end")]
    logs = [("13:02", "TX 突破上軌 → 多單進場 2 口", "已推播"), ("11:45", "MTX 觸及停利 → 出場 +38 點", "已推播"),
            ("10:20", "TF 跌破均線 → 空單進場 1 口", "已推播"), ("09:01", "開盤檢查完成，策略啟動", "系統")]
    for i, (tm, msg, tag) in enumerate(logs):
        y = 388 + i * 24
        b += [t(412, y, tm, 10.5, GH_MUTED, 400, mono=True), t(456, y, msg, 11, GH_TEXT), t(760, y, tag, 10, "#3fb950", 700, "end")]
    return svg("".join(b), defs)


def scene_trading_settings():
    b = [r(0, 0, 800, 500, GH_BG), t(24, 36, "策略設定", 18, GH_TEXT, 900), r(24, 54, 330, 424, GH_PANEL, 10, f'stroke="{GH_LINE}"'),
         field(40, 70, 298, "策略名稱", "均線突破 + 動能濾網", 30, True), field(40, 124, 142, "交易標的", "台指期 TX ▾", 30, True),
         field(196, 124, 142, "K 線週期", "日線 ▾", 30, True), field(40, 178, 298, "回測期間", "2020/01/01 – 2026/09/30", 30, True)]
    sliders = [("短均線週期", 20, 5, 50, "日"), ("長均線週期", 60, 20, 200, "日"), ("停損", 3, 1, 10, "%"), ("停利", 8, 2, 20, "%")]
    for i, (k, v, lo, hi, unit) in enumerate(sliders):
        y = 246 + i * 40
        frac = (v - lo) / (hi - lo)
        b += [t(40, y, k, 11, GH_MUTED, 700), t(338, y, f"{v} {unit}", 11.5, GH_TEXT, 900, "end"), ln(40, y + 14, 338, y + 14, GH_LINE, 4),
              ln(40, y + 14, round(40 + 298 * frac, 1), y + 14, "#58a6ff", 4), c(round(40 + 298 * frac, 1), y + 14, 7, "#58a6ff", 'stroke="#0d1117" stroke-width="2"')]
    b += [checkbox(40, 404, True, "#238636", 13), t(60, 415, "計入手續費與滑價", 11, GH_TEXT), checkbox(190, 404, True, "#238636", 13),
          t(210, 415, "樣本外驗證 30%", 11, GH_TEXT), btn(40, 432, 298, 34, "▶ 開始回測", "#238636", size=13, rx=6),
          r(370, 54, 406, 424, GH_PANEL, 10, f'stroke="{GH_LINE}"'), r(370, 54, 406, 30, "#161b22", 10), r(370, 74, 406, 10, "#161b22"),
          t(386, 74, "strategy.py", 11, GH_MUTED, 400, mono=True)]
    code = [[("class ", "#ff7b72"), ("MaBreakout", "#d2a8ff"), ("(Strategy):", GH_TEXT)],
            [("    fast, slow = ", GH_TEXT), ("20", "#79c0ff"), (", ", GH_TEXT), ("60", "#79c0ff")],
            [("    stop_loss, take_profit = ", GH_TEXT), ("0.03", "#79c0ff"), (", ", GH_TEXT), ("0.08", "#79c0ff")], [],
            [("    def ", "#ff7b72"), ("next", "#d2a8ff"), ("(self, bar):", GH_TEXT)],
            [("        ma_fast = self.", GH_TEXT), ("sma", "#d2a8ff"), ("(self.fast)", GH_TEXT)],
            [("        ma_slow = self.", GH_TEXT), ("sma", "#d2a8ff"), ("(self.slow)", GH_TEXT)],
            [("        momentum = self.", GH_TEXT), ("roc", "#d2a8ff"), ("(", GH_TEXT), ("10", "#79c0ff"), (")", GH_TEXT)], [],
            [("        # 黃金交叉且動能為正 → 進場", "#8b949e")],
            [("        if ", "#ff7b72"), ("cross_over", "#d2a8ff"), ("(ma_fast, ma_slow) ", GH_TEXT), ("and ", "#ff7b72"), ("momentum > ", GH_TEXT), ("0", "#79c0ff"), (":", GH_TEXT)],
            [("            self.", GH_TEXT), ("buy", "#d2a8ff"), ("(size=", GH_TEXT), ("1", "#79c0ff"), (")", GH_TEXT)],
            [("        elif ", "#ff7b72"), ("cross_under", "#d2a8ff"), ("(ma_fast, ma_slow):", GH_TEXT)],
            [("            self.", GH_TEXT), ("close", "#d2a8ff"), ("()", GH_TEXT)], [],
            [("        # 移動停損：獲利後上移停損點", "#8b949e")],
            [("        self.", GH_TEXT), ("trail_stop", "#d2a8ff"), ("(", GH_TEXT), ("0.03", "#79c0ff"), (")", GH_TEXT)]]
    for i, parts in enumerate(code):
        y = 108 + i * 21
        b.append(t(400, y, i + 1, 10.5, "#484f58", 400, "end", True))
        x = 412
        for text, col in parts:
            b.append(t(round(x, 1), y, text, 11, col, 400, mono=True))
            x += sum(11 if ord(ch) > 0x2E80 else 6.05 for ch in text)
    return svg("".join(b))


# ================= 庫存管理系統 =================
INV_NAV = ["商品清單", "進貨登記", "出貨登記", "盤點作業", "供應商", "報表匯出", "系統設定"]


def inv_frame(active):
    defs = diag_grad("wall", "#1e3a8a", "#0ea5e9")
    b = [r(0, 0, 800, 500, "url(#wall)"), app_window(36, 26, 728, 448, "庫存管理系統 v2.1"), r(36, 58, 150, 392, "#f1f5f9"),
         side_nav(36, 90, 150, INV_NAV, active, 34), r(36, 450, 728, 24, "#e2e8f0"), c(52, 462, 4, "#22c55e"),
         t(62, 466, "已連線資料庫 · 最後同步 14:32 · 操作人員：倉管-小林", 10.5, "#475569")]
    return defs, b


def scene_inv_inbound():
    defs, b = inv_frame(1)
    b += [t(200, 86, "進貨登記", 17, "#0f172a", 900), pill(290, 72, "新單據", "#dbeafe", "#1d4ed8", 10),
          field(200, 100, 200, "供應商", "大成文具有限公司 ▾", 28), field(412, 100, 140, "進貨日期", "2026/10/04", 28),
          field(564, 100, 186, "單號（自動產生）", "IN-20261004-03", 28, muted=True),
          r(200, 152, 550, 30, "#eff6ff", 6, 'stroke="#93c5fd" stroke-dasharray="4 3"'), barcode(212, 158, 30, 18, 3, "#1d4ed8"),
          t(252, 172, "掃描條碼可快速加入品項…", 11.5, "#1d4ed8")]
    rows = [["A-10035", "A4 影印紙（箱）", "40", "320", "12,800"], ["B-20418", "USB-C 充電線 1m", "60", "95", "5,700"],
            ["A-10022", "無線滑鼠 M350", "30", "210", "6,300"], ["C-30115", "抗菌濕紙巾 80 抽", "50", "73", "3,650"]]

    def cell(ri, ci, val, x, base, w):
        if ci == 2:
            return r(x + 6, base - 15, w - 12, 20, "#fff", 4, 'stroke="#cbd5e1"') + t(x + w - 12, base, val, 11, "#0f172a", 700, "end")
        return None

    b += [table(200, 194, [90, 190, 80, 80, 110], ["料號", "品名", "數量", "單價", "小計"], rows, 30, 26, "#e2e8f0", "#334155", "#0f172a",
                "#f8fafc", "#e2e8f0", 11, ["start", "start", "end", "end", "end"], cell, (0,)),
          t(210, 362, "＋ 新增一列", 11.5, "#2563eb", 700), ln(200, 372, 750, 372, "#e2e8f0")]
    for i, (k, v) in enumerate([("合計", "NT$ 28,450"), ("營業稅 5%", "NT$ 1,423"), ("總計", "NT$ 29,873")]):
        y = 392 + i * 18
        b += [t(620, y, k, 11, "#64748b" if i < 2 else "#0f172a", 400 if i < 2 else 900), t(750, y, v, 11 if i < 2 else 13, "#0f172a", 700 if i < 2 else 900, "end")]
    b += [btn(200, 404, 124, 32, "儲存並列印", "#2563eb", size=12, rx=6), btn(332, 404, 70, 32, "暫存", "#e2e8f0", "#334155", 12, 6),
          t(422, 425, "取消", 12, "#64748b")]
    return svg("".join(b), defs)


def scene_inv_stocktake():
    defs, b = inv_frame(3)
    b += [t(200, 86, "盤點作業 · 2026 Q3", 17, "#0f172a", 900), t(750, 86, "開始於 10/03 09:00", 11, "#64748b", 400, "end"),
          t(200, 112, "已盤點 1,024 / 1,248 項（82%）", 11.5, "#334155", 700), progress(200, 120, 550, 10, 0.82, "#2563eb", "#e2e8f0"),
          r(200, 142, 550, 44, "#fff", 8, 'stroke="#2563eb" stroke-width="2"'), barcode(214, 152, 40, 24, 9, "#0f172a"),
          t(266, 169, "請掃描商品條碼…", 13, "#94a3b8"), r(560, 152, 180, 24, "#dcfce7", 12), t(650, 168, "✓ B-20418 已記錄", 11, "#15803d", 700, "middle")]
    chips = [("相符", "1,002", "#059669", "#d1fae5"), ("短少", "15", "#dc2626", "#fee2e2"), ("溢出", "7", "#d97706", "#fef3c7"), ("未盤", "224", "#64748b", "#e2e8f0")]
    for i, (k, v, col, bg) in enumerate(chips):
        x = 200 + i * 140
        b += [r(x, 196, 130, 34, bg, 8), t(x + 12, 218, k, 11.5, col, 700), t(x + 118, 219, v, 15, col, 900, "end")]
    rows = [["A-10021", "不鏽鋼保溫瓶 500ml", "342", "342", "0"], ["A-10022", "無線滑鼠 M350", "58", "55", "-3"],
            ["A-10035", "A4 影印紙（箱）", "40", "40", "0"], ["B-20410", "藍牙鍵盤 K380", "126", "128", "+2"],
            ["C-30102", "環保購物袋", "890", "882", "-8"]]

    def cell(ri, ci, val, x, base, w):
        if ci == 4:
            n = int(val)
            col = "#059669" if n == 0 else ("#dc2626" if n < 0 else "#d97706")
            label = "相符" if n == 0 else ("短少" if n < 0 else "溢出")
            return t(x + 40, base, val, 11.5, col, 900, "end") + r(x + 52, base - 13, 40, 18, col, 9, 'opacity="0.15"') + t(x + 72, base, label, 10, col, 700, "middle")
        return None

    b += [table(200, 240, [90, 200, 80, 80, 100], ["料號", "品名", "系統數量", "實盤數量", "差異"], rows, 28, 26, "#e2e8f0", "#334155", "#0f172a",
                "#f8fafc", "#e2e8f0", 11, ["start", "start", "end", "end", "start"], cell, (0,)),
          btn(560, 414, 190, 30, "完成盤點並調整庫存", "#2563eb", size=12, rx=6)]
    return svg("".join(b), defs)


def scene_inv_report():
    defs, b = inv_frame(5)
    b += [t(200, 86, "報表統計", 17, "#0f172a", 900), btn(604, 70, 70, 26, "匯出 Excel", "#059669", size=10.5, rx=6),
          btn(682, 70, 68, 26, "列印", "#e2e8f0", "#334155", 10.5, 6), r(200, 104, 330, 182, "#fff", 8, 'stroke="#e2e8f0"'),
          t(214, 126, "近 6 個月進出貨（件）", 12, "#0f172a", 700), r(400, 117, 10, 10, "#2563eb", 2), t(414, 126, "進貨", 10, "#64748b"),
          r(450, 117, 10, 10, "#a78bfa", 2), t(464, 126, "出貨", 10, "#64748b"), grid_lines(214, 140, 300, 120, 4, "#f1f5f9")]
    ins = [820, 760, 900, 1040, 880, 960]
    outs = [780, 820, 860, 990, 940, 1010]
    for i in range(6):
        x = 224 + i * 50
        b += [r(x, 260 - ins[i] / 1100 * 120, 16, ins[i] / 1100 * 120, "#2563eb", 2), r(x + 18, 260 - outs[i] / 1100 * 120, 16, outs[i] / 1100 * 120, "#a78bfa", 2),
              t(x + 17, 276, f"{i + 4}月", 9.5, "#64748b", 400, "middle")]
    b += [r(542, 104, 208, 182, "#fff", 8, 'stroke="#e2e8f0"'), t(556, 126, "庫存價值分布", 12, "#0f172a", 700),
          donut(596, 200, 34, [(0.38, "#2563eb"), (0.26, "#059669"), (0.2, "#a78bfa"), (0.16, "#f59e0b")], 16)]
    for i, (k, v, col) in enumerate([("3C 周邊", "38%", "#2563eb"), ("生活用品", "26%", "#059669"), ("辦公耗材", "20%", "#a78bfa"), ("其他", "16%", "#f59e0b")]):
        y = 168 + i * 22
        b += [r(644, y - 8, 8, 8, col, 2), t(658, y, k, 10.5, "#334155"), t(740, y, v, 10.5, "#0f172a", 700, "end")]
    b += [r(200, 298, 270, 146, "#fff", 8, 'stroke="#e2e8f0"'), t(214, 320, "週轉率前 5 名", 12, "#0f172a", 700)]
    for i, (name, v) in enumerate([("USB-C 充電線", 1.0), ("A4 影印紙", 0.86), ("抗菌濕紙巾", 0.72), ("無線滑鼠", 0.6), ("環保購物袋", 0.48)]):
        y = 344 + i * 20
        b += [t(214, y, name, 10.5, "#334155"), progress(300, y - 8, 120, 8, v, "#2563eb", "#eff6ff"), t(456, y, f"{v * 12:.1f}", 10.5, "#0f172a", 700, "end")]
    b += [r(482, 298, 268, 146, "#fff", 8, 'stroke="#e2e8f0"'), t(496, 320, "呆滯品提醒（90 天未出貨）", 12, "#dc2626", 700)]
    for i, (name, days, val) in enumerate([("人體工學椅墊", 128, "NT$ 18,500"), ("桌上型風扇", 112, "NT$ 9,600"), ("聖誕裝飾組", 260, "NT$ 6,200"),
                                            ("舊款滑鼠墊", 96, "NT$ 2,880")]):
        y = 346 + i * 24
        b += [t(496, y, name, 11, "#0f172a"), t(640, y, f"{days} 天", 10.5, "#dc2626", 700, "end"), t(738, y, val, 10.5, "#475569", 400, "end")]
    return svg("".join(b), defs)


def scene_inv_labels():
    defs, b = inv_frame(0)
    b += [r(186, 58, 578, 392, "#e2e8f0"), t(204, 86, "條碼標籤列印", 17, "#0f172a", 900), r(204, 100, 190, 334, "#fff", 8, 'stroke="#cbd5e1"'),
          field(218, 116, 162, "標籤尺寸", "40 × 30 mm ▾", 28), field(218, 168, 162, "每項份數", "2", 28), field(218, 220, 162, "印表機", "條碼印表機（USB）▾", 28)]
    for i, (s, on) in enumerate([("顯示品名", True), ("顯示售價", True), ("顯示料號", True), ("加印公司名稱", False)]):
        y = 274 + i * 24
        b += [checkbox(218, y, on, "#2563eb", 13), t(238, y + 11, s, 11.5, "#334155")]
    b += [btn(218, 386, 162, 34, "列印 24 張", "#2563eb", size=13, rx=6), shadow(r(410, 100, 340, 334, "#fff", 4)),
          t(580, 120, "預覽（第 1 / 2 頁）", 10, "#94a3b8", 400, "middle")]
    items = [("不鏽鋼保溫瓶", "A-10021", "390"), ("無線滑鼠 M350", "A-10022", "490"), ("A4 影印紙", "A-10035", "320"),
             ("藍牙鍵盤 K380", "B-20410", "990"), ("USB-C 充電線", "B-20418", "149"), ("環保購物袋", "C-30102", "39")]
    for i in range(12):
        name, code, price = items[i // 2]
        x, y = 422 + (i % 3) * 108, 130 + (i // 3) * 74
        b += [r(x, y, 100, 66, "#fff", 4, 'stroke="#cbd5e1" stroke-dasharray="3 2"'), t(x + 6, y + 14, name, 9, "#0f172a", 700),
              barcode(x + 6, y + 20, 88, 24, i // 2 + 20, "#0f172a"), t(x + 6, y + 58, code, 8.5, "#334155", 400, mono=True),
              t(x + 94, y + 58, "$" + price, 9.5, "#0f172a", 900, "end")]
    return svg("".join(b), defs)


SCREENS = {
    "auto-excel": [scene_excel, scene_excel_raw, scene_excel_dashboard, scene_excel_email, scene_excel_settings],
    "auto-crawler": [scene_crawler, scene_crawler_config, scene_crawler_sheet, scene_crawler_line, scene_crawler_dashboard],
    "auto-trading": [scene_trading, scene_trading_heatmap, scene_trading_trades, scene_trading_live, scene_trading_settings],
    "app-inventory": [scene_inventory, scene_inv_inbound, scene_inv_stocktake, scene_inv_report, scene_inv_labels],
}
