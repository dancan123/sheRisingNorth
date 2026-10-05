"""
apply_gallery.py
Reads scratch/gallery_photos_generated.js and injects the defaultPhotos
array into assets/js/main.js, bumping the gallery key to v6.
"""
import re, sys

JS_MAIN = 'assets/js/main.js'
JS_GEN  = 'scratch/gallery_photos_generated.js'

with open(JS_GEN, 'r', encoding='utf-8') as f:
    new_array = f.read().strip()

with open(JS_MAIN, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Bump gallery key to v6
content = re.sub(
    r"const GALLERY_KEY = 'sirn_gallery_photos_v\d+';",
    "const GALLERY_KEY = 'sirn_gallery_photos_v6';",
    content
)

# 2. Replace the entire defaultPhotos block
pattern = re.compile(
    r'// (?:AUTO-GENERATED.*?\n)?// Authentic exhibition.*?const defaultPhotos = \[.*?\];',
    re.DOTALL
)
if pattern.search(content):
    content = pattern.sub(new_array, content, count=1)
    print('Replaced existing defaultPhotos block.')
else:
    # Fallback: insert after "let photos = loadPhotos();"
    content = content.replace(
        'let photos = loadPhotos();\n',
        f'let photos = loadPhotos();\n\n{new_array}\n'
    )
    print('Inserted new defaultPhotos block after loadPhotos().')

with open(JS_MAIN, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done! {JS_MAIN} updated successfully.')
print('Hard-refresh the browser (Ctrl+Shift+R) to see all photos.')
