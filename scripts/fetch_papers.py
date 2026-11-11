"""Fetch primary paper metadata and retain hashed local reading copies."""
import concurrent.futures
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import urlopen

IDS = ['2610.29121','2610.05701','2610.18083','2610.20431','2610.22791','2610.10310','2610.22192','2610.22740']
ROOT=Path(__file__).resolve().parents[1]


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.meta={}
    def handle_data(self,data):
        self.parts.append(data)
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if tag=='meta' and data.get('name','').startswith('citation_'):
            self.meta.setdefault(data['name'],[]).append(data.get('content'))


def fetch(identifier):
    result={'arxiv_id':identifier,'sources':[]}
    for kind in ['abs','html']:
        url=f'https://arxiv.org/{kind}/{identifier}'
        with urlopen(url,timeout=60) as response:
            body=response.read(); resolved=response.url
        reader=Reader(); reader.feed(body.decode())
        target=ROOT/'.local/papers'/f'{identifier}-{kind}.txt';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(' '.join(reader.parts))
        result['sources'].append({'url':url,'resolved_url':resolved,'sha256':hashlib.sha256(body).hexdigest(),'metadata':reader.meta})
    return result


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    result=list(pool.map(fetch,IDS))
(ROOT/'docs/references/course-papers.json').write_text(json.dumps(result,indent=2)+'\n')
for item in result:
    print(item['arxiv_id'],item['sources'][0]['metadata'].get('citation_title'))
