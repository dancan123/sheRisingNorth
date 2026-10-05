import os
import sys
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.stdout.encoding != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

OUT_DIR = 'assets/images/gallery'
os.makedirs(OUT_DIR, exist_ok=True)

with open('scratch/all_229_drive_files.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

print(f"Total files in list: {len(files)}")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}

def download_file(item):
    name = item['name']
    fid = item['id']
    target_path = os.path.join(OUT_DIR, name)
    
    # If already downloaded and valid image size (> 15KB)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 15000:
        return name, 'skipped', os.path.getsize(target_path)

    # Candidate URLs for fast high quality download
    urls = [
        f'https://lh3.googleusercontent.com/d/{fid}=w1600',
        f'https://drive.google.com/thumbnail?id={fid}&sz=w1600',
        f'https://drive.google.com/uc?export=download&id={fid}'
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
                if len(data) > 15000 and (data[:2] == b'\xff\xd8' or data[:4] == b'\x89PNG' or b'JFIF' in data[:20]):
                    with open(target_path, 'wb') as out_f:
                        out_f.write(data)
                    return name, 'downloaded', len(data)
        except Exception:
            time.sleep(0.2)
            
    return name, 'failed', 0

print("Starting download of all 229 photos with 10 threads...")
start_time = time.time()
counts = {'downloaded': 0, 'skipped': 0, 'failed': 0}

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(download_file, item): item for item in files}
    done = 0
    total = len(files)
    for fut in as_completed(futures):
        done += 1
        name, status, sz = fut.result()
        counts[status] += 1
        if status == 'downloaded':
            print(f"[{done:3d}/{total}] OK: {name} ({sz//1024} KB)")
        elif status == 'skipped':
            pass
        else:
            print(f"[{done:3d}/{total}] FAILED: {name}")

elapsed = time.time() - start_time
print(f"\nDownload finished in {elapsed:.1f}s!")
print(f"Downloaded: {counts['downloaded']}, Skipped (Already existed): {counts['skipped']}, Failed: {counts['failed']}")
