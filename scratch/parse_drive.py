import re
import json

with open('scratch/drive_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for image extensions or file names in the html
extensions = ['jpg', 'jpeg', 'png', 'webp', 'heic', 'tif', 'tiff']
pattern = re.compile(r'([\w\-\.\s\(\)]+\.(?:' + '|'.join(extensions) + r'))', re.IGNORECASE)
found_names = set(pattern.findall(content))
print(f"Found {len(found_names)} image file names:")
for n in sorted(found_names):
    print(" -", n)

# Also look for Google Drive file IDs associated with these names or embedded in JSON-like arrays
# In Drive folder data, items are usually serialized as [..., "id", "name", ...] or similar
# Let's search for standard 33-char drive IDs
id_pattern = re.compile(r'\"([a-zA-Z0-9_-]{28,35})\"')
ids = set(id_pattern.findall(content))
print(f"Total potential Drive IDs: {len(ids)}")

# Let's search for snippets containing file names to find their corresponding IDs
for name in sorted(found_names)[:10]:
    idx = content.find(name)
    if idx != -1:
        snippet = content[max(0, idx - 200):min(len(content), idx + 200)]
        print(f"\nSnippet around '{name}':")
        print(repr(snippet))
