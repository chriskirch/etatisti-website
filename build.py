#!/usr/bin/env python3
"""Build the Etatisti website from site.json into static HTML (GitHub Pages, repo root).

    python3 build.py            # refuses to build while the Impressum address is missing
    python3 build.py --draft    # builds anyway, Impressum shows a visible gap (never push a draft)

Pages: / (en), /de/, /it/, /sv/, impressum.html (de), privacy.html (en),
datenschutz.html (de), 404.html, sitemap.xml, robots.txt.
No cookies, no analytics, no external fonts, no embeds: every asset is served from this repo.
"""
import html, json, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
S = json.loads((ROOT / "site.json").read_text())
TP = json.loads((ROOT / "topics.json").read_text())
BASE = S["base_url"]
SITE_PATH = "/" + BASE.split("://",1)[1].split("/",1)[1]  # "/" on the custom domain
TODAY = date.today().isoformat()
DRAFT = "--draft" in sys.argv
if not S["legal_address"] and not DRAFT:
    sys.exit("build.py: legal_address missing in site.json (Impressum § 5 DDG) -- refusing to build")
e = html.escape

LANGS = {"en": "", "de": "de/", "it": "it/", "sv": "sv/"}
T = {
 "en": {"trio": "David · Cyborg · Cleopatra – the three Etatisti avatars", "madefor": "Made for", "tracklist": "Tracklist", "explore": "Explore", "about": "About", "tag": "Songs about politics, energy, the eye – and the limits we keep pushing.",
        "listen": "Listen now", "disco": "Discography", "soon": "Coming soon", "tracks": "tracks",
        "follow": "Follow", "legal": "Legal notice", "privacy": "Privacy", "contact": "Contact",
        "apple": "Apple Music", "all": "All platforms",
        "types": {"album": "Album", "ep": "EP", "single": "Single"},
        "desc": "Etatisti – songs about politics, energy, the eye and the limits we keep pushing. Listen on Spotify, Apple Music, YouTube and all platforms."},
 "de": {"trio": "David · Cyborg · Kleopatra – die drei Etatisti-Avatare", "madefor": "Gemacht für", "tracklist": "Titelliste", "explore": "Mehr dazu", "about": "Über Etatisti", "tag": "Songs über Politik, Energie, das Auge – und die Grenzen, die wir immer weiter verschieben.",
        "listen": "Jetzt hören", "disco": "Diskografie", "soon": "Demnächst", "tracks": "Titel",
        "follow": "Folgen", "legal": "Impressum", "privacy": "Datenschutz", "contact": "Kontakt",
        "apple": "Apple Music", "all": "Alle Plattformen",
        "types": {"album": "Album", "ep": "EP", "single": "Single"},
        "desc": "Etatisti – Songs über Politik, Energie, das Auge und die Grenzen, die wir verschieben. Auf Spotify, Apple Music, YouTube und allen Plattformen."},
 "it": {"trio": "David · Cyborg · Cleopatra – i tre avatar di Etatisti", "madefor": "Pensato per", "tracklist": "Tracce", "explore": "Scopri", "about": "Chi è Etatisti", "tag": "Canzoni sulla politica, l’energia, l’occhio – e i limiti che continuiamo a spostare.",
        "listen": "Ascolta ora", "disco": "Discografia", "soon": "In arrivo", "tracks": "brani",
        "follow": "Segui", "legal": "Note legali", "privacy": "Privacy", "contact": "Contatto",
        "apple": "Apple Music", "all": "Tutte le piattaforme",
        "types": {"album": "Album", "ep": "EP", "single": "Singolo"},
        "desc": "Etatisti – canzoni sulla politica, l’energia, l’occhio e i limiti che spostiamo. Su Spotify, Apple Music, YouTube e tutte le piattaforme."},
 "sv": {"trio": "David · Cyborg · Kleopatra – Etatistis tre avatarer", "madefor": "Gjord för", "tracklist": "Låtlista", "explore": "Utforska", "about": "Om Etatisti", "tag": "Låtar om politik, energi, ögat – och gränserna vi hela tiden flyttar.",
        "listen": "Lyssna nu", "disco": "Diskografi", "soon": "Kommer snart", "tracks": "låtar",
        "follow": "Följ", "legal": "Juridisk information", "privacy": "Integritet", "contact": "Kontakt",
        "apple": "Apple Music", "all": "Alla plattformar",
        "types": {"album": "Album", "ep": "EP", "single": "Singel"},
        "desc": "Etatisti – låtar om politik, energi, ögat och gränserna vi flyttar. Lyssna på Spotify, Apple Music, YouTube och alla plattformar."},
}
L = S["links"]
SOCIAL = [("Spotify", L["spotify"]), ("Apple Music", L["apple"]), ("YouTube", L["youtube"]), ("Instagram", L["instagram"])]

CSS = """:root{--bg:#07090f;--card:#0f1320;--fg:#e8ecf2;--muted:#8a94a6;--line:#1c2233;--a1:#3ddc97;--a2:#7b5cff}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.6;overflow-x:hidden}
a{color:var(--a1)}
.aurora{position:fixed;inset:-20% -10% auto -10%;height:70vh;background:radial-gradient(ellipse at 30% 60%,rgba(61,220,151,.26),transparent 60%),radial-gradient(ellipse at 70% 40%,rgba(123,92,255,.24),transparent 60%);filter:blur(40px);animation:drift 18s ease-in-out infinite alternate;z-index:0;pointer-events:none}
@keyframes drift{to{transform:translateX(6%) skewX(-6deg)}}
@media (prefers-reduced-motion:reduce){.aurora{animation:none}}
.wrap{position:relative;z-index:1;max-width:1040px;margin:0 auto;padding:0 16px}
nav{display:flex;justify-content:flex-end;gap:14px;padding:18px 0;font-size:.85rem}
nav a{color:var(--muted);text-decoration:none}nav a[aria-current]{color:var(--fg)}
.hero{text-align:center;padding:72px 0 56px}
.logo{font-family:"Trajan Pro",Cinzel,Georgia,serif;font-weight:600;font-size:clamp(3rem,12vw,7rem);letter-spacing:.18em;margin:0 0 .2em;padding-left:.18em;line-height:1.1}
.tag{color:var(--muted);font-size:1.1rem;max-width:36ch;margin:0 auto 2.2rem}
.btn{display:inline-block;padding:14px 32px;border-radius:999px;background:linear-gradient(90deg,var(--a1),var(--a2));color:#07090f;font-weight:600;text-decoration:none;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}
.social{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:22px}
.social a{color:var(--fg);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:7px 16px;font-size:.9rem}
.social a:hover{border-color:var(--a1)}
h2{font-size:1.3rem;letter-spacing:.06em;margin:48px 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px}
.rel{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.rel img{width:100%;height:auto;aspect-ratio:1;object-fit:cover;display:block;background:#111}
.rel .b{padding:12px 14px 14px;display:flex;flex-direction:column;gap:2px;flex:1}
.rel h3{font-size:1rem;margin:0;line-height:1.3}
.rel .m{color:var(--muted);font-size:.82rem}
.rel .l{margin-top:auto;padding-top:8px;display:flex;gap:12px;font-size:.85rem}
.soon{display:inline-block;align-self:flex-start;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#07090f;background:var(--a1);border-radius:6px;padding:1px 7px;margin-bottom:4px}
footer{position:relative;z-index:1;text-align:center;padding:56px 16px 28px;color:var(--muted);font-size:.85rem}
footer a{color:var(--muted)}
.doc{max-width:720px}.doc h1{font-size:1.8rem;margin:1em 0 .2em}.doc h2{font-size:1.1rem;margin:2em 0 .3em;letter-spacing:0}
.home{font-family:"Trajan Pro",Cinzel,Georgia,serif;letter-spacing:.18em;text-decoration:none;color:var(--fg)}
.bio{display:grid;grid-template-columns:minmax(0,340px) 1fr;gap:32px;align-items:start}
.trio{margin:0}.trio video{width:100%;height:auto;border-radius:14px;display:block;background:#111}.trio figcaption{color:var(--muted);font-size:.8rem;margin-top:8px;text-align:center}
@media (max-width:720px){.bio{grid-template-columns:1fr}.trio{max-width:420px;margin:0 auto}}
.about{max-width:68ch}.about p{color:#c9d0dc;margin:0 0 1em}
.topic h2 a{color:var(--fg);text-decoration:none}.topic h2 a:hover{color:var(--a1)}.topic .more{font-size:.9rem}
.aud{columns:2 260px;padding-left:1.2em;color:#c9d0dc}.album{display:grid;grid-template-columns:minmax(0,280px) 1fr;gap:24px;margin:28px 0;align-items:start}
.album img{width:100%;height:auto;border-radius:12px}.album ol{padding-left:1.4em;color:#c9d0dc}.album ol span{color:var(--muted);font-size:.85em}
@media (max-width:640px){.album{grid-template-columns:1fr}}
.muted{color:var(--muted)}.gap{background:#5a1a1a;color:#fff;padding:2px 6px;border-radius:4px}
"""


def head(lang, title, desc, path, prefix, alternates=None, jsonld=None, noindex=False):
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in alternates.items())
        alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{BASE}{path}">{alt}
<meta property="og:type" content="website"><meta property="og:site_name" content="Etatisti">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07090f">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}img/apple-touch-icon.png">
<link rel="stylesheet" href="{prefix}style.css">
{ld}
</head>
<body>
<div class="aurora" aria-hidden="true"></div>
"""


def footer(lang, prefix):
    t = T[lang]
    priv = "datenschutz.html" if lang == "de" else "privacy.html"
    langs = " · ".join(f'<a href="{prefix}{p}" hreflang="{l}" lang="{l}">{l.upper()}</a>' for l, p in LANGS.items())
    return f"""<footer>
© {date.today().year} Etatisti · <a href="{prefix}impressum.html">{t['legal']}</a> · <a href="{prefix}{priv}">{t['privacy']}</a> · <a href="mailto:{S['email']}">{t['contact']}</a><br>
<span>{langs}</span>
</footer>
</body>
</html>
"""


def fmt_date(d, lang):
    y, m, dd = d.split("-")
    return f"{dd}.{m}.{y}" if lang in ("de", "sv", "it") else f"{y}-{m}-{dd}"


def release_card(r, lang, prefix):
    t = T[lang]
    name = r["title"] + (f" ({r['edition']})" if r.get("edition") else "")
    feat = f" · feat. {e(r['feat'])}" if r.get("feat") else ""
    meta = f"{t['types'][r['type']]} · {r['tracks']} {t['tracks']}{feat}"
    if r["date"]:
        meta += f" · {fmt_date(r['date'], lang)}"
        links = (f'<a href="{e(r["apple"])}" rel="noopener">{t["apple"]}</a>' if r.get("apple") else "") + \
                f'<a href="{L["hyperfollow"]}" rel="noopener">{t["all"]}</a>'
        badge = ""
    else:
        links, badge = "", f'<span class="soon">{t["soon"]}</span>'
    return f"""<article class="rel"><img src="{prefix}img/{r['img']}.webp" alt="{e(name)} – cover" width="600" height="600" loading="lazy">
<div class="b">{badge}<h3>{e(name)}</h3><span class="m">{meta}</span><div class="l">{links}</div></div></article>"""


def jsonld_artist():
    return {"@context": "https://schema.org", "@type": "MusicGroup", "name": "Etatisti", "url": BASE, "description": S["description"]["en"],
            "image": BASE + "img/og.jpg", "sameAs": [u for _, u in SOCIAL] + [L["hyperfollow"]],
            "album": [{"@type": "MusicAlbum", "name": r["title"] + (f" ({r['edition']})" if r.get("edition") else ""),
                       "numTracks": r["tracks"], "datePublished": r["date"], "image": f"{BASE}img/{r['img']}.webp",
                       **({"url": r["apple"]} if r.get("apple") else {})}
                      for r in S["releases"] if r["date"]]}


def home(lang):
    t, path = T[lang], LANGS[lang]
    prefix = "../" if path else ""
    nav = "".join(f'<a href="{prefix}{p}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l, p in LANGS.items())
    social = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL)
    body = f"""<div class="wrap">
<nav aria-label="Language">{nav}</nav>
<header class="hero">
<h1 class="logo">ETATISTI</h1>
<p class="tag">{e(S['tagline'][lang])}</p>
<a class="btn" href="{L['hyperfollow']}" rel="noopener">{t['listen']}</a>
<div class="social" aria-label="{t['follow']}">{social}</div>
</header>
<main>
<section id="about"><h2>{t['about']}</h2>
<div class="bio">
<figure class="trio"><video autoplay muted loop playsinline preload="metadata" poster="{prefix}img/trio-poster.webp" width="600" height="600" aria-label="{e(t['trio'])}"><source src="{prefix}img/trio.mp4" type="video/mp4"></video><figcaption>{e(t['trio'])}</figcaption></figure>
<div class="about">{''.join(f'<p>{e(x)}</p>' for x in S['bio'][lang])}</div>
</div>
</section>
<script>if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.querySelectorAll('video').forEach(v=>{{v.removeAttribute('autoplay');v.pause()}})</script>
{topic_sections(lang, prefix)}
</main>
</div>
"""
    doc = head(lang, "Etatisti", S["description"][lang], path, prefix,
               alternates={l: p for l, p in LANGS.items()}, jsonld=jsonld_artist()) + body + footer(lang, prefix)
    out_path = ROOT / path / "index.html"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(doc)


def addr_html():
    if S["legal_address"]:
        return "<br>".join(e(x) for x in S["legal_address"])
    return '<span class="gap">[c/o address missing – do not publish]</span>'


def doc_page(fname, lang, title, desc, body):
    page = head(lang, title, desc, fname, "") + f'<div class="wrap doc"><nav><a class="home" href="./">ETATISTI</a></nav><main>{body}</main></div>' + footer(lang, "")
    (ROOT / fname).write_text(page)


def impressum():
    n, m = e(S["legal_name"]), S["email"]
    body = f"""<h1>Impressum</h1>
<p class="muted">Legal notice (German law, § 5 DDG)</p>
<h2>Angaben gemäß § 5 DDG</h2>
<p>{n}<br>{addr_html()}</p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:{m}">{m}</a></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>{n}, Anschrift wie oben</p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Links</h2>
<p>Diese Seite verlinkt auf Angebote Dritter (z.&nbsp;B. Streaming-Dienste). Für deren Inhalte ist der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entfernen wir entsprechende Links umgehend.</p>
<h2>Urheberrecht</h2>
<p>Musik, Texte und Artwork von Etatisti sind urheberrechtlich geschützt. Jede Verwertung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen Zustimmung.</p>"""
    doc_page("impressum.html", "de", "Impressum – Etatisti", "Impressum von Etatisti nach § 5 DDG.", body)


def privacy_en():
    n, m = e(S["legal_name"]), S["email"]
    body = f"""<h1>Privacy Policy</h1>
<p class="muted">Last updated: {TODAY} · <a href="datenschutz.html" hreflang="de">Deutsche Fassung</a></p>
<h2>1. Controller</h2>
<p>{n}<br>{addr_html()}<br>E-mail: <a href="mailto:{m}">{m}</a></p>
<h2>2. Hosting</h2>
<p>This website is hosted on GitHub Pages (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). When you open a page, GitHub processes technical access data, in particular your IP address, to deliver the site and keep it secure (Art. 6(1)(f) GDPR). This may involve a transfer to the USA. Details: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub Privacy Statement</a>.</p>
<h2>3. No cookies, no tracking</h2>
<p>This website sets no cookies, uses no analytics or tracking tools, loads no external fonts and embeds no third-party players. All images and files are served from the same host.</p>
<h2>4. Links to streaming services and social networks</h2>
<p>Links to Spotify, Apple Music, YouTube, Instagram and HyperFollow (DistroKid) are plain links. No data is transmitted to these services until you click a link; after that, the privacy policy of the respective service applies.</p>
<h2>5. Contact by e-mail</h2>
<p>If you write to us, we use your e-mail address and message only to answer you (Art. 6(1)(b) and (f) GDPR) and delete them once they are no longer needed, unless statutory retention periods apply.</p>
<h2>6. Etatisti Autoloop (Google API use)</h2>
<p>Etatisti Autoloop is a private tool used only by its owner to upload videos to the owner's own Etatisti YouTube channel. It is not offered to the public and has no other users.</p>
<ul>
<li><b>Data accessed:</b> the app requests only the Google OAuth scope <code>youtube.upload</code> for the owner's own channel. It does not access data of any other Google user.</li>
<li><b>Storage:</b> the OAuth token is stored only on the owner's private server. It is not shared with, transferred to or sold to third parties.</li>
<li><b>Revoking access:</b> access can be revoked at any time at <a href="https://myaccount.google.com/permissions" rel="noopener">myaccount.google.com/permissions</a>.</li>
</ul>
<p>Etatisti Autoloop's use and transfer of information received from Google APIs adheres to the <a href="https://developers.google.com/terms/api-services-user-data-policy" rel="noopener">Google API Services User Data Policy</a>, including the Limited Use requirements.</p>
<h2>7. Your rights</h2>
<p>You have the right to access (Art. 15 GDPR), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and to object to processing based on Art. 6(1)(f) (Art. 21). You also have the right to lodge a complaint with a data protection supervisory authority (Art. 77 GDPR), in particular in the member state of your residence.</p>"""
    doc_page("privacy.html", "en", "Privacy Policy – Etatisti", "Privacy policy of the Etatisti website and the Etatisti Autoloop app.", body)


def privacy_de():
    n, m = e(S["legal_name"]), S["email"]
    body = f"""<h1>Datenschutzerklärung</h1>
<p class="muted">Stand: {fmt_date(TODAY, 'de')} · <a href="privacy.html" hreflang="en">English version</a></p>
<h2>1. Verantwortlicher</h2>
<p>{n}<br>{addr_html()}<br>E-Mail: <a href="mailto:{m}">{m}</a></p>
<h2>2. Hosting</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf einer Seite verarbeitet GitHub technische Zugriffsdaten, insbesondere Ihre IP-Adresse, um die Seite auszuliefern und die Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO). Dabei kann eine Übermittlung in die USA erfolgen. Einzelheiten: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub-Datenschutzerklärung</a>.</p>
<h2>3. Keine Cookies, kein Tracking</h2>
<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Werkzeuge, lädt keine externen Schriftarten und bindet keine Player Dritter ein. Alle Bilder und Dateien werden vom selben Server ausgeliefert.</p>
<h2>4. Links zu Streaming-Diensten und sozialen Netzwerken</h2>
<p>Links zu Spotify, Apple Music, YouTube, Instagram und HyperFollow (DistroKid) sind einfache Links. Erst wenn Sie einen Link anklicken, werden Daten an den jeweiligen Dienst übertragen; ab dann gilt dessen Datenschutzerklärung.</p>
<h2>5. Kontakt per E-Mail</h2>
<p>Wenn Sie uns schreiben, verwenden wir Ihre E-Mail-Adresse und Nachricht ausschließlich zur Beantwortung (Art. 6 Abs. 1 lit. b und f DSGVO) und löschen sie, sobald sie nicht mehr erforderlich sind, soweit keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>6. Etatisti Autoloop (Nutzung von Google-APIs)</h2>
<p>Etatisti Autoloop ist ein privates Werkzeug, das ausschließlich vom Inhaber genutzt wird, um Videos auf den eigenen YouTube-Kanal Etatisti hochzuladen. Es wird nicht öffentlich angeboten und hat keine weiteren Nutzer. Die App fordert nur den Google-OAuth-Bereich <code>youtube.upload</code> für den eigenen Kanal an; das Token wird ausschließlich auf dem privaten Server des Inhabers gespeichert und nicht an Dritte weitergegeben. Der Zugriff kann jederzeit unter <a href="https://myaccount.google.com/permissions" rel="noopener">myaccount.google.com/permissions</a> widerrufen werden. Die Nutzung von Informationen aus Google-APIs erfolgt gemäß der <a href="https://developers.google.com/terms/api-services-user-data-policy" rel="noopener">Google API Services User Data Policy</a> einschließlich der Limited-Use-Anforderungen.</p>
<h2>7. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen nach Art. 6 Abs. 1 lit. f (Art. 21). Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO), insbesondere in dem Mitgliedstaat Ihres Aufenthaltsorts.</p>"""
    doc_page("datenschutz.html", "de", "Datenschutzerklärung – Etatisti", "Datenschutzerklärung der Etatisti-Website und der App Etatisti Autoloop.", body)


def extras():
    (ROOT / "style.css").write_text(CSS)
    (ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#3ddc97"/><stop offset="1" stop-color="#7b5cff"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="#07090f"/><text x="32" y="45" font-family="Georgia,serif" font-size="38" font-weight="600" text-anchor="middle" fill="url(#g)">E</text></svg>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{p}"/>' for l, p in LANGS.items())
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>{alts}</url>" for p in LANGS.values())
    for key in TP["order"]:
        sl = TP["topics"][key]["slug"]
        ta = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{p}{sl}/"/>' for l, p in LANGS.items())
        urls += "".join(f"<url><loc>{BASE}{p}{sl}/</loc><lastmod>{TODAY}</lastmod>{ta}</url>" for p in LANGS.values())
    urls += "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in ("impressum.html", "privacy.html", "datenschutz.html"))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + "</urlset>\n")
    nf = head("en", "Not found – Etatisti", "Page not found.", "404.html", SITE_PATH, noindex=True) + \
        '<div class="wrap"><header class="hero"><h1 class="logo">404</h1><p class="tag">This page does not exist.</p><a class="btn" href="' + SITE_PATH + '">Etatisti</a></header></div>' + footer("en", SITE_PATH)
    (ROOT / "404.html").write_text(nf)
    (ROOT / ".nojekyll").write_text("")
    host = BASE.split("://", 1)[1].strip("/")
    if "github.io" not in host:
        (ROOT / "CNAME").write_text(host + "\n")


def rel_sorted(key):
    rs = [r for r in S["releases"] if r["topic"] == key]
    return [r for r in rs if not r["date"]] + [r for r in rs if r["date"]]


def topic_sections(lang, prefix):
    out = []
    for key in TP["order"]:
        tp, tl = TP["topics"][key], TP["topics"][key][lang]
        cards = "\n".join(release_card(r, lang, prefix) for r in rel_sorted(key))
        out.append(f"""<section class="topic" id="{tp['slug']}"><h2><a href="{prefix}{LANGS[lang]}{tp['slug']}/">{e(tl['name'])}</a></h2>
<p class="muted">{e(tl['desc'])} <a class="more" href="{prefix}{LANGS[lang]}{tp['slug']}/">{T[lang]['explore']} →</a></p>
<div class="grid">
{cards}
</div></section>""")
    return "\n".join(out)


def iso_dur(s):
    return f"PT{s // 60}M{s % 60}S"


def album_ld(r):
    name = r["title"] + (f" ({r['edition']})" if r.get("edition") else "")
    d = {"@type": "MusicAlbum", "name": name, "byArtist": {"@type": "MusicGroup", "name": "Etatisti", "url": BASE},
         "image": f"{BASE}img/{r['img']}.webp", "numTracks": r["tracks"], "inLanguage": r["song_lang"],
         "albumReleaseType": {"album": "AlbumRelease", "ep": "EPRelease", "single": "SingleRelease"}[r["type"]]}
    if r.get("date"): d["datePublished"] = r["date"]
    if r.get("genre"): d["genre"] = r["genre"]
    if r.get("apple"): d["url"] = r["apple"]; d["sameAs"] = [r["apple"], L["hyperfollow"]]
    if r.get("tracklist"):
        d["track"] = {"@type": "ItemList", "numberOfItems": len(r["tracklist"]), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "MusicRecording", "name": n, "duration": iso_dur(s), "byArtist": {"@type": "MusicGroup", "name": "Etatisti"}}}
            for i, (n, s) in enumerate(r["tracklist"])]}
    return d


def topic_page(lang, key):
    tp, tl, t = TP["topics"][key], TP["topics"][key][lang], T[lang]
    path = LANGS[lang] + tp["slug"] + "/"
    prefix = "../" * path.count("/")
    alts = {l: p + tp["slug"] + "/" for l, p in LANGS.items()}
    nav = "".join(f'<a href="{prefix}{p}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l, p in alts.items())
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": tl["title"], "description": tl["desc"], "url": BASE + path,
          "inLanguage": lang, "keywords": ", ".join(tp["keywords"]), "about": tl["name"],
          "audience": {"@type": "Audience", "audienceType": "; ".join(tl["audience"])},
          "isPartOf": {"@type": "WebSite", "name": "Etatisti", "url": BASE},
          "hasPart": [album_ld(r) for r in rel_sorted(key)]}
    albums = []
    for r in rel_sorted(key):
        name = r["title"] + (f" ({r['edition']})" if r.get("edition") else "")
        feat = f" · feat. {e(r['feat'])}" if r.get("feat") else ""
        meta = f"{t['types'][r['type']]} · {r['tracks']} {t['tracks']}{feat}" + (f" · {fmt_date(r['date'], lang)}" if r["date"] else "") + (f" · {e(r['genre'])}" if r.get("genre") else "")
        links = (f'<a href="{e(r["apple"])}" rel="noopener">{t["apple"]}</a> · <a href="{L["hyperfollow"]}" rel="noopener">{t["all"]}</a>' if r["date"] and r.get("apple") else f'<span class="soon">{t["soon"]}</span>')
        tracks = "".join(f"<li>{e(n)} <span>{s // 60}:{s % 60:02d}</span></li>" for n, s in r.get("tracklist", []))
        tl_html = f"<h3>{t['tracklist']}</h3><ol>{tracks}</ol>" if tracks else ""
        albums.append(f"""<article class="album" id="{r['img']}"><img src="{prefix}img/{r['img']}.webp" alt="{e(name)} – cover" width="600" height="600" loading="lazy">
<div><h2>{e(name)}</h2><p class="muted">{meta}</p><p>{links}</p>{tl_html}</div></article>""")
    body = f"""<div class="wrap">
<nav aria-label="Language"><a class="home" href="{prefix}{LANGS[lang]}" style="margin-right:auto">ETATISTI</a>{nav}</nav>
<main class="doc" style="max-width:none">
<h1>{e(tl['name'])}</h1>
<p class="about" style="font-size:1.05rem">{e(tl['intro'])}</p>
<h2>{t['madefor']}</h2>
<ul class="aud">{''.join(f'<li>{e(a)}</li>' for a in tl['audience'])}</ul>
{''.join(albums)}
</main>
</div>
"""
    doc = head(lang, tl["title"], tl["desc"], path, prefix, alternates=alts, jsonld=ld) + body + footer(lang, prefix)
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)


for lang in LANGS:
    home(lang)
    for key in TP['order']:
        topic_page(lang, key)
impressum(); privacy_en(); privacy_de(); extras()
print("built" + (" (DRAFT – Impressum address missing, do not push)" if DRAFT else ""))
