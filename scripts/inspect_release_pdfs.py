#!/usr/bin/env python3
"""Read public GitHub release PDF assets and report their actual page counts."""
import argparse, hashlib, io, json, urllib.request
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('tag')
args = parser.parse_args()
headers = {'User-Agent': 'ruogu-books-editorial-check'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()
release = json.loads(get(f'https://api.github.com/repos/njxshr/ruogu-books/releases/tags/{args.tag}'))
report = []
for asset in release['assets']:
    if not asset['name'].endswith('.pdf'):
        continue
    payload = get(asset['browser_download_url'])
    report.append({'name': asset['name'], 'pages': len(PdfReader(io.BytesIO(payload)).pages), 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest(), 'url': asset['browser_download_url']})
print(json.dumps({'tag': args.tag, 'pdfs': report}, ensure_ascii=False, indent=2))
