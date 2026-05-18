// ===== 設定 =====
// ⚠️ 重要：發布前請修改這個密碼！
const ADMIN_PASSWORD = 'future2025';

const STORAGE_KEYS = {
    tools: 'futuretools_v1',
    portfolio: 'futureportfolio_v1',
    session: 'futurelogin_v1',
};

// 預設工具資料
const DEFAULT_TOOLS = [
    {
        id: 1,
        icon: '📝',
        name: '字數計算器',
        desc: '快速計算文字的字數、字元數與段落數，寫作必備！',
        url: '',
    },
    {
        id: 2,
        icon: '🔧',
        name: 'JSON 格式化',
        desc: '美化或壓縮 JSON 資料，方便閱讀與 API 除錯。',
        url: '',
    },
];

// 預設作品集資料
const DEFAULT_PORTFOLIO = [
    {
        id: 1,
        icon: '📊',
        name: 'Excel 自動化報表腳本',
        desc: '為客戶製作自動化報表生成工具，每週節省 3 小時人工整理時間。',
        tags: ['Excel', 'VBA', '自動化'],
        url: '',
    },
    {
        id: 2,
        icon: '🤖',
        name: 'LINE Bot 訂單通知',
        desc: '串接蝦皮 API，自動推送新訂單通知至 LINE 群組，即時掌握商機。',
        tags: ['LINE Bot', 'Python', 'API'],
        url: '',
    },
    {
        id: 3,
        icon: '🕷️',
        name: '比價爬蟲工具',
        desc: '定時抓取多個電商平台的商品價格，匯整至 Google Sheet 供比較分析。',
        tags: ['Python', '爬蟲', 'Google Sheet'],
        url: '',
    },
];

// ===== 狀態 =====
let isAdmin = false;
let tools = [];
let portfolio = [];
let editingToolId = null;
let editingPortfolioId = null;

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    checkSession();
    renderTools();
    renderPortfolio();
    bindEvents();
});

// ===== 資料讀取/儲存 =====
function loadData() {
    const savedTools = localStorage.getItem(STORAGE_KEYS.tools);
    tools = savedTools ? JSON.parse(savedTools) : [...DEFAULT_TOOLS];

    const savedPortfolio = localStorage.getItem(STORAGE_KEYS.portfolio);
    portfolio = savedPortfolio ? JSON.parse(savedPortfolio) : [...DEFAULT_PORTFOLIO];
}

function saveTools() {
    localStorage.setItem(STORAGE_KEYS.tools, JSON.stringify(tools));
}

function savePortfolio() {
    localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(portfolio));
}

// ===== 登入/登出 =====
function checkSession() {
    isAdmin = sessionStorage.getItem(STORAGE_KEYS.session) === 'true';
    updateAdminUI();
}

function login(password) {
    if (password === ADMIN_PASSWORD) {
        isAdmin = true;
        sessionStorage.setItem(STORAGE_KEYS.session, 'true');
        updateAdminUI();
        closeModal('loginModal');
        return true;
    }
    return false;
}

function logout() {
    isAdmin = false;
    sessionStorage.removeItem(STORAGE_KEYS.session);
    updateAdminUI();
}

function updateAdminUI() {
    const loginBtn = document.getElementById('loginBtn');
    const adminToolBar = document.getElementById('adminToolBar');
    const adminPortfolioBar = document.getElementById('adminPortfolioBar');

    if (isAdmin) {
        loginBtn.textContent = '登出';
        loginBtn.classList.add('active');
        adminToolBar.classList.remove('hidden');
        adminPortfolioBar.classList.remove('hidden');
    } else {
        loginBtn.textContent = '登入';
        loginBtn.classList.remove('active');
        adminToolBar.classList.add('hidden');
        adminPortfolioBar.classList.add('hidden');
    }
    renderTools();
    renderPortfolio();
}

// ===== 渲染工具 =====
function renderTools() {
    const grid = document.getElementById('toolsGrid');
    const empty = document.getElementById('toolsEmpty');

    if (tools.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = tools.map(tool => `
        <div class="tool-card" data-id="${tool.id}">
            ${isAdmin ? `
            <div class="card-admin-btns">
                <button class="btn-admin" onclick="openEditTool(${tool.id})" style="padding:4px 10px;font-size:0.75rem;">編輯</button>
                <button class="btn-danger" onclick="deleteTool(${tool.id})">刪除</button>
            </div>` : ''}
            <div class="tool-icon">${escHtml(tool.icon || '🔧')}</div>
            <div class="tool-name">${escHtml(tool.name)}</div>
            <div class="tool-desc">${escHtml(tool.desc)}</div>
            ${tool.url ? `<a href="${escHtml(tool.url)}" target="_blank" class="tool-link">使用工具 →</a>` : ''}
        </div>
    `).join('');
}

// ===== 渲染作品集 =====
function renderPortfolio() {
    const grid = document.getElementById('portfolioGrid');
    const empty = document.getElementById('portfolioEmpty');

    if (portfolio.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = portfolio.map(item => `
        <div class="portfolio-card" data-id="${item.id}">
            ${isAdmin ? `
            <div class="card-admin-btns">
                <button class="btn-admin" onclick="openEditPortfolio(${item.id})" style="padding:4px 10px;font-size:0.75rem;">編輯</button>
                <button class="btn-danger" onclick="deletePortfolio(${item.id})">刪除</button>
            </div>` : ''}
            <div class="portfolio-icon">${escHtml(item.icon || '📁')}</div>
            <div class="portfolio-name">${escHtml(item.name)}</div>
            <div class="portfolio-desc">${escHtml(item.desc)}</div>
            <div class="tags">${(item.tags || []).map(t => `<span class="tag">${escHtml(t)}</span>`).join('')}</div>
            ${item.url ? `<a href="${escHtml(item.url)}" target="_blank" class="portfolio-link">查看詳情 →</a>` : ''}
        </div>
    `).join('');
}

// ===== 工具 CRUD =====
function openAddTool() {
    editingToolId = null;
    document.getElementById('toolModalTitle').textContent = '新增工具';
    document.getElementById('toolId').value = '';
    document.getElementById('toolIcon').value = '';
    document.getElementById('toolName').value = '';
    document.getElementById('toolDesc').value = '';
    document.getElementById('toolUrl').value = '';
    openModal('toolModal');
}

function openEditTool(id) {
    const tool = tools.find(t => t.id === id);
    if (!tool) return;
    editingToolId = id;
    document.getElementById('toolModalTitle').textContent = '編輯工具';
    document.getElementById('toolId').value = id;
    document.getElementById('toolIcon').value = tool.icon || '';
    document.getElementById('toolName').value = tool.name || '';
    document.getElementById('toolDesc').value = tool.desc || '';
    document.getElementById('toolUrl').value = tool.url || '';
    openModal('toolModal');
}

function saveTool() {
    const name = document.getElementById('toolName').value.trim();
    if (!name) { alert('請填入工具名稱'); return; }

    const data = {
        icon: document.getElementById('toolIcon').value.trim() || '🔧',
        name,
        desc: document.getElementById('toolDesc').value.trim(),
        url: document.getElementById('toolUrl').value.trim(),
    };

    if (editingToolId) {
        const idx = tools.findIndex(t => t.id === editingToolId);
        if (idx !== -1) tools[idx] = { ...tools[idx], ...data };
    } else {
        data.id = Date.now();
        tools.push(data);
    }
    saveTools();
    renderTools();
    closeModal('toolModal');
}

function deleteTool(id) {
    if (!confirm('確定要刪除這個工具嗎？')) return;
    tools = tools.filter(t => t.id !== id);
    saveTools();
    renderTools();
}

// ===== 作品集 CRUD =====
function openAddPortfolio() {
    editingPortfolioId = null;
    document.getElementById('portfolioModalTitle').textContent = '新增作品';
    document.getElementById('portfolioId').value = '';
    document.getElementById('portfolioIcon').value = '';
    document.getElementById('portfolioName').value = '';
    document.getElementById('portfolioDesc').value = '';
    document.getElementById('portfolioTags').value = '';
    document.getElementById('portfolioUrl').value = '';
    openModal('portfolioModal');
}

function openEditPortfolio(id) {
    const item = portfolio.find(p => p.id === id);
    if (!item) return;
    editingPortfolioId = id;
    document.getElementById('portfolioModalTitle').textContent = '編輯作品';
    document.getElementById('portfolioId').value = id;
    document.getElementById('portfolioIcon').value = item.icon || '';
    document.getElementById('portfolioName').value = item.name || '';
    document.getElementById('portfolioDesc').value = item.desc || '';
    document.getElementById('portfolioTags').value = (item.tags || []).join(', ');
    document.getElementById('portfolioUrl').value = item.url || '';
    openModal('portfolioModal');
}

function savePortfolioItem() {
    const name = document.getElementById('portfolioName').value.trim();
    if (!name) { alert('請填入作品名稱'); return; }

    const tagsRaw = document.getElementById('portfolioTags').value.trim();
    const data = {
        icon: document.getElementById('portfolioIcon').value.trim() || '📁',
        name,
        desc: document.getElementById('portfolioDesc').value.trim(),
        tags: tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [],
        url: document.getElementById('portfolioUrl').value.trim(),
    };

    if (editingPortfolioId) {
        const idx = portfolio.findIndex(p => p.id === editingPortfolioId);
        if (idx !== -1) portfolio[idx] = { ...portfolio[idx], ...data };
    } else {
        data.id = Date.now();
        portfolio.push(data);
    }
    savePortfolio();
    renderPortfolio();
    closeModal('portfolioModal');
}

function deletePortfolio(id) {
    if (!confirm('確定要刪除這個作品嗎？')) return;
    portfolio = portfolio.filter(p => p.id !== id);
    savePortfolio();
    renderPortfolio();
}

// ===== Modal 控制 =====
function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
}

function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
}

// ===== 事件綁定 =====
function bindEvents() {
    // Navbar mobile
    document.getElementById('navToggle').addEventListener('click', () => {
        document.getElementById('navLinks').classList.toggle('open');
    });

    // 點擊 nav 連結時關閉選單
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            document.getElementById('navLinks').classList.remove('open');
        });
    });

    // 登入按鈕
    document.getElementById('loginBtn').addEventListener('click', () => {
        if (isAdmin) {
            logout();
        } else {
            document.getElementById('loginError').classList.add('hidden');
            document.getElementById('passwordInput').value = '';
            openModal('loginModal');
            setTimeout(() => document.getElementById('passwordInput').focus(), 100);
        }
    });

    // 登入 modal
    document.getElementById('loginSubmit').addEventListener('click', () => {
        const pw = document.getElementById('passwordInput').value;
        if (!login(pw)) {
            document.getElementById('loginError').classList.remove('hidden');
        }
    });
    document.getElementById('passwordInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') document.getElementById('loginSubmit').click();
    });
    document.getElementById('loginCancel').addEventListener('click', () => closeModal('loginModal'));

    // 工具 modal
    document.getElementById('addToolBtn').addEventListener('click', openAddTool);
    document.getElementById('toolSave').addEventListener('click', saveTool);
    document.getElementById('toolCancel').addEventListener('click', () => closeModal('toolModal'));

    // 作品集 modal
    document.getElementById('addPortfolioBtn').addEventListener('click', openAddPortfolio);
    document.getElementById('portfolioSave').addEventListener('click', savePortfolioItem);
    document.getElementById('portfolioCancel').addEventListener('click', () => closeModal('portfolioModal'));

    // 點擊 overlay 關閉 modal
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', e => {
            if (e.target === overlay) overlay.classList.add('hidden');
        });
    });

    // Navbar scroll 效果
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 20) {
            navbar.style.borderBottomColor = 'rgba(30, 41, 59, 0.8)';
        } else {
            navbar.style.borderBottomColor = '';
        }
    });
}

// ===== 工具函式 =====
function escHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}
