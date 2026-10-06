#!/usr/bin/env python3
"""Genera il sito HTML classico di Senad Transporti (EL / EN / DE / RU).

Uso:  python3 build_html.py
I testi stanno in L.json (una voce per lingua). I dati dell'attivita' stanno in BUSINESS:
i campi vuoti restano vuoti e nel sito appare "da aggiungere".
"""
import json, os, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')
L = json.load(open(os.path.join(HERE, 'L.json'), encoding='utf8'))

# ---- impostazioni -----------------------------------------------------------
SITE_URL = 'https://DOMINIO-DA-DECIDERE.example'   # sostituire quando il dominio e' scelto
NOINDEX = True                                       # mettere False al lancio
BRAND = 'Senad Transporti'
BUSINESS = {                                         # campi vuoti = restano vuoti
    'phone': '', 'email': '', 'address': '', 'hours': '',
    'facebook': '', 'instagram': '',
}
LANGS = ['el', 'en', 'de', 'ru']
LANG_LABEL = {'el': 'EL', 'en': 'EN', 'de': 'DE', 'ru': 'RU'}
OG_LOCALE = {'el': 'el_GR', 'en': 'en_GB', 'de': 'de_DE', 'ru': 'ru_RU'}
PAGES = ['index', 'services', 'routes', 'book', 'about', 'faq', 'contact']
NAVKEY = {'index': 'home', 'services': 'services', 'routes': 'routes', 'book': 'book',
          'about': 'about', 'faq': 'faq', 'contact': 'contact'}
LEGAL = ['impressum', 'privacy', 'cookies', 'terms']
LG = json.load(open(os.path.join(HERE, 'legal.json'), encoding='utf8'))   # testi legali in bozza (4 lingue)


def legal_name(lang, t, page):
    return LG[lang]['cookieName'] if page == 'cookies' else t['legal'][{'impressum': 0, 'privacy': 1, 'terms': 2}[page]]
SKIP = {'en': 'Skip to content', 'el': 'Μετάβαση στο περιεχόμενο', 'de': 'Zum Inhalt springen', 'ru': 'Перейти к содержимому'}
CHAT_INPUT_CLOSE = {'en': 'Close', 'el': 'Κλείσιμο', 'de': 'Schließen', 'ru': 'Закрыть'}
LEGAL_FIELDS = {
    'en': ['Company name', 'Address', 'Contact', 'Licence number'],
    'el': ['Επωνυμία', 'Διεύθυνση', 'Επικοινωνία', 'Αριθμός άδειας'],
    'de': ['Firmenname', 'Adresse', 'Kontakt', 'Lizenznummer'],
    'ru': ['Название компании', 'Адрес', 'Контакты', 'Номер лицензии'],
}
PRIVACY_NOTE = {
    'en': 'The booking form saves the data you enter (name, contact details, trip). This text must be completed and checked by a professional before real use.',
    'el': 'Η φόρμα κράτησης αποθηκεύει τα στοιχεία που συμπληρώνετε (όνομα, επικοινωνία, διαδρομή). Το κείμενο πρέπει να συμπληρωθεί και να ελεγχθεί από επαγγελματία πριν από την πραγματική χρήση.',
    'de': 'Das Buchungsformular speichert die eingegebenen Daten (Name, Kontaktdaten, Fahrt). Dieser Text muss vor dem echten Einsatz von einem Fachmann ergänzt und geprüft werden.',
    'ru': 'Форма заказа сохраняет введённые данные (имя, контакты, поездка). Перед реальным использованием этот текст должен быть дополнен и проверен специалистом.',
}
SCHEMA_DESC = {
    'en': 'Private transfers across Crete', 'el': 'Ιδιωτικές μεταφορές σε όλη την Κρήτη',
    'de': 'Privattransfers auf ganz Kreta', 'ru': 'Частные трансферы по всему Криту',
}

PTS_ORDER = ['chq', 'her', 'port', 'cha', 'ret', 'hei', 'agn', 'sit', 'che']
SEL_KEYS = PTS_ORDER


def e(x):
    return html.escape(str(x), quote=True)


def lab(t, k):
    return {'chq': t['chq'], 'her': t['her'], 'port': t['port'], 'cha': t['places'][0], 'ret': t['places'][1],
            'hei': t['places'][2], 'agn': t['places'][3], 'sit': t['places'][4], 'che': t['routes'][0][1]}[k]


def route_keys(t, r):
    frm = r[0]
    if r[1] == 'her':
        to = 'her' if r[0] == 'port' else 'hei'
    else:
        to = next(k for k in PTS_ORDER if lab(t, k) == r[1])
    return frm, to


def empty(t):
    return f'<span class="empty">— {e(t["empty"])}</span>'


# ---- pezzi di pagina --------------------------------------------------------
def head(lang, t, page, title, desc, extra_head=''):
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}/{l}/{page}.html">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{page}.html">'
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    og_alt = ''.join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang)
    fonts = ['latin']
    if lang == 'el':
        fonts.append('greek')
    if lang == 'ru':
        fonts.append('cyrillic')
    preload = ''.join(f'<link rel="preload" href="../fonts/playpen-sans-{f}.woff" as="font" type="font/woff" crossorigin>' for f in fonts)
    if page == 'index':
        preload += '<link rel="preload" href="../img/bay.webp" as="image">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{SITE_URL}/{lang}/{page}.html">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}/{lang}/{page}.html">
<meta property="og:image" content="{SITE_URL}/img/og.jpg">
<meta property="og:image:alt" content="{e(t['alt'][0])}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{og_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#04202f">
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
{preload}
<link rel="stylesheet" href="../css/style.css">
{extra_head}
</head>
'''


def header(lang, t, page):
    nav = ''.join(
        f'<a href="{p}.html"{" aria-current=\"page\"" if p == page else ""}>{e(t["nav"][NAVKEY[p]])}</a>' for p in PAGES)
    langs = ''.join(
        f'<a href="../{l}/{page}.html" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{LANG_LABEL[l]}</a>'
        for l in LANGS)
    return f'''<body class="nojs">
<a class="skip" href="#main">{e(SKIP[lang])}</a>
<header><div class="wrap bar">
  <a class="brand" href="index.html"><i></i><span>{BRAND}</span></a>
  <nav aria-label="Menu">{nav}</nav>
  <div class="lang" role="group" aria-label="Language">{langs}</div>
</div></header>
<main id="main">
'''


def footer(lang, t, page):
    legal = ' · '.join(f'<a href="{p}.html">{e(n)}</a>' for p, n in [(p, legal_name(lang, t, p)) for p in LEGAL])
    return f'''</main>
<footer><div class="wrap"><div>© {BRAND}<br>{e(t['draft'])}</div><div>{legal}</div></div></footer>
'''


def scripts(lang, t, page):
    chat = {
        'title': t['chat'], 'hi': t['chatHi'], 'input': t['chatIn'], 'send': t['chatSend'],
        'quick': [[t['q'][0], 'book'], [t['q'][1], 'routes'], [t['q'][2], 'contact']],
        'bot': t['bot'], 'kw': t['kw'],
        'nav': {'book': t['nav']['book'], 'routes': t['nav']['routes'], 'contact': t['nav']['contact'], 'home': t['nav']['home']},
    }
    site = {
        'lang': lang, 'pts': {k: lab(t, k) for k in PTS_ORDER}, 'lg': t['lg'], 'mapnote': t['mapnote'],
        'mapLabel': ', '.join(t['places']), 'formEndpoint': '', 'chat': chat,
    }
    data = json.dumps(site, ensure_ascii=False)
    return f'''<script>document.body.classList.remove('nojs');window.SITE={data};</script>
<script src="../js/main.js" defer></script>
</body>
</html>
'''


def band(t, bg, pos, h1=None, lead=None, h2=None, cls='bgband head', inner_extra=''):
    inner = ''
    if h1:
        inner += f'<h1>{e(h1)}</h1>'
    if h2:
        inner += f'<h2>{e(h2)}</h2>'
    if lead:
        inner += f'<p class="lead">{e(lead)}</p>'
    inner += inner_extra
    return f'<div class="{cls}" data-bg="../img/{bg}.webp" data-pos="{pos}"><div class="inner">{inner}</div></div>\n'


def cards(items):
    return ''.join(f'<article class="card"><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in items)


ICO = [
    '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    '<path d="M12 22s7-6.2 7-12a7 7 0 10-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    '<path d="M4 4h16v12H9l-5 4V4z"/>',
]


def three(t):
    out = ''
    for i, v in enumerate(t['v']):
        out += (f'<div class="v c{i+1}"><span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICO[i]}</svg></span>'
                f'<h3>{e(v[0])}</h3><p>{e(v[1])}</p></div>')
    return f'<div class="three">{out}</div>\n'


def route_cards(t):
    out = ''
    for r in t['routes']:
        a, b = route_keys(t, r)
        out += (f'<article class="card"><div class="route">{e(lab(t, a))} → {e(lab(t, b))}</div>'
                f'<p class="empty">— {e(t["empty"])}</p>'
                f'<a class="btn line" href="book.html?from={a}&amp;to={b}">{e(t["rq"])}</a></article>')
    return out


def hero(t):
    return f'''<section class="hero-bg"><div class="slides" role="img" aria-label="{e(t['alt'][0])}"><i class="s1"></i><i class="s2"></i><i class="s3"></i></div>
<div class="hero-in"><h1>{e(t['h1'])}</h1><p>{e(t['hsub'])}</p><div class="btns"><a class="btn sun" href="book.html">{e(t['cta'])}</a><a class="btn line" href="routes.html">{e(t['cta2'])}</a></div></div>
<svg class="wave" viewBox="0 0 1200 56" preserveAspectRatio="none" aria-hidden="true"><path class="w1" d="M0 22 Q150 0 300 22 T600 22 T900 22 T1200 22 V56 H0Z"/><path class="w2" d="M0 38 Q150 16 300 38 T600 38 T900 38 T1200 38 V56 H0Z"/></svg></section>
'''


def cta_band(t):
    return (f'<section class="bgband" data-bg="../img/road.webp" data-pos="50% 88%" style="margin-top:3.5rem"><div class="hero-in">'
            f'<h2>{e(t["bt"])}</h2><p>{e(t["bsub"])}</p><div class="btns"><a class="btn sun" href="book.html">{e(t["cta"])}</a></div></div></section>\n')


def map_box(extra_style=''):
    return f'<div class="bigmap" data-map{extra_style}></div>\n'


def options(t, selected):
    return ''.join(f'<option value="{k}"{" selected" if k == selected else ""}>{e(lab(t, k))}</option>' for k in SEL_KEYS)


def jsonld(lang, t, page):
    data = {'@context': 'https://schema.org', '@type': 'TaxiService', 'name': BRAND,
            'description': SCHEMA_DESC[lang], 'areaServed': {'@type': 'Place', 'name': 'Crete'},
            'availableLanguage': ['el', 'en', 'de', 'ru']}
    if BUSINESS['phone']:
        data['telephone'] = BUSINESS['phone']
    if BUSINESS['email']:
        data['email'] = BUSINESS['email']
    if BUSINESS['address']:
        data['address'] = BUSINESS['address']
    if BUSINESS['hours']:
        data['openingHours'] = BUSINESS['hours']
    same = [u for u in (BUSINESS['facebook'], BUSINESS['instagram']) if u]
    if same:
        data['sameAs'] = same
    blocks = [data]
    if page == 'faq':
        blocks.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]})
    return ''.join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)


# ---- pagine -----------------------------------------------------------------
def page_body(lang, t, page):
    if page == 'index':
        return (hero(t) + three(t) +
                f'<div class="bgband" data-bg="../img/lighthouse.webp" data-pos="50% 62%"><div class="inner"><h2>{e(t["hs"])}</h2><div class="grid">{cards(t["s"])}</div></div></div>\n' +
                cta_band(t))
    if page == 'services':
        vehicles = ''.join(f'<article class="card"><h3>{e(v)}</h3>{empty(t)}</article>' for v in t['vl'])
        return (band(t, 'road', '50% 88%', h1=t['hs'], lead=t['hsd']) +
                f'<section><div class="grid">{cards(t["s"])}</div><h2 style="margin-top:3rem">{e(t["veh"])}</h2><div class="grid">{vehicles}</div></section>\n')
    if page == 'routes':
        return (band(t, 'bay', '50% 50%', h1=t['rt'], lead=t['rsub']) +
                f'<section>{map_box(" style=\"margin-top:0\"")}<div class="grid">{route_cards(t)}</div></section>\n')
    if page == 'book':
        f = t['f']
        form = f'''<form id="bf" novalidate>
 <label for="bfrom">{e(f['from'])}<select id="bfrom" name="from">{options(t, 'her')}</select></label>
 <label for="bto">{e(f['to'])}<select id="bto" name="to">{options(t, 'che')}</select></label>
 <label for="bdate">{e(f['date'])}<input id="bdate" name="date" type="date" required></label>
 <label for="btime">{e(f['time'])}<input id="btime" name="time" type="time" required></label>
 <label for="bpax">{e(f['pax'])}<input id="bpax" name="pax" type="number" min="1" value="2"></label>
 <label for="bbags">{e(f['bags'])}<input id="bbags" name="bags" type="number" min="0" value="2"></label>
 <label for="bname">{e(f['name'])}<input id="bname" name="name" required autocomplete="name"></label>
 <label for="bemail">{e(f['email'])}<input id="bemail" name="email" type="email" required autocomplete="email"></label>
 <label for="bphone">{e(f['phone'])}<input id="bphone" name="phone" type="tel" autocomplete="tel"></label>
 <label for="blang">{e(f['lang'])}<select id="blang" name="language"><option>Ελληνικά</option><option>English</option><option>Deutsch</option><option>Русский</option></select></label>
 <label class="full" for="bnote">{e(f['note'])}<textarea id="bnote" name="note" rows="3"></textarea></label>
 <input class="trap" id="bhp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
 <div class="full"><button class="btn sun" type="submit">{e(t['send'])}</button></div>
 <p class="ok full" id="bok" hidden>{e(t['sent'])}</p>
</form>'''
        return (band(t, 'bay', '50% 40%', h1=t['bt'], lead=t['bsub']) +
                f'<section>{map_box(" style=\"margin-top:0\"")}{form}</section>\n')
    if page == 'about':
        return (band(t, 'lighthouse', '50% 64%', h1=t['at']) +
                f'<section><p>{e(t["ap1"])}</p><p class="empty" style="margin-top:.75rem">{e(t["ap2"])}</p>'
                f'<h2 style="margin-top:3rem">{e(t["whereT"])}</h2>'
                f'<dl><dt>{e(t["cl"]["addr"])}</dt><dd style="margin:0">{empty(t)}</dd><dt>{e(t["cl"]["hours"])}</dt><dd style="margin:0">{empty(t)}</dd></dl>'
                f'{map_box()}</section>\n')
    if page == 'faq':
        items = ''.join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faq'])
        return band(t, 'lighthouse', '50% 60%', h1=t['ft']) + f'<section><div>{items}</div></section>\n'
    if page == 'contact':
        keys = [('phone', 'phone'), ('email', 'email'), ('addr', 'address'), ('hours', 'hours')]
        rows = ''.join(f'<dt>{e(t["cl"][a])}</dt><dd style="margin:0">{e(BUSINESS[b]) if BUSINESS[b] else empty(t)}</dd>' for a, b in keys)
        soc = ''
        for name, key in (('Facebook', 'facebook'), ('Instagram', 'instagram')):
            if BUSINESS[key]:
                soc += f'<a href="{e(BUSINESS[key])}" rel="noopener" target="_blank">{name}</a>'
            else:
                soc += f'<a href="contact.html" aria-disabled="true" title="{e(t["empty"])}">{name}</a>'
        return (band(t, 'road', '50% 85%', h1=t['ct']) +
                f'<section><dl>{rows}</dl><h3>{e(t["cl"]["soc"])}</h3><div class="social">{soc}</div>'
                f'<p class="empty" style="margin-top:.5rem">{e(t["empty"])}</p></section>\n')
    raise ValueError(page)


def legal_body(lang, t, page):
    name = legal_name(lang, t, page)
    g = LG[lang]
    items = list(g[page])
    out = f'<p class="legal-note">{e(t["draft"])}</p>'
    if page == 'privacy':
        out += f'<p class="legal-note">{e(PRIVACY_NOTE[lang])}</p>'
    for h, txt in items:
        out += f'<h3>{e(h)}</h3><p>{e(txt)}</p>' if txt else f'<h3>{e(h)}</h3><p>{empty(t)}</p>'
    if page == 'impressum':
        out += '<dl>' + ''.join(f'<dt>{e(n)}</dt><dd style="margin:0">{empty(t)}</dd>' for n in g['fields']) + '</dl>'
    return band(t, 'lighthouse', '50% 60%', h1=name) + f'<section class="legal">{out}</section>\n'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8', newline='\n') as fh:
        fh.write(text)


def build():
    urls = []
    for lang in LANGS:
        t = L[lang]
        for page in PAGES + LEGAL:
            if page in PAGES:
                title, desc = t['seo'][NAVKEY[page]]
                body = page_body(lang, t, page)
                extra = jsonld(lang, t, page) if page in ('index', 'faq') else ''
            else:
                title = f'{legal_name(lang, t, page)} | {BRAND}'
                desc = t['draft']
                body = legal_body(lang, t, page)
                extra = ''
            doc = head(lang, t, page, title, desc, extra) + header(lang, t, page) + body + footer(lang, t, page) + scripts(lang, t, page)
            write(os.path.join(OUT, lang, f'{page}.html'), doc)
            urls.append((lang, page))

    # root: scelta della lingua
    links = ''.join(f'<li><a href="{l}/index.html" hreflang="{l}" lang="{l}">{n}</a></li>' for l, n in
                    (('el', 'Ελληνικά'), ('en', 'English'), ('de', 'Deutsch'), ('ru', 'Русский')))
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    write(os.path.join(OUT, 'index.html'), f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{BRAND}</title>{robots}
<link rel="canonical" href="{SITE_URL}/">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/index.html">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#04202f;color:#fff;font:1.2rem/1.5 system-ui,sans-serif}}
ul{{list-style:none;padding:0;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center}}
a{{display:inline-block;background:#ffc23c;color:#1a2a33;padding:.8rem 1.4rem;border-radius:.5rem;text-decoration:none;font-weight:700}}
main{{text-align:center;padding:1rem}}</style></head>
<body><main><h1>{BRAND}</h1><ul>{links}</ul></main>
<script>try{{var m={{el:1,en:1,de:1,ru:1}},l=(navigator.language||'').slice(0,2);if(m[l])location.replace(l+'/index.html')}}catch(e){{}}</script>
</body></html>
''')

    # favicon
    write(os.path.join(OUT, 'img', 'favicon.svg'),
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#04202f"/>'
          '<path d="M6 40q13-14 26 0t26 0v18H6z" fill="#ffc23c"/><path d="M6 32q13-14 26 0t26 0" fill="none" stroke="#ff6b4a" stroke-width="5" stroke-linecap="round"/></svg>')

    # sitemap + robots
    entries = ''
    for lang in LANGS:
        for page in PAGES:
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}/{l}/{page}.html"/>' for l in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{page}.html"/>'
            entries += f'<url><loc>{SITE_URL}/{lang}/{page}.html</loc>{alts}</url>\n'
    write(os.path.join(OUT, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + entries + '</urlset>\n')
    write(os.path.join(OUT, 'robots.txt'),
          ('# Sito non ancora pubblicato: tutto bloccato. Al lancio cancellare la riga Disallow e mettere NOINDEX=False in build_html.py\nUser-agent: *\nDisallow: /\n'
           if NOINDEX else 'User-agent: *\nAllow: /\n') + f'\nSitemap: {SITE_URL}/sitemap.xml\n')
    print(f'{len(urls)} pagine generate in {OUT}')


if __name__ == '__main__':
    build()
