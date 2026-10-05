import os
import json
import re

gallery_dir = 'assets/images/gallery'
files = sorted([f for f in os.listdir(gallery_dir) if f.startswith('_W1A') and f.endswith('.jpg')])

photos = []

# Special named highlight photos from assets/images
highlights = [
    {
        'id': 'hl-1',
        'src': 'assets/images/photobooth_students.jpg',
        'caption': '#SheIsRisingFromTheNorth Photo Booth — Students & Teachers with the Book',
        'category': 'photobooth',
        'tag': 'Featured'
    },
    {
        'id': 'hl-2',
        'src': 'assets/images/students_reading.jpg',
        'caption': 'Reading the Book — I.G.H.S. Students Exploring Their Stories',
        'category': 'exhibition',
        'tag': 'Featured'
    },
    {
        'id': 'hl-3',
        'src': 'assets/images/students_walking.jpg',
        'caption': 'The Journey of Becoming — Students in Uniform at the Launch',
        'category': 'exhibition',
        'tag': 'Featured'
    },
    {
        'id': 'hl-4',
        'src': 'assets/images/exhibition_outdoor.jpg',
        'caption': 'Outdoor Exhibition Under the Acacia — Photo Prints on Easels',
        'category': 'exhibition',
        'tag': 'Featured'
    },
    {
        'id': 'hl-5',
        'src': 'assets/images/classroom.jpg',
        'caption': 'Inside the Classroom — Where Futures Are Built',
        'category': 'exhibition',
        'tag': 'Featured'
    },
    {
        'id': 'hl-6',
        'src': 'assets/images/support_impact.jpg',
        'caption': 'Education Changes Everything — Support the Girls of Northern Kenya',
        'category': 'exhibition',
        'tag': 'Featured'
    }
]

photos.extend(highlights)

# Curated captions for key known photos
curated_captions = {
    '_W1A5212.jpg': 'Exhibition Gallery Pavilion — Desert Sunset and Stories of Hope',
    '_W1A5213.jpg': 'Inside the Exhibition Tent — 15 Years of Documentary Photography',
    '_W1A5219.jpg': 'Opening Ceremony — Community Leaders & Guests of Honour',
    '_W1A5220.jpg': 'Viewing the Photo-Book — A Moment of Recognition',
    '_W1A5223.jpg': 'School Girls at the Exhibition — Northern Kenya',
    '_W1A5224.jpg': 'The Long Road — From Grazing Fields to Classrooms',
    '_W1A5227.jpg': 'Portrait of Resilience — She Is Rising from the North',
    '_W1A5230.jpg': 'Framed Portraits of Resilience — Community Exhibition',
    '_W1A5235.jpg': 'MOV Foundation Supporters at the Launch Event',
    '_W1A5237.jpg': 'A Girl Reads Her Own Story — Isiolo, Kenya',
    '_W1A5238.jpg': 'Teachers and Students Celebrate 15 Years of Education',
    '_W1A5240.jpg': 'Community Elder Signing the Official Exhibition Guestbook',
    '_W1A5244.jpg': 'Fifteen Years — Five Hundred Girls Documented',
    '_W1A5251.jpg': 'Young Women Graduates — Education Works',
    '_W1A5259.jpg': 'Smiles of Achievement — Graduation Day, Northern Kenya',
    '_W1A5262.jpg': 'Uniform as Dignity — First Day in Secondary School',
    '_W1A5263.jpg': 'Book in Hands — Knowledge is Power',
    '_W1A5266.jpg': 'Stichting MOV Delegation Signing the Exhibition Launch Record',
    '_W1A5269.jpg': 'Conversations That Change Lives — Mentorship Moments',
    '_W1A5273.jpg': 'Community Gathering — Education Advocates and Parents',
    '_W1A5277.jpg': 'Looking Forward — The Next Generation of Leaders',
    '_W1A5279.jpg': 'The Journey Continues — Students on the Road to University',
    '_W1A5290.jpg': 'Exhibition Prints — Stories Told in Photographs',
    '_W1A5292.jpg': 'Breaking the Vicious Cycle — Photo-Book Open Pages',
    '_W1A5295.jpg': 'A Proud Moment — Parent and Child at the Exhibition',
    '_W1A5389.jpg': 'Photo Booth Joy — Students Celebrating Together',
    '_W1A5391.jpg': 'Photo Booth Portrait — She Is Rising from the North',
    '_W1A5401.jpg': 'Smiles and Sisterhood at the Book Launch',
    '_W1A5412.jpg': 'Community Celebrations at the Photo Booth',
    '_W1A5702.jpg': 'Hildah Kathure, MOV Foundation Founder & Team with the Book',
    '_W1A5704.jpg': 'Launch Celebration — Team & Community Under the Acacia',
    '_W1A5765.jpg': 'Hildah Kathure with Microphone & Team — Outdoor Celebration',
    '_W1A5767.jpg': 'MOV Foundation Leadership & Community Champions',
    '_W1A5769.jpg': 'Hildah Kathure and Education Partner — A Milestone Celebrated',
    '_W1A5772.jpg': 'Women Leaders of Northern Kenya — Education Works',
    '_W1A5810.jpg': 'Photo Booth Celebration Under the Northern Kenya Sky',
    '_W1A5811.jpg': 'Hildah Kathure & Education Champions with Photo Booth Frame',
    '_W1A5815.jpg': 'Hildah Kathure & Community Partner at the Exhibition',
    '_W1A5817.jpg': 'Closing Moments — Celebrating 15 Years of Transformation'
}

for i, f in enumerate(files, 1):
    num_match = re.search(r'(\d+)', f)
    num = int(num_match.group(1)) if num_match else 5200 + i
    
    # Determine category
    if 5360 <= num <= 5430:
        cat = 'photobooth'
    elif 5431 <= num <= 5699:
        cat = 'ceremony'
    elif num >= 5700:
        cat = 'portraits'
    else:
        cat = 'exhibition'
        
    caption = curated_captions.get(f, f"She Is Rising from the North — Exhibition Frame #{num}")
    
    photos.append({
        'id': f"photo-{num}",
        'src': f"assets/images/gallery/{f}",
        'caption': caption,
        'category': cat,
        'num': num
    })

print(f"Generated {len(photos)} total gallery items.")
with open('scratch/full_gallery_dataset.json', 'w', encoding='utf-8') as out_f:
    json.dump(photos, out_f, indent=2)
print("Saved scratch/full_gallery_dataset.json")
