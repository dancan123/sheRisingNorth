"""
fetch_all_229.py
Scrape the public Google Drive folder, download ALL images, and
auto-generate the JS defaultPhotos array for main.js gallery.

Drive folder: https://drive.google.com/drive/folders/1oB0c54PgdyChv9M84ZahrArc8MbuqXbq
"""

import re
import os
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

FOLDER_ID   = '1oB0c54PgdyChv9M84ZahrArc8MbuqXbq'
FOLDER_URL  = f'https://drive.google.com/drive/folders/{FOLDER_ID}'
OUT_DIR     = 'assets/images/gallery'
IDS_FILE    = 'scratch/all_drive_ids.json'
JS_OUT      = 'scratch/gallery_photos_generated.js'
MAX_WORKERS = 6
HEADERS     = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
}

os.makedirs(OUT_DIR, exist_ok=True)

# ── STEP 1: Fetch folder HTML and extract all file IDs ────────────────────────
print('Fetching Google Drive folder page...')
req = urllib.request.Request(FOLDER_URL, headers=HEADERS)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode('utf-8', errors='ignore')
    print(f'  Fetched {len(html):,} bytes')
except Exception as e:
    print(f'ERROR fetching folder: {e}')
    raise

# Pattern 1: ["filename.jpg","fileId"] style entries
pat1 = re.findall(r'"([^"]+\.(?:jpg|jpeg|png|webp))"[^[]*?"([\w\-]{25,})"', html, re.I)

# Pattern 2: bare file IDs that appear multiple times in the serialized data
# Drive embeds IDs in multiple forms — use a broad sweep
pat2 = re.findall(r'(?:\/d\/|id=|")([\w\-]{33,})', html)

# Collect unique IDs ──────────────────────────────────────────────────────────
id_map = {}  # id -> filename

for filename, fid in pat1:
    if fid not in id_map:
        safe = re.sub(r'[^\w\.\-]', '_', filename)
        id_map[fid] = safe

# For pat2 IDs without names, assign sequential names
idx = len(id_map) + 1
for fid in pat2:
    if fid not in id_map and len(fid) >= 33:
        id_map[fid] = f'sirn_{idx:03d}.jpg'
        idx += 1

print(f'  Found {len(id_map)} unique file IDs from HTML scrape')

# Also try to get IDs from the JSON-like blobs Drive embeds ───────────────────
# Drive uses a format like: ["name","","","ID",... in its data arrays
# Aggressive extraction of 33+ char alphanumeric-dash IDs
all_ids_broad = re.findall(r'"([\w-]{33,})"', html)
for fid in all_ids_broad:
    if fid not in id_map:
        id_map[fid] = f'sirn_{idx:03d}.jpg'
        idx += 1

print(f'  Total unique IDs after broad sweep: {len(id_map)}')

# Save the ID map
with open(IDS_FILE, 'w', encoding='utf-8') as f:
    json.dump(id_map, f, indent=2)
print(f'  Saved to {IDS_FILE}')

# ── STEP 2: Download each image ───────────────────────────────────────────────
print(f'\nDownloading up to {len(id_map)} images with {MAX_WORKERS} threads...\n')

def download(fid_name):
    fid, name = fid_name
    out_path = os.path.join(OUT_DIR, name)

    # Skip if already downloaded and substantial
    if os.path.exists(out_path) and os.path.getsize(out_path) > 15_000:
        return name, fid, 'skip', 0

    urls = [
        f'https://drive.google.com/thumbnail?id={fid}&sz=w1600',
        f'https://lh3.googleusercontent.com/d/{fid}=w1600',
        f'https://drive.google.com/uc?export=download&id={fid}',
    ]

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                ctype = resp.headers.get('Content-Type', '')
                data  = resp.read()
                if len(data) > 10_000 and ('image' in ctype or data[:3] in (b'\xff\xd8\xff', b'PNG', b'GIF')):
                    # Ensure .jpg extension for JPEG data
                    if data[:2] == b'\xff\xd8' and not name.lower().endswith(('.jpg', '.jpeg')):
                        name = os.path.splitext(name)[0] + '.jpg'
                        out_path = os.path.join(OUT_DIR, name)
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    return name, fid, 'ok', len(data)
        except Exception:
            time.sleep(0.3)

    return name, fid, 'fail', 0

items  = list(id_map.items())
ok_files = []
failed   = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futures = {ex.submit(download, item): item for item in items}
    done = 0
    for fut in as_completed(futures):
        name, fid, status, size = fut.result()
        done += 1
        if status == 'ok':
            ok_files.append(name)
            print(f'  [{done:>3}/{len(items)}] OK    {name}  ({size//1024} KB)')
        elif status == 'skip':
            ok_files.append(name)
            print(f'  [{done:>3}/{len(items)}] SKIP  {name}')
        else:
            failed.append((name, fid))
            print(f'  [{done:>3}/{len(items)}] FAIL  {name}')

print(f'\n✅ Downloaded/available: {len(ok_files)}')
print(f'❌ Failed: {len(failed)}')

# ── STEP 3: Build JS defaultPhotos array from ALL files in gallery dir ────────
print(f'\nGenerating JS gallery array from {OUT_DIR}/ ...')

all_gallery = sorted([
    f for f in os.listdir(OUT_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
])

# Named / curated images (manually placed earlier)
named = {
    'photobooth_students.jpg': '#SheIsRisingFromTheNorth Photo Booth — Students & Teachers with the Book',
    'students_reading.jpg':    'Reading the Book — I.G.H.S. Students Exploring Their Stories',
    'hildah_kathure.jpg':      'Hildah Kathure — Filmmaker & Documentary Photographer',
    'students_walking.jpg':    'The Journey of Becoming — Students in Uniform at the Launch',
    'exhibition_outdoor.jpg':  'Outdoor Exhibition Under the Acacia — Photo Prints on Easels',
}

lines = []
idx = 1

# Curated named images first (from parent images folder)
for fn, cap in named.items():
    lines.append(f"  {{ id: 'p{idx:03d}', src: 'assets/images/{fn}', caption: '{cap}' }},")
    idx += 1

# All gallery images
for fn in all_gallery:
    cap = fn.replace('_', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '').strip()
    cap = f'She Is Rising from the North — {cap}'
    lines.append(f"  {{ id: 'p{idx:03d}', src: 'assets/images/gallery/{fn}', caption: '{cap}' }},")
    idx += 1

# Remove trailing comma from last item
if lines:
    lines[-1] = lines[-1].rstrip(',')

js_block = "const defaultPhotos = [\n" + "\n".join(lines) + "\n];"

with open(JS_OUT, 'w', encoding='utf-8') as f:
    f.write(js_block)

print(f'✅ JS array written to {JS_OUT}  ({idx-1} total photos)')
print('\nAll done! Now run: update_main_js.py  (or copy the array manually)')
