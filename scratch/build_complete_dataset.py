import os
import json
import re

print("=== Starting Full System Photo & Banking Update ===")

# ==============================================================================
# 1. BUILD THE COMPLETE PHOTO DATASET (315 PHOTOS)
# ==============================================================================

# A. Key Featured & Named Stories from Northern Kenya
featured_stories = [
    {
        "id": "rec-dr-zeinab",
        "src": "assets/images/Dr. Zeinab Gura - CEO Kenya University TRR Hospital Nairobi.jpg",
        "caption": "Dr. Zeinab Gura — CEO Kenyatta University Teaching, Referral & Research Hospital (Nairobi)",
        "category": "portraits",
        "tag": "Featured Leader"
    },
    {
        "id": "rec-kaltuma-amina",
        "src": "assets/images/Kaltuma Abdi and her Daughter Amina Abdi- One generation nurturing the dreams of the next.jpg",
        "caption": "Kaltuma Abdi & Daughter Amina Abdi — One Generation Nurturing the Dreams of the Next",
        "category": "portraits",
        "tag": "Generations"
    },
    {
        "id": "rec-kisima-writing",
        "src": "assets/images/A girl at Kisima - writing the future.jpg",
        "caption": "A Girl at Kisima — Writing the Future with Dignity and Determination",
        "category": "portraits",
        "tag": "Education"
    },
    {
        "id": "rec-amintu-gollo",
        "src": "assets/images/Amintu Gollo protects and serves determined that no girl facing violence should stand alone.jpg",
        "caption": "Amintu Gollo Protects and Serves — Determined that No Girl Facing Violence Stands Alone",
        "category": "portraits",
        "tag": "Public Service"
    },
    {
        "id": "rec-batula-fayo",
        "src": "assets/images/Batula Fayo a teacher at Kisima Primary School.jpg",
        "caption": "Batula Fayo — Teacher at Kisima Primary School, Isiolo County",
        "category": "portraits",
        "tag": "Educator"
    },
    {
        "id": "rec-isiolo-girls",
        "src": "assets/images/Sponsored Girls in Isiolo Girls - Ready to learn, lead and be seen.jpg",
        "caption": "Sponsored Girls at Isiolo Girls Secondary — Ready to Learn, Lead and Be Seen",
        "category": "documentary",
        "tag": "Scholars"
    },
    {
        "id": "rec-amina-jaldesa",
        "src": "assets/images/Amina Jaldesa 4.jpeg",
        "caption": "Amina Jaldesa — Community Leadership & Mentorship in Northern Kenya",
        "category": "portraits",
        "tag": "Mentor"
    },
    {
        "id": "rec-boke",
        "src": "assets/images/Boke 2.jpeg",
        "caption": "Boke — The Journey of Resilience, Courage and Transformation",
        "category": "portraits",
        "tag": "Portrait"
    },
    {
        "id": "rec-wa-class",
        "src": "assets/images/IMG-20230220-WA0064.jpg",
        "caption": "Classroom Mentorship Session — Empowering Northern Kenya Scholars",
        "category": "documentary",
        "tag": "Mentorship"
    },
    {
        "id": "rec-bank-details",
        "src": "assets/images/Bank Details .jpeg",
        "caption": "Official Banking & Till Slip — She Rises From The North Mentorship (KCB Bank & Till 8144533)",
        "category": "exhibition",
        "tag": "Banking Details"
    }
]

# B. Highlights from the Launch & Exhibition
highlights = [
    {
        "id": "hl-1",
        "src": "assets/images/photobooth_students.jpg",
        "caption": "#SheIsRisingFromTheNorth Photo Booth — Students & Teachers with the Book",
        "category": "photobooth",
        "tag": "Featured"
    },
    {
        "id": "hl-2",
        "src": "assets/images/students_reading.jpg",
        "caption": "Reading the Book — I.G.H.S. Students Exploring Their Stories",
        "category": "documentary",
        "tag": "Featured"
    },
    {
        "id": "hl-3",
        "src": "assets/images/students_walking.jpg",
        "caption": "The Journey of Becoming — Students in Uniform at the Launch",
        "category": "documentary",
        "tag": "Featured"
    },
    {
        "id": "hl-4",
        "src": "assets/images/exhibition_outdoor.jpg",
        "caption": "Outdoor Exhibition Under the Acacia — Photo Prints on Easels",
        "category": "exhibition",
        "tag": "Featured"
    },
    {
        "id": "hl-5",
        "src": "assets/images/classroom.jpg",
        "caption": "Inside the Classroom — Where Futures Are Built",
        "category": "documentary",
        "tag": "Featured"
    },
    {
        "id": "hl-6",
        "src": "assets/images/support_impact.jpg",
        "caption": "Education Changes Everything — Support the Girls of Northern Kenya",
        "category": "documentary",
        "tag": "Featured"
    }
]

# C. MDV Documentary Series
mdv_captions = {
    'MDV-2.jpg': 'On the Grazing Fields — Dawn in Northern Kenya Pastoralist Lands',
    'MDV-3.jpg': 'Tending Livestock — Early Morning Responsibilities in Isiolo',
    'MDV-4.jpg': 'The Journey Begins — Crossing the Savanna Towards School',
    'MDV-5.jpg': 'Water and Resilience — Everyday Realities of Pastoralist Life',
    'MDV-6.jpg': 'Heritage and Living Culture — Communities Across Northern Kenya',
    'MDV-10.jpg': 'Gathering at the Manyatta — Community Elders and Youth Dialogue',
    'MDV-11.jpg': 'Generational Wisdom — Elders Supporting Girls\' Education Journeys',
    'MDV-13.jpg': 'Dusk on the Northern Plains — Samburu & Isiolo Landscapes',
    'MDV-14.jpg': 'The Long Walk to School — Breaking Distance and Cultural Barriers',
    'MDV-16.jpg': 'Classroom in Session — Dedicated Students Focused on Learning',
    'MDV-17.jpg': 'Writing Dreams — A Desk and Notebook of One\'s Own',
    'MDV-18.jpg': 'Peer Learning — Study Circles Under the Trees',
    'MDV-20.jpg': 'Morning Assembly — Standing Proud in Clean School Uniforms',
    'MDV-22.jpg': 'Primary School Joy — Friends and Shared Academic Aspirations',
    'MDV-25.jpg': 'Mentorship in Action — Alumnae Inspiring the Next Generation',
    'MDV-27.jpg': 'Library Hours — Discovering New Worlds Through Books',
    'MDV-29.jpg': 'Science & Curiosity — Exploring Biology in the School Lab',
    'MDV-30.jpg': 'Breaking Barriers — From Traditional Grazing to High School Success',
    'MDV-31.jpg': 'Sisterhood & Strength — Young Women Supporting Each Other',
    'MDV-33.jpg': 'Graduation Aspirations — Preparing Diligently for National Examinations',
    'MDV-35.jpg': 'Educators Who Care — Teachers Guiding Students in Isiolo',
    'MDV-39.jpg': 'Dignity in Education — The Transformative Power of Scholarships',
    'MDV-40.jpg': 'Community Pride — Parents Celebrating Academic Progress',
    'MDV-42.jpg': 'Voices of Courage — Speaking Up in Classrooms and Community Halls',
    'MDV-43.jpg': 'Future Leaders — Young Northern Kenyan Women Stepping Forward',
    'MDV-45.jpg': 'The Horizon of Possibility — Northern Kenya Savanna Sunset'
}

mdv_photos = []
for f, cap in mdv_captions.items():
    if os.path.exists(os.path.join('assets/images', f)):
        mdv_photos.append({
            'id': f'mdv-{f.replace(".jpg","")}',
            'src': f'assets/images/{f}',
            'caption': cap,
            'category': 'documentary',
            'tag': 'Documentary'
        })

# D. 0O1A Series
prefix_0O1A_captions = {
    '0O1A1925.jpg': 'On the Grazing Fields — Dawn Light in Isiolo County',
    '0O1A1927.jpg': 'Portrait of Grace — Young Pastoralist Girl at Sunrise',
    '0O1A1990.jpg': 'Pastoralist Traditions — Samburu Beadwork and Living Culture',
    '0O1A2340.jpg': 'Daily Responsibilities — Fetching Water Across the Savanna',
    '0O1A8106.jpg': 'Arriving at Secondary School — The First Step to Freedom',
    '0O1A8163.jpg': 'In the Classroom — Deep Focus and Concentration',
    '0O1A8203.jpg': 'Sharing Coursework — Students Collaborating at Isiolo Girls',
    '0O1A8311.jpg': 'Portrait of Determination — An Aspiring Medical Doctor',
    '0O1A8318.jpg': 'Classroom Discussion — Finding Confidence and Purpose',
    '0O1A8340.jpg': 'Courtyard Gathering — Girls Between Lessons in School'
}

prefix_0O1A_photos = []
for f, cap in prefix_0O1A_captions.items():
    if os.path.exists(os.path.join('assets/images', f)):
        cat = 'portraits' if 'Portrait' in cap else 'documentary'
        prefix_0O1A_photos.append({
            'id': f'0o1a-{f.replace(".jpg","")}',
            'src': f'assets/images/{f}',
            'caption': cap,
            'category': cat,
            'tag': 'Field Story'
        })

# E. _32A Series
prefix_32A_captions = {
    '_32A8149.jpg': 'Professional Leadership — Women Shaping Northern Kenya\'s Future',
    '_32A8150.jpg': 'Mentorship in Practice — Guiding Students Towards University',
    '_32A8158.jpg': 'Community Advocacy — Standing Up for Every Girl\'s Right to Learn'
}

prefix_32A_photos = []
for f, cap in prefix_32A_captions.items():
    if os.path.exists(os.path.join('assets/images', f)):
        prefix_32A_photos.append({
            'id': f'32a-{f.replace(".jpg","")}',
            'src': f'assets/images/{f}',
            'caption': cap,
            'category': 'portraits',
            'tag': 'Leaders'
        })

# F. _W1A Root Series
prefix_W1A_root_captions = {
    '_W1A0004.jpg': 'Morning Light on the School Quadrangle — Northern Kenya',
    '_W1A0034.jpg': 'Dignity and Hope — A Student\'s Inspiring Smile',
    '_W1A0072.jpg': 'Science Laboratory — Hands-on STEM Discovery',
    '_W1A0097.jpg': 'Boarding School Community — Safe Spaces for Girls to Excel',
    '_W1A0120.jpg': 'Classroom Discussion — Active Learning and Discussion',
    '_W1A0126.jpg': 'Portrait of an Aspiring Engineer — Isiolo Girls High School',
    '_W1A0154.jpg': 'Study Hall Focus — Dedicated Hours Before National Exams',
    '_W1A0184.jpg': 'Eyes on the Horizon — Focused on Achieving Top Grades',
    '_W1A0212.jpg': 'Study Group — Supporting Each Other Towards Graduation',
    '_W1A0234.jpg': 'School Grounds — Friendship and High Ambition',
    '_W1A0290.jpg': 'Sports and Leadership — Health, Teamwork and Confidence',
    '_W1A0316.jpg': 'Engaging with the Curriculum — Curiosity and Learning',
    '_W1A0351.jpg': 'Teacher Mentoring Students — After-Class Academic Guidance',
    '_W1A0363.jpg': 'Portrait of Hope — Student in Uniform at Isiolo Girls',
    '_W1A0372.jpg': 'School Assembly — Hundreds of Bright Futures in Progress',
    '_W1A0391.jpg': 'Joy and Resilience — Overcoming Challenges Through Education',
    '_W1A0397.jpg': 'Writing in the Notebook — An Archive of Education',
    '_W1A0410.jpg': 'Portrait of an Achiever — High School Graduate',
    '_W1A0413.jpg': 'Mentorship Session in the Hall — Inspiring the Whole Cohort',
    '_W1A0417.jpg': 'Quiet Reflection with the Book — She Is Rising from the North',
    '_W1A0469.jpg': 'Ready for the World — Final Year Students in Isiolo',
    '_W1A8936.jpg': 'Golden Hour Across the Pastoralist Plains of Northern Kenya',
    '_W1A8986.jpg': 'The Road Between Manyattas — The Vast Northern Frontier',
    '_W1A9043.jpg': 'Livestock and Livelihoods — Pastoralist Realities in Isiolo',
    '_W1A9701.jpg': 'Samburu Traditional Attire — Celebrating Heritage and Dignity',
    '_W1A9733.jpg': 'A Mother\'s Pride — Supporting Her Daughter\'s Journey',
    '_W1A9739.jpg': 'Generational Shift — From Livestock Grazing to Higher Education',
    '_W1A9747.jpg': 'Young Pastoralist Girl Looking Confidently Toward the Future',
    '_W1A9750.jpg': 'Community Elders Meeting Under the Acacia Tree',
    '_W1A9784.jpg': 'A Warm Smile on the Plains — Dignity in Every Step',
    '_W1A9801.jpg': 'Northern Kenya Savanna — Where the Transformative Story Begins',
    '_W1A9807.jpg': 'Livestock at Golden Hour — Pastoralist Heartland',
    '_W1A9829.jpg': 'Portrait of Resilience — A Young Samburu Woman'
}

prefix_W1A_photos = []
for f, cap in prefix_W1A_root_captions.items():
    if os.path.exists(os.path.join('assets/images', f)):
        cat = 'portraits' if 'Portrait' in cap else 'documentary'
        prefix_W1A_photos.append({
            'id': f'w1aroot-{f.replace(".jpg","")}',
            'src': f'assets/images/{f}',
            'caption': cap,
            'category': cat,
            'tag': 'Isiolo'
        })

# G. Existing Launch & Gallery Collection (227 images in assets/images/gallery/)
gallery_dir = 'assets/images/gallery'
gallery_files = sorted([f for f in os.listdir(gallery_dir) if f.startswith('_W1A') and f.endswith('.jpg')])

curated_gallery_captions = {
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

gallery_photos = []
for f in gallery_files:
    num_match = re.search(r'_W1A(\d+)\.jpg', f)
    num = int(num_match.group(1)) if num_match else 0

    if f in curated_gallery_captions:
        cap = curated_gallery_captions[f]
    elif 5380 <= num <= 5420 or 5800 <= num <= 5815:
        cap = f"Photo Booth Celebration — Students & Guests Frame #{num}"
    elif 5700 <= num <= 5775:
        cap = f"Exhibition Launch Ceremony & Speeches — Frame #{num}"
    else:
        cap = f"Exhibition Frame #{num} — She Is Rising from the North"

    if 5380 <= num <= 5420 or 5800 <= num <= 5815:
        cat = 'photobooth'
    elif 5700 <= num <= 5775:
        cat = 'ceremony'
    elif 5212 <= num <= 5300:
        cat = 'exhibition'
    else:
        cat = 'exhibition'

    gallery_photos.append({
        'id': f'gal-{num}',
        'src': f'assets/images/gallery/{f}',
        'caption': cap,
        'category': cat,
        'num': num
    })

# COMBINE ALL: featured stories first, then highlights, then recent series, then launch gallery
all_photos_combined = (
    featured_stories +
    highlights +
    mdv_photos +
    prefix_0O1A_photos +
    prefix_32A_photos +
    prefix_W1A_photos +
    gallery_photos
)

print(f"Total photos assembled: {len(all_photos_combined)}")

# Compute Category Counts
cat_counts = {}
for p in all_photos_combined:
    c = p.get('category', 'all')
    cat_counts[c] = cat_counts.get(c, 0) + 1

print("Category breakdown:", cat_counts)

# Save to scratch dataset
with open('scratch/full_gallery_dataset_v2.json', 'w', encoding='utf-8') as f:
    json.dump(all_photos_combined, f, indent=2)

print("Saved scratch/full_gallery_dataset_v2.json")
