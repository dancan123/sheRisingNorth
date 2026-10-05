import re
import json

with open('scratch/drive_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern in the HTML:
# aria-label="(_W1A\d+\.jpg) Image Shared"[^>]*ssk='5:auSv138:([a-zA-Z0-9_-]{25,})-0-16'
# or similar
pattern = re.compile(r'aria-label="([^"]+\.jpe?g)\s+Image\s+Shared"[^>]*ssk=[\'"]5:auSv138:([a-zA-Z0-9_-]{25,})', re.IGNORECASE)
matches = pattern.findall(html)

print(f"Found {len(matches)} matched photos via aria-label + ssk:")
photos = {}
for name, fid in matches:
    if name not in photos:
        photos[name] = fid

# If not all found with that exact pattern, let's also search with a broader regex:
if len(photos) < 30:
    broad_pattern = re.compile(r'([_a-zA-Z0-9]+\.jpe?g).*?5:auSv138:([a-zA-Z0-9_-]{25,})', re.DOTALL)
    # Search in chunks of 500 chars around every jpg
    for m in re.finditer(r'([_a-zA-Z0-9]+\.jpe?g)', html, re.IGNORECASE):
        fname = m.group(1)
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 300)
        chunk = html[start:end]
        ssk_m = re.search(r'5:auSv138:([a-zA-Z0-9_-]{25,})', chunk)
        if ssk_m:
            photos[fname] = ssk_m.group(1)

print(f"Total unique photos matched: {len(photos)}")
for name, fid in sorted(photos.items()):
    print(f"{name}: {fid}")

with open('scratch/drive_photos.json', 'w', encoding='utf-8') as f:
    json.dump(photos, f, indent=2)
print("Saved scratch/drive_photos.json")
