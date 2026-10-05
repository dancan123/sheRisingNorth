from PIL import Image

im = Image.open('assets/images/gallery/_W1A5266.jpg')
w, h = im.size
# Crop around desk bottom left/center:
crop = im.crop((int(w * 0.2), int(h * 0.85), int(w * 0.6), h))
crop.save('scratch/desk_flyer.jpg')
print("Saved scratch/desk_flyer.jpg")
