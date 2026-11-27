#!/usr/bin/env python3
"""Static site generator for worthtrail.app (13 languages × 6 pages = 78 pages).

Zero external dependencies. Reads content/<lang>.json and writes static HTML
pages plus sitemap.xml into docs/.
"""

from __future__ import annotations

import html
import json
import pathlib
import sys
import urllib.parse
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DOCS_DIR = ROOT / "docs"
SITE_ORIGIN = "https://worthtrail.app"
APP_STORE_URL = "https://apps.apple.com/app/id6777620163"
SUPPORT_EMAIL = "support@worthtrail.app"
LASTMOD = "2026-11-27"

LANGUAGES = [
    {"id": "en", "prefix": "", "hreflang": "en", "html_lang": "en", "name": "English", "short": "EN", "screen": "en"},
    {"id": "zh-Hans", "prefix": "/zh", "hreflang": "zh-Hans", "html_lang": "zh-Hans", "name": "简体中文", "short": "中文", "screen": "zh"},
    {"id": "de", "prefix": "/de", "hreflang": "de", "html_lang": "de", "name": "Deutsch", "short": "DE", "screen": "en"},
    {"id": "fr", "prefix": "/fr", "hreflang": "fr", "html_lang": "fr", "name": "Français", "short": "FR", "screen": "en"},
    {"id": "es", "prefix": "/es", "hreflang": "es", "html_lang": "es", "name": "Español", "short": "ES", "screen": "en"},
    {"id": "it", "prefix": "/it", "hreflang": "it", "html_lang": "it", "name": "Italiano", "short": "IT", "screen": "en"},
    {"id": "pt-PT", "prefix": "/pt-pt", "hreflang": "pt-PT", "html_lang": "pt-PT", "name": "Português", "short": "PT", "screen": "en"},
    {"id": "nl", "prefix": "/nl", "hreflang": "nl", "html_lang": "nl", "name": "Nederlands", "short": "NL", "screen": "en"},
    {"id": "sv", "prefix": "/sv", "hreflang": "sv", "html_lang": "sv", "name": "Svenska", "short": "SV", "screen": "en"},
    {"id": "da", "prefix": "/da", "hreflang": "da", "html_lang": "da", "name": "Dansk", "short": "DA", "screen": "en"},
    {"id": "no", "prefix": "/no", "hreflang": "no", "html_lang": "no", "name": "Norsk", "short": "NO", "screen": "en"},
    {"id": "fi", "prefix": "/fi", "hreflang": "fi", "html_lang": "fi", "name": "Suomi", "short": "FI", "screen": "en"},
    {"id": "ru", "prefix": "/ru", "hreflang": "ru", "html_lang": "ru", "name": "Русский", "short": "RU", "screen": "en"},
]

PAGES = ["home", "faq", "vs", "mcp", "support", "privacy"]


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


def page_path(lang_cfg: dict, page: str) -> str:
    prefix = lang_cfg["prefix"]
    if page == "home":
        return f"{prefix}/" if prefix else "/"
    return f"{prefix}/{page}/"


def page_url(lang_cfg: dict, page: str) -> str:
    return f"{SITE_ORIGIN}{page_path(lang_cfg, page)}"


def output_file(lang_cfg: dict, page: str) -> pathlib.Path:
    rel = page_path(lang_cfg, page).lstrip("/")
    return DOCS_DIR / rel / "index.html" if rel else DOCS_DIR / "index.html"


def render_hreflangs(page: str) -> str:
    lines = []
    for cfg in LANGUAGES:
        lines.append(
            f'  <link rel="alternate" hreflang="{cfg["hreflang"]}" href="{page_url(cfg, page)}">'
        )
    lines.append(
        f'  <link rel="alternate" hreflang="x-default" href="{page_url(LANGUAGES[0], page)}">'
    )
    return "\n".join(lines)


def render_header(lang_cfg: dict, data: dict, current_page: str) -> str:
    nav = data["nav"]

    def nav_link(page: str, label: str) -> str:
        cur = ' aria-current="page"' if current_page == page else ""
        return f'<a href="{page_path(lang_cfg, page)}"{cur}>{e(label)}</a>'

    desktop_langs = []
    mobile_langs = []
    for cfg in LANGUAGES:
        is_cur = ' aria-current="true"' if cfg["id"] == lang_cfg["id"] else ""
        href = page_path(cfg, current_page)
        desktop_langs.append(
            f'            <a href="{href}"{is_cur}><span>{e(cfg["name"])}</span><span class="lang-code">{e(cfg["short"])}</span></a>'
        )
        mobile_langs.append(
            f'              <a href="{href}"{is_cur}>{e(cfg["name"])}</a>'
        )

    return f"""  <header class="site-header">
    <div class="nav-wrap">
      <a class="brand" href="{page_path(lang_cfg, 'home')}">
        <img src="/assets/icon-192.png" alt="{e(nav['brand_alt'])}" width="28" height="28">
        <span>WorthTrail</span>
      </a>
      <nav class="nav-links" aria-label="{e(nav['aria_label'])}">
        {nav_link('home', nav['overview'])}
        {nav_link('faq', nav['faq'])}
        {nav_link('vs', nav['compare'])}
        {nav_link('mcp', nav['mcp'])}
        {nav_link('support', nav['support'])}
        {nav_link('privacy', nav['privacy'])}
        <details class="lang-menu">
          <summary aria-label="{e(nav['language_label'])}">{e(lang_cfg['short'])} &#9662;</summary>
          <div class="lang-menu-panel">
{chr(10).join(desktop_langs)}
          </div>
        </details>
        <a class="nav-cta" href="{APP_STORE_URL}" rel="noopener">App Store</a>
      </nav>
      <details class="mobile-nav">
        <summary>{e(nav['menu'])}</summary>
        <div class="mobile-menu-panel">
          {nav_link('home', nav['overview'])}
          {nav_link('faq', nav['faq_long'])}
          {nav_link('vs', nav['compare_long'])}
          {nav_link('mcp', nav['mcp_long'])}
          {nav_link('support', nav['support'])}
          {nav_link('privacy', nav['privacy_long'])}
          <details class="mobile-lang">
            <summary>{e(nav['language_label'])} · {e(lang_cfg['name'])}</summary>
            <div class="mobile-lang-grid">
{chr(10).join(mobile_langs)}
            </div>
          </details>
          <a class="btn btn-primary" href="{APP_STORE_URL}" rel="noopener">{e(nav['download_cta'])}</a>
        </div>
      </details>
    </div>
  </header>"""


def render_footer(lang_cfg: dict, data: dict, current_page: str) -> str:
    nav = data["nav"]
    links = [f'<a href="{APP_STORE_URL}" rel="noopener">App Store</a>']
    for page, key in [
        ("home", "overview"),
        ("faq", "faq"),
        ("vs", "compare"),
        ("mcp", "mcp"),
        ("privacy", "privacy_long"),
        ("support", "support"),
    ]:
        if page != current_page:
            links.append(f'<a href="{page_path(lang_cfg, page)}">{e(nav[key])}</a>')
    links.append(f'<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>')

    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        {(chr(10) + '        ').join(links)}
      </div>
      <p class="disclaimer">{e(data['footer']['disclaimer'])}</p>
    </div>
  </footer>"""


def render_head(
    lang_cfg: dict,
    page: str,
    title: str,
    description: str,
    og_title: str | None = None,
    og_description: str | None = None,
    og_image: str | None = None,
    json_ld: dict | None = None,
) -> str:
    canonical = page_url(lang_cfg, page)
    og_block = ""
    if og_title:
        img_tag = f'\n  <meta property="og:image" content="{e(og_image)}">\n  <meta name="twitter:card" content="summary_large_image">' if og_image else ""
        og_block = f"""
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="WorthTrail">
  <meta property="og:title" content="{e(og_title)}">
  <meta property="og:description" content="{e(og_description or description)}">
  <meta property="og:url" content="{canonical}">{img_tag}"""

    ld_block = ""
    if json_ld:
        ld_json = json.dumps(json_ld, ensure_ascii=False, indent=2)
        indented = "\n".join("  " + line for line in ld_json.splitlines())
        ld_block = f'\n  <script type="application/ld+json">\n{indented}\n  </script>'

    return f"""<!DOCTYPE html>
<html lang="{lang_cfg['html_lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{canonical}">
{render_hreflangs(page)}
  <link rel="icon" type="image/png" href="/assets/icon-192.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">{og_block}
  <link rel="stylesheet" href="/assets/style.css">{ld_block}
</head>"""


def render_home(lang_cfg: dict, data: dict) -> str:
    h = data["home"]
    sc = lang_cfg["screen"]
    overview_img = f"{SITE_ORIGIN}/assets/screens/{sc}-overview.jpg"

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": "WorthTrail",
                "inLanguage": lang_cfg["html_lang"],
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "iOS, iPadOS, macOS",
                "url": page_url(lang_cfg, "home"),
                "downloadUrl": APP_STORE_URL,
                "installUrl": APP_STORE_URL,
                "image": overview_img,
                "screenshot": [
                    f"{SITE_ORIGIN}/assets/screens/{sc}-overview.jpg",
                    f"{SITE_ORIGIN}/assets/screens/{sc}-returns.jpg",
                    f"{SITE_ORIGIN}/assets/screens/{sc}-dividends.jpg",
                    f"{SITE_ORIGIN}/assets/screens/{sc}-composition.jpg",
                    f"{SITE_ORIGIN}/assets/screens/{sc}-ai.jpg",
                ],
                "description": h["meta_description"],
                "offers": [
                    {"@type": "Offer", "name": h["offers"][0], "price": "0", "priceCurrency": h["offer_currency"]},
                    {"@type": "Offer", "name": h["offers"][1], "price": h["offer_prices"][0], "priceCurrency": h["offer_currency"]},
                    {"@type": "Offer", "name": h["offers"][2], "price": h["offer_prices"][1], "priceCurrency": h["offer_currency"]},
                    {"@type": "Offer", "name": h["offers"][3], "price": h["offer_prices"][2], "priceCurrency": h["offer_currency"]},
                ],
            },
            {
                "@type": "Organization",
                "name": "WorthTrail",
                "url": f"{SITE_ORIGIN}/",
                "logo": f"{SITE_ORIGIN}/assets/icon-192.png",
                "email": SUPPORT_EMAIL,
                "sameAs": [APP_STORE_URL, "https://github.com/happy-xjb/WorthTrail-Support"],
            },
        ],
    }

    trust_html = "\n          ".join(f"<span>{e(item)}</span>" for item in h["hero_trust"])
    kpi_html = "\n      ".join(
        f"""<div class="kpi-item">
        <div class="kpi-val{' nums' if k.get('nums') else ''}">{e(k['val'])}</div>
        <div class="kpi-lbl">{e(k['lbl'])}</div>
      </div>"""
        for k in h["kpis"]
    )
    screen_files = ["returns", "dividends", "composition", "ai"]
    screens_html = "\n          ".join(
        f"""<figure class="screen-card">
            <div class="screen-shot">
              <img src="/assets/screens/{sc}-{sf}.jpg" alt="{e(item['alt'])}" loading="lazy">
            </div>
            <figcaption>
              <strong>{e(item['title'])}</strong>
              <span>{e(item['desc'])}</span>
            </figcaption>
          </figure>"""
        for sf, item in zip(screen_files, h["screens"])
    )
    pillars_html = "\n          ".join(
        f"""<div class="pillar">
            <div class="pillar-num">{e(p['num'])}</div>
            <h3>{e(p['title'])}</h3>
            <p>{e(p['desc'])}</p>
          </div>"""
        for p in h["pillars"]
    )
    plans_html = "\n          ".join(
        f"""<div class="plan{' featured' if pl.get('featured') else ''}">
            <div class="plan-tag">{e(pl['tag'])}</div>
            <div class="plan-price nums">{e(pl['price'])}{' <span>' + e(pl['unit']) + '</span>' if pl.get('unit') else ''}</div>
            <p>{e(pl['desc'])}</p>
          </div>"""
        for pl in h["plans"]
    )
    explore_html = "\n          ".join(
        f'<li><a href="{page_path(lang_cfg, item["page"]) if item.get("page") else item["href"]}">{e(item["title"])}</a> — {e(item["desc"])}</li>'
        for item in h["explore_items"]
    )

    head = render_head(
        lang_cfg,
        "home",
        h["title"],
        h["meta_description"],
        og_title=h["og_title"],
        og_description=h["og_description"],
        og_image=overview_img,
        json_ld=json_ld,
    )
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'home')}

  <section class="hero">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">{e(h['hero_eyebrow'])}</p>
        <h1>{e(h['hero_h1'])}</h1>
        <p class="lead">{h['hero_lead_html']}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{APP_STORE_URL}" rel="noopener">{e(h['cta_primary'])}</a>
          <a class="btn btn-secondary" href="{page_path(lang_cfg, 'vs')}">{e(h['cta_secondary'])}</a>
        </div>
        <div class="hero-trust">
          {trust_html}
        </div>
      </div>
      <div class="hero-visual">
        <div class="device-frame">
          <img src="/assets/screens/{sc}-overview.jpg" alt="{e(h['hero_img_alt'])}" width="443" height="960" loading="eager">
        </div>
      </div>
    </div>
  </section>

  <div class="kpi-strip">
    <div class="kpi-inner">
      {kpi_html}
    </div>
  </div>

  <main>
    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{e(h['screens_eyebrow'])}</p>
          <h2>{e(h['screens_h2'])}</h2>
          <p>{e(h['screens_lead'])}</p>
        </div>
        <div class="screen-gallery">
          {screens_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{e(h['pillars_eyebrow'])}</p>
          <h2>{e(h['pillars_h2'])}</h2>
          <p>{e(h['pillars_lead'])}</p>
        </div>
        <div class="pillars">
          {pillars_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="split-feature">
          <div>
            <p class="eyebrow">{e(h['mcp_eyebrow'])}</p>
            <h2>{e(h['mcp_h2'])}</h2>
            <p>{h['mcp_lead_html']}</p>
            <div class="callout">
              <p>{h['mcp_callout_html']}</p>
            </div>
            <p><a href="{page_path(lang_cfg, 'mcp')}">{e(h['mcp_link'])} &rarr;</a></p>
          </div>
          <div class="hero-visual">
            <div class="device-frame" style="max-width: 260px;">
              <img src="/assets/screens/{sc}-ai.jpg" alt="{e(h['mcp_img_alt'])}" loading="lazy">
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{e(h['pricing_eyebrow'])}</p>
          <h2>{e(h['pricing_h2'])}</h2>
          <p>{e(h['pricing_lead'])}</p>
        </div>
        <div class="pricing-grid">
          {plans_html}
        </div>
      </div>
    </section>

    <section class="section-compact">
      <div class="container">
        <h2>{e(h['explore_h2'])}</h2>
        <ul>
          {explore_html}
        </ul>
      </div>
    </section>
  </main>

{render_footer(lang_cfg, data, 'home')}
</body>
</html>
"""


def render_faq(lang_cfg: dict, data: dict) -> str:
    f = data["faq"]
    json_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": lang_cfg["html_lang"],
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a_plain"]},
            }
            for item in f["items"]
        ],
    }
    items_html = "\n\n      ".join(
        f"""<div class="faq-item">
        <h3>{e(item['q'])}</h3>
        <p>{item['a_html'].replace('__MCP_URL__', page_path(lang_cfg, 'mcp')).replace('__APP_STORE_URL__', APP_STORE_URL)}</p>
      </div>"""
        for item in f["items"]
    )
    head = render_head(lang_cfg, "faq", f["title"], f["meta_description"], json_ld=json_ld)
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'faq')}

  <div class="hero">
    <div class="hero-compact">
      <p class="eyebrow">{e(f['eyebrow'])}</p>
      <h1>{e(f['h1'])}</h1>
      <p class="lead">{e(f['lead'])}</p>
    </div>
  </div>

  <main class="container-narrow">
    <section class="section-compact">
      {items_html}
    </section>
  </main>

{render_footer(lang_cfg, data, 'faq')}
</body>
</html>
"""


def render_vs(lang_cfg: dict, data: dict) -> str:
    v = data["vs"]

    def render_table(headers_list: list[str], rows_list: list[list[str]]) -> str:
        headers = "".join(f"<th>{e(col)}</th>" for col in headers_list)
        rows_html = []
        for row in rows_list:
            cells = [f"<td><strong>{e(row[0])}</strong></td>"]
            for cell in row[1:]:
                cells.append(f"<td>{cell}</td>")
            rows_html.append(f"            <tr>\n              {''.join(cells)}\n            </tr>")
        return f"""      <div class="table-wrap">
        <table>
          <thead>
            <tr>{headers}</tr>
          </thead>
          <tbody>
{chr(10).join(rows_html)}
          </tbody>
        </table>
      </div>"""

    eu_section_html = ""
    if v.get("eu_table_rows"):
        eu_section_html = f"""
    <section class="section-compact" id="european-trackers">
      <h2>{e(v['eu_table_h2'])}</h2>
      <p>{e(v['eu_table_lead'])}</p>
{render_table(v['eu_table_headers'], v['eu_table_rows'])}
    </section>"""

    sections_html = []
    for sec in v["sections"]:
        bullets = "\n        ".join(f"<li>{b}</li>" for b in sec["bullets_html"])
        sections_html.append(
            f"""    <section id="{e(sec['id'])}">
      <h2>{e(sec['h2'])}</h2>
      <ul>
        {bullets}
      </ul>
    </section>"""
        )

    head = render_head(lang_cfg, "vs", v["title"], v["meta_description"])
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'vs')}

  <div class="hero">
    <div class="hero-compact" style="max-width: var(--max);">
      <p class="eyebrow">{e(v['eyebrow'])}</p>
      <h1>{e(v['h1'])}</h1>
      <p class="lead">{v['lead_html']}</p>
    </div>
  </div>

  <main class="container">
    <section class="section-compact">
      <h2>{e(v['table_h2'])}</h2>
{render_table(v['table_headers'], v['table_rows'])}
      <p><em>{e(v['table_note'])}</em></p>
    </section>
{eu_section_html}

{chr(10).join(sections_html)}

    <section>
      <h2>{e(v['cta_h2'])}</h2>
      <p>{e(v['cta_lead'])}</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="{APP_STORE_URL}" rel="noopener">{e(v['cta_primary'])}</a>
        <a class="btn btn-secondary" href="{page_path(lang_cfg, 'faq')}">{e(v['cta_secondary'])}</a>
      </div>
    </section>
  </main>

{render_footer(lang_cfg, data, 'vs')}
</body>
</html>
"""


def render_mcp(lang_cfg: dict, data: dict) -> str:
    m = data["mcp"]
    sc = lang_cfg["screen"]
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "inLanguage": lang_cfg["html_lang"],
        "headline": m["ld_headline"],
        "description": m["meta_description"],
        "url": page_url(lang_cfg, "mcp"),
        "author": {"@type": "Organization", "name": "WorthTrail", "url": f"{SITE_ORIGIN}/"},
        "about": {"@type": "SoftwareApplication", "name": "WorthTrail", "operatingSystem": "macOS"},
    }
    spec_rows = "\n".join(
        f"""            <tr>
              <td><strong>{e(r[0])}</strong></td>
              <td>{r[1]}</td>
            </tr>"""
        for r in m["spec_rows"]
    )
    read_items = "\n            ".join(f"<li>{item}</li>" for item in m["read_items_html"])
    write_items = "\n            ".join(f"<li>{item}</li>" for item in m["write_items_html"])
    examples = "\n        ".join(f"<li><em>{e(q)}</em></li>" for q in m["example_questions"])
    security = "\n        ".join(f"<li>{item}</li>" for item in m["security_items_html"])

    head = render_head(lang_cfg, "mcp", m["title"], m["meta_description"], json_ld=json_ld)
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'mcp')}

  <section class="hero">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">{e(m['eyebrow'])}</p>
        <h1>{e(m['h1'])}</h1>
        <p class="lead">{m['lead_html']}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{APP_STORE_URL}" rel="noopener">{e(m['cta_primary'])}</a>
          <a class="btn btn-secondary" href="{page_path(lang_cfg, 'faq')}">{e(m['cta_secondary'])}</a>
        </div>
      </div>
      <div class="hero-visual">
        <div class="device-frame" style="max-width: 268px;">
          <img src="/assets/screens/{sc}-ai.jpg" alt="{e(m['img_alt'])}" loading="eager">
        </div>
      </div>
    </div>
  </section>

  <main class="container-narrow">
    <section class="section-compact">
      <h2>{e(m['specs_h2'])}</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>{e(m['specs_col_prop'])}</th>
              <th>{e(m['specs_col_val'])}</th>
            </tr>
          </thead>
          <tbody>
{spec_rows}
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>{e(m['connect_h2'])}</h2>
      <p>{m['connect_intro_html']}</p>

      <h3>Claude Code</h3>
      <pre><code>claude mcp add --transport http --scope user worthtrail http://127.0.0.1:47821/mcp \\
  --header "Authorization: Bearer YOUR_TOKEN"</code></pre>

      <h3>Claude Desktop (<code>~/.claude.json</code>)</h3>
      <pre><code>{{
  "mcpServers": {{
    "worthtrail": {{
      "type": "http",
      "url": "http://127.0.0.1:47821/mcp",
      "headers": {{
        "Authorization": "Bearer YOUR_TOKEN"
      }}
    }}
  }}
}}</code></pre>

      <h3>Codex (<code>~/.codex/config.toml</code>)</h3>
      <pre><code>[mcp_servers.worthtrail]
url = "http://127.0.0.1:47821/mcp"
http_headers = {{ "Authorization" = "Bearer YOUR_TOKEN" }}</code></pre>
    </section>

    <section>
      <h2>{e(m['tools_h2'])}</h2>
      <div class="grid-2">
        <div class="fact-block">
          <h3>{e(m['read_h3'])}</h3>
          <ul>
            {read_items}
          </ul>
        </div>
        <div class="fact-block">
          <h3>{e(m['write_h3'])}</h3>
          <ul>
            {write_items}
          </ul>
        </div>
      </div>
    </section>

    <section>
      <h2>{e(m['examples_h2'])}</h2>
      <ul>
        {examples}
      </ul>
    </section>

    <section>
      <h2>{e(m['security_h2'])}</h2>
      <ul>
        {security}
      </ul>
    </section>
  </main>

{render_footer(lang_cfg, data, 'mcp')}
</body>
</html>
"""


def render_support(lang_cfg: dict, data: dict) -> str:
    s = data["support"]
    topic_cards = []
    for t in s["topics"]:
        subj = urllib.parse.quote(t["subject"])
        topic_cards.append(
            f"""        <a class="topic-card" href="mailto:{SUPPORT_EMAIL}?subject={subj}">
          <div>
            <div class="topic-tag">{e(t['tag'])}</div>
            <h3>{e(t['title'])}</h3>
            <p>{e(t['desc'])}</p>
          </div>
          <span class="topic-action">{e(t['action'])} &rarr;</span>
        </a>"""
        )

    accordions = []
    for idx, g in enumerate(s["help_groups"]):
        open_attr = " open" if idx == 0 else ""
        bullets = "\n            ".join(f"<li>{item}</li>" for item in g["items_html"])
        accordions.append(
            f"""        <details{open_attr}>
          <summary>{e(g['title'])}</summary>
          <div class="help-body">
            <ul>
              {bullets}
            </ul>
          </div>
        </details>"""
        )

    head = render_head(lang_cfg, "support", s["title"], s["meta_description"])
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'support')}

  <div class="hero">
    <div class="hero-compact">
      <p class="eyebrow">{e(s['eyebrow'])}</p>
      <h1>{e(s['h1'])}</h1>
      <p class="lead">{s['lead_html']}</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="mailto:{SUPPORT_EMAIL}?subject={urllib.parse.quote(s['default_subject'])}">{e(s['cta_email'])}</a>
        <a class="btn btn-secondary" href="{page_path(lang_cfg, 'faq')}">{e(s['cta_faq'])}</a>
      </div>
    </div>
  </div>

  <main class="container-narrow">
    <section class="section-compact">
      <h2>{e(s['contact_h2'])}</h2>
      <p>{e(s['contact_lead'])}</p>
      <div class="topic-grid">
{chr(10).join(topic_cards)}
      </div>
    </section>

    <section>
      <h2>{e(s['diagnostics_h2'])}</h2>
      <p>{s['diagnostics_p1_html']}</p>
      <div class="callout">
        <p>{s['privacy_callout_html']}</p>
      </div>
    </section>

    <section>
      <h2>{e(s['help_h2'])}</h2>
      <p>{e(s['help_lead'])}</p>
      <div class="help-accordion">
{chr(10).join(accordions)}
      </div>
    </section>

    <section>
      <h2>{e(s['more_h2'])}</h2>
      <ul>
        <li><a href="{page_path(lang_cfg, 'faq')}">{e(s['more_faq'])}</a></li>
        <li><a href="{page_path(lang_cfg, 'mcp')}">{e(s['more_mcp'])}</a></li>
        <li><a href="{page_path(lang_cfg, 'privacy')}">{e(s['more_privacy'])}</a></li>
      </ul>
    </section>
  </main>

{render_footer(lang_cfg, data, 'support')}
</body>
</html>
"""


def render_privacy(lang_cfg: dict, data: dict) -> str:
    p = data["privacy"]
    lang_pills = []
    for cfg in LANGUAGES:
        is_cur = ' aria-current="true"' if cfg["id"] == lang_cfg["id"] else ""
        lang_pills.append(
            f'        <a href="{page_path(cfg, "privacy")}"{is_cur}>{e(cfg["name"])}</a>'
        )

    glance_html = "\n      ".join(
        f"""<div class="kpi-item">
        <div class="kpi-val">{e(item['val'])}</div>
        <div class="kpi-lbl">{e(item['lbl'])}</div>
      </div>"""
        for item in p["glance"]
    )

    flow_headers = "".join(f"<th>{e(c)}</th>" for c in p["flow_headers"])
    flow_rows = "\n".join(
        "            <tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
        for row in p["flow_rows"]
    )

    sections_html = []
    for idx, sec in enumerate(p["sections"], start=1):
        paras = "\n      ".join(
            f"<p>{para.replace('__SUPPORT_URL__', page_path(lang_cfg, 'support'))}</p>"
            for para in sec["paragraphs_html"]
        )
        sections_html.append(
            f"""    <section class="policy-section">
      <div class="policy-num">{idx:02d}</div>
      <h2>{e(sec['title'])}</h2>
      {paras}
    </section>"""
        )

    head = render_head(lang_cfg, "privacy", p["title"], p["meta_description"])
    return f"""{head}
<body>
{render_header(lang_cfg, data, 'privacy')}

  <div class="hero">
    <div class="hero-compact">
      <p class="eyebrow">{e(p['eyebrow'])}</p>
      <h1>{e(p['h1'])}</h1>
      <p class="lead">{e(p['lead'])}</p>
      <div class="policy-meta">
        <span>{e(p['effective_date'])}</span>
        <span>{e(p['applies_to'])}</span>
      </div>
      <div class="lang-pills" aria-label="{e(data['nav']['language_label'])}">
{chr(10).join(lang_pills)}
      </div>
    </div>
  </div>

  <div class="kpi-strip">
    <div class="kpi-inner">
      {glance_html}
    </div>
  </div>

  <main class="container-narrow">
    <section class="section-compact">
      <h2>{e(p['flow_h2'])}</h2>
      <p>{e(p['flow_lead'])}</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>{flow_headers}</tr>
          </thead>
          <tbody>
{flow_rows}
          </tbody>
        </table>
      </div>
    </section>

{chr(10).join(sections_html)}
  </main>

{render_footer(lang_cfg, data, 'privacy')}
</body>
</html>
"""


def render_sitemap() -> str:
    entries = []
    for page in PAGES:
        alternates = [
            f'    <xhtml:link rel="alternate" hreflang="{cfg["hreflang"]}" href="{page_url(cfg, page)}" />'
            for cfg in LANGUAGES
        ]
        alternates.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url(LANGUAGES[0], page)}" />'
        )
        alt_block = "\n".join(alternates)
        for cfg in LANGUAGES:
            entries.append(
                f"""  <url>
    <loc>{page_url(cfg, page)}</loc>
    <lastmod>{LASTMOD}</lastmod>
{alt_block}
  </url>"""
            )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


RENDERERS = {
    "home": render_home,
    "faq": render_faq,
    "vs": render_vs,
    "mcp": render_mcp,
    "support": render_support,
    "privacy": render_privacy,
}


def build() -> int:
    loaded = {}
    for cfg in LANGUAGES:
        path = CONTENT_DIR / f"{cfg['id']}.json"
        if not path.exists():
            print(f"ERROR: missing content file {path}", file=sys.stderr)
            return 1
        loaded[cfg["id"]] = json.loads(path.read_text(encoding="utf-8"))

    count = 0
    for cfg in LANGUAGES:
        data = loaded[cfg["id"]]
        for page in PAGES:
            out = output_file(cfg, page)
            out.parent.mkdir(parents=True, exist_ok=True)
            rendered = RENDERERS[page](cfg, data)
            out.write_text(rendered, encoding="utf-8")
            count += 1

    (DOCS_DIR / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    print(f"Generated {count} HTML pages across {len(LANGUAGES)} languages + docs/sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
