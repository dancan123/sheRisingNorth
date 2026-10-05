/* ============================================================
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
window.SITE_CONFIG = {
  mpesa: {
    paybill: '400200',
    account: 'SHERISING',
    till: '9812404'
  },
  bank: {
    name: 'Equity Bank Kenya',
    accountName: 'MOV Foundation',
    accountNumber: '0190 2995 53993',
    swift: 'EQBLKENA',
    branch: 'Westlands Branch, Nairobi, Kenya'
  },
  paypal: {
    url: 'https://paypal.me/MOVFoundation',
    email: 'donate@movfoundation.org'
  },
  cheque: {
    payableTo: 'MOV Foundation',
    address: 'MOV Foundation, P.O. Box 28491-00100, Nairobi, Kenya',
    memo: 'She Is Rising from the North'
  },

  /**
   * Action hook when user clicks "Donate Securely"
   * Replace or extend this to trigger your live payment gateway / checkout.
   */
  onDonate: function(amount) {
    console.log(`[Donation Triggered] Amount: ${amount}`);
    showToast(`Redirecting to secure payment for $${amount}...`, 'info');
    // Open PayPal or your payment gateway:
    setTimeout(() => {
      window.open(`https://paypal.me/MOVFoundation/${amount}USD`, '_blank');
    }, 600);
  }
};

/* ----------------------------------------------------------
   1. NAVIGATION — scroll-aware + mobile menu
   ---------------------------------------------------------- */
const nav = document.getElementById('nav');
const hamburger = document.getElementById('nav-hamburger');
const mobileMenu = document.getElementById('mobile-menu');
const mobileClose = document.getElementById('mobile-menu-close');
const mobileLinks = document.querySelectorAll('.mobile-menu a');

window.addEventListener('scroll', () => {
  nav?.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

hamburger?.addEventListener('click', () => mobileMenu?.classList.add('open'));
mobileClose?.addEventListener('click', () => mobileMenu?.classList.remove('open'));
mobileLinks.forEach(l => l.addEventListener('click', () => mobileMenu?.classList.remove('open')));

/* ----------------------------------------------------------
   2. SCROLL REVEAL — IntersectionObserver
   ---------------------------------------------------------- */
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.08, rootMargin: '0px 0px -30px 0px' }
);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* ----------------------------------------------------------
   3. ANIMATED COUNTERS
   ---------------------------------------------------------- */
function animateCounter(el) {
  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix || '';
  const dur    = 1800;
  const start  = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / dur, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(ease * target).toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        counterObserver.unobserve(e.target);
      }
    });
  },
  { threshold: 0.6 }
);

document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

/* ----------------------------------------------------------
   4. TOAST NOTIFICATIONS
   ---------------------------------------------------------- */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  
  const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
  toast.innerHTML = `<span class="toast-icon">${icon}</span> <span class="toast-msg">${escapeHtml(message)}</span>`;
  
  container.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('visible'));

  setTimeout(() => {
    toast.classList.remove('visible');
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* ----------------------------------------------------------
   5. COMPLETE EXHIBITION GALLERY SYSTEM
   ---------------------------------------------------------- */

const GALLERY_KEY = 'sirn_gallery_photos_v10';

// Built-in master collection of all 233 photos from Northern Kenya
const defaultPhotos = [
  {
    "id": "hl-1",
    "src": "assets/images/photobooth_students.jpg",
    "caption": "#SheIsRisingFromTheNorth Photo Booth \u2014 Students & Teachers with the Book",
    "category": "photobooth",
    "tag": "Featured"
  },
  {
    "id": "hl-2",
    "src": "assets/images/students_reading.jpg",
    "caption": "Reading the Book \u2014 I.G.H.S. Students Exploring Their Stories",
    "category": "exhibition",
    "tag": "Featured"
  },
  {
    "id": "hl-3",
    "src": "assets/images/students_walking.jpg",
    "caption": "The Journey of Becoming \u2014 Students in Uniform at the Launch",
    "category": "exhibition",
    "tag": "Featured"
  },
  {
    "id": "hl-4",
    "src": "assets/images/exhibition_outdoor.jpg",
    "caption": "Outdoor Exhibition Under the Acacia \u2014 Photo Prints on Easels",
    "category": "exhibition",
    "tag": "Featured"
  },
  {
    "id": "hl-5",
    "src": "assets/images/classroom.jpg",
    "caption": "Inside the Classroom \u2014 Where Futures Are Built",
    "category": "exhibition",
    "tag": "Featured"
  },
  {
    "id": "hl-6",
    "src": "assets/images/support_impact.jpg",
    "caption": "Education Changes Everything \u2014 Support the Girls of Northern Kenya",
    "category": "exhibition",
    "tag": "Featured"
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5212.jpg",
    "caption": "Exhibition Gallery Pavilion \u2014 Desert Sunset and Stories of Hope",
    "category": "exhibition",
    "num": 5212
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5213.jpg",
    "caption": "Inside the Exhibition Tent \u2014 15 Years of Documentary Photography",
    "category": "exhibition",
    "num": 5213
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5219.jpg",
    "caption": "Opening Ceremony \u2014 Community Leaders & Guests of Honour",
    "category": "exhibition",
    "num": 5219
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5220.jpg",
    "caption": "Viewing the Photo-Book \u2014 A Moment of Recognition",
    "category": "exhibition",
    "num": 5220
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5223.jpg",
    "caption": "School Girls at the Exhibition \u2014 Northern Kenya",
    "category": "exhibition",
    "num": 5223
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5224.jpg",
    "caption": "The Long Road \u2014 From Grazing Fields to Classrooms",
    "category": "exhibition",
    "num": 5224
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5227.jpg",
    "caption": "Portrait of Resilience \u2014 She Is Rising from the North",
    "category": "exhibition",
    "num": 5227
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5230.jpg",
    "caption": "Framed Portraits of Resilience \u2014 Community Exhibition",
    "category": "exhibition",
    "num": 5230
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5235.jpg",
    "caption": "MOV Foundation Supporters at the Launch Event",
    "category": "exhibition",
    "num": 5235
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5237.jpg",
    "caption": "A Girl Reads Her Own Story \u2014 Isiolo, Kenya",
    "category": "exhibition",
    "num": 5237
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5238.jpg",
    "caption": "Teachers and Students Celebrate 15 Years of Education",
    "category": "exhibition",
    "num": 5238
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5240.jpg",
    "caption": "Community Elder Signing the Official Exhibition Guestbook",
    "category": "exhibition",
    "num": 5240
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5244.jpg",
    "caption": "Fifteen Years \u2014 Five Hundred Girls Documented",
    "category": "exhibition",
    "num": 5244
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5251.jpg",
    "caption": "Young Women Graduates \u2014 Education Works",
    "category": "exhibition",
    "num": 5251
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5259.jpg",
    "caption": "Smiles of Achievement \u2014 Graduation Day, Northern Kenya",
    "category": "exhibition",
    "num": 5259
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5262.jpg",
    "caption": "Uniform as Dignity \u2014 First Day in Secondary School",
    "category": "exhibition",
    "num": 5262
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5263.jpg",
    "caption": "Book in Hands \u2014 Knowledge is Power",
    "category": "exhibition",
    "num": 5263
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5266.jpg",
    "caption": "Stichting MOV Delegation Signing the Exhibition Launch Record",
    "category": "exhibition",
    "num": 5266
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5269.jpg",
    "caption": "Conversations That Change Lives \u2014 Mentorship Moments",
    "category": "exhibition",
    "num": 5269
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5273.jpg",
    "caption": "Community Gathering \u2014 Education Advocates and Parents",
    "category": "exhibition",
    "num": 5273
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5277.jpg",
    "caption": "Looking Forward \u2014 The Next Generation of Leaders",
    "category": "exhibition",
    "num": 5277
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5279.jpg",
    "caption": "The Journey Continues \u2014 Students on the Road to University",
    "category": "exhibition",
    "num": 5279
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5290.jpg",
    "caption": "Exhibition Prints \u2014 Stories Told in Photographs",
    "category": "exhibition",
    "num": 5290
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5292.jpg",
    "caption": "Breaking the Vicious Cycle \u2014 Photo-Book Open Pages",
    "category": "exhibition",
    "num": 5292
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5295.jpg",
    "caption": "A Proud Moment \u2014 Parent and Child at the Exhibition",
    "category": "exhibition",
    "num": 5295
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5297.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5297
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5298.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5298
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5299.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5299
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5300.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5300
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5303.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5303
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5305.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5305
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5307.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5307
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5309.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5309
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5310.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5310
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5311.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5311
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5314.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5314
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5320.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5320
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5321.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5321
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5322.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5322
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5326.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5326
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5329.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5329
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5335.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5335
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5336.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5336
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5345.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5345
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5346.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5346
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5348.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5348
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5350.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5350
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5351.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5351
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5355.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5355
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5358.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "exhibition",
    "num": 5358
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5361.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5361
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5366.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5366
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5367.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5367
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5368.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5368
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5369.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5369
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5371.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5371
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5375.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5375
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5376.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5376
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5380.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5380
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5384.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5384
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5385.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5385
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5386.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5386
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5387.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5387
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5389.jpg",
    "caption": "Photo Booth Joy \u2014 Students Celebrating Together",
    "category": "photobooth",
    "num": 5389
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5391.jpg",
    "caption": "Photo Booth Portrait \u2014 She Is Rising from the North",
    "category": "photobooth",
    "num": 5391
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5392.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5392
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5396.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5396
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5401.jpg",
    "caption": "Smiles and Sisterhood at the Book Launch",
    "category": "photobooth",
    "num": 5401
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5402.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5402
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5403.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5403
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5407.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5407
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5409.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5409
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5412.jpg",
    "caption": "Community Celebrations at the Photo Booth",
    "category": "photobooth",
    "num": 5412
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5413.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5413
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5416.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5416
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5417.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5417
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5420.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5420
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5425.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5425
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5426.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5426
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5427.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5427
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5430.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "photobooth",
    "num": 5430
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5433.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5433
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5436.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5436
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5437.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5437
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5439.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5439
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5442.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5442
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5443.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5443
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5446.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5446
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5448.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5448
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5451.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5451
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5453.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5453
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5454.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5454
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5455.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5455
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5456.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5456
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5459.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5459
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5461.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5461
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5469.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5469
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5470.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5470
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5478.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5478
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5479.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5479
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5480.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5480
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5483.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5483
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5484.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5484
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5489.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5489
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5491.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5491
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5496.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5496
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5497.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5497
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5504.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5504
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5508.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5508
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5518.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5518
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5525.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5525
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5527.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5527
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5532.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5532
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5536.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5536
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5539.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5539
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5544.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5544
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5546.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5546
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5551.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5551
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5554.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5554
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5561.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5561
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5568.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5568
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5569.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5569
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5570.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5570
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5573.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5573
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5574.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5574
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5578.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5578
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5581.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5581
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5584.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5584
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5587.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5587
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5594.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5594
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5595.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5595
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5597.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5597
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5599.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5599
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5601.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5601
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5602.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5602
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5603.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5603
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5604.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5604
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5607.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5607
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5609.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5609
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5611.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5611
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5612.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5612
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5616.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5616
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5619.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5619
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5621.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5621
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5623.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5623
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5625.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5625
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5627.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5627
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5628.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5628
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5629.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5629
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5631.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5631
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5632.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5632
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5633.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5633
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5636.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5636
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5637.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5637
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5638.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5638
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5639.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5639
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5640.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5640
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5643.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5643
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5645.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5645
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5647.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5647
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5648.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5648
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5650.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5650
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5653.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5653
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5665.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5665
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5669.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5669
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5671.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5671
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5674.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "ceremony",
    "num": 5674
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5700.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5700
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5702.jpg",
    "caption": "Hildah Kathure, MOV Foundation Founder & Team with the Book",
    "category": "portraits",
    "num": 5702
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5704.jpg",
    "caption": "Launch Celebration \u2014 Team & Community Under the Acacia",
    "category": "portraits",
    "num": 5704
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5706.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5706
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5707.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5707
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5709.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5709
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5710.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5710
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5712.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5712
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5713.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5713
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5715.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5715
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5718.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5718
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5720.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5720
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5721.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5721
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5722.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5722
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5723.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5723
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5724.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5724
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5727.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5727
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5729.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5729
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5731.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5731
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5733.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5733
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5735.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5735
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5737.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5737
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5739.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5739
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5741.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5741
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5743.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5743
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5746.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5746
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5749.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5749
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5752.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5752
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5754.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5754
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5755.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5755
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5760.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5760
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5761.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5761
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5765.jpg",
    "caption": "Hildah Kathure with Microphone & Team \u2014 Outdoor Celebration",
    "category": "portraits",
    "num": 5765
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5767.jpg",
    "caption": "MOV Foundation Leadership & Community Champions",
    "category": "portraits",
    "num": 5767
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5769.jpg",
    "caption": "Hildah Kathure and Education Partner \u2014 A Milestone Celebrated",
    "category": "portraits",
    "num": 5769
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5772.jpg",
    "caption": "Women Leaders of Northern Kenya \u2014 Education Works",
    "category": "portraits",
    "num": 5772
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5774.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5774
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5776.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5776
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5777.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5777
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5778.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5778
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5781.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5781
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5782.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5782
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5784.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5784
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5785.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5785
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5787.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5787
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5789.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5789
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5790.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5790
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5791.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5791
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5793.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5793
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5796.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5796
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5798.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5798
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5800.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5800
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5802.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5802
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5804.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5804
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5808.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5808
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5810.jpg",
    "caption": "Photo Booth Celebration Under the Northern Kenya Sky",
    "category": "portraits",
    "num": 5810
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5811.jpg",
    "caption": "Hildah Kathure & Education Champions with Photo Booth Frame",
    "category": "portraits",
    "num": 5811
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5813.jpg",
    "caption": "She Is Rising from the North \u2014 Exhibition Frame #1",
    "category": "portraits",
    "num": 5813
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5815.jpg",
    "caption": "Hildah Kathure & Community Partner at the Exhibition",
    "category": "portraits",
    "num": 5815
  },
  {
    "id": "photo-1",
    "src": "assets/images/gallery/_W1A5817.jpg",
    "caption": "Closing Moments \u2014 Celebrating 15 Years of Transformation",
    "category": "portraits",
    "num": 5817
  }
];

function loadPhotos() {
  try {
    const stored = localStorage.getItem(GALLERY_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed) && parsed.length >= defaultPhotos.length) {
        return parsed;
      }
    }
  } catch (e) {
    console.warn('LocalStorage error:', e);
  }
  return [...defaultPhotos];
}

function savePhotos(data) {
  try {
    localStorage.setItem(GALLERY_KEY, JSON.stringify(data));
  } catch (e) {
    console.warn('Failed to save to localStorage:', e);
  }
}

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

function getFilteredPhotos() {
  return allPhotos.filter(photo => {
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
  });
}

function renderGallery(reset = false) {
  if (!grid) return;

  if (reset) {
    visibleCount = PAGE_SIZE;
  }

  const filtered = getFilteredPhotos();
  const total = filtered.length;

  // Update status bar
  if (statusText) {
    const showing = Math.min(visibleCount, total);
    statusText.textContent = `Showing ${showing} of ${total} photographs${searchQuery ? ` matching "${searchQuery}"` : ''}`;
  }

  // Empty state
  if (total === 0) {
    grid.innerHTML = `
      <div class="gallery__empty">
        <div class="gallery__empty-icon">🔍</div>
        <p class="gallery__empty-title">No photos found</p>
        <p style="color:var(--clr-muted);font-size:0.9rem;">Try adjusting your filter or search keywords.</p>
      </div>
    `;
    if (paginationWrap) paginationWrap.style.display = 'none';
    return;
  }

  // Render items up to visibleCount
  grid.innerHTML = '';
  const toShow = filtered.slice(0, visibleCount);

  toShow.forEach((photo, idx) => {
    const item = document.createElement('div');
    item.className = 'gallery__item reveal visible';
    item.dataset.index = idx;

    const isCustom = photo.id && photo.id.startsWith('user-');
    const categoryLabel = photo.category === 'photobooth' ? 'Photo Booth' :
                          photo.category === 'ceremony' ? 'Ceremony' :
                          photo.category === 'portraits' ? 'Portrait' : 'Exhibition';

    item.innerHTML = `
      <img src="${escapeHtml(photo.src)}" alt="${escapeHtml(photo.caption)}" loading="lazy">
      <div class="gallery__item__overlay">
        <span class="gallery__item__tag">${categoryLabel}</span>
        <span class="gallery__item__caption">${escapeHtml(photo.caption)}</span>
      </div>
      <div class="gallery__item__icon" title="View Fullscreen">⤢</div>
      ${isCustom ? `<button class="gallery__item__delete" aria-label="Remove uploaded photo" title="Delete Photo" data-id="${photo.id}">✕</button>` : ''}
    `;

    // Click to open lightbox
    item.addEventListener('click', (e) => {
      if (e.target.closest('.gallery__item__delete')) return;
      openLightbox(idx, filtered);
    });

    // Delete handler for user photos
    const delBtn = item.querySelector('.gallery__item__delete');
    if (delBtn) {
      delBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (confirm('Delete this uploaded photo?')) {
          allPhotos = allPhotos.filter(p => p.id !== photo.id);
          savePhotos(allPhotos);
          renderGallery();
          showToast('Photo removed.', 'info');
        }
      });
    }

    grid.appendChild(item);
  });

  // Pagination controls
  if (paginationWrap) {
    if (visibleCount >= total) {
      paginationWrap.style.display = 'none';
    } else {
      paginationWrap.style.display = 'flex';
      const remaining = total - visibleCount;
      const nextBatch = Math.min(PAGE_SIZE, remaining);
      if (loadMoreBtn) {
        loadMoreBtn.querySelector('span').textContent = `Load Next ${nextBatch} Photos (${remaining} left)`;
      }
    }
  }
}

// Filter buttons
filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    filterButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCategory = btn.dataset.category || 'all';
    renderGallery(true);
  });
});

// Search input
searchInput?.addEventListener('input', (e) => {
  searchQuery = e.target.value.trim();
  if (searchClearBtn) {
    searchClearBtn.style.display = searchQuery ? 'block' : 'none';
  }
  renderGallery(true);
});

searchClearBtn?.addEventListener('click', () => {
  if (searchInput) searchInput.value = '';
  searchQuery = '';
  searchClearBtn.style.display = 'none';
  renderGallery(true);
});

// Load More & Load All
loadMoreBtn?.addEventListener('click', () => {
  visibleCount += PAGE_SIZE;
  renderGallery(false);
});

loadAllBtn?.addEventListener('click', () => {
  visibleCount = allPhotos.length;
  renderGallery(false);
});

// Toggle Upload Zone
const uploadToggleBtn = document.getElementById('upload-toggle-btn');
const uploadZoneWrapper = document.getElementById('upload-zone-wrapper');

uploadToggleBtn?.addEventListener('click', () => {
  if (!uploadZoneWrapper) return;
  const isHidden = uploadZoneWrapper.style.display === 'none';
  uploadZoneWrapper.style.display = isHidden ? 'block' : 'none';
  uploadToggleBtn.classList.toggle('active', isHidden);
});

// --- File Upload ---
const uploadInput  = document.getElementById('upload-input');
const uploadZone   = document.getElementById('upload-zone');
const captionModal = document.getElementById('caption-modal');
const captionInput = document.getElementById('caption-input');
const captionOk    = document.getElementById('caption-ok');
const captionCancel= document.getElementById('caption-cancel');

let pendingFiles = [];

function handleFiles(files) {
  const imageFiles = Array.from(files).filter(f => f.type.startsWith('image/'));
  if (!imageFiles.length) { showToast('Please select image files only.', 'error'); return; }
  if (imageFiles.length > 20) { showToast('Maximum 20 photos at once.', 'error'); return; }

  pendingFiles = imageFiles;
  if (captionModal) {
    if (captionInput) captionInput.value = '';
    captionModal.style.display = 'flex';
    captionInput?.focus();
  } else {
    processPendingFiles('');
  }
}

captionOk?.addEventListener('click', () => {
  const caption = captionInput?.value.trim() || 'Exhibition Photo';
  if (captionModal) captionModal.style.display = 'none';
  processPendingFiles(caption);
});

captionCancel?.addEventListener('click', () => {
  if (captionModal) captionModal.style.display = 'none';
  pendingFiles = [];
});

function processPendingFiles(caption) {
  let loaded = 0;
  const batch = [];

  pendingFiles.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      batch.push({
        id: `user-${Date.now()}-${Math.random().toString(36).slice(2)}`,
        src: e.target.result,
        caption: caption || file.name.replace(/\.[^.]+$/, ''),
        category: 'exhibition'
      });
      loaded++;
      if (loaded === pendingFiles.length) {
        allPhotos = [...batch, ...allPhotos];
        savePhotos(allPhotos);
        renderGallery(true);
        showToast(`${loaded} photo${loaded > 1 ? 's' : ''} added to gallery! 📷`, 'success');
      }
    };
    reader.readAsDataURL(file);
  });
  pendingFiles = [];
}

uploadInput?.addEventListener('change', (e) => handleFiles(e.target.files));

uploadZone?.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});

uploadZone?.addEventListener('dragleave', () => {
  uploadZone.classList.remove('dragover');
});

uploadZone?.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});

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

function openLightbox(idx, photoList = null) {
  currentLightboxList = photoList || getFilteredPhotos();
  currentLightboxIdx = idx;
  updateLightbox();
  if (lightbox) {
    lightbox.style.display = 'flex';
    requestAnimationFrame(() => lightbox.classList.add('active'));
  }
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  if (!lightbox) return;
  lightbox.classList.remove('active');
  setTimeout(() => {
    lightbox.style.display = 'none';
  }, 300);
  document.body.style.overflow = '';
}

function updateLightbox() {
  if (!currentLightboxList.length) return;
  if (currentLightboxIdx < 0) currentLightboxIdx = currentLightboxList.length - 1;
  if (currentLightboxIdx >= currentLightboxList.length) currentLightboxIdx = 0;

  const photo = currentLightboxList[currentLightboxIdx];
  if (lightboxImg) {
    lightboxImg.src = photo.src;
    lightboxImg.alt = photo.caption || 'Exhibition Photograph';
  }
  if (lightboxCaption) {
    lightboxCaption.textContent = photo.caption || 'She Is Rising from the North';
  }
  if (lightboxCounter) {
    lightboxCounter.textContent = `${currentLightboxIdx + 1} / ${currentLightboxList.length}`;
  }
}

lightboxPrev?.addEventListener('click', (e) => {
  e.stopPropagation();
  currentLightboxIdx--;
  updateLightbox();
});

lightboxNext?.addEventListener('click', (e) => {
  e.stopPropagation();
  currentLightboxIdx++;
  updateLightbox();
});

lightboxClose?.addEventListener('click', closeLightbox);
lightboxBackdrop?.addEventListener('click', closeLightbox);

// Keyboard controls
window.addEventListener('keydown', (e) => {
  if (!lightbox?.classList.contains('active')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') {
    currentLightboxIdx--;
    updateLightbox();
  }
  if (e.key === 'ArrowRight') {
    currentLightboxIdx++;
    updateLightbox();
  }
});

// Touch swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;

lightbox?.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

lightbox?.addEventListener('touchend', (e) => {
  touchEndX = e.changedTouches[0].screenX;
  const diff = touchEndX - touchStartX;
  if (Math.abs(diff) > 50) {
    if (diff > 0) {
      currentLightboxIdx--;
    } else {
      currentLightboxIdx++;
    }
    updateLightbox();
  }
}, { passive: true });

// Initial gallery render
renderGallery(true);

/* ----------------------------------------------------------
   7. SUPPORT / DONATION SYSTEM & COPY DETAILS
   ---------------------------------------------------------- */
const impactData = {
  25: {
    title: '$25 Pledge',
    desc: 'Provides full sets of textbooks, notebooks, mathematical sets and stationery for two students.'
  },
  50: {
    title: '$50 Pledge',
    desc: 'Funds a complete school uniform, textbooks, stationery and personal hygiene supplies for one full term.'
  },
  100: {
    title: '$100 Pledge',
    desc: 'Covers full boarding, term tuition, meals and mentorship for one secondary school student.'
  },
  250: {
    title: '$250 Pledge',
    desc: 'Sponsors an entire academic year including school fees, accommodation, uniform and university prep.'
  },
  custom: {
    title: 'Custom Support',
    desc: 'Every single dollar directly powers girls\' scholarships, mentorship workshops and book distributions.'
  }
};

const chips = document.querySelectorAll('.amount-chip');
const customWrap = document.getElementById('custom-wrap');
const customInput = document.getElementById('custom-amount');
const impactBox = document.getElementById('impact-box');
const impactAmount = document.getElementById('impact-amount');
const impactDesc = document.getElementById('impact-desc');
const donateBtn = document.getElementById('donate-btn');
const donateBtnText = document.getElementById('donate-btn-text');

let selectedAmount = '50';

function updatePledgeDisplay(amountVal) {
  if (amountVal === 'custom') {
    if (customWrap) customWrap.style.display = 'flex';
    const entered = customInput?.value ? parseInt(customInput.value, 10) : 0;
    if (impactAmount) impactAmount.textContent = entered > 0 ? `$${entered} Custom Support` : 'Custom Contribution';
    if (impactDesc) impactDesc.textContent = impactData.custom.desc;
    if (donateBtnText) donateBtnText.textContent = entered > 0 ? `Donate $${entered} Securely` : 'Donate Securely';
  } else {
    if (customWrap) customWrap.style.display = 'none';
    const data = impactData[amountVal] || impactData[50];
    if (impactAmount) impactAmount.textContent = data.title;
    if (impactDesc) impactDesc.textContent = data.desc;
    if (donateBtnText) donateBtnText.textContent = `Donate $${amountVal} Securely`;
  }
}

chips.forEach(chip => {
  chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.remove('selected'));
    chip.classList.add('selected');
    selectedAmount = chip.dataset.amount;
    updatePledgeDisplay(selectedAmount);
  });
});

customInput?.addEventListener('input', () => {
  if (selectedAmount === 'custom') {
    updatePledgeDisplay('custom');
  }
});

donateBtn?.addEventListener('click', () => {
  let finalAmount = selectedAmount;
  if (selectedAmount === 'custom') {
    finalAmount = customInput?.value ? parseInt(customInput.value, 10) : 50;
  }
  if (typeof window.SITE_CONFIG?.onDonate === 'function') {
    window.SITE_CONFIG.onDonate(finalAmount);
  }
});

// Copy buttons for payment details
document.querySelectorAll('.copy-btn[data-copy]').forEach(btn => {
  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const textToCopy = btn.dataset.copy;
    if (!textToCopy) return;

    try {
      await navigator.clipboard.writeText(textToCopy);
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy';
      if (span) span.textContent = 'Copied! ✓';
      btn.classList.add('copied');
      showToast(`Copied "${textToCopy}" to clipboard!`, 'success');

      setTimeout(() => {
        if (span) span.textContent = originalText;
        btn.classList.remove('copied');
      }, 2200);
    } catch (err) {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = textToCopy;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
      showToast(`Copied "${textToCopy}" to clipboard!`, 'success');
    }
  });
});

/* ----------------------------------------------------------
   8. CONTACT FORM
   ---------------------------------------------------------- */
const contactForm = document.getElementById('contact-form');
const formSuccess = document.getElementById('form-success');

contactForm?.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('form-name')?.value.trim();
  const email = document.getElementById('form-email')?.value.trim();
  const message = document.getElementById('form-message')?.value.trim();

  if (!name || !email || !message) {
    showToast('Please fill in all required fields.', 'error');
    return;
  }

  if (formSuccess) {
    formSuccess.style.display = 'block';
    contactForm.reset();
    showToast('Thank you! Your message has been sent.', 'success');
    setTimeout(() => {
      formSuccess.style.display = 'none';
    }, 6000);
  }
});

console.log('She Is Rising from the North site initialized with', allPhotos.length, 'gallery photos.');
