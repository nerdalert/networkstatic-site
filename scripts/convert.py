#!/usr/bin/env python3
"""WordPress content parsing and deterministic markup/URL transforms."""
from __future__ import annotations
import hashlib, html, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inventory import read_table, permalink, source_slug

ROOT=Path(__file__).resolve().parents[1]
CONVERTER_VERSION='0.11.0'
KNOWN={'fancy_header3','crayon','image_frame','fancy_list','fancy_link','pullquote1','pullquote2','pullquote3','pullquote4','fancy_numbers','download_link','youtube','vimeo','titled_box','colored_box','info_box','note_box','warning_box','fancy_table','dropcap1','dropcap3','slideshare','gview'}
MEDIA_ATTRS={'src','href','poster','data-src','data-lazy-src','data-original','srcset'}

class MediaRefs(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in MEDIA_ATTRS and v:
                values=v.split(',') if k=='srcset' else [v]
                for item in values:
                    candidate=item.strip().split()[0]
                    if candidate: self.refs.append((candidate,k))

def args_attrs(s):
    return {k:html.unescape(v) for k,q,v in re.findall(r'([\w-]+)\s*=\s*([\'\"])(.*?)\2',s,re.S)}

def shortcode_media_refs(text):
    """Collect local upload dependencies stored in shortcode attributes."""
    text=mask_code(text)[0]
    refs=set()
    for match in re.finditer(r'\[[A-Za-z][\w-]*\b([^\]]*)\]',text):
        values=args_attrs(match.group(1))
        for key in ('src','file','url','href','link','citelink','citationlink'):
            value=values.get(key,'')
            path=unquote(urlparse(value).path)
            marker='/wp-content/uploads/'
            if marker in path:
                refs.add(path.split(marker,1)[1])
    return refs
def esc(s): return html.escape(s,quote=True)

def mask_code(text):
    """Hide code examples from transformations that apply to article prose/markup."""
    digest=hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]
    prefix=f'@@NETWORKSTATIC_CODE_{digest}_'
    while prefix in text: prefix='_'+prefix
    saved=[]
    patterns=(
        re.compile(r'<pre\b[^>]*>.*?</pre\s*>',re.I|re.S),
        re.compile(r'<code\b[^>]*>.*?</code\s*>',re.I|re.S),
        re.compile(r'(?m)^[ \t]*(?:```|~~~)[^\n]*\n.*?^[ \t]*(?:```|~~~)[ \t]*$',re.S),
        re.compile(r'(`+)([^`\n]*?)\1'),
    )
    for pattern in patterns:
        def hold(match):
            token=f'{prefix}{len(saved)}@@'
            saved.append(match.group(0))
            return token
        text=pattern.sub(hold,text)
    return text,saved,prefix

def unmask_code(text,saved,prefix):
    for index,value in enumerate(saved): text=text.replace(f'{prefix}{index}@@',value)
    return text

def unresolved_shortcodes(text):
    prose,_,_=mask_code(text)
    return sorted(set(m.group(1).lower() for m in re.finditer(r'\[/?([A-Za-z][\w-]*)\b[^\]]*\]',prose) if m.group(1).lower() in KNOWN))

def remove_empty_anchor_links(text):
    """Drop empty hyperlink shells while retaining named in-page anchor targets."""
    return re.sub(r'<a\b(?=[^>]*\bhref\s*=)[^>]*>\s*</a\s*>', ' ', text, flags=re.I|re.S)

def shortcode_convert(source):
    text=source
    source_prose,_,_=mask_code(source)
    balance_exceptions=[]
    for name in KNOWN:
        opens=len(re.findall(r'\['+re.escape(name)+r'\b[^\]]*\]',source_prose,re.I))
        closes=len(re.findall(r'\[/'+re.escape(name)+r'\s*\]',source_prose,re.I))
        if opens != closes:
            balance_exceptions.append(name)
    # Preserve the original code bytes/markup before decoding entities in prose.
    # A blanket html.unescape() first turns escaped angle brackets in commands
    # into live HTML tags and silently removes them from rendered code.
    crayon=re.compile(r'\[crayon\b([^\]]*)\](.*?)\[/crayon\s*\]',re.I|re.S)
    text=crayon.sub(lambda m:f'<pre class="code-sample"><code>{m.group(2)}</code></pre>',text)
    text,saved_code,code_prefix=mask_code(text)
    def attr_value(attrs,*names):
        values=args_attrs(attrs)
        for name in names:
            if values.get(name): return values[name]
        return ''
    def valid_link(url):
        u=urlparse(url)
        return (not u.scheme and url.startswith('/')) or (u.scheme in ('https','http') and bool(u.netloc))
    def paired(name, render):
        nonlocal text
        pattern=re.compile(r'\['+re.escape(name)+r'([^\]]*)\](.*?)\[/'+re.escape(name)+r'\]',re.S|re.I)
        text=pattern.sub(lambda m:render(m.group(2),m.group(1)),text)
    def simple_link(name,label):
        def render(body,attrs):
            url=attr_value(attrs,'url','href','file','link')
            link_label=attr_value(attrs,'text','title','label')
            body_url=html.unescape(body.strip())
            if url and not valid_link(url) and valid_link(body_url):
                link_label=link_label or url
                url=body_url
                body=html.escape(link_label)
            elif not url or not valid_link(url):
                return f'[{name}{attrs}]{body}[/{name}]'
            target=attr_value(attrs,'target')
            t=' target="_blank" rel="noopener noreferrer"' if target.lower() in ('_blank','blank','new') else ''
            body=body or html.escape(label)
            return f'<a href="{esc(url)}"{t}>{body}</a>'
        paired(name,render)
    # Innermost pass first for nested legacy presentation containers.
    wrappers={
        'fancy_header3':lambda body,attrs:f'<h2 class="legacy-heading">{body}</h2>',
        'image_frame':lambda body,attrs:image_frame(body,attrs),
        'fancy_list':lambda body,attrs:body if re.search(r'<(?:ul|ol)\b',body,re.I) else f'<ul class="legacy-list">{body}</ul>',
        'fancy_numbers':lambda body,attrs:f'<ol class="legacy-numbers">{body}</ol>',
        'fancy_table':lambda body,attrs:f'<div class="table-scroll"><table>{body}</table></div>',
        'pullquote1':lambda body,attrs:quote(body,attrs),
        'pullquote2':lambda body,attrs:quote(body,attrs),
        'pullquote3':lambda body,attrs:quote(body,attrs),
        'pullquote4':lambda body,attrs:quote(body,attrs),
        'titled_box':lambda body,attrs:callout(body,attrs),
        'colored_box':lambda body,attrs:callout(body,attrs),
        'info_box':lambda body,attrs:callout(body,attrs),
        'note_box':lambda body,attrs:callout(body,attrs),
        'warning_box':lambda body,attrs:callout(body,attrs),
        'dropcap1':lambda body,attrs:f'<span class="drop-cap">{body}</span>',
        'dropcap3':lambda body,attrs:f'<span class="drop-cap">{body}</span>',
    }
    # The source sometimes wraps the shortcode in an existing heading element.
    # Keep that heading level and remove the nested legacy token wrapper.
    heading=re.compile(r'<(?P<tag>h[1-6])(?P<attrs>[^>]*)>\s*\[fancy_header3[^\]]*\](?P<body>.*?)\[/fancy_header3\]\s*</(?P=tag)\s*>',re.I|re.S)
    text=heading.sub(lambda m:f'<{m.group("tag")}{m.group("attrs")}>{m.group("body")}</{m.group("tag")}>',text)
    # Helper definitions are local so all output rules are deterministic.
    def image_frame(body,attrs):
        values=args_attrs(attrs); raw=body.strip()
        if not re.search(r'<img\b',raw,re.I):
            url=values.get('src') or values.get('image') or (raw if re.match(r'^(?:https?:)?//|^/wp-content/uploads/',raw) else '')
            if not url and re.match(r'^hhttps?://',raw,re.I):
                url=raw
            if not url and re.match(r'^(?:href|src)\s*=',raw,re.I):
                # A subset of legacy [image_frame] bodies contain only a
                # truncated href attribute. Recover its URL without allowing
                # the malformed quote to consume the rest of the article.
                url=re.sub(r'^(?:href|src)\s*=\s*["\']?', '', raw, flags=re.I).strip().strip("\"'")
            # A single known legacy image shortcode has a duplicated leading h.
            # The review ledger records this narrow repair as an exception.
            url=re.sub(r'^h(?=https?://)', '', url, count=1, flags=re.I)
            if url:
                alt=values.get('alt','')
                raw=f'<img src="{esc(url)}" alt="{esc(alt)}">'
        caption=values.get('caption')
        return f'<figure class="legacy-figure">{raw}'+(f'<figcaption>{html.escape(caption)}</figcaption>' if caption else '')+'</figure>'
    def quote(body,attrs):
        cite=attr_value(attrs,'cite').strip()
        cite_url=attr_value(attrs,'citeLink','citelink').strip()
        cite_url=re.sub(r'^-\s*(?=https?://)', '', cite_url, count=1, flags=re.I)
        footer=''
        if cite_url and valid_link(cite_url):
            footer=f'<footer><a href="{esc(cite_url)}">{html.escape(cite or cite_url)}</a></footer>'
        elif cite:
            footer=f'<footer>{html.escape(cite)}</footer>'
        return f'<blockquote class="pullquote">{body}{footer}</blockquote>'
    def callout(body,attrs):
        title=attr_value(attrs,'title')
        return '<aside class="legacy-callout">'+(f'<strong>{html.escape(title)}</strong>' if title else '')+body+'</aside>'
    for _ in range(16):
        before=text
        for name,render in wrappers.items(): paired(name,render)
        if text==before: break
    # Remove malformed presentation markers from the rendered page while the
    # imbalance remains a blocking exception in the per-article ledger.
    for name in ('fancy_header3','fancy_list','crayon'):
        text=re.sub(r'\[/?'+re.escape(name)+r'\b[^\]]*\]', '', text, flags=re.I)
    simple_link('fancy_link','Open link')
    simple_link('download_link','Download file')
    # Legacy video syntax stores a full URL in an attribute; retain it as a link
    # rather than loading remote player scripts in the static site.
    for name,host,label in (('youtube','youtube.com','Watch video on YouTube'),('vimeo','vimeo.com','Watch video on Vimeo')):
        def render_video(attrs,body,name=name,host=host,label=label):
            url=attr_value(attrs,'url','link','src') or html.unescape(body.strip())
            if not url and attr_value(attrs,'id'):
                url=('https://' + host + '/watch?v=' + attr_value(attrs,'id') if name=='youtube'
                     else 'https://' + host + '/' + attr_value(attrs,'id'))
            if url and valid_link(url) and host in url.lower(): return f'<p><a href="{esc(url)}">{label}</a></p>'
            return None
        def video(m, host=host, label=label, name=name):
            return render_video(m.group(1),m.group(2) or '',name,host,label) or m.group(0)
        # Paired form first, then single-tag form used by the WordPress theme.
        paired_video=r'\['+name+r'([^\]]*)\]((?:(?!\['+name+r'\b).)*?)\[/'+name+r'\]'
        text=re.sub(paired_video,video,text,flags=re.I|re.S)
        text=re.sub(r'\['+name+r'([^\]]*)\]',lambda m:render_video(m.group(1),'',name,host,label) or m.group(0),text,flags=re.I)
    def render_gview(match):
        url=attr_value(match.group(1),'file','url','src')
        if url and valid_link(url):
            return f'<p><a href="{esc(url)}">Download the document</a></p>'
        return match.group(0)
    text=re.sub(r'\[gview([^\]]*)\]',render_gview,text,flags=re.I)
    slideshare_exception=False
    def render_slideshare(match):
        nonlocal slideshare_exception
        slideshare_exception=True
        values=args_attrs(match.group(1))
        identifier=values.get('id','').strip()
        document=values.get('doc','').strip()
        label='SlideShare presentation'
        if identifier: label+=f' (ID {html.escape(identifier)})'
        elif document: label+=f' ({html.escape(document)})'
        return f'<aside class="legacy-embed-note">{label}; original embed needs review.</aside>'
    text=re.sub(r'\[slideshare([^\]]*)\]',render_slideshare,text,flags=re.I)
    text=unmask_code(text,saved_code,code_prefix)
    unresolved=sorted(set(balance_exceptions + unresolved_shortcodes(text) + (["slideshare"] if slideshare_exception else [])))
    return text,unresolved

def rewrite_internal_urls(text):
    text,saved_code,code_prefix=mask_code(text)
    media=[]; internal_routes=set()
    def internal_destination(raw):
        raw=html.unescape(raw.strip())
        parsed=urlparse(raw)
        host=(parsed.hostname or '').lower()
        if host and host not in ('networkstatic.net','www.networkstatic.net'): return None
        if parsed.scheme and not host: return None
        if not host and not parsed.path.startswith('/'): return None
        path=unquote(parsed.path or '/')
        if path.startswith('/~bbsali0/'):
            path=path[len('/~bbsali0'):]
        suffix=('?'+parsed.query if parsed.query else '')+('#'+parsed.fragment if parsed.fragment else '')
        return path+suffix
    def note_media(destination):
        path=unquote(destination).split('?',1)[0].split('#',1)[0]
        marker='/wp-content/uploads/'
        if marker in path: media.append(path.split(marker,1)[1])
    def rewrite_url(raw,markdown=False,route=False):
        destination=internal_destination(raw)
        if destination is None: return raw
        note_media(destination)
        if route:
            internal_routes.add(urlparse(destination).path or '/')
        delimiter='%' if markdown else '<'
        closing='%' if markdown else '>'
        return '{{'+delimiter+' relurl '+json.dumps(destination,ensure_ascii=False)+' '+closing+'}}'
    shortcodes=[]
    shortcode_prefix='@@NETWORKSTATIC_SHORTCODE_'+hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]+'_'
    while shortcode_prefix in text: shortcode_prefix='_'+shortcode_prefix
    unresolved_names='|'.join(re.escape(name) for name in sorted(KNOWN,key=len,reverse=True))
    shortcode_block=re.compile(r'\[(?P<tag>'+unresolved_names+r')\b[^\]]*\].*?\[/\1\s*\]',re.I|re.S)
    shortcode_pattern=re.compile(r'\[(?P<token>/?[A-Za-z][\w-]*\b[^\]\n]*=[^\]\n]*)\](?!\s*(?:\(|:))')
    internal_url=re.compile(r"""(?:https?://(?:www\.)?networkstatic\.net[^\s"'\[\]]+|(?<!\[)/(?!/)[^\s"'\[\]]+)""",re.I)
    def hold_shortcode(match):
        value=match.group(0)
        for raw in internal_url.findall(value):
            destination=internal_destination(raw)
            if destination:
                note_media(destination)
                internal_routes.add(urlparse(destination).path or '/')
        token=f'{shortcode_prefix}{len(shortcodes)}@@'; shortcodes.append(value); return token
    text=shortcode_block.sub(hold_shortcode,text)
    text=shortcode_pattern.sub(hold_shortcode,text)
    # Rewrite URL-bearing HTML attributes while leaving the rest of the tag and
    # all code examples intact. WordPress srcset and lazy-load attributes count.
    attr=re.compile(r'(?P<prefix>\b(?:href|src|poster|srcset|style|data-[\w-]+)\s*=\s*)(?P<q>[\"\'])(?P<value>.*?)(?P=q)',re.I|re.S)
    css_url=re.compile(r'url\(\s*([\"\']?)([^)\"\']+)\1\s*\)',re.I)
    def rewrite_value(value,key):
        if key.lower()=='srcset':
            parts=[]
            for part in value.split(','):
                bits=part.strip().split()
                if bits: bits[0]=rewrite_url(bits[0])
                parts.append(' '.join(bits))
            return ', '.join(parts)
        if key.lower()=='style':
            return css_url.sub(lambda m:'url('+rewrite_url(m.group(2))+')',value)
        return rewrite_url(value,route=(key.lower()=='href'))
    text=attr.sub(lambda m:m.group('prefix')+m.group('q')+
                  rewrite_value(m.group('value'),re.search(r'^[\w-]+',m.group('prefix').strip()).group(0))+
                  m.group('q'),text)
    # The href is rewritten above. Shield the anchor body so bare-URL handling
    # cannot turn a URL used as link text into a nested Markdown link.
    anchors=[]
    anchor_prefix='@@NETWORKSTATIC_ANCHOR_'+hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]+'_'
    while anchor_prefix in text: anchor_prefix='_'+anchor_prefix
    def hold_anchor(match):
        token=f'{anchor_prefix}{len(anchors)}@@'; anchors.append(match.group(0)); return token
    text=re.sub(r'<a\b[^>]*>.*?</a\s*>',hold_anchor,text,flags=re.I|re.S)
    # Markdown destinations accept Markdown-notation shortcodes. This lets Hugo
    # apply the project-site base path before Goldmark renders the link/image.
    tag_pattern=re.compile(r'</?[A-Za-z][^>]*>')
    tags=[]
    tag_prefix='@@NETWORKSTATIC_TAG_'+hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]+'_'
    while tag_prefix in text: tag_prefix='_'+tag_prefix
    def hold_tag(match):
        token=f'{tag_prefix}{len(tags)}@@'; tags.append(match.group(0)); return token
    text=tag_pattern.sub(hold_tag,text)
    md_target=r'(?P<url>(?:https?:)?//(?:www\.)?networkstatic\.net[^\s)]+|/(?!/)[^\s)]+)'
    md_link=re.compile(r'(?P<prefix>!?\[[^\]\n]*\]\()'+md_target+r'(?P<suffix>\s+(?:"[^"]*"|\'[^\']*\'))?\)',re.I)
    text=md_link.sub(lambda m:m.group('prefix')+rewrite_url(m.group('url'),markdown=True,route=not m.group('prefix').startswith('!['))+
                     (m.group('suffix') or '')+')',text)
    ref_link=re.compile(r'(?m)^(?P<prefix>\s*\[[^\]]+\]:\s*)'+md_target+r'(?P<suffix>\s+.*)?$',re.I)
    text=ref_link.sub(lambda m:m.group('prefix')+rewrite_url(m.group('url'),markdown=True,route=True)+
                      (m.group('suffix') or ''),text)
    auto_link=re.compile(r'<(?P<url>(?:https?:)?//(?:www\.)?networkstatic\.net[^\s>]+)>',re.I)
    text=auto_link.sub(lambda m:'<'+rewrite_url(m.group('url'),markdown=True,route=True)+'>',text)
    bare=re.compile(r'https?://(?:www\.)?networkstatic\.net/[^\s<>\)\("\'`]+',re.I)
    def bare_link(match):
        raw=match.group(0); suffix=''
        while raw and raw[-1] in '.,;:!?': suffix=raw[-1]+suffix; raw=raw[:-1]
        if not raw: return match.group(0)
        return '['+raw+']('+rewrite_url(raw,markdown=True,route=True)+')'+suffix
    text=bare.sub(bare_link,text)
    for index,anchor in enumerate(anchors): text=text.replace(f'{anchor_prefix}{index}@@',anchor)
    for index,tag in enumerate(tags): text=text.replace(f'{tag_prefix}{index}@@',tag)
    for index,shortcode in enumerate(shortcodes): text=text.replace(f'{shortcode_prefix}{index}@@',shortcode)
    return unmask_code(text,saved_code,code_prefix),sorted(set(media)),sorted(internal_routes)

def sanitize_html(text):
    # Remove executable embedding and inline event handlers. Article HTML remains
    # otherwise intact so technical markup and code samples are preserved.
    text,saved_code,code_prefix=mask_code(text)
    text=re.sub(r'<(script|style|iframe|object|embed|form)\b[^>]*>.*?</\1\s*>','',text,flags=re.I|re.S)
    text=re.sub(r'<(script|style|iframe|object|embed|form)\b[^>]*/?>','',text,flags=re.I)
    text=re.sub(r'\s+on[a-z]+\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)','',text,flags=re.I)
    text=re.sub(r'\s+(href|src)\s*=\s*([\'\"])\s*(?:javascript|vbscript|data):[^\'\"]*\2','',text,flags=re.I)
    return unmask_code(text,saved_code,code_prefix)

def main():
    from review_conversion import main as run_review_conversion
    return run_review_conversion()

if __name__=='__main__':
    raise SystemExit(main())
