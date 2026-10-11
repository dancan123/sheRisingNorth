import os, re

img_dir = 'assets/images'
all_imgs = set(f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)))

with open('assets/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = re.compile(r'"src":\s*"assets/images/([^"]+)"')
gallery_refs = set(m.group(1) for m in pattern.finditer(js))

print("Total images in folder:", len(all_imgs))
print("Images referenced in gallery:", len(gallery_refs))
print()
print("=== NOT in gallery ===")
for f in sorted(all_imgs - gallery_refs):
    print(" ", f)
print()
print("=== In gallery but file missing ===")
for f in sorted(gallery_refs - all_imgs):
    print(" ", f)
