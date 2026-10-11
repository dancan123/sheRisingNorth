import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check all img src
srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
print(f'Total src tags: {len(srcs)}')
for s in srcs:
    exists = os.path.exists(s)
    print(f'  {s:75} -> exists: {exists}')
    if not exists:
        print(f'  FAILED: File does not exist: {s}')

# 2. Check for any drive or photos app links
drive_matches = re.findall(r'drive\.google|photos\.app', content)
print(f'Drive/Photos links in index.html: {len(drive_matches)}')

# 3. Check for Bank Details
print('Bank Details .jpeg in HTML:', 'Bank Details .jpeg' in content)
print('KCB Paybill 522533 in HTML:', '522533' in content)
print('KCB Till 8144533 in HTML:', '8144533' in content)
print('Account Name in HTML:', 'SHE RISES FROM THE NORTH MENTORSHIP' in content)

# 4. Check for Press Release text
print('Press Release in HTML:', 'Press Release for Immediate Publication' in content)
print('Dr. Zeinab quote in HTML:', 'The strategies I use to lead are often influenced' in content)
print('Kamila quote in HTML:', 'In our communities, livestock is life' in content)
print('Macline quote in HTML:', 'St. Mary’s Girls School' in content or "St. Mary" in content)
print('Zeituna quote in HTML:', 'My mother died of unknown sickness' in content)
print('Tour Nairobi in HTML:', 'Baraza Media Lab' in content)
print('Tour Isiolo in HTML:', 'Ministry of Education Offices' in content)
print('Tour Merti in HTML:', 'Merti Boarding School' in content)
