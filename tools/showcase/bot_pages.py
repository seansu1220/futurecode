"""聊天機器人類作品：LINE 官方帳號、Discord 社群機器人的其他畫面。"""
from .common import *  # noqa: F401,F403
from .bots import scene_discord, scene_line

LINE_GREEN, CAFE_BROWN = "#06c755", "#8b5e34"


# ================= LINE 官方帳號 =================
def line_side_panel(kicker, title1, title2, feats, color="#064e3b", accent=LINE_GREEN):
    b = [t(400, 112, kicker, 15, "#059669", 700), t(400, 156, title1, 32, color, 900), t(400, 196, title2, 32, color, 900)]
    for i, (k, v) in enumerate(feats):
        y = 250 + i * 56
        b += [c(414, y - 5, 13, accent), t(414, y, "✓", 13, "#fff", 900, "middle"), t(438, y, k, 16, color, 900), t(438, y + 20, v, 12, "#047857")]
    return b


def line_phone(title, screen="#fff"):
    return [phone(90, 14, 252, 472, screen), r(99, 23, 234, 48, "#fff", 22), r(99, 47, 234, 24, "#fff"), ln(99, 71, 333, 71, "#eee"),
            t(113, 60, "✕", 13, "#111", 700), t(216, 60, title, 12.5, "#111", 700, "middle")]


def scene_line_booking():
    defs = diag_grad("lbg", "#ecfdf3", "#bbf7d0")
    b = [r(0, 0, 800, 500, "url(#lbg)")] + line_phone("晨光咖啡 · 線上訂位", "#f8fafc")
    b += [t(112, 98, "選擇日期", 11.5, "#111", 700)]
    for i, (d, w) in enumerate([("10/04", "日"), ("10/05", "一"), ("10/06", "二"), ("10/07", "三")]):
        x = 112 + i * 54
        on = i == 1
        b += [r(x, 106, 48, 44, LINE_GREEN if on else "#fff", 10, "" if on else 'stroke="#e5e7eb"'),
              t(x + 24, 124, w, 10, "#fff" if on else "#6b7280", 700, "middle"), t(x + 24, 141, d, 11, "#fff" if on else "#111", 900, "middle")]
    b.append(t(112, 174, "選擇時段", 11.5, "#111", 700))
    for i, s in enumerate(["11:00", "12:30", "14:00", "15:30", "17:00", "18:30"]):
        x, y = 112 + (i % 3) * 70, 182 + (i // 3) * 34
        if i == 2:
            b.append(btn(x, y, 64, 28, s, LINE_GREEN, size=11, rx=8))
        elif i == 4:
            b.append(r(x, y, 64, 28, "#f1f5f9", 8) + t(x + 32, y + 18, "額滿", 10.5, "#cbd5e1", 700, "middle"))
        else:
            b.append(r(x, y, 64, 28, "#fff", 8, 'stroke="#e5e7eb"') + t(x + 32, y + 18, s, 11, "#111", 500, "middle"))
    b += [t(112, 272, "人數", 11.5, "#111", 700), r(112, 280, 208, 32, "#fff", 8, 'stroke="#e5e7eb"'), c(132, 296, 10, "#f1f5f9"),
          t(132, 300, "－", 11, "#111", 700, "middle"), t(216, 301, "2 位大人", 12, "#111", 700, "middle"), c(300, 296, 10, LINE_GREEN), t(300, 300, "＋", 11, "#fff", 700, "middle"),
          t(112, 334, "座位偏好", 11.5, "#111", 700)]
    for i, s in enumerate(["靠窗", "沙發區", "吧台"]):
        x = 112 + i * 70
        b += [r(x, 342, 64, 28, "#e8faf0" if i == 0 else "#fff", 8, f'stroke="{LINE_GREEN if i == 0 else "#e5e7eb"}"'),
              t(x + 32, 360, s, 11, "#047857" if i == 0 else "#111", 700 if i == 0 else 400, "middle")]
    b += [r(112, 382, 208, 34, "#fff", 8, 'stroke="#e5e7eb"'), t(122, 403, "備註：慶生，想要安靜座位", 11, "#6b7280"),
          btn(112, 428, 208, 40, "確認預約", LINE_GREEN, size=13, rx=10)]
    b += line_side_panel("LINE 線上預約", "不用下載 App", "LINE 裡直接訂位", [
        ("即時查詢空位", "自動排除額滿時段，不會重複訂位"), ("預約自動提醒", "前一天推播提醒，減少放鳥"),
        ("一鍵改期取消", "客人自行操作，店家免接電話"), ("同步 Google 日曆", "店員手機即時看到訂位")])
    return svg("".join(b), defs)


def scene_line_member():
    defs = diag_grad("lbg", "#fdf6ec", "#f3e3cc") + diag_grad("card", "#5b3a1e", "#c08552")
    b = [r(0, 0, 800, 500, "url(#lbg)")] + line_phone("我的會員卡", "#f8fafc")
    b += [r(108, 84, 216, 126, "url(#card)", 14), c(300, 100, 50, "#fff", 'opacity="0.08"'), t(122, 108, "晨光咖啡", 13, "#fff", 900),
          pill(260, 94, "金卡會員", "#fbbf24", "#3b2412", 9), t(122, 136, "林○婷", 16, "#fff", 900), t(122, 154, "會員編號 MB-002841", 9.5, "#f3e3cc", 400, mono=True),
          r(122, 164, 188, 36, "#fff", 6), barcode(130, 169, 172, 26, 41, "#111"), t(112, 236, "集點卡", 12, "#111", 900), t(320, 236, "8 / 10 點", 11, CAFE_BROWN, 700, "end")]
    for i in range(10):
        x, y = 130 + (i % 5) * 42, 260 + (i // 5) * 40
        on = i < 8
        b += [c(x, y, 15, CAFE_BROWN if on else "#fff", "" if on else 'stroke="#d6c2a8" stroke-dasharray="3 2"'),
              t(x, y + 4, "✓" if on else str(i + 1), 11, "#fff" if on else "#c4b096", 900, "middle")]
    b += [r(112, 300 + 22, 208, 22, "#fef3c7", 6), t(216, 337, "再集 2 點即可兌換免費飲品", 10.5, "#92400e", 700, "middle"),
          t(112, 370, "我的優惠券", 12, "#111", 900)]
    for i, (k, v, col) in enumerate([("生日禮：免費拿鐵一杯", "10/31 前有效", "#ef4444"), ("滿 NT$300 折 NT$50", "10/15 前有效", LINE_GREEN)]):
        y = 382 + i * 46
        b += [r(112, y, 208, 40, "#fff", 8, 'stroke="#e5e7eb"'), r(112, y, 6, 40, col, 3), t(126, y + 17, k, 11, "#111", 700),
              t(126, y + 32, v, 9.5, "#6b7280"), btn(268, y + 9, 44, 22, "使用", col, size=10, rx=6)]
    b += line_side_panel("會員經營", "數位會員卡", "讓熟客一直回來", [
        ("消費自動集點", "結帳掃條碼，點數即時入帳"), ("會員等級制度", "依消費金額自動升等"),
        ("生日與專屬優惠", "系統自動發送，不用人工記"), ("會員資料分析", "了解誰是最常來的熟客")], "#3b2412", CAFE_BROWN)
    return svg("".join(b), defs)


def line_admin_frame(active, title, url):
    b = [r(0, 36, 800, 464, "#f6f8fa"), browser_bar(url), r(0, 36, 168, 464, "#fff"), ln(168, 36, 168, 500, "#e5e7eb"),
         c(28, 64, 11, LINE_GREEN), t(46, 69, "晨光咖啡 LINE 後台", 12, "#111", 900),
         side_nav(0, 108, 168, ["今日預約", "關鍵字回覆", "推播訊息", "會員管理", "數據分析", "設定"], active, 36, "#4b5563", "#047857", "#e8faf0", 12.5),
         t(188, 76, title, 18, "#111", 900)]
    return b


def scene_line_admin():
    b = line_admin_frame(0, "今日預約 · 10/05（一）", "bot-admin.morningbrew.tw/bookings")
    stats = [("LINE 好友數", "3,284", "+46 本週"), ("今日預約", "18 組", "42 位"), ("自動回覆率", "92%", "本週 1,208 則")]
    for i, (k, v, sub) in enumerate(stats):
        x = 188 + i * 196
        b += [r(x, 92, 186, 70, "#fff", 10, 'stroke="#e5e7eb"'), t(x + 14, 114, k, 11, "#6b7280"), t(x + 14, 144, v, 20, "#111", 900),
              t(x + 172, 144, sub, 10, "#059669", 700, "end")]
    rows = [["11:00", "王○明", "2", "靠窗", "已報到"], ["12:30", "陳○豪", "4", "沙發區", "已確認"], ["14:00", "林○婷", "2", "靠窗", "已確認"],
            ["14:00", "張○芳", "3", "吧台", "已確認"], ["15:30", "李○宇", "2", "沙發區", "已取消"], ["17:00", "黃○琪", "6", "包廂", "已確認"],
            ["18:30", "吳○翰", "2", "靠窗", "待確認"]]
    colors = {"已報到": ("#2563eb", "#dbeafe"), "已確認": ("#047857", "#d1fae5"), "已取消": ("#9ca3af", "#f3f4f6"), "待確認": ("#b45309", "#fef3c7")}

    def cell(ri, ci, val, x, base, w):
        if ci == 4:
            fg, bg = colors[val]
            return r(x + 8, base - 13, 52, 18, bg, 9) + t(x + 34, base, val, 10, fg, 700, "middle")
        if ci == 5:
            return t(x + 8, base, "傳訊息", 11, LINE_GREEN, 700)
        return None

    b += [r(188, 176, 584, 310, "#fff", 10, 'stroke="#e5e7eb"'), t(204, 200, "預約清單", 13, "#111", 900),
          btn(684, 186, 76, 26, "+ 手動新增", LINE_GREEN, size=10.5, rx=6),
          table(204, 216, [80, 120, 70, 110, 100, 72], ["時段", "姓名", "人數", "座位", "狀態", ""],
                [row + [""] for row in rows], 32, 26, "#f9fafb", "#6b7280", "#111", None, "#f1f5f9", 11.5, cell=cell)]
    return svg("".join(b))


def scene_line_broadcast():
    b = line_admin_frame(2, "建立推播訊息", "bot-admin.morningbrew.tw/broadcast")
    b += [r(188, 92, 360, 392, "#fff", 10, 'stroke="#e5e7eb"'), t(204, 118, "訊息類型", 11, "#374151", 700)]
    for i, s in enumerate(["文字", "圖片", "卡片訊息", "優惠券"]):
        x = 204 + i * 82
        b.append(btn(x, 126, 74, 26, s, LINE_GREEN, size=11, rx=6) if i == 2 else outline_btn(x, 126, 74, 26, s, "#9ca3af", 11, 6))
    b += [t(204, 178, "卡片圖片", 11, "#374151", 700), r(204, 186, 328, 70, "#f9fafb", 8, 'stroke="#d1d5db" stroke-dasharray="5 4"'),
          r(214, 194, 80, 54, "#c08552", 6), t(306, 218, "autumn_latte.png", 11, "#111", 700), t(306, 236, "已上傳 · 1040 × 1040", 10, "#6b7280"),
          field(204, 272, 328, "標題", "秋季限定｜栗子拿鐵上市", 28), r(204, 320, 328, 50, "#fff", 6, 'stroke="#cbd5e1"'),
          t(214, 340, "本週會員專屬 9 折，", 11.5, "#111"), t(214, 358, "出示會員卡即可享優惠！", 11.5, "#111"),
          t(204, 392, "發送對象", 11, "#374151", 700)]
    for i, (s, on) in enumerate([("全部好友（3,284 人）", False), ("標籤：金卡會員（412 人）", True), ("近 30 天未到店（640 人）", False)]):
        y = 410 + i * 20
        b += [radio(212, y, on, LINE_GREEN, 6), t(226, y + 4, s, 11, "#111", 700 if on else 400)]
    b += [r(560, 92, 212, 250, "#8fb0d9", 10), t(666, 112, "預覽", 10.5, "#fff", 700, "middle"), c(580, 136, 10, CAFE_BROWN),
          r(596, 126, 160, 180, "#fff", 12), r(596, 126, 160, 86, "#c08552", 12), r(596, 196, 160, 16, "#c08552"),
          t(606, 236, "秋季限定｜栗子拿鐵上市", 10.5, "#111", 900), t(606, 254, "本週會員專屬 9 折，", 9.5, "#374151"),
          t(606, 270, "出示會員卡即可享優惠！", 9.5, "#374151"), ln(596, 282, 756, 282, "#eee"), t(676, 298, "查看詳情 ›", 10, LINE_GREEN, 700, "middle"),
          r(560, 352, 212, 132, "#fff", 10, 'stroke="#e5e7eb"'), t(576, 374, "排程發送", 11, "#374151", 700), field(576, 380, 180, "", "2026/10/05  11:30", 26),
          t(576, 434, "預估開封率 68%", 10.5, "#059669", 700), btn(576, 444, 180, 30, "排程推播", LINE_GREEN, size=12, rx=6)]
    return svg("".join(b))


# ================= Discord =================
DC_BG, DC_SIDE, DC_RAIL, DC_TEXT, DC_MUTED, DC_BLURPLE = "#313338", "#2b2d31", "#1e1f22", "#f2f3f5", "#949ba4", "#5865f2"
DC_CHANNELS = ["歡迎", "公告", "一般聊天", "抽獎活動", "等級排行", "音樂點播"]


def discord_frame(active, topic):
    b = [r(0, 0, 800, 500, DC_BG), r(0, 0, 60, 500, DC_RAIL), r(60, 0, 176, 500, DC_SIDE)]
    for i, col in enumerate([DC_BLURPLE, "#ed4245", "#57f287", "#fee75c", "#eb459e"]):
        b.append(c(30, 34 + i * 56, 20, col, f'opacity="{1 if i == 0 else 0.75}"'))
    b += [r(0, 22, 4, 24, "#fff", 2), t(76, 36, "遊戲社群伺服器", 14, DC_TEXT, 900), ln(60, 52, 236, 52, DC_RAIL, 2), t(76, 80, "文字頻道", 10, DC_MUTED, 700)]
    for i, s in enumerate(DC_CHANNELS):
        y = 108 + i * 30
        if i == active:
            b.append(r(68, y - 18, 160, 26, "#404249", 4))
        b.append(t(80, y, "#  " + s, 13, DC_TEXT if i == active else DC_MUTED, 700 if i == active else 400))
    b += [r(60, 452, 176, 48, "#232428"), c(84, 476, 14, "#f0b232"), t(106, 474, "管理員 Sean", 12, DC_TEXT, 700), t(106, 489, "線上", 10, DC_MUTED),
          ln(236, 48, 800, 48, "#26272b", 2), t(256, 30, "#  " + DC_CHANNELS[active], 15, DC_TEXT, 900),
          t(270 + tw(DC_CHANNELS[active], 15) + 12, 30, "| " + topic, 12, DC_MUTED)]
    return b


def bot_header(y, time="今天 20:15"):
    return (c(272, y + 6, 18, DC_BLURPLE) + t(272, y + 11, "F", 14, "#fff", 900, "middle") + t(300, y, "FutureBot", 13, DC_TEXT, 700)
            + r(368, y - 11, 30, 15, DC_BLURPLE, 3) + t(383, y, "BOT", 9, "#fff", 700, "middle") + t(406, y, time, 10, DC_MUTED))


def scene_discord_welcome():
    defs = diag_grad("ban", "#5865f2", "#eb459e")
    b = discord_frame(0, "新朋友請先到這裡選擇身分組") + [bot_header(74, "今天 19:02"), r(300, 86, 440, 180, DC_SIDE, 6), r(300, 86, 4, 180, DC_BLURPLE, 2),
                                                   r(316, 98, 410, 120, "url(#ban)", 8), c(370, 158, 32, "#fff"), c(370, 158, 28, "#f0b232"),
                                                   t(370, 166, "雨", 22, "#fff", 900, "middle"), t(418, 150, "歡迎 小雨 加入！", 20, "#fff", 900),
                                                   t(418, 176, "你是本伺服器第 1,024 位成員！", 12, "#fff", 500),
                                                   t(316, 240, "請先閱讀 #公告 的社群規範，再到下方選擇身分組～", 11.5, "#dbdee1"),
                                                   t(316, 258, "輸入 /說明 可查看所有指令。", 11.5, "#dbdee1")]
    b += [bot_header(294, "今天 19:02"), r(300, 306, 440, 124, DC_SIDE, 6), r(300, 306, 4, 124, "#57f287", 2),
          t(318, 330, "選擇你的遊戲身分組", 14, DC_TEXT, 900), t(318, 350, "點擊按鈕即可加入或移除（可複選）", 11, "#b5bac1")]
    roles = [("射擊遊戲", "#ed4245"), ("角色扮演", DC_BLURPLE), ("策略遊戲", "#57f287"), ("休閒手遊", "#fee75c"), ("主機玩家", "#eb459e")]
    for i, (s, col) in enumerate(roles):
        x, y = 318 + (i % 4) * 104, 362 + (i // 4) * 32
        on = i == 1
        b += [r(x, y, 96, 26, DC_BLURPLE if on else "#4e5058", 4), c(x + 14, y + 13, 5, col), t(x + 56, y + 17, s + (" ✓" if on else ""), 11, "#fff", 700, "middle")]
    b += [t(272, 452, "→", 13, "#23a55a", 900, "middle"), t(300, 452, "小雨 已取得身分組「角色扮演」", 12, DC_MUTED),
          r(256, 462, 524, 30, "#383a40", 8), t(274, 482, "傳送訊息到 #歡迎", 12, "#6d6f78")]
    return svg("".join(b), defs)


def scene_discord_music():
    defs = diag_grad("art", "#f472b6", "#6366f1")
    b = discord_frame(5, "語音頻道點歌，輸入 /播放") + [c(272, 80, 18, "#57f287"), t(300, 74, "阿傑", 13, DC_TEXT, 700), t(338, 74, "今天 21:30", 10, DC_MUTED),
                                                  r(300, 82, 230, 22, DC_SIDE, 4), t(308, 97, "/播放 lofi 讀書音樂", 11.5, "#dbdee1", 400, mono=True),
                                                  bot_header(130, "今天 21:30"), r(300, 142, 440, 154, DC_SIDE, 6), r(300, 142, 4, 154, "#eb459e", 2),
                                                  t(318, 166, "♪ 正在播放", 12, "#b5bac1", 700), r(318, 178, 86, 86, "url(#art)", 8),
                                                  c(361, 221, 22, "#fff", 'opacity="0.25"'), c(361, 221, 6, "#fff", 'opacity="0.6"'),
                                                  t(418, 196, "Lofi Study Mix · 專注讀書", 15, DC_TEXT, 900), t(418, 216, "點播者：阿傑　·　語音頻道：讀書室", 11, "#b5bac1"),
                                                  progress(418, 232, 300, 6, 0.37, "#eb459e", "#1e1f22"), t(418, 254, "01:24", 10, DC_MUTED, 400, mono=True),
                                                  t(718, 254, "03:45", 10, DC_MUTED, 400, "end", True)]
    for i, s in enumerate(["◀◀", "❚❚", "▶▶", "↻", "♡"]):
        b.append(r(318 + i * 50, 270, 44, 20, "#4e5058" if i != 1 else DC_BLURPLE, 4) + t(340 + i * 50, 284, s, 10, "#fff", 700, "middle"))
    b += [bot_header(320, "今天 21:31"), r(300, 332, 440, 112, DC_SIDE, 6), r(300, 332, 4, 112, DC_BLURPLE, 2), t(318, 356, "播放佇列（4 首）", 13, DC_TEXT, 900)]
    for i, (song, who, dur) in enumerate([("Rainy Café Jazz", "小雨", "04:12"), ("Night Drive Synthwave", "Kevin", "03:58"), ("Piano for Focus", "貓貓", "05:01")]):
        y = 380 + i * 20
        b += [t(318, y, f"{i + 1}.", 11, DC_MUTED, 700), t(338, y, song, 11.5, "#dbdee1"), t(560, y, "點播：" + who, 10.5, DC_MUTED), t(730, y, dur, 10.5, DC_MUTED, 400, "end", True)]
    b += [r(256, 456, 524, 34, "#383a40", 8), t(274, 478, "傳送訊息到 #音樂點播", 12, "#6d6f78")]
    return svg("".join(b), defs)


def scene_discord_dashboard():
    b = [r(0, 36, 800, 464, "#1e1f22"), browser_bar("futurebot.app/dashboard/guild/1024", True), r(0, 36, 800, 50, "#2b2d31"),
         c(28, 61, 12, DC_BLURPLE), t(28, 66, "F", 12, "#fff", 900, "middle"), t(48, 66, "FutureBot 控制台", 14, DC_TEXT, 900),
         r(560, 48, 210, 26, "#1e1f22", 6), c(576, 61, 7, DC_BLURPLE), t(590, 65, "遊戲社群伺服器 ▾", 11.5, DC_TEXT, 700)]
    stats = [("成員數", "1,024", "+38 本週"), ("今日訊息", "3,482", "+12%"), ("指令使用次數", "612", "今日"), ("在線人數", "187", "目前")]
    for i, (k, v, sub) in enumerate(stats):
        x = 24 + i * 190
        b += [r(x, 100, 180, 64, "#2b2d31", 10), t(x + 14, 122, k, 11, DC_MUTED), t(x + 14, 150, v, 20, DC_TEXT, 900), t(x + 166, 150, sub, 10, "#57f287", 700, "end")]
    b.append(t(24, 192, "功能模組", 14, DC_TEXT, 900))
    mods = [("歡迎訊息", "新成員加入時自動發送歡迎圖卡", True, "#57f287"), ("等級系統", "依發言給予經驗值與等級身分組", True, "#fee75c"),
            ("自動管理", "過濾垃圾訊息、連結與不當言論", True, "#ed4245"), ("音樂播放", "語音頻道點歌與播放佇列", True, "#eb459e"),
            ("抽獎活動", "按鈕參加、到時自動抽出得主", True, DC_BLURPLE), ("自訂指令", "設定關鍵字自動回覆內容", False, "#949ba4")]
    for i, (name, desc, on, col) in enumerate(mods):
        x, y = 24 + (i % 3) * 254, 206 + (i // 3) * 132
        b += [r(x, y, 244, 120, "#2b2d31", 10), r(x + 16, y + 16, 36, 36, col, 10, 'opacity="0.22"'), c(x + 34, y + 34, 8, col),
              t(x + 64, y + 32, name, 14, DC_TEXT, 900), t(x + 64, y + 50, "已啟用" if on else "未啟用", 10.5, "#57f287" if on else DC_MUTED, 700),
              toggle(x + 194, y + 20, on, "#23a55a"), t(x + 16, y + 80, desc, 11, "#b5bac1"), t(x + 16, y + 104, "設定 ›", 11, "#00a8fc", 700)]
    return svg("".join(b))


def scene_discord_commands():
    b = discord_frame(2, "聊天、揪團都在這裡") + [c(272, 80, 18, "#eb459e"), t(300, 74, "小明", 13, DC_TEXT, 700), t(338, 74, "今天 22:01", 10, DC_MUTED),
                                               t(300, 96, "今晚有人要一起打嗎？", 12.5, "#dbdee1"), c(272, 136, 18, "#57f287"), t(300, 130, "阿傑", 13, DC_TEXT, 700),
                                               t(338, 130, "今天 22:02", 10, DC_MUTED), t(300, 152, "+1，等我 10 分鐘", 12.5, "#dbdee1"),
                                               shadow(r(256, 174, 524, 270, "#2b2d31", 8)), t(272, 196, "符合「/」的指令", 10.5, DC_MUTED, 700),
                                               t(764, 196, "FutureBot", 10.5, DC_MUTED, 700, "end")]
    cmds = [("/抽獎", "建立抽獎活動（獎品、時間、名額）"), ("/等級", "查看自己或他人的等級與經驗值"), ("/排行榜", "本週發言與等級排行"),
            ("/播放", "在語音頻道播放音樂"), ("/身分組", "加入或移除遊戲身分組"), ("/揪團", "發起組隊邀請並自動標記成員"), ("/說明", "列出所有可用指令")]
    for i, (cmd, desc) in enumerate(cmds):
        y = 222 + i * 30
        if i == 5:
            b.append(r(264, y - 19, 508, 28, "#404249", 4))
        b += [c(284, y - 5, 9, DC_BLURPLE), t(284, y - 1, "F", 9, "#fff", 900, "middle"), t(302, y, cmd, 12.5, DC_TEXT, 700), t(372, y, desc, 11.5, "#b5bac1")]
    b += [r(256, 452, 524, 38, "#383a40", 8), r(268, 460, 54, 22, "#4e5058", 4), t(295, 476, "/揪團", 11.5, DC_TEXT, 700, "middle"),
          t(330, 476, "遊戲：策略遊戲　人數：4　時間：22:30", 11.5, "#dbdee1")]
    return svg("".join(b))


SCREENS = {
    "bot-line": [scene_line, scene_line_booking, scene_line_member, scene_line_admin, scene_line_broadcast],
    "bot-discord": [scene_discord, scene_discord_welcome, scene_discord_music, scene_discord_dashboard, scene_discord_commands],
}
