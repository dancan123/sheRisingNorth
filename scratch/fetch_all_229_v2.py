"""
fetch_all_229_v2.py
Improved Drive folder scraper:
- Fixes Unicode console error
- Extracts file IDs from Drive's embedded AF_initDataCallback JSON blobs
- Falls back to broad regex sweeps
- Downloads everything at high-res
- Auto-generates updated main.js gallery array
"""
import sys, re, os, json, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix Windows cp1252 console encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

FOLDER_ID   = '1oB0c54PgdyChv9M84ZahrArc8MbuqXbq'
FOLDER_URL  = f'https://drive.google.com/drive/folders/{FOLDER_ID}?hl=en'
OUT_DIR     = 'assets/images/gallery'
HTML_CACHE  = 'scratch/drive_folder.html'
IDS_FILE    = 'scratch/all_drive_ids_v2.json'
JS_OUT      = 'scratch/gallery_photos_generated.js'
MAX_WORKERS = 6

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs('scratch', exist_ok=True)

# ── STEP 1: Fetch folder HTML ─────────────────────────────────────────────────
print('=== STEP 1: Fetching Drive folder HTML ===')
req = urllib.request.Request(FOLDER_URL, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as r:
    html = r.read().decode('utf-8', errors='ignore')

with open(HTML_CACHE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'  Fetched {len(html):,} bytes, saved to {HTML_CACHE}')

# ── STEP 2: Extract file IDs using multiple strategies ────────────────────────
print('\n=== STEP 2: Extracting file IDs ===')
id_set = set()

# Strategy A: Named files — ["filename.jpg","...","FILE_ID",...]
# Drive serialises file entries as arrays; file IDs are 33-char base64url strings
# Pattern: something that looks like a file ID (28+ chars, alphanum + dash + underscore)
FILE_ID_RE = re.compile(r'["\[]([A-Za-z0-9_-]{28,})["\],]')

# Find all candidate IDs
all_candidates = FILE_ID_RE.findall(html)
print(f'  Candidate IDs found: {len(all_candidates)}')

# Filter: real Drive file IDs are typically 33 chars, sometimes 28-44
for cid in all_candidates:
    if 28 <= len(cid) <= 44:
        id_set.add(cid)

# Strategy B: IDs that appear right after file size markers (bytes)
# Drive often encodes: ["filename", null, "id", [size_bytes], ...]
size_context = re.findall(r'"([A-Za-z0-9_-]{28,44})"[^"]{0,80}?\d{4,}', html)
for cid in size_context:
    id_set.add(cid)

# Strategy C: AF_initDataCallback blobs — extract everything between callback data
init_blobs = re.findall(r'AF_initDataCallback\((.{100,}?)\)\s*;', html, re.DOTALL)
print(f'  AF_initDataCallback blobs: {len(init_blobs)}')
for blob in init_blobs:
    ids = re.findall(r'"([A-Za-z0-9_-]{28,44})"', blob)
    for cid in ids:
        id_set.add(cid)

# Strategy D: Look for "_" separated IDs in data arrays
# e.g., "1ABC...XYZ","1DEF...ABC"
pairs = re.findall(r'"(1[A-Za-z0-9_-]{27,43})"', html)
print(f'  IDs starting with "1" (typical Drive file IDs): {len(set(pairs))}')
for cid in pairs:
    id_set.add(cid)

print(f'  Total unique candidate IDs: {len(id_set)}')

# Remove the folder ID itself and known non-file IDs (short, or all same char)
id_set.discard(FOLDER_ID)
id_set = {cid for cid in id_set if len(set(cid)) > 4}  # reject repetitive strings

# Save
id_list = sorted(id_set)
with open(IDS_FILE, 'w', encoding='utf-8') as f:
    json.dump(id_list, f, indent=2)
print(f'  Saved {len(id_list)} IDs to {IDS_FILE}')

# ── STEP 3: Download images ───────────────────────────────────────────────────
print(f'\n=== STEP 3: Downloading {len(id_list)} candidate images ===')

def download(fid, idx):
    name = f'sirn_{idx:03d}.jpg'
    out_path = os.path.join(OUT_DIR, name)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 15_000:
        return name, 'skip', 0

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
                if len(data) > 10_000 and ('image' in ctype or data[:2] == b'\xff\xd8' or data[:4] == b'\x89PNG'):
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    return name, 'ok', len(data)
        except Exception:
            time.sleep(0.2)

    return name, 'fail', 0

ok_files  = []
fail_list = []
total = len(id_list)

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futures = {ex.submit(download, fid, i+1): (fid, i+1) for i, fid in enumerate(id_list)}
    done = 0
    for fut in as_completed(futures):
        fid, i = futures[fut]
        name, status, size = fut.result()
        done += 1
        if status == 'ok':
            ok_files.append(name)
            print(f'  [{done:>3}/{total}] OK    {name}  ({size//1024} KB)')
        elif status == 'skip':
            ok_files.append(name)
            print(f'  [{done:>3}/{total}] SKIP  {name}')
        else:
            fail_list.append((name, fid))
            print(f'  [{done:>3}/{total}] FAIL  {name}  (id={fid[:12]}...)')

print(f'\nDownloaded/available: {len(ok_files)}')
print(f'Failed: {len(fail_list)}')

# ── STEP 4: Build JS defaultPhotos array ─────────────────────────────────────
print(f'\n=== STEP 4: Building JS gallery array ===')

all_gallery = sorted([
    f for f in os.listdir(OUT_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
])

print(f'  Total images in {OUT_DIR}/: {len(all_gallery)}')

named_captions = {
    'photobooth_students.jpg': '#SheIsRisingFromTheNorth Photo Booth - Students & Teachers with the Book',
    'students_reading.jpg':    'Reading the Book - I.G.H.S. Students Exploring Their Stories',
    'hildah_kathure.jpg':      'Hildah Kathure - Filmmaker & Documentary Photographer',
    'students_walking.jpg':    'The Journey of Becoming - Students in Uniform at the Launch',
    'exhibition_outdoor.jpg':  'Outdoor Exhibition Under the Acacia - Photo Prints on Easels',
    'classroom.jpg':           'Inside the Classroom - Where Futures Are Built',
    'support_impact.jpg':      'Education Changes Everything - Support the Girls of Northern Kenya',
    'press1.jpg':              'The Standard Books Feature - Education Works',
    'press2.jpg':              'The Sunday Standard Cover Feature - Dreams of Africa',
    'press3.jpg':              'Media Coverage - She Is Rising from the North Goes National',
}

js_lines = []
idx = 1

# Named images first (from parent images/ folder)
for fn, cap in named_captions.items():
    js_lines.append(f"  {{ id: 'p{idx:03d}', src: 'assets/images/{fn}', caption: \"{cap}\" }},")
    idx += 1

# All gallery images
for fn in all_gallery:
    num = fn.replace('sirn_', '').replace('.jpg', '').replace('_W1A', 'W1A')
    cap = f'She Is Rising from the North - Exhibition Photo {num}'
    js_lines.append(f"  {{ id: 'p{idx:03d}', src: 'assets/images/gallery/{fn}', caption: \"{cap}\" }},")
    idx += 1

# Remove trailing comma
if js_lines:
    js_lines[-1] = js_lines[-1].rstrip(',')

js_block = (
    f"// AUTO-GENERATED: {idx-1} exhibition photos\n"
    f"// Gallery key: sirn_gallery_photos_v6\n"
    f"const defaultPhotos = [\n"
    + "\n".join(js_lines)
    + "\n];"
)

with open(JS_OUT, 'w', encoding='utf-8') as f:
    f.write(js_block)

print(f'  JS array written to {JS_OUT} ({idx-1} total photos)')
print('\nDone! Run apply_gallery.py to inject this into main.js automatically.')
