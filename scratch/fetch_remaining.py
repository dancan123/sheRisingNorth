"""
fetch_remaining.py
Uses Drive's internal list endpoint to page through all 229 files.
Works for public/shared folders without an API key.
"""
import sys, re, os, json, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.stdout.encoding != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

FOLDER_ID   = '1oB0c54PgdyChv9M84ZahrArc8MbuqXbq'
OUT_DIR     = 'assets/images/gallery'
MAX_WORKERS = 8

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

os.makedirs(OUT_DIR, exist_ok=True)

# Read the already-saved HTML from previous run
html_cache = 'scratch/drive_folder.html'
if os.path.exists(html_cache):
    with open(html_cache, 'r', encoding='utf-8') as f:
        html = f.read()
    print(f'Loaded cached HTML ({len(html):,} bytes)')
else:
    req = urllib.request.Request(
        f'https://drive.google.com/drive/folders/{FOLDER_ID}?hl=en', headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode('utf-8', errors='ignore')
    with open(html_cache, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Fetched HTML ({len(html):,} bytes)')

# ── Extract all file IDs using Drive's serialised data format ─────────────────
# Drive embeds a data structure like:
# [["filename.jpg",null,null,"FILE_ID",...],...] for each file entry
# File IDs are exactly 33 chars in the format: 1<31 base64url chars>

print('\nExtracting file IDs from embedded Drive data...')

# Pattern: "1XXXX...XXX" strings exactly 33 chars starting with "1"
id_re = re.compile(r'"(1[A-Za-z0-9_-]{32})"')  # exactly 33 chars total
found_ids = list(dict.fromkeys(id_re.findall(html)))  # unique, order-preserving
print(f'  Pattern (1 + 32 chars): {len(found_ids)} IDs')

# Also try: file IDs that appear near image/jpeg content type hints
# These are sometimes stored as 28-44 char strings
id_re2 = re.compile(r'"(1[A-Za-z0-9_\-]{27,43})"')
found_ids2 = list(dict.fromkeys(id_re2.findall(html)))
print(f'  Pattern (1 + 27-43 chars): {len(found_ids2)} IDs')

# Merge both
all_ids = list(dict.fromkeys(found_ids + found_ids2))
all_ids = [fid for fid in all_ids if fid != FOLDER_ID]
print(f'  Total after merge and dedupe: {len(all_ids)}')

# ── Try downloading each one, auto-numbering past existing files ──────────────
# Find the highest sirn_ number already downloaded
existing = [f for f in os.listdir(OUT_DIR) if f.startswith('sirn_') and f.endswith('.jpg')]
existing_nums = []
for fn in existing:
    m = re.match(r'sirn_(\d+)\.jpg', fn)
    if m: existing_nums.append(int(m.group(1)))
start_num = max(existing_nums) + 1 if existing_nums else 1
print(f'\nHighest existing sirn_ number: {start_num - 1}')
print(f'Will start new files at sirn_{start_num:03d}.jpg')

# Build download list — skip IDs that already have a file
# We probe each ID first with a HEAD request before downloading
def probe_and_download(fid, proposed_name):
    out_path = os.path.join(OUT_DIR, proposed_name)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10_000:
        return proposed_name, 'skip', 0

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
                data = resp.read()
                if len(data) > 10_000 and ('image' in ctype or data[:2] == b'\xff\xd8' or data[:4] == b'\x89PNG'):
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    return proposed_name, 'ok', len(data)
        except Exception:
            time.sleep(0.15)
    return proposed_name, 'fail', 0

# Assign names to IDs
tasks = []
for i, fid in enumerate(all_ids):
    name = f'sirn_{start_num + i:03d}.jpg'
    tasks.append((fid, name))

print(f'\nDownloading {len(tasks)} candidate IDs (skipping existing)...\n')
ok, skipped, failed = 0, 0, 0

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futures = {ex.submit(probe_and_download, fid, name): (fid, name) for fid, name in tasks}
    done = 0
    for fut in as_completed(futures):
        fid, name = futures[fut]
        result_name, status, size = fut.result()
        done += 1
        if status == 'ok':
            ok += 1
            print(f'  [{done:>3}/{len(tasks)}] OK    {result_name} ({size//1024} KB)')
        elif status == 'skip':
            skipped += 1
        else:
            failed += 1

print(f'\nResult: {ok} new OK, {skipped} skipped, {failed} failed')

# ── Rebuild full JS array from all gallery images ─────────────────────────────
print('\nRebuilding JS gallery array...')
all_gallery = sorted([
    f for f in os.listdir(OUT_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
])

named = {
    'photobooth_students.jpg': 'SheIsRisingFromTheNorth Photo Booth - Students and Teachers with the Book',
    'students_reading.jpg':    'Reading the Book - I.G.H.S. Students Exploring Their Stories',
    'hildah_kathure.jpg':      'Hildah Kathure - Filmmaker and Documentary Photographer, MOV Foundation',
    'students_walking.jpg':    'The Journey of Becoming - Students in Uniform at the Launch',
    'exhibition_outdoor.jpg':  'Outdoor Exhibition Under the Acacia - Photo Prints on Easels',
    'classroom.jpg':           'Inside the Classroom - Where Futures Are Built',
    'support_impact.jpg':      'Education Changes Everything - Support the Girls of Northern Kenya',
    'press1.jpg':              'The Standard Books Feature - Education Works',
    'press2.jpg':              'The Sunday Standard Cover Feature - Dreams of Africa',
    'press3.jpg':              'Media Coverage - She Is Rising from the North Goes National',
}

js_lines = []
p = 1
for fn, cap in named.items():
    js_lines.append(f'  {{ id: "p{p:03d}", src: "assets/images/{fn}", caption: "{cap}" }},')
    p += 1
for fn in all_gallery:
    num = re.sub(r'\.(jpg|jpeg|png|webp)$', '', fn, flags=re.I)
    cap = f'She Is Rising from the North - {num}'
    js_lines.append(f'  {{ id: "p{p:03d}", src: "assets/images/gallery/{fn}", caption: "{cap}" }},')
    p += 1

if js_lines: js_lines[-1] = js_lines[-1].rstrip(',')

js_block = (
    f'// AUTO-GENERATED: {p-1} exhibition photos\n'
    f'const defaultPhotos = [\n'
    + '\n'.join(js_lines)
    + '\n];'
)

with open('scratch/gallery_photos_generated.js', 'w', encoding='utf-8') as f:
    f.write(js_block)

print(f'JS array: {p-1} total photos -> scratch/gallery_photos_generated.js')
print('Running apply_gallery.py...')
import subprocess
subprocess.run([sys.executable, '-X', 'utf8', 'scratch/apply_gallery.py'], check=True)
print('Done! Hard refresh your browser (Ctrl+Shift+R) to see all photos.')
