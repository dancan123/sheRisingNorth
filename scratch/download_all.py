import json
import urllib.request
import os
import time
from concurrent.futures import ThreadPoolExecutor

os.makedirs('assets/images/gallery', exist_ok=True)

with open('scratch/drive_photos.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

print(f"Starting download of {len(photos)} photos...")

def download_photo(item):
    name, raw_id = item
    # Strip any trailing suffix like -0-16
    clean_id = raw_id.split('-0-')[0]
    out_path = os.path.join('assets/images/gallery', name)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"Skipping {name} (already downloaded)")
        return name, True

    # Try thumbnail URL first with high res (1600px width), fallback to export download
    urls = [
        f"https://drive.google.com/thumbnail?id={clean_id}&sz=w1600",
        f"https://lh3.googleusercontent.com/d/{clean_id}",
        f"https://drive.google.com/uc?id={clean_id}&export=download"
    ]

    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) > 5000 and 'image' in resp.headers.get('Content-Type', ''):
                    with open(out_path, 'wb') as out_f:
                        out_f.write(data)
                    print(f"Downloaded {name} ({len(data)//1024} KB)")
                    return name, True
        except Exception as e:
            pass

    print(f"Failed to download {name}")
    return name, False

# Download with 5 threads
results = []
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(download_photo, photos.items()))

success_count = sum(1 for name, ok in results if ok)
print(f"\nDone! Successfully downloaded {success_count}/{len(photos)} photos to assets/images/gallery/")
