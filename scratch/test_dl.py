import urllib.request

file_id = "17HSBPvecNeQsXX04AYQptgGSb-eJ4tRi"
urls_to_test = [
    f"https://drive.google.com/thumbnail?id={file_id}&sz=w1600",
    f"https://lh3.googleusercontent.com/d/{file_id}",
    f"https://drive.google.com/uc?id={file_id}&export=download"
]

for url in urls_to_test:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            print(f"URL: {url}")
            print(f"Status: {resp.status}, Content-Type: {resp.headers.get('Content-Type')}, Size: {len(data)} bytes")
            if len(data) > 1000 and 'image' in resp.headers.get('Content-Type', ''):
                with open("scratch/test_download.jpg", "wb") as f:
                    f.write(data)
                print("Successfully saved test_download.jpg!")
                break
    except Exception as e:
        print(f"Failed {url}: {e}")
