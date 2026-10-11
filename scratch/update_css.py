import json
import re

print("Starting full site update script...")

# 1. Read verified gallery JSON
with open('scratch/verified_gallery.json', 'r', encoding='utf-8') as f:
    gallery_photos = json.load(f)

print(f"Loaded {len(gallery_photos)} gallery photos.")

# ==============================================================================
# 2. UPDATE assets/css/style.css
# ==============================================================================
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

new_styles = """
/* ============================================================
   VOICES OF THE NORTH — TESTIMONIAL QUOTES
   ============================================================ */
.voices {
  padding: var(--sp-xl) 0;
  background: var(--clr-cream);
  position: relative;
}

.voices__header {
  text-align: center;
  max-width: 760px;
  margin: 0 auto 3.5rem auto;
}

.voices__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.voice-card {
  background: var(--clr-white);
  border-radius: var(--radius-md);
  padding: 2.25rem;
  box-shadow: 0 4px 20px rgba(26, 14, 5, 0.06);
  border: 1px solid rgba(212, 168, 83, 0.25);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform var(--dur-med), box-shadow var(--dur-med);
  position: relative;
}

.voice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 36px rgba(26, 14, 5, 0.12);
  border-color: var(--clr-gold);
}

.voice-card__quote-mark {
  font-family: var(--font-serif);
  font-size: 3.5rem;
  line-height: 1;
  color: var(--clr-gold);
  opacity: 0.45;
  margin-bottom: -1rem;
}

.voice-card__text {
  font-family: var(--font-serif);
  font-size: 1.12rem;
  line-height: 1.65;
  color: var(--clr-earth-deep);
  font-style: italic;
  margin-bottom: 1.75rem;
  position: relative;
  z-index: 1;
}

.voice-card__author {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(26, 14, 5, 0.08);
}

.voice-card__avatar {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--clr-gold);
  flex-shrink: 0;
}

.voice-card__avatar-placeholder {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--clr-earth-mid), var(--clr-gold));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.voice-card__name {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--clr-earth-deep);
  margin-bottom: 0.2rem;
}

.voice-card__title {
  font-size: 0.85rem;
  color: var(--clr-earth-mid);
  font-weight: 500;
  line-height: 1.35;
}

/* ============================================================
   EXHIBITION TOUR — DATES & PLACES
   ============================================================ */
.tour {
  padding: var(--sp-xl) 0;
  background: var(--clr-earth-deep);
  color: var(--clr-white);
  position: relative;
  overflow: hidden;
}

.tour__header {
  text-align: center;
  max-width: 750px;
  margin: 0 auto 3.5rem auto;
}

.tour__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
}

.tour-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(212, 168, 83, 0.25);
  border-radius: var(--radius-md);
  padding: 2.2rem 1.8rem;
  backdrop-filter: blur(8px);
  transition: all var(--dur-med);
  display: flex;
  flex-direction: column;
}

.tour-card:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: var(--clr-gold);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.tour-card__date-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(212, 168, 83, 0.15);
  border: 1px solid var(--clr-gold);
  color: var(--clr-gold);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 1.25rem;
  align-self: flex-start;
}

.tour-card__city {
  font-size: 1.6rem;
  color: var(--clr-white);
  margin-bottom: 0.4rem;
  font-family: var(--font-display);
}

.tour-card__venue {
  font-size: 1rem;
  color: var(--clr-gold-light);
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.tour-card__details {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.tour-card__tag {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #a3e635;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.tour__footer {
  margin-top: 3rem;
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.tour__footer p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
  margin: 0;
}

/* ============================================================
   PRESS RELEASE DOCUMENT SECTION
   ============================================================ */
.press-release {
  padding: var(--sp-xl) 0;
  background: #f5efe6;
}

.press-release__wrap {
  max-width: 960px;
  margin: 0 auto;
  background: var(--clr-white);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 40px rgba(26, 14, 5, 0.08);
  border: 1px solid rgba(122, 69, 32, 0.15);
  padding: 3.5rem;
}

.press-release__badge {
  display: inline-block;
  background: var(--clr-earth-deep);
  color: var(--clr-gold);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.4rem 1rem;
  border-radius: var(--radius-pill);
  margin-bottom: 1.5rem;
}

.press-release__headline {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.5vw, 2.5rem);
  line-height: 1.25;
  color: var(--clr-earth-deep);
  margin-bottom: 1.5rem;
}

.press-release__sub {
  font-size: 1.1rem;
  line-height: 1.65;
  color: var(--clr-earth-mid);
  font-weight: 500;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid var(--clr-sand);
}

.press-release__body p {
  font-size: 1rem;
  line-height: 1.75;
  color: #38302a;
  margin-bottom: 1.5rem;
}

.press-release__body h3 {
  font-family: var(--font-serif);
  font-size: 1.4rem;
  color: var(--clr-earth-deep);
  margin: 2.25rem 0 1rem 0;
}

.press-release__body blockquote {
  border-left: 3.5px solid var(--clr-gold);
  padding-left: 1.5rem;
  margin: 1.75rem 0;
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 1.08rem;
  line-height: 1.65;
  color: var(--clr-earth-mid);
}

.press-release__contact {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px dashed rgba(122, 69, 32, 0.2);
  background: rgba(212, 168, 83, 0.06);
  border-radius: var(--radius-sm);
  padding: 1.75rem;
}

.press-release__contact h4 {
  font-size: 1.05rem;
  color: var(--clr-earth-deep);
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.press-release__contact-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  font-size: 0.92rem;
  line-height: 1.6;
}

/* ============================================================
   BANK DETAILS FLYER DISPLAY IN SUPPORT
   ============================================================ */
.payment-card--official-slip {
  border-left: 4px solid #006837;
  background: linear-gradient(135deg, rgba(0, 104, 55, 0.08) 0%, rgba(212, 168, 83, 0.06) 100%), rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 104, 55, 0.3);
}

.payment-card--official-slip:hover {
  border-color: #008848;
  box-shadow: 0 12px 32px rgba(0, 104, 55, 0.2);
}

.payment-logo--kcb {
  background: #006837;
  color: #ffffff;
  font-weight: 800;
  letter-spacing: 0.06em;
  padding: 0.22rem 0.6rem;
  border-radius: 4px;
}

.bank-slip-preview {
  position: relative;
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin-top: 0.85rem;
  cursor: pointer;
  border: 1.5px solid rgba(0, 104, 55, 0.35);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
  transition: transform var(--dur-med), border-color var(--dur-med), box-shadow var(--dur-med);
  background: #111;
}

.bank-slip-preview:hover {
  transform: translateY(-2px);
  border-color: #008848;
  box-shadow: 0 10px 28px rgba(0, 104, 55, 0.35);
}

.bank-slip-img {
  width: 100%;
  max-height: 240px;
  object-fit: cover;
  object-position: top center;
  display: block;
  transition: transform var(--dur-med);
}

.bank-slip-preview:hover .bank-slip-img {
  transform: scale(1.02);
}

.bank-slip-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 40, 20, 0.9) 0%, rgba(0, 0, 0, 0.3) 60%, transparent 100%);
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  color: #fff;
  font-weight: 600;
  font-size: 0.88rem;
  transition: background 0.3s ease;
}

.bank-slip-btn {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-pill);
  font-size: 0.78rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

/* Responsive updates */
@media (max-width: 900px) {
  .voices__grid { grid-template-columns: 1fr; }
  .tour__grid { grid-template-columns: 1fr; }
  .press-release__wrap { padding: 2rem 1.5rem; }
  .press-release__contact-grid { grid-template-columns: 1fr; }
}
"""

if '/* VOICES OF THE NORTH' not in css_content and '.voices {' not in css_content:
    with open('assets/css/style.css', 'a', encoding='utf-8') as f:
        f.write('\n' + new_styles)
    print("Appended new styles to assets/css/style.css")
else:
    print("Styles already present in assets/css/style.css")

print("CSS updated successfully.")
