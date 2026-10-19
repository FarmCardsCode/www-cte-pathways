# CTE Pathways site

A public, informational website for the district's Career and Technical
Education (CTE) programs. Its main audience is **junior high students and
their teachers/counselors** choosing a high school CTE pathway. For each
pathway it should answer:

- What the pathway is and what careers it leads toward
- Whether (and where) it's taught in the district
- Which courses make it up, and in what order (grade level, prerequisites)
- What a student earns for completing it: completer status, industry
  certifications, dual credit, endorsements, etc.

Status (2026-10-19): **first build done** for Farmington High School (FHS):
18 CTE pathways from the FHS "Honor Graduate Requirements & Pathways" guide
(a Google Doc the maintainer shared), an overview page with filters, one page
per pathway, and a Diplomas & Honors explainer. Branding follows the district
site, farmcards.org (red `#DA2323`, black, white, logo gold, Inter, cardinal
logo), with permission from the maintainer.

## Audience and tone

- Readers are ~12-15 years old, plus teachers and parents. Plain language,
  short paragraphs, no jargon without a one-line explanation.
- Many will view it on a phone or a school Chromebook. Mobile-first, fast,
  readable at small sizes.
- It's an official-looking school resource: clean and trustworthy, not
  playful-gamer. (The maintainer's other site, farmcardscode.org, has a
  heavy CRT/terminal look; don't carry that style over unless asked.)
- **No emoji anywhere in the UI.** Use simple SVG line icons instead.
- Accessibility matters: real headings, good contrast in light and dark
  mode, keyboard navigable, no information conveyed by color alone.

## Content model

Content lives in JSON files so it can be updated quickly without touching
templates, mirroring farmcardscode.org's `app/content/*` pattern:

- `app/content/pathways/<slug>.json`: one file per pathway. `levels` is a list
  of `{level, options}`; more than one option renders as "Choose one". `h2`
  (high demand, high wage) means it counts toward Merit/Distinction/Honor
  Grad. `partners` (`NWTI`, `NWACC`) plus `partner_note` say where classes
  outside FHS are taught. `certifications` and grade levels are not in the
  guide yet, so they stay empty and hidden.
- `app/content/career_areas.json`: area order, names, and icon names (icons
  are SVG macros in `app/templates/_icons.html`).
- `app/content/diplomas.json`: Honor Grad / Merit / Distinction rules and
  the "Words to know" glossary.
- `app/content/site.json`: school name, partner names, application note.
- Files with `"published": false` are skipped, so drafts can sit in the repo.
- Never invent real course numbers, certifications, or requirements. Use
  only what the user provides, and leave clear `TODO` placeholders otherwise.
  Course names and requirements come verbatim from the guide; the pathway
  `summary` and `careers` text was drafted by Claude for the maintainer to
  review.

## Stack

- Python 3.13, Flask 3.1, Jinja templates, plain CSS/JS (no build step).
- `app/__init__.py` holds the app factory. Static URLs are versioned by file
  mtime so deploys never serve stale CSS/JS.
- Run locally:
  ```sh
  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  .venv/bin/flask --app wsgi run --debug
  ```
- `requirements.txt` lists only direct dependencies (pinned to the versions
  on the server). Keep it that way; don't paste a full `pip freeze`.

## Hosting and deploys

- **Live at `https://cte.farmcardscode.org`** since 2026-10-19, public.
  **Every push to `main` is live within ~5 minutes**, so never push
  placeholder or unconfirmed content as published. Long-term hosting is
  still pending district IT approval (the maintainer's IT request sheet), and
  a district hostname may be added later, so don't hardcode any domain in
  the app.
- **Repo:** public on GitHub, `FarmCardsCode/www-cte-pathways`, the only
  remote. Kept on GitHub (not the maintainer's Forgejo) because pve2's
  guests can reach GitHub but not Forgejo, and public means the server pulls
  over HTTPS with no key.
- **Server:** its own dedicated VM, `508` `cte` at `172.30.1.13` on pve2's
  svcpub network, not shared with farmcardscode.org (blast radius), with its
  own Cloudflare tunnel `cte-pathways` (route: `cte.farmcardscode.org` to
  HTTP `127.0.0.1:8000`). Managed from `~/Code/school-services-infra`:
  catalog entry in `ansible/vars/servers.yml`, role
  `ansible/tasks/server-roles/cte.yml`, and **`docs/cte-pathways.md`, the
  source of truth for hosting**.
- **Deploys:** the role clones this repo and runs this repo's
  `deploy/auto-update.sh` on a 5-minute timer, so pushing to `main` is the
  deploy. Keep `main` deployable at all times. The timer doesn't reinstall
  dependencies: if `requirements.txt` changes, the role must be re-run. The
  role writes its own systemd units; `deploy/cte-pathways.service` and
  `deploy/install-auto-update.sh` are only the by-hand fallback.
- **District hostname (maybe later).** A plain CNAME from the district's
  DNS to the tunnel won't work (a tunnel only routes hostnames in the same
  Cloudflare account); the likely route is a Cloudflare for SaaS custom
  hostname on top of `cte.farmcardscode.org`. Details in
  `docs/cte-pathways.md` in school-services-infra.
- Requests to update the site come in ad hoc from staff; quick, safe content
  edits are the common case.

## Decisions (2026-10-19)

- Structure: overview grouped by career area with filters (career area,
  where taught, counts toward Honor Grad) that work without JS; detail page
  per pathway; Diplomas & Honors page.
- License: MIT.

## Still open

- Grade levels for each course, and per-pathway certifications.
- Who besides the maintainer requests/approves content changes.
