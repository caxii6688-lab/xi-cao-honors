#!/usr/bin/env python3
"""Read-only checks for the static V1 preview. Python standard library only."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import hashlib, json, re
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
def require(condition,message):
    if not condition:raise SystemExit('FAIL: '+message)
class References(HTMLParser):
    def __init__(self):super().__init__();self.urls=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ('src','href'):
            if k in a:self.urls.append(a[k])

html=(ROOT/'index.html').read_text(encoding='utf-8')
parser=References();parser.feed(html)
js=(ROOT/'assets/js/content.js').read_text(encoding='utf-8')
match=re.fullmatch(r"'use strict';\s*//[^\n]*\nwindow\.XI_CAO_CONTENT = (.*?);\s*window\.XI_CAO_ASSETS = (.*);\s*",js,re.S)
require(match is not None,'content.js format')
data=json.loads(match.group(1));assets=json.loads(match.group(2))
records=data['records'];counts=Counter(r['category'] for r in records)
require(len(records)==15 and len({r['id'] for r in records})==15,'15 unique recognition records')
require(dict(counts)=={'national':2,'international':2,'municipal-regional':3,'university':2,'scholarships':3,'campus':3},'category totals')
scholarships=[r for r in records if r['category']=='scholarships']
require(len(scholarships)==3 and all(len(r['categories'])==5 for r in scholarships),'15 scholarship distinctions over 3 years')
pending=[r for r in records if r.get('evidenceStatus')=='pending']
require(len(pending)==1 and pending[0]['id']=='S03','only the new scholarship certificate is pending')
require(pending[0]['year']=='2025–26' and pending[0]['awardStatus']=='Confirmed' and not pending[0]['certificates'] and not pending[0].get('issued'),'confirmed 2025–2026 award has no invented certificate or issue date')
require(pending[0]['evidenceNote']=='Official certificate pending issuance. Supporting documentation will be added once available.','exact pending-issuance note')
require(pending[0]['categories']==[['Ideological & moral conduct','First class'],['Academic performance','Second class'],['Innovation','Second class'],['Sports & arts','Third class'],['Outstanding student','Second class']],'confirmed 2025–2026 scholarship categories and levels')
require({r['id'] for r in records}=={'N01','N02','I01','I02','M01','M02','M03','U01','U02','S01','S02','S03','H01','H02','H03'},'only approved recognition records; no individual sports event additions')
require(Counter(r['kind'] for r in data['research'])=={'published_journal':1,'accepted_conference':1},'separate research statuses')
require(all(r['prize']=='Successful Participant' for r in records if r['category']=='international'),'official MCM/ICM result labels')
certs=[c['asset'] for r in records for c in r['certificates']]
require(len(certs)==15 and all(c in assets for c in certs),'15 award-certificate references')
for p in data['projects'].values():
    for key,_ in p['gallery']:require(key in assets,'project gallery asset '+key)
for r in data['research']:require(r['certificate']['asset'] in assets,'research letter')

def check_path(value):
    if value.startswith('#'):
        require(value[1:] in parser.ids,'anchor '+value);return
    if value.startswith(('https://','mailto:','data:')):return
    require(not urlsplit(value).scheme,'unexpected URL scheme: '+value)
    require(not value.startswith('/'),'root-relative URL: '+value)
    path=(ROOT/unquote(urlsplit(value).path)).resolve()
    require(path.is_relative_to(ROOT),'path escapes project: '+value)
    require(path.is_file(),'missing file: '+value)
for url in parser.urls+list(assets.values()):check_path(url)
css=(ROOT/'assets/css/site.css').read_text(encoding='utf-8')
require('@import' not in css and '@font-face' not in css,'no undisclosed remote/font dependency')
require(all(u.strip(' \"\x27').startswith(('data:','#')) for u in re.findall(r'url\((.*?)\)',css,re.S)),'unexpected CSS resource URL')
for p in [ROOT/'index.html',ROOT/'assets/css/site.css',*sorted((ROOT/'assets/js').glob('*.js'))]:
    text=p.read_text(encoding='utf-8')
    require(not any(t in text for t in ['file://','localhost','127.0.0.1','/Users/','/private/','/tmp/','rawFilename','roleSource']),'machine-specific reference in '+str(p.relative_to(ROOT)))
require(not any(p.is_symlink() for p in ROOT.rglob('*')),'no symbolic links')
require((ROOT/'.nojekyll').is_file(),'.nojekyll included')
manifest=json.loads((ROOT/'ASSET_MANIFEST.json').read_text(encoding='utf-8'))
require(len(manifest['assets'])==28,'28 approved image assets')
for a in manifest['assets']:
    p=ROOT/a['path'];require(p.is_file(),'manifest file '+a['path'])
    require(hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],'checksum '+a['path'])
require(set(a['path'] for a in manifest['assets'])=={v.removeprefix('./') for v in assets.values()},'asset-map / manifest consistency')
require(not list((ROOT/'assets/evidence').glob('*.jpg')),'no original evidence JPEGs')
require(not any(k.startswith('senvix-') for k in assets),'uncleared SenviX assets absent')
require(not data['projects']['senvix']['gallery'],'uncleared SenviX gallery absent')
require(next(r for r in records if r['id']=='M03')['prize']=='Regional Third Prize','certificate-supported regional award')
require(all(assets[c].startswith('./assets/evidence/awards/') for c in certs),'owner-approved original award certificates only')
require(not list((ROOT/'assets/evidence/public').glob('cert-*')),'superseded redacted award copies absent')
require(set(p.name for p in (ROOT/'assets/evidence/public').iterdir() if p.is_file())=={'journal-letter.png','conference-letter.png'},'only protected research letters in public evidence directory')
require({str(p.relative_to(ROOT)) for p in (ROOT/'assets/evidence/awards').iterdir() if p.is_file()}=={assets[c].removeprefix('./') for c in certs},'no unrelated files in award evidence directory')
require(all(assets[r['certificate']['asset']].startswith('./assets/evidence/public/') for r in data['research']),'public research copies only')
require(not any(t in js for t in ['Abstract 77','printed page 79','North China Regional Third Prize','included in the official Book']),'unsupported claims absent')
for p in ROOT.rglob('*'):
    if '.git' in p.relative_to(ROOT).parts or not p.is_file():continue
    require(p.suffix.lower() not in {'.zip','.pdf','.docx','.doc','.pptx','.xlsx','.pem','.key'},'excluded private/source file: '+str(p.relative_to(ROOT)))
    require(not p.name.startswith('PRIVATE_'),'private handoff absent')
print('PASS: approved original award certificates, protected research letters, omitted SenviX images and corrected factual scope.')
print('PASS: 15 records; 3 scholarship years / 15 distinctions; 15 award certificates; 1 confirmed record with certificate pending.')
print('PASS: 2 protected research letters; 28 approved image assets.')
print('PASS: relative paths, local files, checksums, anchors, category totals and metadata exclusions.')
print('Publication/privacy approval and external-host availability require human review; this script does not publish.')
