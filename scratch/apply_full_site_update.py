import json
import re
import os

print("=== Starting Full Site Fine-Tuning ===")

# 1. Load dataset of 233 photos
with open('scratch/full_gallery_dataset.json', 'r', encoding='utf-8') as f:
    photos_data = json.load(f)

print(f"Loaded {len(photos_data)} photos from dataset.")

# Count by category
cat_counts = {}
for p in photos_data:
    c = p.get('category', 'all')
    cat_counts[c] = cat_counts.get(c, 0) + 1
print("Category counts:", cat_counts)

# ==============================================================================
# A. UPDATE index.html: Insert Gallery Section and Lightbox & Caption Modals
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check if gallery already exists in html
if 'id="gallery"' not in html:
    gallery_html = f'''
  <!-- ====================================================
       EXHIBITION GALLERY — 227+ Photographs
       ==================================================== -->
  <section class="gallery-section" id="gallery" aria-label="Exhibition photo gallery">
    <div class="container container--wide">
      <div class="gallery__header reveal">
        <div class="gallery__header-badge">
          <span class="badge-dot"></span>
          <span>Live Exhibition Archive · {len(photos_data)} Photographs</span>
        </div>
        <h2>The Exhibition <em class="text-earth">Gallery</em></h2>
        <p class="gallery__subtitle">
          Over fifteen years of documentary photography in Northern Kenya. Tracing girls from grazing fields
          to secondary schools, universities, and professional careers.
        </p>

        <!-- Filter & Search Controls -->
        <div class="gallery__controls">
          <div class="gallery__filters" role="tablist" aria-label="Filter gallery photos">
            <button class="gallery-filter-btn active" data-category="all" role="tab" aria-selected="true" type="button">
              All Photos <span class="filter-count" id="count-all">({len(photos_data)})</span>
            </button>
            <button class="gallery-filter-btn" data-category="exhibition" role="tab" aria-selected="false" type="button">
              Book &amp; Exhibition <span class="filter-count" id="count-exhibition">({cat_counts.get('exhibition', 0)})</span>
            </button>
            <button class="gallery-filter-btn" data-category="photobooth" role="tab" aria-selected="false" type="button">
              Photo Booth <span class="filter-count" id="count-photobooth">({cat_counts.get('photobooth', 0)})</span>
            </button>
            <button class="gallery-filter-btn" data-category="ceremony" role="tab" aria-selected="false" type="button">
              Ceremony &amp; Speeches <span class="filter-count" id="count-ceremony">({cat_counts.get('ceremony', 0)})</span>
            </button>
            <button class="gallery-filter-btn" data-category="portraits" role="tab" aria-selected="false" type="button">
              Portraits &amp; Team <span class="filter-count" id="count-portraits">({cat_counts.get('portraits', 0)})</span>
            </button>
          </div>

          <div class="gallery__search-row">
            <div class="gallery__search-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input type="text" id="gallery-search" placeholder="Search photos by keyword or frame #..." aria-label="Search gallery photos">
              <button id="gallery-search-clear" style="display:none;" aria-label="Clear search" type="button">✕</button>
            </div>
            <button class="btn btn--outline btn--upload-toggle" id="upload-toggle-btn" type="button">
              <span>📷 Add Photos</span>
            </button>
          </div>
        </div>

        <!-- Optional Drag & Drop Upload Zone (Collapsible) -->
        <div class="upload-zone-wrapper" id="upload-zone-wrapper" style="display: none;">
          <div class="upload-zone" id="upload-zone">
            <input type="file" id="upload-input" multiple accept="image/*" style="display:none">
            <div class="upload-zone__content">
              <div class="upload-zone__icon">📤</div>
              <p class="upload-zone__title">Drag &amp; drop photos here or <button type="button" class="upload-zone__browse-btn" onclick="document.getElementById('upload-input').click()">Browse files</button></p>
              <p class="upload-zone__sub">Supports JPG, PNG, WEBP · Max 20 photos at a time</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Photo Counter Status -->
      <div class="gallery__status-bar">
        <span id="gallery-status-text">Showing 24 of {len(photos_data)} photographs</span>
      </div>

      <!-- Responsive Photo Grid -->
      <div class="gallery__grid" id="gallery-grid" aria-live="polite">
        <!-- Rendered dynamically by main.js with lazy loading and captions -->
      </div>

      <!-- Load More / Pagination -->
      <div class="gallery__pagination" id="gallery-pagination">
        <button class="btn btn--secondary btn--load-more" id="load-more-btn" type="button">
          <span>Load Next 24 Photos</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <button class="btn btn--outline" id="load-all-btn" type="button">
          <span>Show All Photos</span>
        </button>
      </div>
    </div>
  </section>
'''
    # Insert right before <section class="filmmaker"
    filmmaker_idx = html.find('<!-- ====================================================\n       FILMMAKER')
    if filmmaker_idx == -1:
        filmmaker_idx = html.find('<section class="filmmaker"')
    
    html = html[:filmmaker_idx] + gallery_html + '\n\n  ' + html[filmmaker_idx:]
    print("Inserted #gallery section into index.html")

# Check modals before </body>
if 'id="lightbox"' not in html:
    modals_html = '''
  <!-- Fullscreen Lightbox Modal -->
  <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
    <div class="lightbox__backdrop" id="lightbox-backdrop"></div>
    <div class="lightbox__container">
      <button class="lightbox__close" id="lightbox-close" aria-label="Close photo viewer">✕</button>
      <button class="lightbox__nav lightbox__nav--prev" id="lightbox-prev" aria-label="Previous photo">‹</button>
      <div class="lightbox__image-wrap">
        <img id="lightbox-img" src="" alt="Exhibition photo enlarged">
        <div class="lightbox__meta">
          <div class="lightbox__caption" id="lightbox-caption"></div>
          <div class="lightbox__counter" id="lightbox-counter">1 / 233</div>
        </div>
      </div>
      <button class="lightbox__nav lightbox__nav--next" id="lightbox-next" aria-label="Next photo">›</button>
    </div>
  </div>

  <!-- Caption Modal for uploads -->
  <div class="caption-modal" id="caption-modal" role="dialog" aria-modal="true" aria-label="Add photo caption">
    <div class="caption-modal__card">
      <h3>Add a Caption</h3>
      <p>Give your uploaded photo(s) a title or location:</p>
      <input type="text" id="caption-input" placeholder="e.g. Graduation ceremony, Marsabit">
      <div class="caption-modal__actions">
        <button type="button" class="btn btn--outline" id="caption-cancel">Cancel</button>
        <button type="button" class="btn btn--primary" id="caption-ok">Add to Gallery</button>
      </div>
    </div>
  </div>
'''
    toast_idx = html.find('<div class="toast-container"')
    if toast_idx != -1:
        html = html[:toast_idx] + modals_html + '\n  ' + html[toast_idx:]
    else:
        body_close = html.find('</body>')
        html = html[:body_close] + modals_html + '\n' + html[body_close:]
    print("Inserted Lightbox and Caption Modals into index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html")

# ==============================================================================
# B. UPDATE assets/css/style.css: Gallery, Lightbox, Filter & Upload styles
# ==============================================================================
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

gallery_css = '''
/* ============================================================
   EXHIBITION GALLERY SECTION
   ============================================================ */
.gallery-section {
  padding: var(--sp-xl) 0;
  background-color: #f7f3eb;
  position: relative;
  overflow: hidden;
}

.gallery-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,125,62,0.3), transparent);
}

.gallery__header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 3rem auto;
}

.gallery__header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(212,168,83,0.15);
  border: 1px solid rgba(212,168,83,0.35);
  color: var(--clr-earth-warm);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.4rem 1rem;
  border-radius: var(--radius-pill);
  margin-bottom: 1.25rem;
}

.gallery__header h2 {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  font-weight: 700;
  color: var(--clr-earth-deep);
  line-height: 1.15;
  margin-bottom: 1rem;
}

.gallery__subtitle {
  font-size: 1.1rem;
  color: var(--clr-muted);
  line-height: 1.7;
}

/* Controls: Filters & Search */
.gallery__controls {
  margin-top: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  align-items: center;
}

.gallery__filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  justify-content: center;
}

.gallery-filter-btn {
  background: var(--clr-white);
  border: 1px solid rgba(122,69,32,0.18);
  color: var(--clr-charcoal);
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 500;
  padding: 0.6rem 1.15rem;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: all var(--dur-fast) var(--ease-smooth);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.gallery-filter-btn:hover {
  border-color: var(--clr-earth-warm);
  background: #fffdf9;
  transform: translateY(-1px);
}

.gallery-filter-btn.active {
  background: var(--clr-earth-deep);
  color: var(--clr-gold);
  border-color: var(--clr-earth-deep);
  box-shadow: 0 4px 14px rgba(26,14,5,0.22);
}

.filter-count {
  font-size: 0.78rem;
  opacity: 0.75;
}

.gallery-filter-btn.active .filter-count {
  color: var(--clr-sand);
  opacity: 0.9;
}

.gallery__search-row {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  max-width: 600px;
  justify-content: center;
  align-items: center;
}

.gallery__search-box {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  background: var(--clr-white);
  border: 1px solid rgba(122,69,32,0.2);
  border-radius: var(--radius-pill);
  padding: 0 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: border-color var(--dur-fast);
}

.gallery__search-box:focus-within {
  border-color: var(--clr-earth-warm);
  box-shadow: 0 0 0 3px rgba(201,125,62,0.15);
}

.gallery__search-box svg {
  color: var(--clr-muted);
  flex-shrink: 0;
  margin-right: 0.5rem;
}

.gallery__search-box input {
  border: none;
  background: transparent;
  padding: 0.7rem 0;
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--clr-charcoal);
  width: 100%;
  outline: none;
}

.gallery__search-box input::placeholder {
  color: #9c9288;
}

#gallery-search-clear {
  background: none;
  border: none;
  color: var(--clr-muted);
  font-size: 1rem;
  cursor: pointer;
  padding: 0 0.3rem;
}

.btn--upload-toggle {
  font-size: 0.85rem;
  padding: 0.65rem 1.1rem;
  white-space: nowrap;
}

/* Upload zone */
.upload-zone-wrapper {
  width: 100%;
  max-width: 650px;
  margin: 1.5rem auto 0 auto;
}

.upload-zone {
  border: 2px dashed rgba(201,125,62,0.45);
  border-radius: var(--radius-md);
  background: rgba(255,255,255,0.7);
  padding: 2rem;
  text-align: center;
  transition: all var(--dur-fast);
  cursor: pointer;
}

.upload-zone.dragover {
  border-color: var(--clr-earth-warm);
  background: rgba(212,168,83,0.12);
  transform: scale(1.01);
}

.upload-zone__icon {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
}

.upload-zone__title {
  font-weight: 600;
  color: var(--clr-earth-deep);
  margin-bottom: 0.25rem;
}

.upload-zone__browse-btn {
  background: none;
  border: none;
  color: var(--clr-earth-warm);
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
}

.upload-zone__sub {
  font-size: 0.8rem;
  color: var(--clr-muted);
}

/* Gallery Status Bar */
.gallery__status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: var(--clr-muted);
  margin-bottom: 1.5rem;
  padding: 0 0.5rem;
  font-weight: 500;
}

/* Gallery Grid */
.gallery__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
  gap: 1.5rem;
}

.gallery__item {
  position: relative;
  aspect-ratio: 4/3;
  border-radius: var(--radius-md);
  overflow: hidden;
  background-color: #e4dcce;
  box-shadow: 0 4px 16px rgba(26,14,5,0.08);
  cursor: pointer;
  transition: transform var(--dur-fast) var(--ease-spring), box-shadow var(--dur-fast);
}

.gallery__item:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(26,14,5,0.18);
}

.gallery__item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s var(--ease-smooth);
}

.gallery__item:hover img {
  transform: scale(1.06);
}

.gallery__item__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26,14,5,0.92) 0%, rgba(26,14,5,0.4) 45%, transparent 100%);
  opacity: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 1.25rem;
  transition: opacity var(--dur-fast) var(--ease-smooth);
}

.gallery__item:hover .gallery__item__overlay,
.gallery__item:focus-within .gallery__item__overlay {
  opacity: 1;
}

.gallery__item__tag {
  align-self: flex-start;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: var(--clr-gold);
  color: var(--clr-earth-deep);
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.4rem;
}

.gallery__item__caption {
  color: var(--clr-white);
  font-size: 0.88rem;
  line-height: 1.4;
  font-weight: 500;
  text-shadow: 0 1px 3px rgba(0,0,0,0.4);
}

.gallery__item__icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 32px;
  height: 32px;
  background: rgba(255,255,255,0.25);
  backdrop-filter: blur(4px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
}

.gallery__item__delete {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  background: rgba(220, 53, 69, 0.85);
  color: white;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity var(--dur-fast), transform var(--dur-fast);
}

.gallery__item:hover .gallery__item__delete {
  opacity: 1;
}

.gallery__item__delete:hover {
  transform: scale(1.15);
  background: #c82333;
}

/* Pagination */
.gallery__pagination {
  margin-top: 3.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn--load-more {
  padding: 0.9rem 2.2rem;
  font-size: 1rem;
  box-shadow: 0 4px 18px rgba(122,69,32,0.25);
}

/* Empty State */
.gallery__empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 1rem;
  background: rgba(255,255,255,0.6);
  border-radius: var(--radius-md);
  border: 1px dashed rgba(122,69,32,0.2);
}

.gallery__empty-icon {
  font-size: 3rem;
  margin-bottom: 0.75rem;
}

.gallery__empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--clr-earth-deep);
  margin-bottom: 0.5rem;
}

/* ============================================================
   FULLSCREEN LIGHTBOX MODAL
   ============================================================ */
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--dur-med) var(--ease-smooth);
}

.lightbox.active {
  opacity: 1;
  pointer-events: auto;
}

.lightbox__backdrop {
  position: absolute;
  inset: 0;
  background-color: rgba(14, 8, 3, 0.94);
  backdrop-filter: blur(14px);
}

.lightbox__container {
  position: relative;
  z-index: 2;
  width: 92vw;
  max-width: 1200px;
  height: 88vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox__image-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 100%;
  max-height: 100%;
}

.lightbox__image-wrap img {
  max-width: 100%;
  max-height: 74vh;
  object-fit: contain;
  border-radius: var(--radius-sm);
  box-shadow: 0 16px 64px rgba(0,0,0,0.6);
}

.lightbox__meta {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 800px;
  padding: 0.5rem 1rem;
  color: var(--clr-white);
  gap: 1rem;
}

.lightbox__caption {
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 500;
  line-height: 1.4;
  color: #f0e6d6;
}

.lightbox__counter {
  font-size: 0.85rem;
  color: var(--clr-gold);
  font-weight: 600;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.lightbox__close {
  position: absolute;
  top: -1rem;
  right: -1rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--dur-fast);
}

.lightbox__close:hover {
  background: var(--clr-earth-warm);
  transform: scale(1.1);
}

.lightbox__nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  font-size: 2.2rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--dur-fast);
  z-index: 10;
  user-select: none;
}

.lightbox__nav--prev { left: -2rem; }
.lightbox__nav--next { right: -2rem; }

.lightbox__nav:hover {
  background: var(--clr-gold);
  color: var(--clr-earth-deep);
  transform: translateY(-50%) scale(1.12);
}

/* Caption Modal */
.caption-modal {
  position: fixed;
  inset: 0;
  z-index: 999999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(8px);
  padding: 1.5rem;
}

.caption-modal__card {
  background: var(--clr-white);
  border-radius: var(--radius-md);
  padding: 2rem;
  width: min(90%, 460px);
  box-shadow: 0 16px 48px rgba(0,0,0,0.3);
}

.caption-modal__card h3 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  color: var(--clr-earth-deep);
  margin-bottom: 0.5rem;
}

.caption-modal__card p {
  color: var(--clr-muted);
  font-size: 0.9rem;
  margin-bottom: 1.25rem;
}

.caption-modal__card input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(122,69,32,0.25);
  border-radius: var(--radius-sm);
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  outline: none;
}

.caption-modal__card input:focus {
  border-color: var(--clr-earth-warm);
}

.caption-modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
'''

if '.gallery-section' not in css:
    # Insert right before FILMMAKER PROFILE
    filmmaker_idx = css.find('/* ============================================================\n   FILMMAKER PROFILE')
    if filmmaker_idx == -1:
        filmmaker_idx = css.find('.filmmaker {')
    css = css[:filmmaker_idx] + gallery_css + '\n' + css[filmmaker_idx:]
    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Inserted Gallery & Lightbox CSS into assets/css/style.css")

print("=== index.html and style.css successfully updated! ===")
