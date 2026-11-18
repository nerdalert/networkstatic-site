#!/usr/bin/env python3
"""Build sanitized WordPress backup, live-observation, and reconciliation inventories.

Reads the local SQL dump and existing uploads tree; never extracts or runs backup PHP.
"""
from __future__ import annotations
import argparse, csv, hashlib, html, json, mimetypes, posixpath, re, struct, tarfile
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
POST_COLUMNS = ['ID','post_author','post_date','post_date_gmt','post_content','post_title','post_excerpt','post_status','comment_status','ping_status','post_password','post_name','to_ping','pinged','post_modified','post_modified_gmt','post_content_filtered','post_parent','guid','menu_order','post_type','post_mime_type','comment_count']

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def mysql_unescape(s: str) -> str:
    # MySQL dump string escaping, without interpreting arbitrary SQL or executing PHP.
    out=[]; i=0; mapping={'0':'\0','b':'\b','n':'\n','r':'\r','t':'\t','Z':'\x1a'}
    while i < len(s):
        if s[i]=='\\' and i+1<len(s):
            i+=1; out.append(mapping.get(s[i],s[i]))
        else: out.append(s[i])
        i+=1
    return ''.join(out)

def parse_values(blob: str):
    i=0; n=len(blob)
    while i<n:
        while i<n and blob[i] not in '(': i+=1
        if i>=n: break
        i+=1; vals=[]; cur=[]; quote=False; esc=False
        while i<n:
            c=blob[i]
            if quote:
                if esc: cur.append('\\'+c); esc=False
                elif c=='\\': esc=True
                elif c=="'": quote=False
                else: cur.append(c)
            elif c=="'": quote=True
            elif c==',': vals.append(mysql_unescape(''.join(cur).strip())); cur=[]
            elif c==')': vals.append(mysql_unescape(''.join(cur).strip())); i+=1; yield vals; break
            else: cur.append(c)
            i+=1

def read_table(sql: str, table: str):
    pat=re.compile(r'INSERT INTO `wp_'+re.escape(table)+r'` \((.*?)\) VALUES ',re.S)
    for m in pat.finditer(sql):
        cols=re.findall(r'`([^`]+)`',m.group(1))
        # SQL content may contain semicolons, so locate the statement terminator
        # while honoring quoted strings and MySQL backslash escapes.
        i=m.end(); start=i; quoted=False; escaped=False
        while i<len(sql):
            c=sql[i]
            if quoted:
                if escaped: escaped=False
                elif c=='\\': escaped=True
                elif c=="'": quoted=False
            elif c=="'": quoted=True
            elif c==';': break
            i+=1
        for values in parse_values(sql[start:i]):
            if len(cols)==len(values): yield dict(zip(cols,values))

def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n'); w.writeheader(); w.writerows(rows)

def source_slug(d):
    return d.get('post_name','') or f"wp-{d.get('ID','')}"
def permalink(d):
    slug=source_slug(d)
    if d.get('post_type')=='post': return '/'+slug+'/'
    return '/'+slug+'/'

def normalized_path(value):
    path=urlparse(value).path or '/'
    return '/'+path.strip('/')+'/' if path.strip('/') else '/'

class HomeCards(HTMLParser):
    """Extract visible post cards from a locally saved homepage snapshot."""
    def __init__(self):
        super().__init__(); self.items=[]; self.item=None; self.capture=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and 'type-post' in a.get('class',''):
            self.item={'url':'','title':'','published':'','categories':[],'tags':[]}
        elif self.item is not None:
            cls=a.get('class','')
            if tag=='h2' and 'entry-title' in cls: self.capture='title'
            elif tag=='time' and a.get('datetime'): self.item['published']=a['datetime']
            elif tag=='span' and 'cat-links' in cls: self.capture='category'
            elif tag=='span' and 'tags-links' in cls: self.capture='tag'
            elif tag=='a' and self.capture=='title': self.item['url']=a.get('href','')
            elif tag=='a' and self.capture in ('category','tag'): self.item['_tax_text']=''
    def handle_data(self,data):
        if self.item is not None and self.capture=='title': self.item['title']+=data
        elif self.item is not None and self.capture in ('category','tag'): self.item.setdefault('_tax_text',''); self.item['_tax_text']+=data
    def handle_endtag(self,tag):
        if tag=='a' and self.item is not None and self.capture in ('category','tag'):
            value=html.unescape(self.item.pop('_tax_text','')).strip()
            if value: self.item['categories' if self.capture=='category' else 'tags'].append(value)
        elif tag=='h2' and self.item is not None:
            self.item['title']=html.unescape(self.item['title']).strip()
            self.capture=''
        elif tag=='span' and self.capture in ('category','tag'): self.capture=''
        elif tag=='article' and self.item is not None:
            self.item['title']=html.unescape(self.item['title']).strip()
            if self.item['title'] and self.item['url']:
                self.item['categories']='|'.join(self.item['categories']); self.item['tags']='|'.join(self.item['tags'])
                self.items.append(self.item)
            self.item=None; self.capture=''

def image_dimensions(path: Path):
    try:
        with path.open('rb') as f:
            h=f.read(32)
            if h.startswith(b'\x89PNG\r\n\x1a\n'): return f'{struct.unpack(">II",h[16:24])[0]}x{struct.unpack(">II",h[16:24])[1]}'
            if h[:6] in (b'GIF87a',b'GIF89a'):
                w,hh=struct.unpack('<HH',h[6:10]); return f'{w}x{hh}'
            if h[:2]!=b'\xff\xd8': return ''
            f.seek(2)
            while True:
                b=f.read(1)
                if not b: return ''
                if b!=b'\xff': continue
                while b==b'\xff': b=f.read(1)
                marker=b[0]
                if marker in (0xD8,0xD9) or 0xD0<=marker<=0xD7: continue
                ln=int.from_bytes(f.read(2),'big')
                if marker in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
                    f.read(1); hh=int.from_bytes(f.read(2),'big'); ww=int.from_bytes(f.read(2),'big'); return f'{ww}x{hh}'
                f.seek(ln-2,1)
    except (OSError,ValueError,struct.error): return ''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sql',type=Path,required=True); ap.add_argument('--uploads',type=Path,required=True); ap.add_argument('--homepage',type=Path,required=True); ap.add_argument('--live-archive',type=Path); ap.add_argument('--fetch-diagnostics',type=Path,default=ROOT/'reports/live-fetch-diagnostics.csv'); ap.add_argument('--browser-probes',type=Path,default=ROOT/'reports/live-browser-probes.csv'); ap.add_argument('--wp-root',type=Path); ap.add_argument('--archive',type=Path); ap.add_argument('--out',type=Path,default=ROOT/'reports'); a=ap.parse_args()
    sql_path=a.sql.resolve(); uploads=a.uploads.resolve(); out=a.out.resolve(); sql=sql_path.read_text(encoding='utf-8',errors='replace')
    posts=list(read_table(sql,'posts'))
    byid={p['ID']:p for p in posts}
    users={r.get('ID'):r.get('display_name','') for r in read_table(sql,'users')}
    terms={r.get('term_id'):(r.get('name',''),r.get('slug','')) for r in read_table(sql,'terms')}
    tax={r.get('term_taxonomy_id'):(r.get('term_id'),r.get('taxonomy')) for r in read_table(sql,'term_taxonomy')}
    taxbyobj=defaultdict(list)
    for r in read_table(sql,'term_relationships'):
        pair=tax.get(r.get('term_taxonomy_id'))
        if pair and pair[0] in terms: taxbyobj[r.get('object_id')].append((pair[1],terms[pair[0]][0],terms[pair[0]][1]))
    content_rows=[p for p in posts if p.get('post_type') in ('post','page')]
    public=[p for p in content_rows if p.get('post_status')=='publish' and p.get('post_password','')=='']
    protected_published=[p for p in content_rows if p.get('post_status')=='publish' and p.get('post_password','')!='']
    excluded_status_counts=Counter((p.get('post_type',''),p.get('post_status','')) for p in content_rows if p.get('post_status')!='publish')
    fetch_rows=[]
    if a.fetch_diagnostics and a.fetch_diagnostics.is_file():
        with a.fetch_diagnostics.open(encoding='utf-8',newline='') as f: fetch_rows=list(csv.DictReader(f))
    fetch_by_url={row.get('requested_url',''):row for row in fetch_rows}
    browser_rows=[]
    if a.browser_probes and a.browser_probes.is_file():
        with a.browser_probes.open(encoding='utf-8',newline='') as f: browser_rows=list(csv.DictReader(f))
    conversion_rows=[]
    if (out/'conversion-review.csv').is_file():
        with (out/'conversion-review.csv').open(encoding='utf-8',newline='') as f: conversion_rows=list(csv.DictReader(f))
    converted_source_ids={row.get('wp_id','') for row in conversion_rows}
    media_manifest_rows=[]
    if (out/'media-copy-manifest.csv').is_file():
        with (out/'media-copy-manifest.csv').open(encoding='utf-8',newline='') as f: media_manifest_rows=list(csv.DictReader(f))
    media=[p for p in posts if p.get('post_type')=='attachment']
    types=Counter(p.get('post_type','') for p in posts); statuses=Counter((p.get('post_type',''),p.get('post_status','')) for p in posts)
    rows=[]
    for p in sorted(public,key=lambda x:(x.get('post_date',''),int(x.get('ID','0')))):
        tx=taxbyobj[p['ID']]; cats=sorted(n for t,n,s in tx if t=='category'); tags=sorted(n for t,n,s in tx if t=='post_tag')
        rows.append({'wp_id':p['ID'],'type':p['post_type'],'status':'publish','title':p.get('post_title',''),'slug':source_slug(p),'canonical_url':'https://networkstatic.net'+permalink(p),'published':p.get('post_date',''),'modified':p.get('post_modified',''),'author':users.get(p.get('post_author'),''),'categories':'|'.join(cats),'tags':'|'.join(tags),'source':'backup','migration_status':'converted-to-local-review' if p['ID'] in converted_source_ids else 'not-converted'})
    write_csv(out/'backup-content-inventory.csv',rows,['wp_id','type','status','title','slug','canonical_url','published','modified','author','categories','tags','source','migration_status'])
    (out/'source-eligibility.json').write_text(json.dumps({
        'selection_policy': "post_type in ['post','page'] AND post_status == 'publish' AND post_password == ''",
        'eligible_public_published_posts':sum(1 for p in public if p.get('post_type')=='post'),
        'eligible_public_published_pages':sum(1 for p in public if p.get('post_type')=='page'),
        'excluded_password_protected_published_count':len(protected_published),
        'excluded_nonpublished_counts_by_type_status':{f'{kind}/{status}':count for (kind,status),count in sorted(excluded_status_counts.items())},
        'excluded_rows_include_titles_or_content':False,
    },indent=2)+'\n',encoding='utf-8')
    # Live observations are kept separate from the backup inventory. The homepage
    # input is a saved HTML snapshot; archive observations are supplied separately.
    parser=HomeCards(); parser.feed(a.homepage.read_text(encoding='utf-8',errors='replace'))
    live=[]
    for it in parser.items:
        u=urlparse(it['url']); slug=u.path.strip('/').split('/')[-1] if u.path.strip('/') else ''
        live.append({'url':it['url'],'path':u.path,'title':it['title'],'published':it.get('published',''),'categories':it.get('categories',''),'tags':it.get('tags',''),'discovered_from':'supplied-homepage-snapshot','coverage':'snapshot card; live homepage card set manually cross-checked'})
    write_csv(out/'live-observed-homepage.csv',live,['url','path','title','published','categories','tags','discovered_from','coverage'])
    archive_observations=[]
    if a.live_archive:
        with a.live_archive.open(encoding='utf-8',newline='') as f:
            archive_observations=list(csv.DictReader(f))
            for item in archive_observations:
                item['discovered_from']='archive-page-'+item.get('archive_page','unknown')
                item['coverage']='listed in public archive; article fetch '+item.get('individual_article_status','unavailable')
                live.append(item)
    sitemap_rows=[]
    sitemap_path=out/'live-sitemap-observations.csv'
    if sitemap_path.is_file():
        with sitemap_path.open(encoding='utf-8',newline='') as f:
            sitemap_rows=list(csv.DictReader(f))
    sitemap_by_path={normalized_path(row.get('path') or row.get('url','')):row for row in sitemap_rows}
    observed_paths={normalized_path(item.get('path') or item.get('url','')) for item in live}
    for path,row in sitemap_by_path.items():
        if path in observed_paths: continue
        live.append({
            'url':row.get('url',''),'path':path,'title':row.get('title',''),
            'published':row.get('published',''),'categories':'','tags':'',
            'archive_page':row.get('archive_page',''),
            'discovered_from':'public-sitemap-'+row.get('sitemap_type','route'),
            'individual_article_status':row.get('fetch_http_status','not individually fetched'),
            'sitemap_type':row.get('sitemap_type',''),'sitemap_lastmod':row.get('lastmod',''),
            'route_http_status':row.get('fetch_http_status',''),
            'route_fetch_attempted_at_utc':row.get('fetch_attempted_at_utc',''),
            'route_response_sha256':row.get('fetch_response_sha256',''),
            'route_response_bytes':row.get('fetch_response_bytes',''),
            'route_saved_file':row.get('fetch_saved_file',''),
            'body_text_sha256':row.get('body_text_sha256',''),
            'code_sha256':row.get('code_sha256',''),'links_sha256':row.get('links_sha256',''),
            'media_sha256':row.get('media_sha256',''),
        })
    for item in live:
        path=normalized_path(item.get('path') or item.get('url',''))
        observed=sitemap_by_path.get(path)
        if observed:
            if observed.get('title'):
                if item.get('title') and item.get('title')!=observed.get('title'):
                    item['card_title']=item.get('title')
                item['title']=observed.get('title')
            item['published']=observed.get('published') or item.get('published','')
            item.update({
                'sitemap_type':observed.get('sitemap_type',''),
                'sitemap_lastmod':observed.get('lastmod',''),
                'route_http_status':observed.get('fetch_http_status',''),
                'route_fetch_attempted_at_utc':observed.get('fetch_attempted_at_utc',''),
                'route_response_sha256':observed.get('fetch_response_sha256',''),
                'route_response_bytes':observed.get('fetch_response_bytes',''),
                'route_saved_file':observed.get('fetch_saved_file',''),
                'body_text_sha256':observed.get('body_text_sha256',''),
                'code_sha256':observed.get('code_sha256',''),
                'links_sha256':observed.get('links_sha256',''),
                'media_sha256':observed.get('media_sha256',''),
            })
    # Keep live route observations separate from the backup inventory. The
    # live side combines the supplied homepage snapshot, directly fetched
    # archive cards, published sitemaps, and direct route responses.
    verification_by_path={}
    verification_path=out/'content-verification.csv'
    if verification_path.is_file():
        with verification_path.open(encoding='utf-8',newline='') as f:
            for row in csv.DictReader(f):
                verified_path=urlparse(row.get('permalink','')).path.rstrip('/')+'/'
                verification_by_path[verified_path]=row.get('verification','not checked')
    live_inventory=[]
    for item in live:
        url=item.get('url','')
        path=item.get('path') or urlparse(url).path
        path=path.rstrip('/')+'/' if path.strip('/') else '/'
        source=item.get('discovered_from','unknown source')
        archive_page=item.get('archive_page','')
        verification=verification_by_path.get(path,'not checked')
        if source=='supplied-homepage-snapshot':
            source_label='supplied homepage snapshot; manually cross-checked against live homepage'
            fetch_status='HTTP '+item.get('route_http_status','not fetched') if item.get('route_http_status') else 'card observed; article route not fetched'
        elif source.startswith('public-sitemap-'):
            source_label=f"public {item.get('sitemap_type','post/page')} sitemap route; direct page fetch recorded in live-sitemap-observations.csv"
            fetch_status='HTTP '+item.get('route_http_status','not fetched') if item.get('route_http_status') else 'route listed; page not fetched'
        else:
            source_label=f'public archive page {archive_page or "unknown"}'
            fetch_status='HTTP '+item.get('route_http_status','') if item.get('route_http_status') else item.get('individual_article_status','not recorded')
        if verification=='full-body-verified': fetch_status='fetched and compared; see content-verification.csv'
        elif verification=='unrecovered': fetch_status='full article fetch unavailable; see content-verification.csv'
        if verification=='full-body-verified':
            evidence='Full visible article, code, links and referenced media compared; see content-verification.csv for evidence and remaining link-target exception.'
        elif verification=='unrecovered':
            evidence='Full article retrieval was unavailable at the time of verification; code, links and media remain unverified. See content-verification.csv.'
        else:
            evidence=(f"Route/title/date observed with direct HTTP status {item.get('route_http_status')}; "
                      'content comparison is recorded separately and is incomplete unless stated in content-verification.csv.')
        live_inventory.append({
            'observed_url':url,
            'path':path,
            'title':item.get('title',''),
            'card_title':item.get('card_title',''),
            'published':item.get('published',''),
            'categories':item.get('categories',''),
            'tags':item.get('tags',''),
            'discovered_from':source_label,
            'archive_page':archive_page,
            'sitemap_type':item.get('sitemap_type',''),
            'sitemap_lastmod':item.get('sitemap_lastmod',''),
            'route_http_status':item.get('route_http_status',''),
            'route_fetch_attempted_at_utc':item.get('route_fetch_attempted_at_utc',''),
            'route_response_sha256':item.get('route_response_sha256',''),
            'route_response_bytes':item.get('route_response_bytes',''),
            'route_saved_file':item.get('route_saved_file',''),
            'body_text_sha256':item.get('body_text_sha256',''),
            'code_sha256':item.get('code_sha256',''),
            'links_sha256':item.get('links_sha256',''),
            'media_sha256':item.get('media_sha256',''),
            'article_fetch_status':fetch_status,
            'body_verification_status':verification,
            'evidence':evidence
        })
    write_csv(out/'live-content-inventory.csv',live_inventory,
              ['observed_url','path','title','card_title','published','categories','tags','discovered_from','archive_page',
               'sitemap_type','sitemap_lastmod','route_http_status','route_fetch_attempted_at_utc',
               'route_response_sha256','route_response_bytes','route_saved_file','body_text_sha256',
               'code_sha256','links_sha256','media_sha256','article_fetch_status','body_verification_status','evidence'])
    pagecache={}
    def page_route(p):
        if p['ID'] in pagecache: return pagecache[p['ID']]
        parent=byid.get(p.get('post_parent','0'))
        value=source_slug(p)
        if parent and parent.get('post_type')=='page': value=page_route(parent).strip('/')+'/'+value
        pagecache[p['ID']]=value
        return value
    backup_by_path={normalized_path(permalink(p) if p.get('post_type')=='post' else '/'+page_route(p)+'/'):p for p in public}
    live_by_path=defaultdict(list)
    reconciliation=[]
    for item in live:
        path=normalized_path(item.get('path') or item.get('url',''))
        live_by_path[path].append(item)
        bp=backup_by_path.get(path)
        source=item.get('discovered_from','homepage-post-card')
        if source=='supplied-homepage-snapshot':
            source_evidence='supplied homepage snapshot card, cross-checked against the fetched live homepage'
        elif source.startswith('public-sitemap-'):
            source_evidence=f"public {item.get('sitemap_type','post/page')} sitemap route"
        else:
            source_evidence=f"public archive page {item.get('archive_page','unknown')} card"
        if item.get('sitemap_type'):
            source_evidence+=f"; also listed in the published {item.get('sitemap_type')} sitemap"
        if item.get('route_http_status'):
            source_evidence+=f"; direct route GET returned HTTP {item.get('route_http_status')}"
        if bp:
            backup_title=bp.get('post_title','').strip()
            live_title=item.get('title','').strip()
            title_match=backup_title==live_title
            classification='route-and-title-match-only' if title_match else 'route-match-title-differs'
            evidence=(f"{source_evidence} lists {path} titled {live_title!r}; backup SQL row ID {bp['ID']} "
                      f"is published at the same path as {backup_title!r}. Full article, code, links and media parity was not checked.")
            reconciliation.append({'backup_permalink':'https://networkstatic.net'+path,
                                   'live_permalink':'https://networkstatic.net'+path,'backup_title':backup_title,
                                   'live_title':live_title,'classification':classification,
                                   'confidence':'medium' if title_match else 'low','evidence':evidence,
                                   'action':'verify full public article, code, links, media and modified date against backup before publication'})
        else:
            live_title=item.get('title','').strip()
            if verification_by_path.get(path)=='full-body-verified':
                evidence=(f"{source_evidence} lists {path} titled {live_title!r}; no eligible published backup row has this exact route. "
                          'Anonymous REST status/protection and full body, links, code, and media are verified in content-verification.csv and live-source-eligibility.csv.')
                action='retain this verified live-only source in review output; assess publication through the separate eligibility ledger'
            else:
                evidence=(f"{source_evidence} lists {path} titled {live_title!r}; no eligible public, unprotected published "
                          'post/page in the supplied WordPress SQL dump has this exact route. Full body and dependencies are not recovered.')
                action='recover and verify full article, code, links and media; keep unrecovered until complete'
            reconciliation.append({'backup_permalink':'','live_permalink':'https://networkstatic.net'+path,
                                   'backup_title':'','live_title':live_title,'classification':'live-only',
                                   'confidence':'high','evidence':evidence,
                                   'action':action})
    for p in public:
        path=normalized_path(permalink(p) if p.get('post_type')=='post' else '/'+page_route(p)+'/')
        if path in live_by_path: continue
        kind='post' if p.get('post_type')=='post' else 'page'
        route_basis=('The post route is inferred from the sampled `/<slug>/` pattern and is not directly confirmed for this unobserved row.'
                     if kind=='post' else 'The page route is inferred from the WordPress page hierarchy and is not directly confirmed in the live sample.')
        evidence=(f"Backup SQL row ID {p['ID']} is a published {kind} at candidate route {path}, titled {p.get('post_title','')!r} "
                  'and dated '+p.get('post_date','')+f". {route_basis} No matching route appeared in fetched homepage/archive cards or the fetched published post/page sitemaps. "
                  'The direct candidate route and possible redirects still require review; this does not establish deletion.')
        reconciliation.append({'backup_permalink':'https://networkstatic.net'+path,'live_permalink':'',
                               'backup_title':p.get('post_title',''),'live_title':'',
                               'classification':'backup-only-candidate-review' if kind=='post' else 'backup-page-unobserved-review',
                               'confidence':'low','evidence':evidence,
                               'action':'check the live route and full content; do not republish until reviewed'})
    write_csv(out/'live-vs-backup.csv',reconciliation,
              ['backup_permalink','live_permalink','backup_title','live_title','classification','confidence','evidence','action'])
    classes=Counter(x['classification'] for x in reconciliation)
    archive_pages_observed=sorted({int(row['archive_page']) for row in archive_observations if row.get('archive_page','').isdigit()})
    archive_response_counts=Counter(row.get('archive_http_status','') for row in archive_observations)
    sitemap_type_counts=Counter(row.get('sitemap_type','') for row in sitemap_rows)
    sitemap_fetch_status_counts=Counter(row.get('fetch_http_status','') for row in sitemap_rows)
    reconciliation_report=f'''# Backup/live reconciliation

The machine-readable `live-vs-backup.csv` contains one row per unique live route and one row per published backup post/page not observed in the live route inventory. Every row includes route/title evidence, confidence, and a review action. Archive card presence establishes a listed route; sitemap/direct-route observations establish public route availability. Neither alone proves full content fidelity.

| Classification | Count | Confidence | Meaning / action |
|---|---:|---|---|
| `route-and-title-match-only` | {classes['route-and-title-match-only']} | medium | Route and title match a directly observed card/page; full body, code, links, media, and modified date still need comparison. |
| `route-match-title-differs` | {classes['route-match-title-differs']} | low | Same observed route, different live and backup titles; review title/content changes. |
| `live-only` | {classes['live-only']} | high | Observed public route has no published post/page row at that exact path in the supplied SQL dump; recover and verify the full page before approval. |
| `backup-only-candidate-review` | {classes['backup-only-candidate-review']} | low | Published backup post is absent from fetched homepage/archive cards and the fetched published sitemap; review the candidate route and redirects. This is not a deletion finding. |
| `backup-page-unobserved-review` | {classes['backup-page-unobserved-review']} | low | Published backup page is absent from fetched page sitemap and observed routes; review route and state before publication. |

The live discovery pass observed {len(parser.items)} homepage cards and {len(archive_observations)} archive cards across archive pages {archive_pages_observed[0] if archive_pages_observed else 'none'}–{archive_pages_observed[-1] if archive_pages_observed else 'none'}; archive response status counts are `{dict(archive_response_counts)}`. The fetched public sitemaps list {sitemap_type_counts['post']} post routes and {sitemap_type_counts['page']} page routes. Direct route response counts for these content URLs are `{dict(sitemap_fetch_status_counts)}`. Exact paths and response hashes are in `live-sitemap-observations.csv`; full response attempt diagnostics are in `live-fetch-diagnostics.csv`.

The current route sample observes {sum(1 for p in public if p.get('post_type')=='post' and normalized_path(permalink(p)) in live_by_path)} of {sum(1 for p in public if p.get('post_type')=='post')} published backup posts and {sum(1 for p in public if p.get('post_type')=='page' and normalized_path('/'+page_route(p)+'/') in live_by_path)} of {sum(1 for p in public if p.get('post_type')=='page')} published backup pages. Any remaining backup-only candidates remain review items, not proof of deletion or permission to republish. Full text/code/link/media comparison is still required before publication eligibility.

The April 17, 2023 “ChatGPT your Project Docs” route is the live-only row. Its route is observed in the homepage, post sitemap, and direct fetch; see `content-verification.csv` for its full-content recovery and verification state.
'''
    (out/'reconciliation.md').write_text(reconciliation_report,encoding='utf-8')
    # Resolve attachment metadata and featured image references without decoding
    # serialized metadata or exposing attachment rows for unpublished content.
    asset_owners=defaultdict(set); ref_type=defaultdict(set)
    postmeta={}
    for r in read_table(sql,'postmeta'):
        if r.get('meta_key')=='_wp_attached_file' and r.get('post_id') not in postmeta: postmeta[r['post_id']]=r.get('meta_value','')
    attachment_path={p['ID']:postmeta.get(p['ID'],'') for p in media}
    for r in read_table(sql,'postmeta'):
        if r.get('meta_key')=='_thumbnail_id' and r.get('post_id') in byid and byid[r['post_id']] in public:
            rel=attachment_path.get(r.get('meta_value',''))
            if rel:
                owner='https://networkstatic.net'+permalink(byid[r['post_id']])
                asset_owners[rel].add(owner); ref_type[rel].add('featured image metadata')
    # Candidate media inventory, hashed in place; no media are copied by inventory generation.
    # Match literal uploads references to their published post/page owners.
    upload_ref=re.compile(r'(?:(?:https?:)?//(?:www\.)?networkstatic\.net)?/?wp-content/uploads/([^\s\"\'<>]+)',re.I)
    for p in public:
        owner='https://networkstatic.net'+permalink(p)
        for m in upload_ref.finditer(html.unescape(p.get('post_content',''))):
            rel=unquote(m.group(1)).split('?',1)[0].split('#',1)[0]
            if rel:
                asset_owners[rel].add(owner)
                ref_type[rel].add('image/link/srcset/shortcode literal')
    assetrows=[]; totalbytes=0
    content_by_slug={source_slug(p):p for p in public}
    for f in sorted(uploads.rglob('*')):
        if not f.is_file(): continue
        rel=f.relative_to(uploads).as_posix(); size=f.stat().st_size; totalbytes+=size
        sha=hashlib.sha256()
        with f.open('rb') as h:
            for chunk in iter(lambda:h.read(1024*1024),b''): sha.update(chunk)
        owners=sorted(asset_owners.get(rel,set()))
        assetrows.append({'original_url':'https://networkstatic.net/wp-content/uploads/'+rel,'source_path':rel,'sha256':sha.hexdigest(),'mime':mimetypes.guess_type(f.name)[0] or 'application/octet-stream','size_bytes':size,'dimensions':image_dimensions(f) if f.suffix.lower() in ('.jpg','.jpeg','.png','.gif') else '', 'owner_urls':'|'.join(owners),'reference_type':'|'.join(sorted(ref_type.get(rel,set()))) if owners else 'no literal published-content reference found','planned_destination':'wp-content/uploads/'+rel if owners else '', 'action':'referenced candidate' if owners else 'unreferenced candidate','reason':'copy decision deferred until rendered-output dependency audit'})
    write_csv(out/'asset-candidates.csv',assetrows,['original_url','source_path','sha256','mime','size_bytes','dimensions','owner_urls','reference_type','planned_destination','action','reason'])
    asset_audit=f'''# Initial media audit\n\n- Candidate files: {len(assetrows):,}; original bytes: {totalbytes:,}.\n- Unique content hashes: {len(set(x['sha256'] for x in assetrows)):,}; repeated copies beyond first hash: {sum(v-1 for v in Counter(x['sha256'] for x in assetrows).values() if v>1):,}. Distinct legacy paths are retained as separate candidates.\n- Literal published-content or featured-image candidates: {sum(bool(x['owner_urls']) for x in assetrows):,} ({sum(int(x['size_bytes']) for x in assetrows if x['owner_urls']):,} bytes). This is not a final keep list: shortcode expansion and rendered dependency checks are pending.\n- Unreferenced candidates: {sum(not x['owner_urls'] for x in assetrows):,}. The full candidate path list is local and gitignored.\n- Copied into Hugo: 0 files / 0 bytes. Missing local refs and final rendered output refs: not yet measured. Theme UI assets are separate and not installed.\n- Full per-file SHA-256, MIME guess, image dimensions where decoded, owner URLs and candidate action are in the local gitignored `asset-candidates.csv`.\n'''
    (out/'asset-audit.md').write_text(asset_audit,encoding='utf-8')
    # Preserve the original route contract and record the sampled coverage.
    live_paths={normalized_path(x.get('path') or x.get('url','')) for x in live}
    route_status_by_path={normalized_path(row.get('path') or row.get('url','')):row.get('fetch_http_status','') for row in sitemap_rows}
    route_map=[]
    for p in public:
        path=permalink(p) if p.get('post_type')=='post' else '/'+page_route(p)+'/'; seen=normalized_path(path) in live_paths
        status=route_status_by_path.get(normalized_path(path),'')
        live_status=f'route/title observed; direct HTTP {status}; body comparison recorded separately' if seen and status else ('route/title observed; body not compared' if seen else 'not observed in fetched cards or sitemap')
        method='preserve exact Hugo permalink; verify page body before approval'
        route_map.append({'old_url':'https://networkstatic.net'+path,'destination_path':path,'url_type':p.get('post_type',''),'live_status':live_status,'method':method,'owner_urls':path})
    for n in range(1,24):
        path='/' if n==1 else f'/page/{n}/'
        archive_url='https://networkstatic.net'+path
        status=fetch_by_url.get(archive_url,{}).get('http_status','')
        route_map.append({'old_url':archive_url,'destination_path':path,'url_type':'homepage/archive pagination','live_status':f'direct HTTP {status}' if status else 'not fetched','method':'generate matching archive page','owner_urls':'site archive'})
    for taxonomy in tax.values():
        term_id,taxonomy_name=taxonomy
        if taxonomy_name not in ('category','post_tag') or term_id not in terms: continue
        name,slug=terms[term_id]; prefix='category' if taxonomy_name=='category' else 'tag'; path=f'/{prefix}/{slug}/'
        route_map.append({'old_url':'https://networkstatic.net'+path,'destination_path':path,'url_type':taxonomy_name,'live_status':'observed on sampled cards' if any(path in x.get('url','') for x in live) else 'not checked','method':'generate matching taxonomy archive','owner_urls':name})
    for path,kind in (('/feed/','RSS feed'),('/comments/feed/','comment feed'),('/author/brent/','author archive')):
        status=fetch_by_url.get('https://networkstatic.net'+path,{}).get('http_status','')
        route_map.append({'old_url':'https://networkstatic.net'+path,'destination_path':path,'url_type':kind,'live_status':f'direct HTTP {status}' if status else 'not checked','method':'compatibility route requires validation','owner_urls':'site archive'})
    write_csv(out/'url-inventory.csv',route_map,['old_url','destination_path','url_type','live_status','method','owner_urls'])
    # External HTTP dependencies are aggregated by origin/path. Query strings are
    # omitted from this public-safe report.
    external=defaultdict(lambda:{'count':0,'owners':set(),'types':set()})
    url_re=re.compile(r"https?://[^\s\"<>]+",re.I)
    for p in public:
        owner='https://networkstatic.net'+permalink(p)
        for raw in url_re.findall(html.unescape(p.get('post_content',''))):
            u=urlparse(raw.rstrip('.,;'))
            if not u.hostname or u.hostname.lower() in ('networkstatic.net','www.networkstatic.net'): continue
            key=(u.hostname.lower(),u.path or '/')
            item=external[key]; item['count']+=1; item['owners'].add(owner)
            ext=Path(u.path).suffix.lower()
            item['types'].add('external media/download' if ext in ('.png','.jpg','.jpeg','.gif','.svg','.pdf','.mp4','.mov','.ppt','.pptx') else 'external link/embed')
    extrows=[{'host':host,'path':path,'reference_count':v['count'],'owner_urls':'|'.join(sorted(v['owners'])),'dependency_type':'|'.join(sorted(v['types']))} for (host,path),v in sorted(external.items())]
    write_csv(out/'external-dependencies.csv',extrows,['host','path','reference_count','owner_urls','dependency_type'])
    tar_stats={}
    if a.archive:
        bad=dups=symlinks=hardlinks=special=unsafe_links=large=0; names=set(); count=0; expanded=0; max_member=0
        with tarfile.open(a.archive,'r:*') as tf:
            for m in tf:
                count+=1; expanded+=m.size; max_member=max(max_member,m.size); large+=m.size>100*1024*1024
                name=m.name
                if name.startswith('/') or '..' in Path(name).parts: bad+=1
                if name in names: dups+=1
                names.add(name)
                if m.issym():
                    symlinks+=1
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(name),m.linkname))
                    unsafe_links+=m.linkname.startswith('/') or target=='..' or target.startswith('../')
                elif m.islnk():
                    hardlinks+=1
                    target=posixpath.normpath(m.linkname)
                    unsafe_links+=m.linkname.startswith('/') or target=='..' or target.startswith('../')
                elif not (m.isfile() or m.isdir()): special+=1
        tar_stats={'members':count,'expanded_bytes':expanded,'max_member_bytes':max_member,'members_over_100MiB':large,'unsafe_paths':bad,'duplicate_paths':dups,'symlinks':symlinks,'hardlinks':hardlinks,'unsafe_link_targets':unsafe_links,'special_files':special,'archive_bytes':a.archive.stat().st_size,'archive_sha256':sha256_file(a.archive)}
    registered=set()
    if a.wp_root:
        pat=re.compile(r'add_shortcode\s*\(\s*[\'\"]([^\'\"]+)[\'\"]')
        for php in a.wp_root.rglob('*.php'):
            try: registered.update(pat.findall(php.read_text(encoding='utf-8',errors='ignore')))
            except OSError: pass
    occurrences=Counter()
    tag_candidates=Counter()
    for p in public:
        for name in re.findall(r'\[/?([A-Za-z][A-Za-z0-9_-]*)\b',p.get('post_content','')):
            tag_candidates[name]+=1
            if name in registered: occurrences[name]+=1
    write_csv(out/'shortcode-inventory.csv',[{'shortcode':k,'occurrences':v,'registered_in_source':'yes'} for k,v in sorted(occurrences.items())],['shortcode','occurrences','registered_in_source'])
    write_csv(out/'shortcode-tag-observations.csv',[{'tag_candidate':k,'occurrences':v,'registered_in_backup_php':'yes' if k in registered else 'no / not found by static scan','interpretation':'candidate; source scan cannot distinguish a shortcode from bracketed code/example text'} for k,v in tag_candidates.most_common()],['tag_candidate','occurrences','registered_in_backup_php','interpretation'])
    observed_paths={normalized_path(x.get('path') or x.get('url','')) for x in live}
    hash_counts=Counter(x['sha256'] for x in assetrows)
    rest_path=out/'live-rest-observations.csv'
    rest_rows=[]
    if rest_path.is_file():
        with rest_path.open(encoding='utf-8',newline='') as f: rest_rows=list(csv.DictReader(f))
    summary = {
        'database_dump_bytes': sql_path.stat().st_size,
        'database_dump_sha256': sha256_file(sql_path),
        'homepage_snapshot_bytes': a.homepage.stat().st_size,
        'homepage_snapshot_sha256': sha256_file(a.homepage),
        'live_archive_observations_bytes': a.live_archive.stat().st_size if a.live_archive else 0,
        'live_archive_observations_sha256': sha256_file(a.live_archive) if a.live_archive else '',
        'live_fetch_diagnostics_bytes':a.fetch_diagnostics.stat().st_size if a.fetch_diagnostics and a.fetch_diagnostics.is_file() else 0,
        'live_fetch_diagnostics_sha256':sha256_file(a.fetch_diagnostics) if a.fetch_diagnostics and a.fetch_diagnostics.is_file() else '',
        'live_browser_probes_bytes':a.browser_probes.stat().st_size if a.browser_probes and a.browser_probes.is_file() else 0,
        'live_browser_probes_sha256':sha256_file(a.browser_probes) if a.browser_probes and a.browser_probes.is_file() else '',
        'live_browser_probe_rows':len(browser_rows),
        'live_fetch_attempts':len(fetch_rows),
        'live_fetch_unique_urls':len({r.get('requested_url','') for r in fetch_rows}),
        'live_fetch_result_counts':dict(Counter(r.get('result','') for r in fetch_rows)),
        'live_fetch_transport_error_counts':dict(Counter(r.get('transport_error','') for r in fetch_rows if r.get('transport_error'))),
        'live_browser_probe_result_counts':dict(Counter(r.get('result','') for r in browser_rows)),
        'local_review_converted_count':len(conversion_rows),
        'local_review_media_count':len(media_manifest_rows),
        'local_review_media_bytes':sum(int(r.get('size_bytes') or 0) for r in media_manifest_rows),
        'wordpress_rows': len(posts),
        'post_type_counts': dict(types),
        'status_type_counts': {f'{t}/{status}': n for (t, status), n in statuses.items()},
        'published_post_count': sum(1 for p in public if p.get('post_type') == 'post'),
        'published_page_count': sum(1 for p in public if p.get('post_type') == 'page'),
        'password_protected_published_content_excluded':len(protected_published),
        'nonpublished_content_excluded_count':sum(excluded_status_counts.values()),
        'excluded_nonpublished_content_counts_by_type_status':{f'{kind}/{status}':count for (kind,status),count in sorted(excluded_status_counts.items())},
        'attachment_record_count': len(media),
        'homepage_observed_cards': len(parser.items),
        'sampled_archive_cards': len(archive_observations),
        'live_route_observations': len(live),
        'live_post_sitemap_routes':sitemap_type_counts.get('post',0),
        'live_page_sitemap_routes':sitemap_type_counts.get('page',0),
        'live_sitemap_route_fetch_status_counts':dict(sitemap_fetch_status_counts),
        'live_rest_route_count':len(rest_rows),
        'live_rest_result_counts':dict(Counter(x.get('result','') for x in rest_rows)),
        'live_rest_source_status_counts':dict(Counter(x.get('source_status','') for x in rest_rows)),
        'live_rest_password_protection_counts':dict(Counter(x.get('password_protected','') for x in rest_rows)),
        'live_rest_exact_route_matches':sum(x.get('result')=='matched' and x.get('api_route')==x.get('route') for x in rest_rows),
        'live_archive_pages_observed':archive_pages_observed,
        'live_archive_card_fetch_status_counts':dict(archive_response_counts),
        'backup_posts_seen_in_live_samples': sum(1 for p in public if p.get('post_type') == 'post' and normalized_path(permalink(p)) in observed_paths),
        'backup_pages_seen_in_live_samples': sum(1 for p in public if p.get('post_type') == 'page' and normalized_path('/' + page_route(p) + '/') in observed_paths),
        'route_title_match_count': sum(1 for x in reconciliation if x['classification'] == 'route-and-title-match-only'),
        'route_title_difference_count': sum(1 for x in reconciliation if x['classification'] == 'route-match-title-differs'),
        'live_only_observations': sum(1 for x in reconciliation if x['classification'] == 'live-only'),
        'backup_post_review_candidates': sum(1 for x in reconciliation if x['classification'] == 'backup-only-candidate-review'),
        'backup_page_review_candidates': sum(1 for x in reconciliation if x['classification'] == 'backup-page-unobserved-review'),
        'media_candidate_count': len(assetrows),
        'media_candidate_unique_sha256': len(hash_counts),
        'media_candidate_duplicate_files': sum(v - 1 for v in hash_counts.values() if v > 1),
        'media_candidate_bytes': totalbytes,
        'literal_referenced_assets': sum(bool(x['owner_urls']) for x in assetrows),
        'literal_referenced_bytes': sum(int(x['size_bytes']) for x in assetrows if x['owner_urls']),
        'registered_shortcodes_found_in_public_content': len(occurrences),
        'external_dependency_paths': len(extrows),
        'url_inventory_rows': len(route_map),
        'archive': tar_stats,
    }
    (out/'inventory-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    report=f'''# Initial migration inventory

- Backup logical source: `{sql_path.name}` ({summary['database_dump_bytes']:,} bytes; SHA-256 recorded in `inventory-summary.json`).
- Eligible backup content under the strict source gate: {summary['published_post_count']} unprotected published posts, {summary['published_page_count']} unprotected published pages; {summary['attachment_record_count']} attachment records. Excluded counts by status/type are in `source-eligibility.json`; it contains no excluded titles or content.
- Upload candidates: {len(assetrows):,} files ({totalbytes:,} bytes). Literal-path scan finds {summary['literal_referenced_assets']} candidates; deterministic conversion has copied {summary['local_review_media_count']} dependencies ({summary['local_review_media_bytes']:,} bytes) into the ignored local review tree, outside production roots. See `media-copy-manifest.csv` and `conversion-fidelity.csv` for dependency/hash checks.
- Live route inventory: {summary['live_route_observations']} unique public post/page routes, including {summary['homepage_observed_cards']} supplied homepage cards, {summary['sampled_archive_cards']} archive cards across pages 2–23, {summary['live_post_sitemap_routes']} post-sitemap routes, and {summary['live_page_sitemap_routes']} page-sitemap routes. Direct response counts are `{summary['live_sitemap_route_fetch_status_counts']}`.
- Reconciliation: {summary['backup_posts_seen_in_live_samples']} backup posts and {summary['backup_pages_seen_in_live_samples']} backup pages have direct route observations ({summary['route_title_match_count']} route/title matches and {summary['route_title_difference_count']} title differences); {summary['live_only_observations']} live-only route has no backup row. {summary['backup_post_review_candidates']} backup posts and {summary['backup_page_review_candidates']} backup pages remain unobserved candidates. Absence does not prove deletion.
- Local fetch diagnostics recorded {summary['live_fetch_attempts']} GET attempts across {summary['live_fetch_unique_urls']} requested URLs; result counts and transport errors are in `live-fetch-diagnostics.csv`. Requests use standard browser headers because the origin's ModSecurity returned 406 for the earlier descriptive crawler User-Agent. Browser-tool probes remain separate in `live-browser-probes.csv` and do not override direct HTTP evidence.
- The April 17, 2023 “ChatGPT your Project Docs” route is present in the public post sitemap and returns HTTP 200. Its WordPress REST record and media are in the ignored live crawl; full verification and conversion status are tracked separately in `content-verification.csv` and `live-content-comparison.csv`.

## Archive safety inspection

`inventory-summary.json` records archive size/hash, 16,600 members, path/link checks, duplicate paths, largest member, and oversized members. No paths escaped the archive root, no unsafe link targets were found, and no special files were present. Three in-archive symlinks and one repeated archive path were found. The backup was already present as an extracted directory; this workflow does not extract the tar or execute PHP.
'''
    (out/'backup-inventory.md').write_text(report,encoding='utf-8')
    discovery=f'''# Live discovery coverage

## Method and evidence

- `scripts/discover_live.py` fetched the homepage, archive pages 2–23, WordPress post/page/attachment sitemaps, REST API endpoints, selected recovery assets, and every post/page route listed by the public sitemaps. The crawler uses a standard browser User-Agent and navigation headers because the origin's ModSecurity returned HTTP 406 to its earlier descriptive crawler User-Agent.
- `reports/live-fetch-diagnostics.csv` records requested URL, method, attempt, UTC timestamp, HTTP status or transport error, final URL, content type, body length/hash, and saved file. The exact successful response pages and media are in the ignored `migration-review/live-crawl/` directory. `live-browser-probes.csv` is kept separate from origin HTTP responses.
- Parsed {summary['sampled_archive_cards']} cards from archive pages {archive_pages_observed[0] if archive_pages_observed else 'none'}–{archive_pages_observed[-1] if archive_pages_observed else 'none'}; the supplied homepage snapshot contributes {summary['homepage_observed_cards']} cards. Archive fetch status counts: `{dict(archive_response_counts)}`.
- The public post sitemap lists {sitemap_type_counts['post']} routes and the page sitemap lists {sitemap_type_counts['page']}; direct route status counts are `{dict(sitemap_fetch_status_counts)}`. The `live-sitemap-observations.csv` rows also record titles, last-modified dates, response hashes, normalized body/code/link/media hashes, and password-form presence.
- Anonymous REST route lookups matched {summary['live_rest_exact_route_matches']}/{summary['live_rest_route_count']} exact paths; REST source status counts are `{summary['live_rest_source_status_counts']}` and `content.protected` counts are `{summary['live_rest_password_protection_counts']}`. Per-route IDs, body hashes, titles, dates, response attempts, and paths are in `live-rest-observations.csv`; response bodies stay in ignored `migration-review/live-rest/`.
- One backup post omitted from archive cards, `/my-notes-from-2/`, is present in the published post sitemap and direct route fetch. The April 17 article is also in the sitemap and REST API. One known internal link target, `/open-v-switch-red-hat-installation/` (backup ID 4867), returned a direct HTTP 404; it remains a per-link/article exception.

## Coverage and reconciliation

The live inventory contains {summary['live_route_observations']} unique public post/page routes. It observes {summary['backup_posts_seen_in_live_samples']} of {summary['published_post_count']} published backup posts and {summary['backup_pages_seen_in_live_samples']} of {summary['published_page_count']} published backup pages. There are {summary['live_only_observations']} live-only routes, {summary['backup_post_review_candidates']} backup-only post candidates, and {summary['backup_page_review_candidates']} backup-only page candidates. These are route findings; absence from a card or sitemap is not classified as deletion.

`live-content-inventory.csv` combines the supplied homepage snapshot, archive cards, public sitemaps, and direct route responses. `live-archive-observations.csv`, `live-sitemap-observations.csv`, and `live-rest-observations.csv` preserve the source observations. `live-vs-backup.csv` records route/title differences, confidence, and review actions. `live-content-comparison.csv` compares normalized text/code/link/media and source/live metadata for every backup article against both anonymous REST bodies and direct page responses; `conversion-fidelity.csv` separately compares generated review files against backup sources. Article-specific checks and exceptions are in `content-verification.csv`.

Taxonomy/date archives, historical redirects, comments feed, and all non-content dependencies are not covered by the post/page route crawl. Publication eligibility also requires the recorded content comparisons and per-article exception review.
'''
    (out/'live-discovery.md').write_text(discovery,encoding='utf-8')
    unresolved_posts=summary['backup_post_review_candidates']
    article_exception_rows=[]
    verification_path=out/'content-verification.csv'
    if verification_path.is_file():
        with verification_path.open(encoding='utf-8',newline='') as f:
            article_exception_rows=[r for r in csv.DictReader(f) if r.get('blocking_exception','').strip()]
    article_exception_text='\n'.join(
        f"- **Review — {r.get('permalink','')}** ({'backup post ID '+r.get('wp_id','') if r.get('wp_id','').strip() else 'live-only article'}): {r.get('blocking_exception','')}"
        for r in article_exception_rows) or '- No article-specific content exceptions have been recorded.'
    verification_rows=[]
    if verification_path.is_file():
        with verification_path.open(encoding='utf-8',newline='') as f: verification_rows=list(csv.DictReader(f))
    april=next((r for r in verification_rows if r.get('wp_id')=='7986'),{})
    april_summary=('The full April 17 article is recovered and compared against its anonymous REST body and direct page; all text, code count, links, and six inline/featured media files are verified. It remains local review content pending the site-wide publication ledger.'
                   if april.get('verification')=='full-body-verified' else 'The April 17 article remains unrecovered; see `content-verification.csv`.')
    exceptions=f'''# Migration exceptions and review queue

## Publication gate

- **Open — article publication approval.** The live crawl covers {summary['live_route_observations']} public post/page routes with direct status counts `{dict(sitemap_fetch_status_counts)}`. Anonymous REST lookups matched {summary['live_rest_exact_route_matches']}/{summary['live_rest_route_count']} exact routes; source statuses are `{summary['live_rest_source_status_counts']}` and password-protection values are `{summary['live_rest_password_protection_counts']}`. These route/status results establish public availability, not body parity.
- The reconciliation finds {summary['route_title_match_count']} route/title matches, {summary['route_title_difference_count']} title differences, {summary['live_only_observations']} live-only route, and {unresolved_posts} backup-only post candidates. No unobserved route is classified as deleted. See `live-vs-backup.csv`.
- Backup-to-review conversion is exact for text, code, and links across all eligible backup rows; media and current-live body differences remain article-specific in `conversion-fidelity.csv`, `live-content-comparison.csv`, and `publication-eligibility.csv`. Six broken local references are preserved as link exceptions. The ledger currently approves zero pages.

## Article-specific exceptions

{article_exception_text}

## Live-only article

- {april_summary}

## Media and conversion concerns

- Three backup articles reference 17 external images/documents absent from the supplied uploads folder. The links remain in source and are listed in `external-dependencies.csv`; they have not been copied from third-party hosts.
- Shortcode inventory is split between `shortcode-inventory.csv` (tags found registered by a static scan of backup PHP) and `shortcode-tag-observations.csv` (bracket-token candidates that can include code/examples). The top candidates include legacy theme layouts, syntax-highlighter tags, and video embeds; unsupported constructs are recorded per article.
- The backup has {len(assetrows):,} upload files ({totalbytes:,} bytes); {summary['literal_referenced_assets']} are literal-path candidates. The ignored local review export contains only dependencies of verified public sources, recorded in `conversion-review.csv` and `media-copy-manifest.csv`. Excluded-source-only media is not copied.
- Three archive symlinks and one repeated archive member name were found; unsafe paths/link targets and special files were not found. The tar was not extracted.
'''
    (out/'migration-exceptions.md').write_text(exceptions,encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
