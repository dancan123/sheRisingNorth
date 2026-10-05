import json

with open('scratch/full_gallery_dataset.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

print(f"Embedding {len(photos)} photos into main.js")

photos_json_str = json.dumps(photos, indent=2)

js_code = f'''/* ============================================================
   SHE IS RISING FROM THE NORTH — Main JavaScript System
   ============================================================ */

'use strict';

/**
 * ============================================================
 * 0. SITE CONFIGURATION (CENTRALIZED FOR EASY MODIFICATION)
 * Easily change payment details, numbers, or connect real APIs
 * (Daraja M-Pesa, Stripe, Pesapal, Flutterwave) in one place.
 * ============================================================
 */
window.SITE_CONFIG = {{
  mpesa: {{
    paybill: '400200',
    account: 'SHERISING',
    till: '9812404'
  }},
  bank: {{
    name: 'Equity Bank Kenya',
    accountName: 'MOV Foundation',
    accountNumber: '0190 2995 53993',
    swift: 'EQBLKENA',
    branch: 'Westlands Branch, Nairobi, Kenya'
  }},
  paypal: {{
    url: 'https://paypal.me/MOVFoundation',
    email: 'donate@movfoundation.org'
  }},
  cheque: {{
    payableTo: 'MOV Foundation',
    address: 'MOV Foundation, P.O. Box 28491-00100, Nairobi, Kenya',
    memo: 'She Is Rising from the North'
  }},

  /**
   * Action hook when user clicks "Donate Securely"
   * Replace or extend this to trigger your live payment gateway / checkout.
   */
  onDonate: function(amount) {{
    console.log(`[Donation Triggered] Amount: ${{amount}}`);
    showToast(`Redirecting to secure payment for $${{amount}}...`, 'info');
    // Open PayPal or your payment gateway:
    setTimeout(() => {{
      window.open(`https://paypal.me/MOVFoundation/${{amount}}USD`, '_blank');
    }}, 600);
  }}
}};

/* ----------------------------------------------------------
   1. NAVIGATION — scroll-aware + mobile menu
   ---------------------------------------------------------- */
const nav = document.getElementById('nav');
const hamburger = document.getElementById('nav-hamburger');
const mobileMenu = document.getElementById('mobile-menu');
const mobileClose = document.getElementById('mobile-menu-close');
const mobileLinks = document.querySelectorAll('.mobile-menu a');

window.addEventListener('scroll', () => {{
  nav?.classList.toggle('scrolled', window.scrollY > 60);
}}, {{ passive: true }});

hamburger?.addEventListener('click', () => mobileMenu?.classList.add('open'));
mobileClose?.addEventListener('click', () => mobileMenu?.classList.remove('open'));
mobileLinks.forEach(l => l.addEventListener('click', () => mobileMenu?.classList.remove('open')));

/* ----------------------------------------------------------
   2. SCROLL REVEAL — IntersectionObserver
   ---------------------------------------------------------- */
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }}),
  {{ threshold: 0.08, rootMargin: '0px 0px -30px 0px' }}
);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* ----------------------------------------------------------
   3. ANIMATED COUNTERS
   ---------------------------------------------------------- */
function animateCounter(el) {{
  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix || '';
  const dur    = 1800;
  const start  = performance.now();

  function update(now) {{
    const elapsed = now - start;
    const progress = Math.min(elapsed / dur, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(ease * target).toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }}
  requestAnimationFrame(update);
}}

const counterObserver = new IntersectionObserver(
  (entries) => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        animateCounter(e.target);
        counterObserver.unobserve(e.target);
      }}
    }});
  }},
  {{ threshold: 0.6 }}
);

document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

/* ----------------------------------------------------------
   4. TOAST NOTIFICATIONS
   ---------------------------------------------------------- */
function showToast(message, type = 'info') {{
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${{type}}`;
  
  const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
  toast.innerHTML = `<span class="toast-icon">${{icon}}</span> <span class="toast-msg">${{escapeHtml(message)}}</span>`;
  
  container.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('visible'));

  setTimeout(() => {{
    toast.classList.remove('visible');
    setTimeout(() => toast.remove(), 400);
  }}, 3500);
}}

function escapeHtml(str) {{
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}}

/* ----------------------------------------------------------
   5. COMPLETE EXHIBITION GALLERY SYSTEM
   ---------------------------------------------------------- */

const GALLERY_KEY = 'sirn_gallery_photos_v10';

// Built-in master collection of all 233 photos from Northern Kenya
const defaultPhotos = {photos_json_str};

function loadPhotos() {{
  try {{
    const stored = localStorage.getItem(GALLERY_KEY);
    if (stored) {{
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed) && parsed.length >= defaultPhotos.length) {{
        return parsed;
      }}
    }}
  }} catch (e) {{
    console.warn('LocalStorage error:', e);
  }}
  return [...defaultPhotos];
}}

function savePhotos(data) {{
  try {{
    localStorage.setItem(GALLERY_KEY, JSON.stringify(data));
  }} catch (e) {{
    console.warn('Failed to save to localStorage:', e);
  }}
}}

let allPhotos = loadPhotos();
savePhotos(allPhotos);

// Gallery state
let activeCategory = 'all';
let searchQuery = '';
const PAGE_SIZE = 24;
let visibleCount = PAGE_SIZE;

const grid = document.getElementById('gallery-grid');
const statusText = document.getElementById('gallery-status-text');
const loadMoreBtn = document.getElementById('load-more-btn');
const loadAllBtn = document.getElementById('load-all-btn');
const paginationWrap = document.getElementById('gallery-pagination');
const searchInput = document.getElementById('gallery-search');
const searchClearBtn = document.getElementById('gallery-search-clear');
const filterButtons = document.querySelectorAll('.gallery-filter-btn');

function getFilteredPhotos() {{
  return allPhotos.filter(photo => {{
    // Category match
    const matchCat = activeCategory === 'all' || photo.category === activeCategory;
    if (!matchCat) return false;

    // Search query match
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    const captionMatch = (photo.caption || '').toLowerCase().includes(q);
    const numMatch = (photo.num ? String(photo.num) : '').includes(q);
    const srcMatch = (photo.src || '').toLowerCase().includes(q);
    return captionMatch || numMatch || srcMatch;
  }});
}}

function renderGallery(reset = false) {{
  if (!grid) return;

  if (reset) {{
    visibleCount = PAGE_SIZE;
  }}

  const filtered = getFilteredPhotos();
  const total = filtered.length;

  // Update status bar
  if (statusText) {{
    const showing = Math.min(visibleCount, total);
    statusText.textContent = `Showing ${{showing}} of ${{total}} photographs${{searchQuery ? ` matching "${{searchQuery}}"` : ''}}`;
  }}

  // Empty state
  if (total === 0) {{
    grid.innerHTML = `
      <div class="gallery__empty">
        <div class="gallery__empty-icon">🔍</div>
        <p class="gallery__empty-title">No photos found</p>
        <p style="color:var(--clr-muted);font-size:0.9rem;">Try adjusting your filter or search keywords.</p>
      </div>
    `;
    if (paginationWrap) paginationWrap.style.display = 'none';
    return;
  }}

  // Render items up to visibleCount
  grid.innerHTML = '';
  const toShow = filtered.slice(0, visibleCount);

  toShow.forEach((photo, idx) => {{
    const item = document.createElement('div');
    item.className = 'gallery__item reveal visible';
    item.dataset.index = idx;

    const isCustom = photo.id && photo.id.startsWith('user-');
    const categoryLabel = photo.category === 'photobooth' ? 'Photo Booth' :
                          photo.category === 'ceremony' ? 'Ceremony' :
                          photo.category === 'portraits' ? 'Portrait' : 'Exhibition';

    item.innerHTML = `
      <img src="${{escapeHtml(photo.src)}}" alt="${{escapeHtml(photo.caption)}}" loading="lazy">
      <div class="gallery__item__overlay">
        <span class="gallery__item__tag">${{categoryLabel}}</span>
        <span class="gallery__item__caption">${{escapeHtml(photo.caption)}}</span>
      </div>
      <div class="gallery__item__icon" title="View Fullscreen">⤢</div>
      ${{isCustom ? `<button class="gallery__item__delete" aria-label="Remove uploaded photo" title="Delete Photo" data-id="${{photo.id}}">✕</button>` : ''}}
    `;

    // Click to open lightbox
    item.addEventListener('click', (e) => {{
      if (e.target.closest('.gallery__item__delete')) return;
      openLightbox(idx, filtered);
    }});

    // Delete handler for user photos
    const delBtn = item.querySelector('.gallery__item__delete');
    if (delBtn) {{
      delBtn.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (confirm('Delete this uploaded photo?')) {{
          allPhotos = allPhotos.filter(p => p.id !== photo.id);
          savePhotos(allPhotos);
          renderGallery();
          showToast('Photo removed.', 'info');
        }}
      }});
    }}

    grid.appendChild(item);
  }});

  // Pagination controls
  if (paginationWrap) {{
    if (visibleCount >= total) {{
      paginationWrap.style.display = 'none';
    }} else {{
      paginationWrap.style.display = 'flex';
      const remaining = total - visibleCount;
      const nextBatch = Math.min(PAGE_SIZE, remaining);
      if (loadMoreBtn) {{
        loadMoreBtn.querySelector('span').textContent = `Load Next ${{nextBatch}} Photos (${{remaining}} left)`;
      }}
    }}
  }}
}}

// Filter buttons
filterButtons.forEach(btn => {{
  btn.addEventListener('click', () => {{
    filterButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCategory = btn.dataset.category || 'all';
    renderGallery(true);
  }});
}});

// Search input
searchInput?.addEventListener('input', (e) => {{
  searchQuery = e.target.value.trim();
  if (searchClearBtn) {{
    searchClearBtn.style.display = searchQuery ? 'block' : 'none';
  }}
  renderGallery(true);
}});

searchClearBtn?.addEventListener('click', () => {{
  if (searchInput) searchInput.value = '';
  searchQuery = '';
  searchClearBtn.style.display = 'none';
  renderGallery(true);
}});

// Load More & Load All
loadMoreBtn?.addEventListener('click', () => {{
  visibleCount += PAGE_SIZE;
  renderGallery(false);
}});

loadAllBtn?.addEventListener('click', () => {{
  visibleCount = allPhotos.length;
  renderGallery(false);
}});

// Toggle Upload Zone
const uploadToggleBtn = document.getElementById('upload-toggle-btn');
const uploadZoneWrapper = document.getElementById('upload-zone-wrapper');

uploadToggleBtn?.addEventListener('click', () => {{
  if (!uploadZoneWrapper) return;
  const isHidden = uploadZoneWrapper.style.display === 'none';
  uploadZoneWrapper.style.display = isHidden ? 'block' : 'none';
  uploadToggleBtn.classList.toggle('active', isHidden);
}});

// --- File Upload ---
const uploadInput  = document.getElementById('upload-input');
const uploadZone   = document.getElementById('upload-zone');
const captionModal = document.getElementById('caption-modal');
const captionInput = document.getElementById('caption-input');
const captionOk    = document.getElementById('caption-ok');
const captionCancel= document.getElementById('caption-cancel');

let pendingFiles = [];

function handleFiles(files) {{
  const imageFiles = Array.from(files).filter(f => f.type.startsWith('image/'));
  if (!imageFiles.length) {{ showToast('Please select image files only.', 'error'); return; }}
  if (imageFiles.length > 20) {{ showToast('Maximum 20 photos at once.', 'error'); return; }}

  pendingFiles = imageFiles;
  if (captionModal) {{
    if (captionInput) captionInput.value = '';
    captionModal.style.display = 'flex';
    captionInput?.focus();
  }} else {{
    processPendingFiles('');
  }}
}}

captionOk?.addEventListener('click', () => {{
  const caption = captionInput?.value.trim() || 'Exhibition Photo';
  if (captionModal) captionModal.style.display = 'none';
  processPendingFiles(caption);
}});

captionCancel?.addEventListener('click', () => {{
  if (captionModal) captionModal.style.display = 'none';
  pendingFiles = [];
}});

function processPendingFiles(caption) {{
  let loaded = 0;
  const batch = [];

  pendingFiles.forEach(file => {{
    const reader = new FileReader();
    reader.onload = (e) => {{
      batch.push({{
        id: `user-${{Date.now()}}-${{Math.random().toString(36).slice(2)}}`,
        src: e.target.result,
        caption: caption || file.name.replace(/\\.[^.]+$/, ''),
        category: 'exhibition'
      }});
      loaded++;
      if (loaded === pendingFiles.length) {{
        allPhotos = [...batch, ...allPhotos];
        savePhotos(allPhotos);
        renderGallery(true);
        showToast(`${{loaded}} photo${{loaded > 1 ? 's' : ''}} added to gallery! 📷`, 'success');
      }}
    }};
    reader.readAsDataURL(file);
  }});
  pendingFiles = [];
}}

uploadInput?.addEventListener('change', (e) => handleFiles(e.target.files));

uploadZone?.addEventListener('dragover', (e) => {{
  e.preventDefault();
  uploadZone.classList.add('dragover');
}});

uploadZone?.addEventListener('dragleave', () => {{
  uploadZone.classList.remove('dragover');
}});

uploadZone?.addEventListener('drop', (e) => {{
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
}});

/* ----------------------------------------------------------
   6. FULLSCREEN LIGHTBOX SYSTEM
   ---------------------------------------------------------- */
const lightbox       = document.getElementById('lightbox');
const lightboxImg    = document.getElementById('lightbox-img');
const lightboxClose  = document.getElementById('lightbox-close');
const lightboxPrev   = document.getElementById('lightbox-prev');
const lightboxNext   = document.getElementById('lightbox-next');
const lightboxCaption= document.getElementById('lightbox-caption');
const lightboxCounter= document.getElementById('lightbox-counter');
const lightboxBackdrop = document.getElementById('lightbox-backdrop');

let currentLightboxIdx = 0;
let currentLightboxList = [];

function openLightbox(idx, photoList = null) {{
  currentLightboxList = photoList || getFilteredPhotos();
  currentLightboxIdx = idx;
  updateLightbox();
  if (lightbox) {{
    lightbox.style.display = 'flex';
    requestAnimationFrame(() => lightbox.classList.add('active'));
  }}
  document.body.style.overflow = 'hidden';
}}

function closeLightbox() {{
  if (!lightbox) return;
  lightbox.classList.remove('active');
  setTimeout(() => {{
    lightbox.style.display = 'none';
  }}, 300);
  document.body.style.overflow = '';
}}

function updateLightbox() {{
  if (!currentLightboxList.length) return;
  if (currentLightboxIdx < 0) currentLightboxIdx = currentLightboxList.length - 1;
  if (currentLightboxIdx >= currentLightboxList.length) currentLightboxIdx = 0;

  const photo = currentLightboxList[currentLightboxIdx];
  if (lightboxImg) {{
    lightboxImg.src = photo.src;
    lightboxImg.alt = photo.caption || 'Exhibition Photograph';
  }}
  if (lightboxCaption) {{
    lightboxCaption.textContent = photo.caption || 'She Is Rising from the North';
  }}
  if (lightboxCounter) {{
    lightboxCounter.textContent = `${{currentLightboxIdx + 1}} / ${{currentLightboxList.length}}`;
  }}
}}

lightboxPrev?.addEventListener('click', (e) => {{
  e.stopPropagation();
  currentLightboxIdx--;
  updateLightbox();
}});

lightboxNext?.addEventListener('click', (e) => {{
  e.stopPropagation();
  currentLightboxIdx++;
  updateLightbox();
}});

lightboxClose?.addEventListener('click', closeLightbox);
lightboxBackdrop?.addEventListener('click', closeLightbox);

// Keyboard controls
window.addEventListener('keydown', (e) => {{
  if (!lightbox?.classList.contains('active')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') {{
    currentLightboxIdx--;
    updateLightbox();
  }}
  if (e.key === 'ArrowRight') {{
    currentLightboxIdx++;
    updateLightbox();
  }}
}});

// Touch swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;

lightbox?.addEventListener('touchstart', (e) => {{
  touchStartX = e.changedTouches[0].screenX;
}}, {{ passive: true }});

lightbox?.addEventListener('touchend', (e) => {{
  touchEndX = e.changedTouches[0].screenX;
  const diff = touchEndX - touchStartX;
  if (Math.abs(diff) > 50) {{
    if (diff > 0) {{
      currentLightboxIdx--;
    }} else {{
      currentLightboxIdx++;
    }}
    updateLightbox();
  }}
}}, {{ passive: true }});

// Initial gallery render
renderGallery(true);

/* ----------------------------------------------------------
   7. SUPPORT / DONATION SYSTEM & COPY DETAILS
   ---------------------------------------------------------- */
const impactData = {{
  25: {{
    title: '$25 Pledge',
    desc: 'Provides full sets of textbooks, notebooks, mathematical sets and stationery for two students.'
  }},
  50: {{
    title: '$50 Pledge',
    desc: 'Funds a complete school uniform, textbooks, stationery and personal hygiene supplies for one full term.'
  }},
  100: {{
    title: '$100 Pledge',
    desc: 'Covers full boarding, term tuition, meals and mentorship for one secondary school student.'
  }},
  250: {{
    title: '$250 Pledge',
    desc: 'Sponsors an entire academic year including school fees, accommodation, uniform and university prep.'
  }},
  custom: {{
    title: 'Custom Support',
    desc: 'Every single dollar directly powers girls\\' scholarships, mentorship workshops and book distributions.'
  }}
}};

const chips = document.querySelectorAll('.amount-chip');
const customWrap = document.getElementById('custom-wrap');
const customInput = document.getElementById('custom-amount');
const impactBox = document.getElementById('impact-box');
const impactAmount = document.getElementById('impact-amount');
const impactDesc = document.getElementById('impact-desc');
const donateBtn = document.getElementById('donate-btn');
const donateBtnText = document.getElementById('donate-btn-text');

let selectedAmount = '50';

function updatePledgeDisplay(amountVal) {{
  if (amountVal === 'custom') {{
    if (customWrap) customWrap.style.display = 'flex';
    const entered = customInput?.value ? parseInt(customInput.value, 10) : 0;
    if (impactAmount) impactAmount.textContent = entered > 0 ? `$${{entered}} Custom Support` : 'Custom Contribution';
    if (impactDesc) impactDesc.textContent = impactData.custom.desc;
    if (donateBtnText) donateBtnText.textContent = entered > 0 ? `Donate $${{entered}} Securely` : 'Donate Securely';
  }} else {{
    if (customWrap) customWrap.style.display = 'none';
    const data = impactData[amountVal] || impactData[50];
    if (impactAmount) impactAmount.textContent = data.title;
    if (impactDesc) impactDesc.textContent = data.desc;
    if (donateBtnText) donateBtnText.textContent = `Donate $${{amountVal}} Securely`;
  }}
}}

chips.forEach(chip => {{
  chip.addEventListener('click', () => {{
    chips.forEach(c => c.classList.remove('selected'));
    chip.classList.add('selected');
    selectedAmount = chip.dataset.amount;
    updatePledgeDisplay(selectedAmount);
  }});
}});

customInput?.addEventListener('input', () => {{
  if (selectedAmount === 'custom') {{
    updatePledgeDisplay('custom');
  }}
}});

donateBtn?.addEventListener('click', () => {{
  let finalAmount = selectedAmount;
  if (selectedAmount === 'custom') {{
    finalAmount = customInput?.value ? parseInt(customInput.value, 10) : 50;
  }}
  if (typeof window.SITE_CONFIG?.onDonate === 'function') {{
    window.SITE_CONFIG.onDonate(finalAmount);
  }}
}});

// Copy buttons for payment details
document.querySelectorAll('.copy-btn[data-copy]').forEach(btn => {{
  btn.addEventListener('click', async (e) => {{
    e.preventDefault();
    const textToCopy = btn.dataset.copy;
    if (!textToCopy) return;

    try {{
      await navigator.clipboard.writeText(textToCopy);
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy';
      if (span) span.textContent = 'Copied! ✓';
      btn.classList.add('copied');
      showToast(`Copied "${{textToCopy}}" to clipboard!`, 'success');

      setTimeout(() => {{
        if (span) span.textContent = originalText;
        btn.classList.remove('copied');
      }}, 2200);
    }} catch (err) {{
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = textToCopy;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
      showToast(`Copied "${{textToCopy}}" to clipboard!`, 'success');
    }}
  }});
}});

/* ----------------------------------------------------------
   8. CONTACT FORM
   ---------------------------------------------------------- */
const contactForm = document.getElementById('contact-form');
const formSuccess = document.getElementById('form-success');

contactForm?.addEventListener('submit', (e) => {{
  e.preventDefault();
  const name = document.getElementById('form-name')?.value.trim();
  const email = document.getElementById('form-email')?.value.trim();
  const message = document.getElementById('form-message')?.value.trim();

  if (!name || !email || !message) {{
    showToast('Please fill in all required fields.', 'error');
    return;
  }}

  if (formSuccess) {{
    formSuccess.style.display = 'block';
    contactForm.reset();
    showToast('Thank you! Your message has been sent.', 'success');
    setTimeout(() => {{
      formSuccess.style.display = 'none';
    }}, 6000);
  }}
}});

console.log('She Is Rising from the North site initialized with', allPhotos.length, 'gallery photos.');
'''

with open('assets/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Generated and written new assets/js/main.js successfully!")
