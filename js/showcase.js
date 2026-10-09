// ===== 作品展示牆（分類篩選 + 多畫面燈箱）=====
// 純前端顯示，不依賴 Firebase；資料來源為 showcase-data.js
(() => {
    const CARD_THUMB_COUNT = 4; // 卡片下方小縮圖數量（封面以外）

    let activeCategory = 'all';
    let visibleItems = [];
    let itemIndex = -1;   // 燈箱中目前的作品
    let screenIndex = 0;  // 燈箱中目前的畫面

    function escapeText(str) {
        return String(str ?? '')
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function categoryLabel(categoryId) {
        const found = SHOWCASE_CATEGORIES.find(c => c.id === categoryId);
        return found ? found.label : '';
    }

    /** 依分類篩選作品（純函式） */
    function filterItems(items, categoryId) {
        return categoryId === 'all' ? items : items.filter(item => item.category === categoryId);
    }

    /** 循環索引（純函式） */
    function wrapIndex(index, length) {
        return (index + length) % length;
    }

    function renderFilters() {
        document.getElementById('showcaseFilters').innerHTML = SHOWCASE_CATEGORIES.map(c => {
            const count = filterItems(SHOWCASE_ITEMS, c.id).length;
            const active = c.id === activeCategory;
            return `<button class="showcase-filter${active ? ' active' : ''}" data-category="${escapeText(c.id)}" role="tab"
                        aria-selected="${active}">${escapeText(c.label)}<span>${count}</span></button>`;
        }).join('');
    }

    function renderCard(item, index) {
        const [cover, ...rest] = item.screens;
        const thumbs = rest.slice(0, CARD_THUMB_COUNT).map((screen, i) => `
            <button class="showcase-mini" data-screen="${i + 1}" aria-label="查看${escapeText(screen.caption)}">
                <img src="${escapeText(screen.src)}" alt="" loading="lazy" width="160" height="100">
            </button>`).join('');
        return `
            <article class="showcase-card" data-index="${index}" tabindex="0" aria-label="查看 ${escapeText(item.title)}">
                <div class="showcase-thumb">
                    <img src="${escapeText(cover.src)}" alt="${escapeText(item.title)}：${escapeText(cover.caption)}" loading="lazy" width="800" height="500">
                    <span class="showcase-badge">${escapeText(categoryLabel(item.category))}</span>
                    ${item.isReal ? '<span class="showcase-real">✔ 實際作品</span>' : ''}
                    <span class="showcase-count">▦ ${item.screens.length} 個畫面</span>
                    <span class="showcase-zoom">點擊放大 ⤢</span>
                </div>
                <div class="showcase-minis">${thumbs}</div>
                <div class="showcase-body">
                    <h3>${escapeText(item.title)}</h3>
                    <p>${escapeText(item.summary)}</p>
                    <div class="tags">${item.tags.map(t => `<span class="tag">${escapeText(t)}</span>`).join('')}</div>
                </div>
            </article>`;
    }

    function renderGrid() {
        visibleItems = filterItems(SHOWCASE_ITEMS, activeCategory);
        document.getElementById('showcaseGrid').innerHTML = visibleItems.map(renderCard).join('');
    }

    // ---------- 燈箱 ----------
    function renderLightboxScreen() {
        const item = visibleItems[itemIndex];
        const screen = item.screens[screenIndex];
        const img = document.getElementById('lightboxImage');
        img.src = screen.src;
        img.alt = `${item.title}：${screen.caption}`;
        document.getElementById('lightboxCaption').textContent = `${screen.caption}（${screenIndex + 1} / ${item.screens.length}）`;
        document.querySelectorAll('#lightboxThumbs .lightbox-thumb').forEach((btn, i) => {
            btn.classList.toggle('active', i === screenIndex);
            btn.setAttribute('aria-current', i === screenIndex ? 'true' : 'false');
        });
    }

    function renderLightboxItem() {
        const item = visibleItems[itemIndex];
        document.getElementById('lightboxCategory').textContent = categoryLabel(item.category);
        document.getElementById('lightboxReal').classList.toggle('hidden', !item.isReal);
        document.getElementById('lightboxCounter').textContent = `作品 ${itemIndex + 1} / ${visibleItems.length}`;
        document.getElementById('lightboxTitle').textContent = item.title;
        document.getElementById('lightboxDesc').textContent = item.description;
        document.getElementById('lightboxFeatures').innerHTML = item.features.map(f => `<li>${escapeText(f)}</li>`).join('');
        document.getElementById('lightboxTags').innerHTML = item.tags.map(t => `<span class="tag">${escapeText(t)}</span>`).join('');
        document.getElementById('lightboxThumbs').innerHTML = item.screens.map((screen, i) => `
            <button class="lightbox-thumb" data-screen="${i}" title="${escapeText(screen.caption)}">
                <img src="${escapeText(screen.src)}" alt="${escapeText(screen.caption)}" width="160" height="100">
            </button>`).join('');
        renderLightboxScreen();
    }

    function openLightbox(index, startScreen = 0) {
        if (!visibleItems[index]) return;
        itemIndex = index;
        screenIndex = Math.min(startScreen, visibleItems[index].screens.length - 1);
        renderLightboxItem();
        document.getElementById('showcaseLightbox').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        document.getElementById('showcaseLightbox').classList.add('hidden');
        document.body.style.overflow = '';
        itemIndex = -1;
    }

    function stepScreen(offset) {
        if (itemIndex < 0) return;
        screenIndex = wrapIndex(screenIndex + offset, visibleItems[itemIndex].screens.length);
        renderLightboxScreen();
    }

    function stepItem(offset) {
        if (itemIndex < 0 || visibleItems.length === 0) return;
        itemIndex = wrapIndex(itemIndex + offset, visibleItems.length);
        screenIndex = 0;
        renderLightboxItem();
    }

    // ---------- 事件 ----------
    function onGridActivate(target) {
        const card = target.closest('.showcase-card');
        if (!card) return;
        const mini = target.closest('.showcase-mini');
        openLightbox(Number(card.dataset.index), mini ? Number(mini.dataset.screen) : 0);
    }

    function bindShowcaseEvents() {
        document.getElementById('showcaseFilters').addEventListener('click', e => {
            const btn = e.target.closest('.showcase-filter');
            if (!btn) return;
            activeCategory = btn.dataset.category;
            renderFilters();
            renderGrid();
        });

        const grid = document.getElementById('showcaseGrid');
        grid.addEventListener('click', e => onGridActivate(e.target));
        grid.addEventListener('keydown', e => {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            if (!e.target.classList.contains('showcase-card')) return; // 小縮圖按鈕交給原生 click
            e.preventDefault();
            onGridActivate(e.target);
        });

        const lightbox = document.getElementById('showcaseLightbox');
        lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
        document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
        document.getElementById('lightboxPrev').addEventListener('click', () => stepScreen(-1));
        document.getElementById('lightboxNext').addEventListener('click', () => stepScreen(1));
        document.getElementById('lightboxPrevItem').addEventListener('click', () => stepItem(-1));
        document.getElementById('lightboxNextItem').addEventListener('click', () => stepItem(1));
        document.getElementById('lightboxThumbs').addEventListener('click', e => {
            const thumb = e.target.closest('.lightbox-thumb');
            if (!thumb) return;
            screenIndex = Number(thumb.dataset.screen);
            renderLightboxScreen();
        });
        document.addEventListener('keydown', e => {
            if (itemIndex < 0) return;
            if (e.key === 'Escape') closeLightbox();
            else if (e.key === 'ArrowLeft') stepScreen(-1);
            else if (e.key === 'ArrowRight') stepScreen(1);
            else if (e.key === 'ArrowUp') { e.preventDefault(); stepItem(-1); }
            else if (e.key === 'ArrowDown') { e.preventDefault(); stepItem(1); }
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        try {
            document.getElementById('lightboxCta').href = SHOWCASE_CTA_URL;
            renderFilters();
            renderGrid();
            bindShowcaseEvents();
        } catch (e) {
            console.error('作品展示牆初始化失敗（showcase.js）：', e);
        }
    });
})();
