// ===== 作品展示牆資料（新增 / 調整作品只需修改此檔）=====
// 圖片由 tools/gen_showcase.py 產生，路徑為 images/showcase/<作品代碼>/<序號>.svg

// 燈箱內「委託類似作品」按鈕的連結
const SHOWCASE_CTA_URL = 'https://shopee.tw/product/84156043/48060712536/';

/**
 * @typedef {Object} ShowcaseCategory
 * @property {string} id    分類代碼
 * @property {string} label 顯示名稱
 */

/**
 * @typedef {Object} ShowcaseScreen
 * @property {string} src     圖片路徑
 * @property {string} caption 畫面說明
 */

/**
 * @typedef {Object} ShowcaseItem
 * @property {string}           id          唯一代碼（同圖片資料夾名稱）
 * @property {string}           category    對應 ShowcaseCategory.id
 * @property {string}           title       作品名稱
 * @property {string}           summary     卡片上的一句話簡介
 * @property {string}           description 燈箱內的完整說明
 * @property {string[]}         features    功能重點
 * @property {string[]}         tags        技術標籤
 * @property {ShowcaseScreen[]} screens     作品畫面（第一張為封面）
 */

/**
 * 依作品代碼與畫面說明產生畫面清單（純函式）
 * @param {string} id
 * @param {string[]} captions
 * @param {string} [ext='svg'] 圖片副檔名（示範作品為 svg，實際截圖為 png）
 * @returns {ShowcaseScreen[]}
 */
function buildScreens(id, captions, ext = 'svg') {
    return captions.map((caption, index) => ({ src: `images/showcase/${id}/${index + 1}.${ext}`, caption }));
}

/** @type {ShowcaseCategory[]} */
const SHOWCASE_CATEGORIES = [
    { id: 'all',        label: '全部' },
    { id: 'web',        label: '網頁設計' },
    { id: 'platform',   label: '架站平台' },
    { id: 'automation', label: '程式與自動化' },
    { id: 'bot',        label: '聊天機器人' },
    { id: 'game',       label: '遊戲設計' },
];

/** @type {ShowcaseItem[]} */
const SHOWCASE_ITEMS = [
    // ---------- 台指期＆BTC 交易系統（排最前面）----------
    {
        id: 'real-trading', category: 'automation',
        title: '台指期＆BTC 程式交易系統',
        summary: '實際運行中：永豐台指期、幣安 BTC 自動下單、跟單與 LINE 推播。',
        description: '我自己開發並每天實際使用的交易系統，整合永豐 Shioaji 與幣安 API，涵蓋行情處理、策略訊號、自動下單、部位對帳、風險控管與 LINE 即時推播。自 2026 年 5 月起持續改版，約 5 萬行 Python、近 470 次版本紀錄。截圖中的帳號、持倉與策略參數已做遮蔽。本作品展示的是系統開發能力，不提供投資建議或代客操作。',
        features: [
            '永豐 Shioaji API 連線，帳戶與持倉即時查詢',
            '五支策略組合實盤，決策邏輯與回測同源',
            'BTC 幣安永續合約 24 小時自動交易與多層風控',
            '跟單引擎：每秒同步另一帳號部位，異常即停機並 LINE 通知',
            '歷史回測與 Walk-Forward 樣本外驗證',
            '每日財經新聞 AI 分析（Claude／Gemini／Groq）',
            '紀錄與通知自動遮蔽 token、身分證等敏感資料',
        ],
        tags: ['Python', 'Shioaji API', 'Binance API', 'LINE Bot', 'pandas'],
        screens: buildScreens('real-trading', ['實盤連線與帳戶監控', '多策略組合實盤', 'BTC 24 小時自動交易', '跟單引擎', '策略回測與參數設定', '每日財經新聞 AI 分析'], 'png'),
    },

    // ---------- 網頁設計 ----------
    {
        id: 'web-cafe', category: 'web',
        title: '咖啡廳品牌形象官網',
        summary: '溫暖質感的品牌網站，含菜單、線上訂位與門市資訊。',
        description: '為實體店家打造的品牌官網，從配色、排版到文案風格一次到位，手機與電腦都能完美瀏覽。',
        features: ['響應式設計（手機 / 平板 / 電腦）', '菜單分類與今日推薦', '線上訂位：日期、時段、人數即時確認', '門市據點與地圖導航'],
        tags: ['HTML', 'CSS', 'JavaScript', 'RWD'],
        screens: buildScreens('web-cafe', ['首頁', '菜單頁', '線上訂位', '門市據點', '手機版畫面']),
    },
    {
        id: 'web-shop', category: 'web',
        title: '電商購物網站',
        summary: '商品篩選、購物車、會員中心與物流追蹤一應俱全。',
        description: '完整的線上商店，支援商品分類、篩選搜尋、購物車與多種付款方式，會員可隨時追蹤訂單物流。',
        features: ['商品分類、品牌與價格篩選', '商品規格選擇與庫存顯示', '購物車、優惠券與多元付款', '會員中心與物流進度追蹤'],
        tags: ['React', 'Node.js', '金流串接', 'Firebase'],
        screens: buildScreens('web-shop', ['首頁', '商品列表與篩選', '商品詳細頁', '購物車結帳', '會員中心 · 訂單追蹤']),
    },
    {
        id: 'web-dashboard', category: 'web',
        title: '營運數據管理後台',
        summary: '營收、訂單、商品、會員一站管理，老闆一眼看懂。',
        description: '把分散在各系統的資料彙整成一個後台，支援訂單批次處理、商品上下架、會員分析與兩步驟驗證登入。',
        features: ['KPI 指標卡與營收趨勢圖', '訂單管理與批次出貨', '商品上下架與庫存警示', '會員分群與回購留存分析', '兩步驟驗證登入、權限分級'],
        tags: ['Vue', 'Chart.js', 'REST API', '資料庫'],
        screens: buildScreens('web-dashboard', ['營運總覽', '訂單管理', '商品管理', '會員分析', '登入頁（兩步驟驗證）']),
    },

    // ---------- 架站平台 ----------
    {
        id: 'platform-shopify', category: 'platform',
        title: 'Shopify 品牌電商官網',
        summary: '保養品牌的 Shopify 商店，含定期訂閱與主題客製。',
        description: '以 Shopify 架設品牌電商，從主題客製、商品與訂閱方案設定，到金流物流串接與後台數據追蹤一次完成，品牌自己也能輕鬆維護。',
        features: ['主題版型客製與品牌視覺', '定期配送訂閱方案', '折扣碼、首購優惠設定', '超商取貨、宅配運送設定', '後台數據與熱銷商品分析'],
        tags: ['Shopify', 'Liquid', '電商', '訂閱制'],
        screens: buildScreens('platform-shopify', ['商店首頁', '商品頁（定期配送）', '結帳頁', '商店後台 · 數據分析', '主題自訂編輯器']),
    },
    {
        id: 'platform-woocommerce', category: 'platform',
        title: 'WooCommerce 茶行網路商店',
        summary: 'WordPress + WooCommerce 打造的線上購物網站。',
        description: '適合已有 WordPress 網站、想加上購物功能的店家；支援商品規格、特價、台灣常用付款方式與銷售報表。',
        features: ['商品分類、規格與特價設定', '價格篩選與熱門標籤', '信用卡、ATM、超商代碼付款', '滿額免運與優惠券', '銷售報表與熱銷排行'],
        tags: ['WooCommerce', 'WordPress', 'PHP', '金流外掛'],
        screens: buildScreens('platform-woocommerce', ['商店首頁', '商品分類頁', '單一商品頁', '結帳頁（台灣付款方式）', 'WordPress 後台 · 銷售報表']),
    },
    {
        id: 'platform-wordpress', category: 'platform',
        title: 'WordPress 室內設計官網',
        summary: '作品集、部落格、預約諮詢，客戶自己就能更新內容。',
        description: '以 WordPress 打造的企業形象網站，搭配區塊編輯器，非工程背景的店家也能自行發文、更新作品案例。',
        features: ['作品案例分類展示', '部落格與 SEO 設定', '文章目錄與社群分享', '預約諮詢表單', '交付後台操作教學'],
        tags: ['WordPress', '佈景主題', 'SEO', 'RWD'],
        screens: buildScreens('platform-wordpress', ['首頁', '作品案例頁', '部落格列表', '文章內頁', '區塊編輯器（後台）']),
    },

    // ---------- 程式與自動化 ----------
    {
        id: 'auto-excel', category: 'automation',
        title: 'Excel 自動化月報表',
        summary: '多檔案自動合併、產出圖表並寄信，月報一鍵完成。',
        description: '讀取各部門匯出的原始資料，自動清洗彙整、套用格式、產生圖表，最後依排程寄送給相關主管。',
        features: ['多檔案自動合併與資料清洗', '條件式格式（達標 / 未達自動標色）', '自動產生圖表儀表板', '排程執行並寄送 Email', '圖形化設定介面，免改程式'],
        tags: ['Python', 'openpyxl', 'Excel', '自動化'],
        screens: buildScreens('auto-excel', ['自動產出的月報表', '多檔案自動合併', '圖表儀表板', '自動寄出的報表信', '設定與排程介面']),
    },
    {
        id: 'auto-crawler', category: 'automation',
        title: '多平台比價爬蟲',
        summary: '每日定時抓取多個平台價格，降價自動推播 LINE。',
        description: '針對指定關鍵字定時抓取多個電商平台價格，清洗後寫入試算表與資料庫，並透過 LINE 推播降價提醒。',
        features: ['多平台同時抓取、排程執行', '設定檔管理關鍵字與門檻', '寫入 Google 試算表 / MySQL', 'LINE 降價即時通知', '價格走勢儀表板'],
        tags: ['Python', '爬蟲', 'Google Sheet', 'LINE Notify'],
        screens: buildScreens('auto-crawler', ['爬蟲執行與比價結果', '設定檔', 'Google 試算表紀錄', 'LINE 降價通知', '價格追蹤儀表板']),
    },
    // 示範版「量化交易策略回測系統」(auto-trading) 已由上方台指期＆BTC 交易系統取代；圖片與產生器保留，需要時加回此處即可
    {
        id: 'app-inventory', category: 'automation',
        title: '桌面版庫存管理系統',
        summary: '進出貨、盤點、報表、條碼列印，小公司也能輕鬆管理。',
        description: '取代手寫帳本與零散 Excel 的桌面應用程式，支援條碼掃描，讓庫存一目了然。',
        features: ['商品資料管理與低庫存警示', '進貨登記與條碼快速輸入', '掃碼盤點與差異比對', '進出貨報表與呆滯品提醒', '條碼標籤批次列印'],
        tags: ['Python', '桌面程式', 'SQLite', 'GUI'],
        screens: buildScreens('app-inventory', ['商品清單', '進貨登記', '盤點作業', '報表統計', '條碼標籤列印']),
    },

    // ---------- 聊天機器人 ----------
    {
        id: 'bot-line', category: 'bot',
        title: 'LINE 官方帳號自動客服',
        summary: '自動回覆、線上預約、會員集點、推播行銷一次到位。',
        description: '讓 LINE 官方帳號變成店裡的小幫手，自動回覆常見問題、處理預約、經營會員，並提供店家專用管理後台。',
        features: ['自動回覆與圖文選單', 'LINE 內直接線上預約', '數位會員卡與集點優惠券', '預約管理後台', '分眾推播與排程發送'],
        tags: ['LINE Bot', 'LIFF', 'Messaging API', '雲端部署'],
        screens: buildScreens('bot-line', ['自動客服對話', '線上預約（LINE 內開啟）', '數位會員卡與集點', '預約管理後台', '推播訊息排程']),
    },
    {
        id: 'bot-discord', category: 'bot',
        title: 'Discord 社群機器人',
        summary: '抽獎、等級、身分組、音樂點播，附網頁控制台。',
        description: '為遊戲或興趣社群打造專屬機器人，自動化活動與管理，並提供網頁控制台讓管理員開關功能。',
        features: ['抽獎活動與等級排行', '新成員歡迎圖卡與身分組按鈕', '語音頻道音樂點播', '網頁控制台模組開關', '斜線指令（Slash Command）'],
        tags: ['Discord.js', 'Node.js', '資料庫', '雲端部署'],
        screens: buildScreens('bot-discord', ['抽獎活動與排行榜', '新成員歡迎與身分組', '音樂點播', '網頁控制台', '斜線指令選單']),
    },

    // ---------- 遊戲設計 ----------
    {
        id: 'game-mahjong', category: 'game',
        title: '台灣 16 張麻將（多人連線）',
        summary: '大廳、牌桌、台數自動計算、好友房，完整連線麻將。',
        description: '完整實作台灣 16 張麻將規則的多人連線遊戲，包含吃碰槓胡判定、台數自動計算、好友開房與排行榜系統。',
        features: ['吃、碰、槓、聽、胡牌判定', '台數自動計算（自摸、門清、刻子等）', '好友房自訂規則與房號邀請', '即時多人連線對戰', '戰績統計與排行榜'],
        tags: ['JavaScript', 'WebSocket', 'Node.js', '遊戲設計'],
        screens: buildScreens('game-mahjong', ['遊戲大廳', '牌桌對局', '胡牌結算 · 台數計算', '建立好友房', '個人戰績與排行榜']),
    },
    {
        id: 'game-cardbattle', category: 'game',
        title: '集換式卡牌對戰遊戲',
        summary: '牌組構築、開卡包、英雄技能，策略卡牌對戰。',
        description: '回合制集換式卡牌對戰遊戲，包含卡牌效果系統、法力水晶、英雄技能、牌組構築與抽卡機制。',
        features: ['卡牌效果與嘲諷、戰吼等關鍵字', '法力水晶與回合制戰鬥', '牌組構築與法力曲線', '開卡包與稀有度系統', '英雄選擇與英雄技能'],
        tags: ['TypeScript', 'Canvas', '遊戲平衡', '遊戲設計'],
        screens: buildScreens('game-cardbattle', ['主選單', '對戰畫面', '牌組構築', '開卡包', '英雄選擇']),
    },
    {
        id: 'game-tactics', category: 'game',
        title: '戰棋策略 RPG',
        summary: '格子地圖、地形效果、武器相剋、劇情對話。',
        description: '回合制戰棋角色扮演遊戲，包含地形加成、移動範圍計算、武器相剋、戰鬥預測、角色成長與劇情系統。',
        features: ['格子地圖與移動範圍（尋路演算法）', '地形防禦與迴避加成', '武器相剋與戰鬥預測', '角色升級、轉職與裝備', '劇情對話與分歧選項'],
        tags: ['C#', 'Unity', 'AI 演算法', '遊戲設計'],
        screens: buildScreens('game-tactics', ['標題畫面', '戰場地圖 · 移動範圍', '戰鬥預測與戰鬥畫面', '角色能力與裝備', '劇情對話']),
    },
    {
        id: 'game-platformer', category: 'game',
        title: '2D 橫向平台跳躍遊戲',
        summary: '經典闖關玩法，世界地圖、角色選擇、Boss 戰。',
        description: '可直接在瀏覽器遊玩的 2D 動作遊戲，包含角色物理、碰撞判定、多角色能力與關卡設計。',
        features: ['角色移動、跳躍物理', '敵人 AI 與碰撞判定', '世界地圖與關卡解鎖', '多角色不同能力', 'Boss 戰與多階段攻擊'],
        tags: ['JavaScript', 'Canvas', 'Phaser', '遊戲設計'],
        screens: buildScreens('game-platformer', ['標題畫面', '世界地圖', '遊戲畫面', '角色選擇', 'Boss 戰']),
    },
    {
        id: 'game-match3', category: 'game',
        title: '寶石消除益智遊戲',
        summary: '連鎖 Combo、關卡地圖、道具商店，越玩越上癮。',
        description: '經典三消玩法，加入關卡目標、道具與商店系統，適合做成行銷活動小遊戲或手機遊戲原型。',
        features: ['三消判定與連鎖 Combo', '關卡地圖與星等評分', '炸彈、彩虹等特殊道具', '道具商店與禮包', '過關結算與獎勵'],
        tags: ['JavaScript', 'Canvas', '動畫', '遊戲設計'],
        screens: buildScreens('game-match3', ['標題畫面', '關卡地圖', '遊戲畫面', '道具商店', '過關結算']),
    },
    {
        id: 'game-shooter', category: 'game',
        title: '太空射擊遊戲',
        summary: '多機體選擇、武器研發、Boss 戰與全球排行榜。',
        description: '縱向捲軸射擊遊戲，具備多種敵機行為、Boss 戰、機體選擇與武器升級系統。',
        features: ['敵機編隊與彈幕設計', '三種機體不同屬性', '武器研發科技樹', 'Boss 戰與血量條', '任務評價與排行榜'],
        tags: ['JavaScript', 'Canvas', '粒子特效', '遊戲設計'],
        screens: buildScreens('game-shooter', ['標題畫面', '機庫 · 選擇機體', '遊戲畫面', '武器研發', '任務結算與排行榜']),
    },
];
