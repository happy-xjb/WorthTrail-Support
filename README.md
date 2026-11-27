# WorthTrail Website & Support

Static website and public support repository for **WorthTrail** (`https://worthtrail.app`).

## Languages (14)

- **Default (root `/`)**: English (`en`)
- **Chinese**: Simplified Chinese (`/zh/`, `zh-Hans`) & Traditional Chinese (`/zh-hant/`, `zh-Hant`)
- **Key European & Russian markets**:
  - German (`/de/`), French (`/fr/`), Spanish (`/es/`), Italian (`/it/`), European Portuguese (`/pt-pt/`), Dutch (`/nl/`), Swedish (`/sv/`), Danish (`/da/`), Norwegian (`/no/`), Finnish (`/fi/`), Russian (`/ru/`)

## Pages per Language (6 × 14 = 84 pages)

- `/` (or `/<lang>/`) — Landing / Overview (`SoftwareApplication` & `Organization` JSON-LD)
- `/faq/` — FAQ & Product Facts (`FAQPage` JSON-LD)
- `/vs/` — Objective comparison vs Monarch Money, Copilot Money, Kubera, and spreadsheets
- `/mcp/` — Mac local MCP server guide (`TechArticle` JSON-LD)
- `/support/` — Support hub, topic mailto cards, encrypted diagnostics (`.wtdiag`), and troubleshooting
- `/privacy/` — Privacy Policy with data-flow overview and structured legal sections

## Editing & Building

Do not hand-edit generated HTML files under `docs/`. Instead:

1. Edit `content/<lang>.json` (or `scripts/build_site.py` / `docs/assets/style.css`).
2. Run:

```sh
python3 scripts/build_site.py
```

This regenerates all 78 HTML pages and `docs/sitemap.xml` with full `hreflang` alternates.

## Deployment (Cloudflare Workers Static Assets / Pages)

- Build command: *(empty — static files in `docs/` are committed directly)*
- Output directory: `docs` (`wrangler.jsonc`)
- Custom domain: `worthtrail.app`
