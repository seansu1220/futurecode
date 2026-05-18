// ===== 設定 =====
const FIREBASE_CONFIG = {
    apiKey:            "AIzaSyAweLS1tjYntmk14TinElVMEkCn8g2wQss",
    authDomain:        "futurecode-9da9e.firebaseapp.com",
    projectId:         "futurecode-9da9e",
    storageBucket:     "futurecode-9da9e.firebasestorage.app",
    messagingSenderId: "134105605896",
    appId:             "1:134105605896:web:43bbd961657650e488aebd",
};

// 擁有者 UID（固定，不可透過介面更改）
const OWNER_UID = 'QSGTkyJ1PjMk0kF6RiIbxFHfQVT2';

// ===== 初始資料（首次建立資料庫時使用）=====
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
const auth = firebase.auth();
const googleProvider = new firebase.auth.GoogleAuthProvider();

// ===== 狀態 =====
let currentUser = null;
let currentRole = null; // 'owner' | 'admin' | 'user' | null
let editingToolId = null;
let editingPortfolioId = null;
let captchaAnswer = null;

// ===== 權限判斷 =====
const isOwner  = () => currentRole === 'owner';
const canAdd   = () => ['owner', 'admin'].includes(currentRole);
const canEdit  = () => currentRole === 'owner';
const canDelete = () => currentRole === 'owner';

// ===== 密碼強度驗證 =====
function isStrongPassword(pw) {
    return pw.length >= 8 &&
           /[A-Z]/.test(pw) &&
           /[a-z]/.test(pw) &&
           /[0-9]/.test(pw) &&
           /[^A-Za-z0-9]/.test(pw);
}

// ===== 驗證碼 =====
function refreshCaptcha(displayId, inputId) {
    const a = Math.floor(Math.random() * 9) + 1;
    const b = Math.floor(Math.random() * 9) + 1;
    captchaAnswer = a + b;
    document.getElementById(displayId).textContent = `${a} + ${b} = ?`;
    document.getElementById(inputId).value = '';
}

function checkCaptcha(inputId) {
    return parseInt(document.getElementById(inputId).value, 10) === captchaAnswer;
}

// ===== 認證狀態監聽 =====
auth.onAuthStateChanged(async (user) => {
    if (user) {
        currentUser = user;
        await resolveRole(user);
    } else {
        currentUser = null;
        currentRole = null;
    }
    updateAuthUI();
    await loadAll();
});

async function resolveRole(user) {
    const ref = db.collection('users').doc(user.uid);
    const snap = await ref.get();

    if (user.uid === OWNER_UID) {
        currentRole = 'owner';
        if (!snap.exists) {
            await ref.set({
                username: 'seansu1220',
                email: user.email || '',
                role: 'owner',
                createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            });
        }
        return;
    }

    if (snap.exists) {
        const data = snap.data();
        if (data.disabled) {
            await auth.signOut();
            alert('此帳號已被停用，請聯繫管理員。');
            return;
        }
        currentRole = data.role || 'user';
    } else {
        // 第一次 Google 登入，自動建立用戶文件
        currentRole = 'user';
        await ref.set({
            username: user.displayName || user.email.split('@')[0],
            email: user.email || '',
            role: 'user',
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        });
    }
}

// ===== 登入（帳號或信箱 + 密碼）=====
async function loginWithEmail() {
    const input   = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errorEl  = document.getElementById('loginError');

    if (!input || !password) { showAuthError(errorEl, '請填寫帳號與密碼'); return; }
    if (!checkCaptcha('loginCaptchaInput')) {
        showAuthError(errorEl, '驗證碼錯誤，請再試一次');
        refreshCaptcha('loginCaptchaText', 'loginCaptchaInput');
        return;
    }

    try {
        let email = input;
        if (!input.includes('@')) {
            const qs = await db.collection('users').where('username', '==', input).limit(1).get();
            if (qs.empty) {
                showAuthError(errorEl, '帳號不存在，請確認或改用信箱登入');
                return;
            }
            email = qs.docs[0].data().email;
        }
        await auth.signInWithEmailAndPassword(email, password);
        closeModal('loginModal');
    } catch {
        showAuthError(errorEl, '帳號或密碼錯誤');
        refreshCaptcha('loginCaptchaText', 'loginCaptchaInput');
    }
}

// ===== Google 登入 =====
async function loginWithGoogle() {
    try {
        await auth.signInWithPopup(googleProvider);
        closeModal('loginModal');
        closeModal('registerModal');
    } catch (e) {
        const el = document.getElementById('loginError');
        showAuthError(el, 'Google 登入失敗，請再試一次');
    }
}

// ===== 登出 =====
async function logout() {
    await auth.signOut();
}

// ===== 註冊 =====
async function registerUser() {
    const username = document.getElementById('regUsername').value.trim();
    const email    = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    const confirm  = document.getElementById('regConfirmPassword').value;
    const errorEl  = document.getElementById('regError');

    if (!username || !email || !password || !confirm) { showAuthError(errorEl, '請填寫所有欄位'); return; }
    if (password !== confirm) { showAuthError(errorEl, '兩次輸入的密碼不一致'); return; }
    if (!isStrongPassword(password)) {
        showAuthError(errorEl, '密碼需至少 8 碼，並包含大寫字母、小寫字母、數字及特殊符號（如 @#$!）');
        return;
    }
    if (!checkCaptcha('regCaptchaInput')) {
        showAuthError(errorEl, '驗證碼錯誤，請再試一次');
        refreshCaptcha('regCaptchaText', 'regCaptchaInput');
        return;
    }

    // 檢查帳號是否重複
    const qs = await db.collection('users').where('username', '==', username).limit(1).get();
    if (!qs.empty) { showAuthError(errorEl, '此帳號名稱已被使用'); return; }

    try {
        const cred = await auth.createUserWithEmailAndPassword(email, password);
        await db.collection('users').doc(cred.user.uid).set({
            username, email, role: 'user',
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        });
        closeModal('registerModal');
    } catch (e) {
        if (e.code === 'auth/email-already-in-use') showAuthError(errorEl, '此信箱已被註冊');
        else if (e.code === 'auth/invalid-email')   showAuthError(errorEl, '信箱格式不正確');
        else showAuthError(errorEl, '註冊失敗，請稍後再試');
    }
}

function showAuthError(el, msg) {
    el.textContent = msg;
    el.classList.remove('hidden');
}

// ===== 帳號設定 =====
async function openAccountSettings() {
    if (!currentUser) return;
    await currentUser.reload();
    const providers = currentUser.providerData.map(p => p.providerId);
    const hasGoogle   = providers.includes('google.com');
    const hasPassword = providers.includes('password');

    const methodList = [
        hasPassword ? '📧 信箱／密碼' : null,
        hasGoogle   ? '🔵 Google'     : null,
    ].filter(Boolean).join('、');

    document.getElementById('providerList').innerHTML =
        `<p style="color:var(--text-secondary);font-size:0.9rem;">已連結：<strong style="color:var(--text-primary);">${methodList}</strong></p>`;

    document.getElementById('linkGoogleArea').classList.toggle('hidden', hasGoogle);
    document.getElementById('alreadyLinked').classList.toggle('hidden', !hasGoogle);
    document.getElementById('accountMsg').classList.add('hidden');

    openModal('accountModal');
}

async function linkWithGoogle() {
    const msgEl = document.getElementById('accountMsg');
    try {
        await currentUser.linkWithPopup(googleProvider);
        msgEl.style.color = 'var(--color-cyan)';
        msgEl.textContent = '✅ Google 帳號連結成功！';
        msgEl.classList.remove('hidden');
        await openAccountSettings();
    } catch (e) {
        msgEl.style.color = '#f87171';
        if (e.code === 'auth/credential-already-in-use') {
            msgEl.textContent = '此 Google 帳號已被其他帳號使用';
        } else if (e.code === 'auth/popup-closed-by-user') {
            msgEl.textContent = '視窗被關閉，請再試一次';
        } else {
            msgEl.textContent = '連結失敗，請稍後再試';
        }
        msgEl.classList.remove('hidden');
    }
}

// ===== Modal 切換 =====
function switchToRegister() {
    closeModal('loginModal');
    document.getElementById('regError').classList.add('hidden');
    clearForm(['regUsername', 'regEmail', 'regPassword', 'regConfirmPassword']);
    refreshCaptcha('regCaptchaText', 'regCaptchaInput');
    openModal('registerModal');
}

function switchToLogin() {
    closeModal('registerModal');
    document.getElementById('loginError').classList.add('hidden');
    clearForm(['loginUsername', 'loginPassword']);
    refreshCaptcha('loginCaptchaText', 'loginCaptchaInput');
    openModal('loginModal');
}

// ===== 更新 Auth UI =====
function updateAuthUI() {
    const loginBtn          = document.getElementById('loginBtn');
    const userInfoEl        = document.getElementById('userInfo');
    const adminToolBar      = document.getElementById('adminToolBar');
    const adminPortfolioBar = document.getElementById('adminPortfolioBar');
    const userMgmtBtn       = document.getElementById('userMgmtBtn');
    const accountSettingsBtn = document.getElementById('accountSettingsBtn');

    if (currentUser) {
        loginBtn.textContent = '登出';
        loginBtn.classList.add('active');
        const labels = { owner: '👑 擁有者', admin: '🔑 管理員', user: '👤 一般用戶' };
        userInfoEl.textContent = labels[currentRole] || '👤';
        userInfoEl.classList.remove('hidden');
    } else {
        loginBtn.textContent = '登入';
        loginBtn.classList.remove('active');
        userInfoEl.classList.add('hidden');
    }

    adminToolBar.classList.toggle('hidden', !canAdd());
    adminPortfolioBar.classList.toggle('hidden', !canAdd());
    if (userMgmtBtn) userMgmtBtn.classList.toggle('hidden', !isOwner());
    if (accountSettingsBtn) accountSettingsBtn.classList.toggle('hidden', !currentUser);
}

// ===== 用戶管理 =====
async function openUserMgmt() {
    if (!isOwner()) return;
    const snap = await db.collection('users').orderBy('createdAt', 'asc').get();
    const users = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));

    document.getElementById('userMgmtList').innerHTML = users.map(u => {
        const isDisabled = !!u.disabled;
        const isMe = u.id === OWNER_UID;
        return `
        <tr ${isDisabled ? 'style="opacity:0.45;"' : ''}>
            <td>${escHtml(u.username || '-')}${isDisabled ? ' <span style="color:#f87171;font-size:0.75rem;">（停用）</span>' : ''}</td>
            <td>${escHtml(u.email || '-')}</td>
            <td>
                <select class="role-select" data-uid="${escHtml(u.id)}" ${isMe || isDisabled ? 'disabled' : ''}>
                    <option value="user"  ${u.role === 'user'  ? 'selected' : ''}>一般用戶</option>
                    <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>管理員</option>
                    ${isMe ? '<option value="owner" selected>擁有者</option>' : ''}
                </select>
            </td>
            <td style="display:flex;gap:6px;flex-wrap:wrap;">
                ${isMe ? '<span class="owner-tag">不可修改</span>' : `
                    ${!isDisabled ? `<button class="btn-admin" onclick="saveUserRole('${escHtml(u.id)}')" style="padding:4px 10px;font-size:0.75rem;">儲存</button>` : ''}
                    <button class="btn-danger" onclick="${isDisabled ? `restoreUser('${escHtml(u.id)}')` : `disableUser('${escHtml(u.id)}')`}"
                        style="padding:4px 10px;font-size:0.75rem;">
                        ${isDisabled ? '恢復' : '停用'}
                    </button>
                `}
            </td>
        </tr>`;
    }).join('');

    openModal('userMgmtModal');
}

async function saveUserRole(uid) {
    if (!isOwner() || uid === OWNER_UID) return;
    const select = document.querySelector(`.role-select[data-uid="${uid}"]`);
    try {
        await db.collection('users').doc(uid).update({ role: select.value });
        alert('角色已更新');
    } catch (e) {
        alert('更新失敗：' + e.message);
    }
}

async function disableUser(uid) {
    if (!isOwner() || uid === OWNER_UID) return;
    if (!confirm('確定要停用此帳號嗎？該用戶將立即無法登入。')) return;
    try {
        await db.collection('users').doc(uid).update({ disabled: true });
        await openUserMgmt();
    } catch (e) {
        alert('操作失敗：' + e.message);
    }
}

async function restoreUser(uid) {
    if (!isOwner() || uid === OWNER_UID) return;
    if (!confirm('確定要恢復此帳號嗎？')) return;
    try {
        await db.collection('users').doc(uid).update({ disabled: false });
        await openUserMgmt();
    } catch (e) {
        alert('操作失敗：' + e.message);
    }
}

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    bindEvents();
    // 資料載入由 onAuthStateChanged 觸發，不在此重複呼叫
});

// ===== 載入所有資料 =====
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

    renderTools(snap.docs.map(doc => ({ id: doc.id, ...doc.data() })));
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

    renderPortfolio(snap.docs.map(doc => ({ id: doc.id, ...doc.data() })));
}

// ===== 渲染工具 =====
function renderTools(tools) {
    const grid  = document.getElementById('toolsGrid');
    const empty = document.getElementById('toolsEmpty');

    if (!tools || tools.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = tools.map(t => `
        <div class="tool-card">
            ${canEdit() ? `
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
    const grid  = document.getElementById('portfolioGrid');
    const empty = document.getElementById('portfolioEmpty');

    if (!items || items.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = items.map(item => `
        <div class="portfolio-card">
            ${canEdit() ? `
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
    if (!canAdd()) return;
    editingToolId = null;
    document.getElementById('toolModalTitle').textContent = '新增工具';
    clearForm(['toolIcon', 'toolName', 'toolDesc', 'toolUrl']);
    openModal('toolModal');
}

async function openEditTool(id) {
    if (!canEdit()) return;
    const doc = await db.collection('tools').doc(id).get();
    if (!doc.exists) return;
    const t = doc.data();
    editingToolId = id;
    document.getElementById('toolModalTitle').textContent = '編輯工具';
    document.getElementById('toolIcon').value  = t.icon || '';
    document.getElementById('toolName').value  = t.name || '';
    document.getElementById('toolDesc').value  = t.desc || '';
    document.getElementById('toolUrl').value   = t.url  || '';
    openModal('toolModal');
}

async function saveTool() {
    if (!canAdd()) return;
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
            if (!canEdit()) return;
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
    if (!canDelete()) return;
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
    if (!canAdd()) return;
    editingPortfolioId = null;
    document.getElementById('portfolioModalTitle').textContent = '新增作品';
    clearForm(['portfolioIcon', 'portfolioName', 'portfolioDesc', 'portfolioTags', 'portfolioUrl']);
    openModal('portfolioModal');
}

async function openEditPortfolio(id) {
    if (!canEdit()) return;
    const doc = await db.collection('portfolio').doc(id).get();
    if (!doc.exists) return;
    const item = doc.data();
    editingPortfolioId = id;
    document.getElementById('portfolioModalTitle').textContent = '編輯作品';
    document.getElementById('portfolioIcon').value = item.icon || '';
    document.getElementById('portfolioName').value = item.name || '';
    document.getElementById('portfolioDesc').value = item.desc || '';
    document.getElementById('portfolioTags').value = (item.tags || []).join(', ');
    document.getElementById('portfolioUrl').value  = item.url  || '';
    openModal('portfolioModal');
}

async function savePortfolioItem() {
    if (!canAdd()) return;
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
            if (!canEdit()) return;
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
    if (!canDelete()) return;
    if (!confirm('確定要刪除這個作品嗎？')) return;
    try {
        await db.collection('portfolio').doc(id).delete();
        await loadPortfolio();
    } catch (e) {
        alert('刪除失敗：' + e.message);
    }
}

// ===== Modal 控制 =====
function openModal(id)  { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }
function clearForm(ids) { ids.forEach(id => { document.getElementById(id).value = ''; }); }

// ===== 事件綁定 =====
function bindEvents() {
    // 漢堡選單
    document.getElementById('navToggle').addEventListener('click', () => {
        document.getElementById('navLinks').classList.toggle('open');
    });
    document.querySelectorAll('.nav-links a').forEach(a => {
        a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open'));
    });

    // 登入/登出按鈕
    document.getElementById('loginBtn').addEventListener('click', () => {
        if (currentUser) {
            logout();
        } else {
            document.getElementById('loginError').classList.add('hidden');
            clearForm(['loginUsername', 'loginPassword']);
            refreshCaptcha('loginCaptchaText', 'loginCaptchaInput');
            openModal('loginModal');
            setTimeout(() => document.getElementById('loginUsername').focus(), 100);
        }
    });

    // 用戶管理
    document.getElementById('userMgmtBtn').addEventListener('click', openUserMgmt);

    // 帳號設定
    document.getElementById('accountSettingsBtn').addEventListener('click', openAccountSettings);

    // 登入 Modal
    document.getElementById('loginSubmit').addEventListener('click', loginWithEmail);
    document.getElementById('loginGoogleBtn').addEventListener('click', loginWithGoogle);
    document.getElementById('loginCaptchaInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') loginWithEmail();
    });
    document.getElementById('loginPassword').addEventListener('keydown', e => {
        if (e.key === 'Enter') loginWithEmail();
    });
    document.getElementById('loginCancel').addEventListener('click', () => closeModal('loginModal'));
    document.getElementById('toRegister').addEventListener('click', e => { e.preventDefault(); switchToRegister(); });

    // 註冊 Modal
    document.getElementById('regSubmit').addEventListener('click', registerUser);
    document.getElementById('regGoogleBtn').addEventListener('click', loginWithGoogle);
    document.getElementById('regCancel').addEventListener('click', () => closeModal('registerModal'));
    document.getElementById('toLogin').addEventListener('click', e => { e.preventDefault(); switchToLogin(); });

    // 工具
    document.getElementById('addToolBtn').addEventListener('click', openAddTool);
    document.getElementById('toolSave').addEventListener('click', saveTool);
    document.getElementById('toolCancel').addEventListener('click', () => closeModal('toolModal'));

    // 作品集
    document.getElementById('addPortfolioBtn').addEventListener('click', openAddPortfolio);
    document.getElementById('portfolioSave').addEventListener('click', savePortfolioItem);
    document.getElementById('portfolioCancel').addEventListener('click', () => closeModal('portfolioModal'));

    // 點擊遮罩關閉 Modal
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', e => {
            if (e.target === overlay) overlay.classList.add('hidden');
        });
    });

    // 滾動導覽列效果
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
