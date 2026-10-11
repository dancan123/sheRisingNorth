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
    paybill: '522533',
    account: '8144533',
    till: '8144533',
    name: 'SHE RISES FROM THE NORTH MENTORSHIP'
  },
  bank: {
    name: 'KCB Bank Kenya',
    accountName: 'SHE RISES FROM THE NORTH MENTORSHIP',
    till: '8144533',
    paybill: '522533',
    ussd: '*522#'
  },
  contact: {
    author: 'Hildah Kathure',
    company: 'Kalmax Productions, Nairobi',
    phone: '0720280171',
    email: 'hildahk83@gmail.com',
    website: 'https://www.kalmaxproductions.com',
    movFoundation: 'http://www.stichtingmov.nl'
  },
  onDonate: function(amount) {
    console.log(`[Donation Triggered] Amount: ${amount}`);
    showToast(`To complete your pledge of $${amount}, use KCB Paybill 522533 (Acc: 8144533) or Till 8144533.`, 'info');
  }
};

/* ----------------------------------------------------------
   1. NAVIGATION — scroll-aware + mobile menu
   ---------------------------------------------------------- */
const siteHeader = document.getElementById('site-header');
const nav = document.getElementById('nav');
const hamburger = document.getElementById('nav-hamburger');
const mobileMenu = document.getElementById('mobile-menu');
const mobileClose = document.getElementById('mobile-menu-close');
const mobileLinks = document.querySelectorAll('.mobile-menu a');

window.addEventListener('scroll', () => {
  const isScrolled = window.scrollY > 40;
  siteHeader?.classList.toggle('scrolled', isScrolled);
  nav?.classList.toggle('scrolled', isScrolled);
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

const GALLERY_KEY = 'sirn_gallery_photos_v12';

// Built-in master collection of all 233 photos from Northern Kenya
const defaultPhotos = [
  {
    "id": "photo-1",
    "src": "assets/images/Dr. Zeinab Gura - CEO Kenya University TRR Hospital Nairobi.jpg",
    "caption": "Dr. Zeinab Gura — CEO Kenyatta University Teaching, Referral & Research Hospital",
    "category": "portraits",
    "tag": "Leadership"
  },
  {
    "id": "photo-2",
    "src": "assets/images/Dr. Zeinab Gura - CEO Kenya University TRR Hospital Nairobi (1).jpg",
    "caption": "Dr. Zeinab Gura — Executive Portrait & Mentor to Northern Kenyan Girls",
    "category": "portraits",
    "tag": "Leadership"
  },
  {
    "id": "photo-3",
    "src": "assets/images/Dr. Zeinab Gura - CEO Kenya University TRR Hospital Nairobi (2).jpg",
    "caption": "Dr. Zeinab Gura — Leadership in Healthcare & Community Advocacy",
    "category": "portraits",
    "tag": "Leadership"
  },
  {
    "id": "photo-4",
    "src": "assets/images/Batula Fayo a teacher at Kisima Primary School.jpg",
    "caption": "Batula Fayo — Teacher at Kisima Primary School, Isiolo County",
    "category": "portraits",
    "tag": "Educator"
  },
  {
    "id": "photo-5",
    "src": "assets/images/A girl at Kisima - writing the future.jpg",
    "caption": "A Girl at Kisima — Writing the Future with Dignity and Determination",
    "category": "school",
    "tag": "Education"
  },
  {
    "id": "photo-6",
    "src": "assets/images/Amintu Gollo protects and serves determined that no girl facing violence should stand alone.jpg",
    "caption": "Amintu Gollo Protects and Serves — Determined that No Girl Facing Violence Stands Alone",
    "category": "job",
    "tag": "Public Service"
  },
  {
    "id": "photo-7",
    "src": "assets/images/Kaltuma Abdi and her Daughter Amina Abdi- One generation nurturing the dreams of the next.jpg",
    "caption": "Kaltuma Abdi & Daughter Amina Abdi — One Generation Nurturing the Dreams of the Next",
    "category": "portraits",
    "tag": "Generations"
  },
  {
    "id": "photo-8",
    "src": "assets/images/Sponsored Girls in Isiolo Girls - Ready to learn, lead and be seen.jpg",
    "caption": "Sponsored Girls at Isiolo Girls Secondary — Ready to Learn, Lead and Be Seen",
    "category": "school",
    "tag": "Scholars"
  },
  {
    "id": "photo-9",
    "src": "assets/images/Amina Jaldesa 4.jpeg",
    "caption": "Amina Jaldesa — Community Leadership & Mentorship in Northern Kenya",
    "category": "portraits",
    "tag": "Mentor"
  },
  {
    "id": "photo-10",
    "src": "assets/images/Boke 2.jpeg",
    "caption": "Boke — Stories of Resilience, Courage and Transformation",
    "category": "portraits",
    "tag": "Resilience"
  },

  {
    "id": "photo-12",
    "src": "assets/images/IMG-20230220-WA0064.jpg",
    "caption": "Classroom Mentorship Session — MOV Foundation Scholars in Northern Kenya",
    "category": "school",
    "tag": "Mentorship"
  },
  {
    "id": "photo-13",
    "src": "assets/images/photobooth_students.jpg",
    "caption": "#SheIsRisingFromTheNorth Photo Booth — Students & Teachers with the Book",
    "category": "launch",
    "tag": "Celebration"
  },
  {
    "id": "photo-14",
    "src": "assets/images/students_reading.jpg",
    "caption": "Reading the Book — I.G.H.S. Students Exploring Their Stories",
    "category": "school",
    "tag": "Students"
  },
  {
    "id": "photo-15",
    "src": "assets/images/students_walking.jpg",
    "caption": "The Journey of Becoming — Students in Uniform at the Launch",
    "category": "school",
    "tag": "Students"
  },
  {
    "id": "photo-16",
    "src": "assets/images/exhibition_outdoor.jpg",
    "caption": "Outdoor Exhibition Under the Acacia — Photo Prints on Easels",
    "category": "launch",
    "tag": "Exhibition"
  },
  {
    "id": "photo-17",
    "src": "assets/images/classroom.jpg",
    "caption": "Inside the Classroom — Where Futures Are Built",
    "category": "school",
    "tag": "Classroom"
  },
  {
    "id": "photo-18",
    "src": "assets/images/support_impact.jpg",
    "caption": "Education Changes Everything — Support the Girls of Northern Kenya",
    "category": "school",
    "tag": "Impact"
  },
  {
    "id": "photo-19",
    "src": "assets/images/Hildas pics .png",
    "caption": "Hildah Kathure — Author, Photographer & MOV Liaison Officer",
    "category": "portraits",
    "tag": "Author"
  },
  {
    "id": "photo-20",
    "src": "assets/images/MDV-2.jpg",
    "caption": "On the Grazing Fields — Dawn Across the Northern Kenya Savanna",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-21",
    "src": "assets/images/MDV-3.jpg",
    "caption": "Tending Livestock — Early Morning Pastoralist Responsibilities",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-22",
    "src": "assets/images/MDV-4.jpg",
    "caption": "The Journey Begins — Crossing the Savanna Towards School",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-23",
    "src": "assets/images/MDV-5.jpg",
    "caption": "Water and Resilience — Everyday Realities in Northern Kenya",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-24",
    "src": "assets/images/MDV-6.jpg",
    "caption": "Pastoralist Heritage — Communities Across Isiolo and Samburu",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-25",
    "src": "assets/images/MDV-10.jpg",
    "caption": "Gathering at the Manyatta — Community Elders and Youth Dialogue",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-26",
    "src": "assets/images/MDV-11.jpg",
    "caption": "Generational Wisdom — Elders Supporting Girls' Education",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-27",
    "src": "assets/images/MDV-13.jpg",
    "caption": "Dusk on the Northern Plains — Vast Savanna Horizons",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-28",
    "src": "assets/images/MDV-14.jpg",
    "caption": "The Long Walk to School — Breaking Distance Barriers",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-29",
    "src": "assets/images/MDV-16.jpg",
    "caption": "Classroom in Session — Dedicated Students Focused on Learning",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-30",
    "src": "assets/images/MDV-17.jpg",
    "caption": "Writing Dreams — A Desk and Notebook of One's Own",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-31",
    "src": "assets/images/MDV-18.jpg",
    "caption": "Peer Learning — Study Circles Under the Trees",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-32",
    "src": "assets/images/MDV-20.jpg",
    "caption": "Morning Assembly — Standing Proud in Clean School Uniforms",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-33",
    "src": "assets/images/MDV-22.jpg",
    "caption": "Primary School Joy — Friends and Shared Academic Aspirations",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-34",
    "src": "assets/images/MDV-25.jpg",
    "caption": "Mentorship in Action — Alumnae Inspiring Younger Girls",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-35",
    "src": "assets/images/MDV-27.jpg",
    "caption": "Library Hours — Discovering New Worlds Through Books",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-36",
    "src": "assets/images/MDV-29.jpg",
    "caption": "Science & Curiosity — Exploring Biology in the School Lab",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-37",
    "src": "assets/images/MDV-30.jpg",
    "caption": "Breaking Barriers — From Traditional Grazing to High School Success",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-38",
    "src": "assets/images/MDV-31.jpg",
    "caption": "Sisterhood & Strength — Young Women Supporting Each Other",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-39",
    "src": "assets/images/MDV-33.jpg",
    "caption": "Graduation Aspirations — Preparing Diligently for National Exams",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-40",
    "src": "assets/images/MDV-35.jpg",
    "caption": "Educators Who Care — Teachers Guiding Students in Isiolo",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-41",
    "src": "assets/images/MDV-39.jpg",
    "caption": "Dignity in Education — The Transformative Power of Scholarships",
    "category": "school",
    "tag": "School"
  },
  {
    "id": "photo-42",
    "src": "assets/images/MDV-40.jpg",
    "caption": "Community Pride — Parents Celebrating Academic Progress",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-43",
    "src": "assets/images/MDV-42.jpg",
    "caption": "Voices of Courage — Speaking Up in Classrooms and Community Halls",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-44",
    "src": "assets/images/MDV-43.jpg",
    "caption": "Future Leaders — Young Northern Kenyan Women Stepping Forward",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-45",
    "src": "assets/images/MDV-45.jpg",
    "caption": "The Horizon of Possibility — Northern Kenya Savanna Sunset",
    "category": "grazing",
    "tag": "Grazing Fields"
  },
  {
    "id": "photo-46",
    "src": "assets/images/0O1A1925.jpg",
    "caption": "On the Grazing Fields — Dawn Light in Isiolo County",
    "category": "grazing",
    "tag": "Field Story"
  },
  {
    "id": "photo-47",
    "src": "assets/images/0O1A1927.jpg",
    "caption": "Portrait of Grace — Young Pastoralist Girl at Sunrise",
    "category": "portraits",
    "tag": "Field Story"
  },
  {
    "id": "photo-48",
    "src": "assets/images/0O1A1990.jpg",
    "caption": "Pastoralist Traditions — Samburu Beadwork and Living Culture",
    "category": "portraits",
    "tag": "Field Story"
  },
  {
    "id": "photo-49",
    "src": "assets/images/0O1A2340.jpg",
    "caption": "Daily Responsibilities — Fetching Water Across the Savanna",
    "category": "grazing",
    "tag": "Field Story"
  },
  {
    "id": "photo-50",
    "src": "assets/images/0O1A8106.jpg",
    "caption": "Arriving at Secondary School — The First Step to Freedom",
    "category": "school",
    "tag": "Field Story"
  },
  {
    "id": "photo-51",
    "src": "assets/images/0O1A8163.jpg",
    "caption": "In the Classroom — Deep Focus and Academic Concentration",
    "category": "school",
    "tag": "Field Story"
  },
  {
    "id": "photo-52",
    "src": "assets/images/0O1A8203.jpg",
    "caption": "Sharing Coursework — Students Collaborating at Isiolo Girls",
    "category": "school",
    "tag": "Field Story"
  },
  {
    "id": "photo-53",
    "src": "assets/images/0O1A8311.jpg",
    "caption": "Portrait of Determination — An Aspiring Medical Doctor in Uniform",
    "category": "portraits",
    "tag": "Field Story"
  },
  {
    "id": "photo-54",
    "src": "assets/images/0O1A8318.jpg",
    "caption": "Classroom Discussion — Finding Confidence and Purpose",
    "category": "school",
    "tag": "Field Story"
  },
  {
    "id": "photo-55",
    "src": "assets/images/0O1A8340.jpg",
    "caption": "Courtyard Gathering — Girls Between Lessons in School",
    "category": "school",
    "tag": "Field Story"
  },
  {
    "id": "photo-56",
    "src": "assets/images/_32A8149.jpg",
    "caption": "Professional Leadership — Women Shaping Northern Kenya's Future",
    "category": "job",
    "tag": "Leadership"
  },
  {
    "id": "photo-57",
    "src": "assets/images/_32A8150.jpg",
    "caption": "Mentorship in Practice — Guiding Students Towards University",
    "category": "job",
    "tag": "Leadership"
  },
  {
    "id": "photo-58",
    "src": "assets/images/_32A8158.jpg",
    "caption": "Community Advocacy — Standing Up for Every Girl's Right to Learn",
    "category": "job",
    "tag": "Leadership"
  },
  {
    "id": "photo-59",
    "src": "assets/images/_W1A0004.jpg",
    "caption": "Morning Light on the School Quadrangle — Northern Kenya",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-60",
    "src": "assets/images/_W1A0034.jpg",
    "caption": "Dignity and Hope — A Student's Inspiring Smile",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-61",
    "src": "assets/images/_W1A0072.jpg",
    "caption": "Science Laboratory — Hands-on STEM Discovery",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-62",
    "src": "assets/images/_W1A0097.jpg",
    "caption": "Boarding School Community — Safe Spaces for Girls to Excel",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-63",
    "src": "assets/images/_W1A0120.jpg",
    "caption": "Classroom Discussion — Active Learning and Discussion",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-64",
    "src": "assets/images/_W1A0126.jpg",
    "caption": "Portrait of an Aspiring Engineer — Isiolo Girls High School",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-65",
    "src": "assets/images/_W1A0154.jpg",
    "caption": "Study Hall Focus — Dedicated Hours Before National Exams",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-66",
    "src": "assets/images/_W1A0184.jpg",
    "caption": "Eyes on the Horizon — Focused on Achieving Top Grades",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-67",
    "src": "assets/images/_W1A0212.jpg",
    "caption": "Study Group — Supporting Each Other Towards Graduation",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-68",
    "src": "assets/images/_W1A0234.jpg",
    "caption": "School Grounds — Friendship and High Ambition",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-69",
    "src": "assets/images/_W1A0290.jpg",
    "caption": "Sports and Leadership — Health, Teamwork and Confidence",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-70",
    "src": "assets/images/_W1A0316.jpg",
    "caption": "Engaging with the Curriculum — Curiosity and Learning",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-71",
    "src": "assets/images/_W1A0351.jpg",
    "caption": "Teacher Mentoring Students — After-Class Academic Guidance",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-72",
    "src": "assets/images/_W1A0363.jpg",
    "caption": "Portrait of Hope — Student in Uniform at Isiolo Girls",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-73",
    "src": "assets/images/_W1A0372.jpg",
    "caption": "School Assembly — Hundreds of Bright Futures in Progress",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-74",
    "src": "assets/images/_W1A0391.jpg",
    "caption": "Joy and Resilience — Overcoming Challenges Through Education",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-75",
    "src": "assets/images/_W1A0397.jpg",
    "caption": "Writing in the Notebook — An Archive of Education",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-76",
    "src": "assets/images/_W1A0410.jpg",
    "caption": "Portrait of an Achiever — High School Graduate",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-77",
    "src": "assets/images/_W1A0413.jpg",
    "caption": "Mentorship Session in the Hall — Inspiring the Whole Cohort",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-78",
    "src": "assets/images/_W1A0417.jpg",
    "caption": "Quiet Reflection with the Book — She Is Rising from the North",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-79",
    "src": "assets/images/_W1A0469.jpg",
    "caption": "Ready for the World — Final Year Students in Isiolo",
    "category": "school",
    "tag": "Isiolo Girls"
  },
  {
    "id": "photo-80",
    "src": "assets/images/_W1A8936.jpg",
    "caption": "Golden Hour Across the Pastoralist Plains of Northern Kenya",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-81",
    "src": "assets/images/_W1A8986.jpg",
    "caption": "The Road Between Manyattas — The Vast Northern Frontier",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-82",
    "src": "assets/images/_W1A9043.jpg",
    "caption": "Livestock and Livelihoods — Pastoralist Realities in Isiolo",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-83",
    "src": "assets/images/_W1A9701.jpg",
    "caption": "Samburu Traditional Attire — Celebrating Heritage and Dignity",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-84",
    "src": "assets/images/_W1A9733.jpg",
    "caption": "A Mother's Pride — Supporting Her Daughter's Journey",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-85",
    "src": "assets/images/_W1A9739.jpg",
    "caption": "Generational Shift — From Livestock Grazing to Higher Education",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-86",
    "src": "assets/images/_W1A9747.jpg",
    "caption": "Young Pastoralist Girl Looking Confidently Toward the Future",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-87",
    "src": "assets/images/_W1A9750.jpg",
    "caption": "Community Elders Meeting Under the Acacia Tree",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-88",
    "src": "assets/images/_W1A9784.jpg",
    "caption": "A Warm Smile on the Plains — Dignity in Every Step",
    "category": "portraits",
    "tag": "Portrait"
  },
  {
    "id": "photo-89",
    "src": "assets/images/_W1A9801.jpg",
    "caption": "Northern Kenya Savanna — Where the Transformative Story Begins",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-90",
    "src": "assets/images/_W1A9807.jpg",
    "caption": "Livestock at Golden Hour — Pastoralist Heartland",
    "category": "grazing",
    "tag": "Savanna"
  },
  {
    "id": "photo-91",
    "src": "assets/images/_W1A9829.jpg",
    "caption": "Portrait of Resilience — A Young Samburu Woman",
    "category": "portraits",
    "tag": "Portrait"
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
    const categoryLabel = photo.category === 'portraits' ? 'Role Model' :
                          photo.category === 'school' ? 'At School' :
                          photo.category === 'grazing' ? 'Grazing Fields' :
                          photo.category === 'job' ? 'On The Job' :
                          photo.category === 'banking' ? 'Bank Details' :
                          photo.category === 'launch' ? 'Exhibition' : 'Documentary';

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

// Bank slip preview lightbox
const bankSlipTrigger = document.getElementById('bank-slip-trigger');
bankSlipTrigger?.addEventListener('click', () => {
  openLightbox(0, [{
    src: 'assets/images/Bank Details .jpeg',
    caption: 'Official KCB Bank & Till Credentials — She Rises From The North Mentorship (Paybill: 522533 | Till / Acc: 8144533 | Dial *522#)'
  }]);
});
