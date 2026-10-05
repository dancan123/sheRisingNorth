import urllib.request
import re
import json
import os

url = 'https://drive.google.com/drive/folders/1oB0c54PgdyChv9M84ZahrArc8MbuqXbq'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        print(f"HTML length: {len(html)}")
        
        # Save html to examine structure
        with open('scratch/drive_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved drive_page.html")
except Exception as e:
    print(f"Error fetching URL: {e}")
