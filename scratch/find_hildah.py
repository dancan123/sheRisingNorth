import os
from PIL import Image

ref_path = r"C:\Users\Angaza Computecs\.gemini\antigravity-ide\brain\945167de-650b-4d53-a6ea-0b77215a6d95\.user_uploaded\media_1790951685961.png"
ref = Image.open(ref_path).convert('RGB')
ref_w, ref_h = ref.size
print(f"Reference image size: {ref_w}x{ref_h}")

# Let's take a small distinctive patch, like the banner pattern
# banner is roughly in the middle vertical: y from 0.48 to 0.65
banner = ref.crop((10, int(ref_h * 0.48), ref_w - 10, int(ref_h * 0.65)))
banner.save("scratch/ref_banner.jpg")
bw, bh = banner.size

# Also check average color or search with sliding window on small thumbnails
# Or even simpler: calculate color histograms or average RGB
banner_pixels = list(banner.getdata())
avg_r = sum(p[0] for p in banner_pixels) / len(banner_pixels)
avg_g = sum(p[1] for p in banner_pixels) / len(banner_pixels)
avg_b = sum(p[2] for p in banner_pixels) / len(banner_pixels)
print(f"Banner avg RGB: {avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f}")

# Look for gallery photos that have similar features or dimensions
gallery_dir = "assets/images/gallery"
files = [f for f in os.listdir(gallery_dir) if f.lower().endswith('.jpg') and not f.startswith('sirn_')]

# Let's resize images to thumbnail and check if a slice matches the banner or ref
import math

results = []
# Precompute a small representation of banner (e.g. 16x16)
small_banner = banner.resize((16, 16))
sb_data = list(small_banner.getdata())

for fname in files:
    fpath = os.path.join(gallery_dir, fname)
    try:
        with Image.open(fpath) as img:
            iw, ih = img.size
            # The ref is a portrait crop from a larger photo.
            # Let's find images where similar color or pattern exists
            # Let's downscale image to width 200
            scale = 200 / iw
            thumb = img.resize((200, int(ih * scale)))
            tw, th = thumb.size
            
            # Slide a window of size sb_w x sb_h
            min_diff = float('inf')
            best_y = 0
            # Test step of 10 pixels
            sw = max(10, int(bw * scale))
            sh = max(10, int(bh * scale))
            
            for y in range(0, th - sh, 15):
                for x in range(0, tw - sw, 20):
                    patch = thumb.crop((x, y, x + sw, y + sh)).resize((16, 16))
                    p_data = list(patch.getdata())
                    diff = sum(abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]) 
                               for p1, p2 in zip(sb_data, p_data)) / len(sb_data)
                    if diff < min_diff:
                        min_diff = diff
            results.append((min_diff, fname))
    except Exception as e:
        pass

results.sort(key=lambda x: x[0])
print("\nTop 15 closest candidate photos:")
for diff, fn in results[:15]:
    print(f"Diff: {diff:.2f} -> {fn}")
