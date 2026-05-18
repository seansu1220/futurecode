// ===== ① 填入你的 Firebase 設定 =====
// 從 Firebase 主控台複製貼上，格式如下：
const FIREBASE_CONFIG = {
    apiKey:            "AIzaSyAweLS1tjYntmk14TinElVMEkCn8g2wQss",
    authDomain:        "futurecode-9da9e.firebaseapp.com",
    projectId:         "futurecode-9da9e",
    storageBucket:     "futurecode-9da9e.firebasestorage.app",
    messagingSenderId: "134105605896",
    appId:             "1:134105605896:web:43bbd961657650e488aebd",
};

// ===== ② 管理員密碼 =====
const ADMIN_PASSWORD = 'future2025'; // ⚠️ 記得改成自己的密碼

// ===== 初始資料（只有第一次建立資料庫時使用）=====
const SEED_TOOLS = [
    { icon: '📝', name: '字數計算器', desc: '快速計算文字的字數、字元數與段落數，寫作必備！', url: '' },
    { icon: '🔧', name: 'JSON 格式化', desc: '美化或壓縮 JSON 資料，方便閱讀與 API 除錯。', url: '' },
];
const SEED_PORTFOLIO = [
    { icon: '📊', name: 'Excel 自動化報表腳本', desc: '為客戶製作自動化報表生成工具，每週節省 3 小時人工整理時間。', tags: ['Excel', 'VBA', '自動化'], url: '' },
    { icon: '🤖', name: 'LINE Bot 訂單通知', desc: '串接蝦皮 API，自動推送新訂單通知至 LINE 群組，即時掌握商機。', tags: ['LINE Bot', 'Python', 'API'], url: '' },
    { icon: '🕷️', name: '比價爬蟲工具', desc: '定時抓取多個電商平台商品價格，匯整至 Google Sheet 供比較分析。', tags: ['Python', '爬蟲', 'Google Sheet'], url: '' },
];

// ===== Firebase 初始化 =====
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.firestore();

// ===== 狀態 =====
let isAdmin = false;
let editingToolId = null;
let editingPortfolioId = null;

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', async () => {
    checkSession();
    bindEvents();
    await loadAll();
});

async function loadAll() {
    showLoading(true);
    try {
        await Promise.all([loadTools(), loadPortfolio()]);
    } catch (e) {
        console.error('載入資料失敗：', e);
        showError('資料庫連線失敗，請確認 Firebase 設定是否正確。');
    } finally {
        showLoading(false);
    }
}

function showLoading(on) {
    document.getElementById('toolsGrid').innerHTML = on ? '<p class="loading-msg">載入中...</p>' : '';
    document.getElementById('portfolioGrid').innerHTML = on ? '<p class="loading-msg">載入中...</p>' : '';
}

function showError(msg) {
    document.getElementById('toolsGrid').innerHTML = `<p class="error-msg-inline">${msg}</p>`;
}

// ===== 工具 — 讀取 =====
async function loadTools() {
    const col = db.collection('tools');
    const snap = await col.orderBy('createdAt', 'asc').get();

    if (snap.empty) {
        for (const t of SEED_TOOLS) {
            await col.add({ ...t, createdAt: firebase.firestore.FieldValue.serverTimestamp() });
        }
        return loadTools();
    }

    const tools = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderTools(tools);
}

// ===== 作品集 — 讀取 =====
async function loadPortfolio() {
    const col = db.collection('portfolio');
    const snap = await col.orderBy('createdAt', 'asc').get();

    if (snap.empty) {
        for (const p of SEED_PORTFOLIO) {
            await col.add({ ...p, createdAt: firebase.firestore.FieldValue.serverTimestamp() });
        }
        return loadPortfolio();
    }

    const items = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    renderPortfolio(items);
}

// ===== 渲染工具 =====
function renderTools(tools) {
    const grid = document.getElementById('toolsGrid');
    const empty = document.getElementById('toolsEmpty');

    if (!tools || tools.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = tools.map(t => `
        <div class="tool-card">
            ${isAdmin ? `
            <div class="card-admin-btns">
                <button class="btn-admin" onclick="openEditTool('${escHtml(t.id)}')" style="padding:4px 10px;font-size:0.75rem;">編輯</button>
                <button class="btn-danger" onclick="deleteTool('${escHtml(t.id)}')">刪除</button>
            </div>` : ''}
            <div class="tool-icon">${escHtml(t.icon || '🔧')}</div>
            <div class="tool-name">${escHtml(t.name)}</div>
            <div class="tool-desc">${escHtml(t.desc)}</div>
            ${t.url ? `<a href="${escHtml(t.url)}" target="_blank" class="tool-link">使用工具 →</a>` : ''}
        </div>
    `).join('');
}

// ===== 渲染作品集 =====
function renderPortfolio(items) {
    const grid = document.getElementById('portfolioGrid');
    const empty = document.getElementById('portfolioEmpty');

    if (!items || items.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = items.map(item => `
        <div class="portfolio-card">
            ${isAdmin ? `
            <div class="card-admin-btns">
                <button class="btn-admin" onclick="openEditPortfolio('${escHtml(item.id)}')" style="padding:4px 10px;font-size:0.75rem;">編輯</button>
                <button class="btn-danger" onclick="deletePortfolio('${escHtml(item.id)}')">刪除</button>
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
    clearForm(['toolIcon', 'toolName', 'toolDesc', 'toolUrl']);
    openModal('toolModal');
}

async function openEditTool(id) {
    const doc = await db.collection('tools').doc(id).get();
    if (!doc.exists) return;
    const t = doc.data();
    editingToolId = id;
    document.getElementById('toolModalTitle').textContent = '編輯工具';
    document.getElementById('toolIcon').value = t.icon || '';
    document.getElementById('toolName').value = t.name || '';
    document.getElementById('toolDesc').value = t.desc || '';
    document.getElementById('toolUrl').value = t.url || '';
    openModal('toolModal');
}

async function saveTool() {
    const name = document.getElementById('toolName').value.trim();
    if (!name) { alert('請填入工具名稱'); return; }

    const data = {
        icon: document.getElementById('toolIcon').value.trim() || '🔧',
        name,
        desc: document.getElementById('toolDesc').value.trim(),
        url:  document.getElementById('toolUrl').value.trim(),
    };

    try {
        if (editingToolId) {
            await db.collection('tools').doc(editingToolId).update(data);
        } else {
            data.createdAt = firebase.firestore.FieldValue.serverTimestamp();
            await db.collection('tools').add(data);
        }
        closeModal('toolModal');
        await loadTools();
    } catch (e) {
        alert('儲存失敗：' + e.message);
    }
}

async function deleteTool(id) {
    if (!confirm('確定要刪除這個工具嗎？')) return;
    try {
        await db.collection('tools').doc(id).delete();
        await loadTools();
    } catch (e) {
        alert('刪除失敗：' + e.message);
    }
}

// ===== 作品集 CRUD =====
function openAddPortfolio() {
    editingPortfolioId = null;
    document.getElementById('portfolioModalTitle').textContent = '新增作品';
    clearForm(['portfolioIcon', 'portfolioName', 'portfolioDesc', 'portfolioTags', 'portfolioUrl']);
    openModal('portfolioModal');
}

async function openEditPortfolio(id) {
    const doc = await db.collection('portfolio').doc(id).get();
    if (!doc.exists) return;
    const item = doc.data();
    editingPortfolioId = id;
    document.getElementById('portfolioModalTitle').textContent = '編輯作品';
    document.getElementById('portfolioIcon').value = item.icon || '';
    document.getElementById('portfolioName').value = item.name || '';
    document.getElementById('portfolioDesc').value = item.desc || '';
    document.getElementById('portfolioTags').value = (item.tags || []).join(', ');
    document.getElementById('portfolioUrl').value = item.url || '';
    openModal('portfolioModal');
}

async function savePortfolioItem() {
    const name = document.getElementById('portfolioName').value.trim();
    if (!name) { alert('請填入作品名稱'); return; }

    const tagsRaw = document.getElementById('portfolioTags').value.trim();
    const data = {
        icon: document.getElementById('portfolioIcon').value.trim() || '📁',
        name,
        desc: document.getElementById('portfolioDesc').value.trim(),
        tags: tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [],
        url:  document.getElementById('portfolioUrl').value.trim(),
    };

    try {
        if (editingPortfolioId) {
            await db.collection('portfolio').doc(editingPortfolioId).update(data);
        } else {
            data.createdAt = firebase.firestore.FieldValue.serverTimestamp();
            await db.collection('portfolio').add(data);
        }
        closeModal('portfolioModal');
        await loadPortfolio();
    } catch (e) {
        alert('儲存失敗：' + e.message);
    }
}

async function deletePortfolio(id) {
    if (!confirm('確定要刪除這個作品嗎？')) return;
    try {
        await db.collection('portfolio').doc(id).delete();
        await loadPortfolio();
    } catch (e) {
        alert('刪除失敗：' + e.message);
    }
}

// ===== 登入/登出 =====
function checkSession() {
    isAdmin = sessionStorage.getItem('futureAdmin') === 'true';
    updateAdminUI();
}

function login(password) {
    if (password === ADMIN_PASSWORD) {
        isAdmin = true;
        sessionStorage.setItem('futureAdmin', 'true');
        updateAdminUI();
        closeModal('loginModal');
        return true;
    }
    return false;
}

function logout() {
    isAdmin = false;
    sessionStorage.removeItem('futureAdmin');
    updateAdminUI();
}

function updateAdminUI() {
    const loginBtn = document.getElementById('loginBtn');
    const adminToolBar = document.getElementById('adminToolBar');
    const adminPortfolioBar = document.getElementById('adminPortfolioBar');

    loginBtn.textContent = isAdmin ? '登出' : '登入';
    loginBtn.classList.toggle('active', isAdmin);
    adminToolBar.classList.toggle('hidden', !isAdmin);
    adminPortfolioBar.classList.toggle('hidden', !isAdmin);

    loadAll();
}

// ===== Modal 控制 =====
function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }
function clearForm(ids) { ids.forEach(id => { document.getElementById(id).value = ''; }); }

// ===== 事件綁定 =====
function bindEvents() {
    document.getElementById('navToggle').addEventListener('click', () => {
        document.getElementById('navLinks').classList.toggle('open');
    });
    document.querySelectorAll('.nav-links a').forEach(a => {
        a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open'));
    });

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

    document.getElementById('loginSubmit').addEventListener('click', () => {
        if (!login(document.getElementById('passwordInput').value)) {
            document.getElementById('loginError').classList.remove('hidden');
        }
    });
    document.getElementById('passwordInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') document.getElementById('loginSubmit').click();
    });
    document.getElementById('loginCancel').addEventListener('click', () => closeModal('loginModal'));

    document.getElementById('addToolBtn').addEventListener('click', openAddTool);
    document.getElementById('toolSave').addEventListener('click', saveTool);
    document.getElementById('toolCancel').addEventListener('click', () => closeModal('toolModal'));

    document.getElementById('addPortfolioBtn').addEventListener('click', openAddPortfolio);
    document.getElementById('portfolioSave').addEventListener('click', savePortfolioItem);
    document.getElementById('portfolioCancel').addEventListener('click', () => closeModal('portfolioModal'));

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', e => { if (e.target === overlay) overlay.classList.add('hidden'); });
    });

    window.addEventListener('scroll', () => {
        document.getElementById('navbar').style.borderBottomColor =
            window.scrollY > 20 ? 'rgba(30,41,59,0.8)' : '';
    });
}

// ===== 工具函式 =====
function escHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
