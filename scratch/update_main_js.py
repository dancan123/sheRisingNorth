import json
import re

print("Starting main.js update...")

with open('scratch/verified_gallery.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

print(f"Total photos to inject: {len(photos)}")

photos_js_str = json.dumps(photos, indent=2, ensure_ascii=False)

with open('assets/js/main.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 1. Update SITE_CONFIG
new_site_config = """window.SITE_CONFIG = {
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
};"""

js_code = re.sub(
    r'window\.SITE_CONFIG\s*=\s*\{[\s\S]*?\n\};',
    lambda m: new_site_config,
    js_code
)

# 2. Update GALLERY_KEY and defaultPhotos
js_code = re.sub(
    r"const GALLERY_KEY = '[^']+';",
    "const GALLERY_KEY = 'sirn_gallery_photos_v12';",
    js_code
)

# Replace defaultPhotos
pattern = r'const defaultPhotos\s*=\s*\[[\s\S]*?\];\s*(?=\/\*|\n\s*function|\n\s*let allPhotos|\n\s*\/\/)'
replacement = f"const defaultPhotos = {photos_js_str};\n"

js_code = re.sub(pattern, lambda m: replacement, js_code)

# 3. Add bank slip trigger click handler if not already present
if 'bank-slip-trigger' not in js_code:
    slip_handler = """
// Bank slip preview lightbox
const bankSlipTrigger = document.getElementById('bank-slip-trigger');
bankSlipTrigger?.addEventListener('click', () => {
  openLightbox(0, [{
    src: 'assets/images/Bank Details .jpeg',
    caption: 'Official KCB Bank & Till Credentials — She Rises From The North Mentorship (Paybill: 522533 | Till / Acc: 8144533 | Dial *522#)'
  }]);
});
"""
    js_code += slip_handler

with open('assets/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("assets/js/main.js successfully updated!")
