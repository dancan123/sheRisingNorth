import urllib.request
import urllib.parse
import json

KEY = 'AIzaSyAWGrfCCr7albM3lmCc937gx4uIphbpeKQ'
FOLDER_ID = '1oB0c54PgdyChv9M84ZahrArc8MbuqXbq'

all_files = []
page_token = None

while True:
    params = {
        'q': f"'{FOLDER_ID}' in parents and trashed = false",
        'pageSize': 100,
        'fields': 'nextPageToken, files(id, name, mimeType, size)',
        'key': KEY
    }
    if page_token:
        params['pageToken'] = page_token
    url = 'https://www.googleapis.com/drive/v3/files?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        files = data.get('files', [])
        all_files.extend(files)
        page_token = data.get('nextPageToken')
        print(f"Fetched {len(files)} files, cumulative: {len(all_files)}")
        if not page_token:
            break

print(f"\nTotal files in folder: {len(all_files)}")
with open('scratch/all_229_drive_files.json', 'w', encoding='utf-8') as f:
    json.dump(all_files, f, indent=2)
print("Saved to scratch/all_229_drive_files.json")
