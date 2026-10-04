// ===== 作品展示牆（分類篩選 + 燈箱）=====
// 純前端顯示，不依賴 Firebase；資料來源為 showcase-data.js
(() => {
    let activeCategory = 'all';
    let visibleItems = [];
    let lightboxIndex = -1;

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

    function renderFilters() {
        const bar = document.getElementById('showcaseFilters');
        bar.innerHTML = SHOWCASE_CATEGORIES.map(c => {
            const count = filterItems(SHOWCASE_ITEMS, c.id).length;
            const active = c.id === activeCategory ? ' active' : '';
            return `<button class="showcase-filter${active}" data-category="${escapeText(c.id)}" role="tab"
                        aria-selected="${c.id === activeCategory}">${escapeText(c.label)}<span>${count}</span></button>`;
        }).join('');
    }

    function renderGrid() {
        visibleItems = filterItems(SHOWCASE_ITEMS, activeCategory);
        document.getElementById('showcaseGrid').innerHTML = visibleItems.map((item, index) => `
            <article class="showcase-card" data-index="${index}" tabindex="0" aria-label="查看 ${escapeText(item.title)}">
                <div class="showcase-thumb">
                    <img src="${escapeText(item.image)}" alt="${escapeText(item.title)} 介面示意圖" loading="lazy" width="800" height="500">
                    <span class="showcase-badge">${escapeText(categoryLabel(item.category))}</span>
                    <span class="showcase-zoom">點擊放大 ⤢</span>
                </div>
                <div class="showcase-body">
                    <h3>${escapeText(item.title)}</h3>
                    <p>${escapeText(item.summary)}</p>
                    <div class="tags">${item.tags.map(t => `<span class="tag">${escapeText(t)}</span>`).join('')}</div>
                </div>
            </article>
        `).join('');
    }

    function openLightbox(index) {
        const item = visibleItems[index];
        if (!item) return;
        lightboxIndex = index;
        document.getElementById('lightboxImage').src = item.image;
        document.getElementById('lightboxImage').alt = `${item.title} 介面示意圖`;
        document.getElementById('lightboxCategory').textContent = categoryLabel(item.category);
        document.getElementById('lightboxTitle').textContent = item.title;
        document.getElementById('lightboxDesc').textContent = item.description;
        document.getElementById('lightboxFeatures').innerHTML =
            item.features.map(f => `<li>${escapeText(f)}</li>`).join('');
        document.getElementById('lightboxTags').innerHTML =
            item.tags.map(t => `<span class="tag">${escapeText(t)}</span>`).join('');
        document.getElementById('lightboxCounter').textContent = `${index + 1} / ${visibleItems.length}`;
        document.getElementById('showcaseLightbox').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        document.getElementById('showcaseLightbox').classList.add('hidden');
        document.body.style.overflow = '';
        lightboxIndex = -1;
    }

    function stepLightbox(offset) {
        if (lightboxIndex < 0 || visibleItems.length === 0) return;
        const next = (lightboxIndex + offset + visibleItems.length) % visibleItems.length;
        openLightbox(next);
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
        grid.addEventListener('click', e => {
            const card = e.target.closest('.showcase-card');
            if (card) openLightbox(Number(card.dataset.index));
        });
        grid.addEventListener('keydown', e => {
            const card = e.target.closest('.showcase-card');
            if (card && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                openLightbox(Number(card.dataset.index));
            }
        });

        const lightbox = document.getElementById('showcaseLightbox');
        lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
        document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
        document.getElementById('lightboxPrev').addEventListener('click', () => stepLightbox(-1));
        document.getElementById('lightboxNext').addEventListener('click', () => stepLightbox(1));
        document.addEventListener('keydown', e => {
            if (lightboxIndex < 0) return;
            if (e.key === 'Escape') closeLightbox();
            else if (e.key === 'ArrowLeft') stepLightbox(-1);
            else if (e.key === 'ArrowRight') stepLightbox(1);
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
