# WorthTrail-Support Agent Notes

This repository publishes the static website for **WorthTrail** (`https://worthtrail.app`) from `docs/` via Cloudflare Workers Static Assets (`wrangler.jsonc`).

## Relationship with the WorthTrail App Repo

- Product facts, UI navigation paths, pricing, and key-market financial terminology live in the sibling app repo `../WorthTrail/`:
  - `../WorthTrail/docs/localization-rules.md` — 12 key markets & broker/bank financial terminology rules.
  - `../WorthTrail/WorthTrail/<lang>.lproj/Localizable.strings` — authoritative in-app UI paths and financial terms.
  - `../WorthTrail/docs/fresh-design-system.md` — visual language reference.

## Build Workflow

- Source of truth: `content/<lang>.json` + `scripts/build_site.py` + `docs/assets/style.css`.
- Never hand-edit generated HTML files in `docs/`.
- After editing content or templates, run:

```sh
python3 scripts/build_site.py
```

- Always verify all generated pages, JSON-LD blocks, internal links, and `docs/sitemap.xml` before committing.
- Commit and push only when asked by the user.
