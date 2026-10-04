// ===== 作品展示牆資料（新增 / 調整作品只需修改此檔）=====

// 燈箱內「委託類似作品」按鈕的連結
const SHOWCASE_CTA_URL = 'https://shopee.tw/product/84156043/48060712536/';

/**
 * @typedef {Object} ShowcaseCategory
 * @property {string} id    分類代碼
 * @property {string} label 顯示名稱
 */

/**
 * @typedef {Object} ShowcaseItem
 * @property {string}   id          唯一代碼
 * @property {string}   category    對應 ShowcaseCategory.id
 * @property {string}   image       圖片路徑
 * @property {string}   title       作品名稱
 * @property {string}   summary     卡片上的一句話簡介
 * @property {string}   description 燈箱內的完整說明
 * @property {string[]} features    功能重點
 * @property {string[]} tags        技術標籤
 */

/** @type {ShowcaseCategory[]} */
const SHOWCASE_CATEGORIES = [
    { id: 'all',        label: '全部' },
    { id: 'web',        label: '網頁設計' },
    { id: 'automation', label: '程式與自動化' },
    { id: 'bot',        label: '聊天機器人' },
    { id: 'game',       label: '遊戲設計' },
];

/** @type {ShowcaseItem[]} */
const SHOWCASE_ITEMS = [
    {
        id: 'web-cafe', category: 'web', image: 'images/showcase/web-cafe.svg',
        title: '咖啡廳品牌形象官網',
        summary: '溫暖質感的一頁式形象網站，含菜單與線上訂位。',
        description: '為實體店家打造的品牌官網，從配色、排版到文案風格一次到位，手機與電腦都能完美瀏覽。',
        features: ['響應式設計（手機 / 平板 / 電腦）', '菜單、門市資訊、最新消息區塊', '線上訂位表單串接 Google 試算表', 'SEO 基礎設定與 Google 地圖嵌入'],
        tags: ['HTML', 'CSS', 'JavaScript', 'RWD'],
    },
    {
        id: 'web-shop', category: 'web', image: 'images/showcase/web-shop.svg',
        title: '電商購物網站',
        summary: '商品展示、購物車、限時活動倒數一應俱全。',
        description: '完整的線上商店前台，支援商品分類、搜尋、購物車與促銷活動，可串接金流與物流。',
        features: ['商品分類與關鍵字搜尋', '購物車與結帳流程', '限時特賣倒數計時', '會員中心與訂單查詢'],
        tags: ['React', 'Node.js', '金流串接', 'Firebase'],
    },
    {
        id: 'web-dashboard', category: 'web', image: 'images/showcase/web-dashboard.svg',
        title: '營運數據管理後台',
        summary: '營收、訂單、流量即時視覺化，老闆一眼看懂。',
        description: '把分散在各系統的資料彙整成一個後台儀表板，支援權限管理與報表匯出。',
        features: ['KPI 指標卡與成長率', '營收趨勢圖、流量來源圖', '訂單管理與狀態追蹤', '帳號權限分級（擁有者 / 管理員）'],
        tags: ['Vue', 'Chart.js', 'REST API', '資料庫'],
    },
    {
        id: 'auto-excel', category: 'automation', image: 'images/showcase/auto-excel.svg',
        title: 'Excel 自動化月報表',
        summary: '一鍵產出各部門報表並自動寄信，3 小時縮短為 8 秒。',
        description: '讀取 ERP 匯出的原始資料，自動彙整、套用格式、產生圖表，最後寄送給相關主管。',
        features: ['多檔案自動合併與彙整', '條件式格式（達標 / 未達自動標色）', '自動產生圖表與樞紐分析', '排程執行並寄送 Email'],
        tags: ['Python', 'openpyxl', 'Excel', '自動化'],
    },
    {
        id: 'auto-crawler', category: 'automation', image: 'images/showcase/auto-crawler.svg',
        title: '多平台比價爬蟲',
        summary: '每日定時抓取多個平台價格，降價自動通知。',
        description: '針對指定關鍵字定時抓取多個電商平台的商品價格，清洗後寫入試算表與資料庫，並推播降價提醒。',
        features: ['多平台同時抓取', '資料清洗、去除重複', '寫入 Google Sheet / MySQL', '降價商品 LINE 推播通知'],
        tags: ['Python', '爬蟲', 'Google Sheet', '排程'],
    },
    {
        id: 'auto-trading', category: 'automation', image: 'images/showcase/auto-trading.svg',
        title: '量化交易策略回測系統',
        summary: 'K 線、買賣訊號與完整績效指標一次呈現。',
        description: '把交易想法寫成程式，用歷史資料回測驗證，輸出報酬率、最大回撤、夏普比率等專業指標。',
        features: ['歷史資料下載與整理', '自訂技術指標與進出場規則', '買賣點標示與 K 線圖', '績效報告與資金曲線'],
        tags: ['Python', 'pandas', '數據分析', '視覺化'],
    },
    {
        id: 'app-inventory', category: 'automation', image: 'images/showcase/app-inventory.svg',
        title: '桌面版庫存管理系統',
        summary: '進出貨、盤點、低庫存警示，小公司也能輕鬆管理。',
        description: '免安裝複雜軟體的桌面應用程式，取代手寫帳本與零散的 Excel，讓庫存一目了然。',
        features: ['商品資料管理與條碼列印', '進貨 / 出貨登記', '低庫存與缺貨自動警示', 'Excel 匯入匯出'],
        tags: ['Python', '桌面程式', 'SQLite', 'GUI'],
    },
    {
        id: 'bot-line', category: 'bot', image: 'images/showcase/bot-line.svg',
        title: 'LINE 官方帳號自動客服',
        summary: '訂位、會員集點、圖文選單，24 小時自動服務。',
        description: '讓 LINE 官方帳號變成店裡的小幫手，自動回覆常見問題、處理預約並推播通知。',
        features: ['自動訂位 / 預約與提醒', '訂單狀態即時推播', '數位會員卡與優惠券', '客製化圖文選單'],
        tags: ['LINE Bot', 'Python', 'Messaging API', '雲端部署'],
    },
    {
        id: 'bot-discord', category: 'bot', image: 'images/showcase/bot-discord.svg',
        title: 'Discord 社群機器人',
        summary: '抽獎、等級排行、指令互動，讓社群更熱絡。',
        description: '為遊戲或興趣社群打造專屬機器人，自動化活動管理，提升成員互動與黏著度。',
        features: ['斜線指令（Slash Command）', '抽獎活動與按鈕互動', '發言經驗值與等級排行', '管理員工具與自動通知'],
        tags: ['Discord.js', 'Node.js', '資料庫', '雲端部署'],
    },
    {
        id: 'game-platformer', category: 'game', image: 'images/showcase/game-platformer.svg',
        title: '2D 橫向平台跳躍遊戲',
        summary: '經典闖關玩法，金幣、敵人、關卡一應俱全。',
        description: '可直接在瀏覽器遊玩的 2D 動作遊戲，包含角色物理、碰撞判定與多個關卡設計。',
        features: ['角色移動、跳躍物理', '敵人 AI 與碰撞判定', '金幣、計分、計時系統', '多關卡與存檔'],
        tags: ['JavaScript', 'Canvas', 'Phaser', '遊戲設計'],
    },
    {
        id: 'game-match3', category: 'game', image: 'images/showcase/game-match3.svg',
        title: '寶石消除益智遊戲',
        summary: '連鎖 Combo、關卡目標、道具系統，越玩越上癮。',
        description: '經典三消玩法，加入關卡目標與特殊道具，適合做成行銷活動小遊戲或手機遊戲原型。',
        features: ['三消判定與連鎖 Combo', '關卡目標與步數限制', '炸彈、彩虹等特殊道具', '星等評分與排行榜'],
        tags: ['JavaScript', 'Canvas', '動畫', '遊戲設計'],
    },
    {
        id: 'game-shooter', category: 'game', image: 'images/showcase/game-shooter.svg',
        title: '太空射擊遊戲',
        summary: '彈幕閃避、Boss 戰、武器升級，爽快感十足。',
        description: '縱向捲軸射擊遊戲，具備多種敵機行為、Boss 戰與武器強化系統。',
        features: ['敵機編隊與彈幕設計', 'Boss 戰與血量條', '武器火力升級', '音效、爆炸特效'],
        tags: ['JavaScript', 'Canvas', '粒子特效', '遊戲設計'],
    },
];
