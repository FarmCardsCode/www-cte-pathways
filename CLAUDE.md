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

Status (2026-10-19): **live and in use.** Farmington High School (FHS):
18 CTE pathways from the FHS "Honor Graduate Requirements & Pathways" guide
(a Google Doc the maintainer shared; ask them for the link if it isn't in
your memory. Export it with `/export?format=html` to see merged table
cells, which show shared courses), an overview page with filters, one page per pathway, a
Diplomas & Honors explainer, and an Auto/Light/Dark theme menu. Branding
follows the district site, farmcards.org, with the maintainer's permission.

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

## Design

- Colors match farmcards.org: cardinal red `#DA2323` header with a black
  rule, black footer, logo gold `#F6BC3E` for "Counts toward Honor Graduate"
  tags. Inter/Helvetica font stack (no web font download). Logo is
  `app/static/img/cardinal.png`, resized from the district site's logo.
- All colors are tokens on `:root` in `app/static/css/style.css`. Dark mode
  applies via `prefers-color-scheme` unless `<html data-theme="light">`,
  and is forced by `data-theme="dark"`.
- Theme menu (header, top right): an accessible menu button (`menuitemradio`
  items) in `base.html` + `app/static/js/theme.js`. The choice is saved in
  `localStorage` and applied by an inline script in `<head>` before paint.
  The button's icon is picked by CSS from `data-theme`. The menu is hidden
  without JS (the site then follows the device).
- Icons: all from the hand-drawn SVG macro set in `app/templates/_icons.html`
  (`icon(name, class)`), 24x24, stroke 1.8. Add new icons there; don't use
  Unicode glyphs as icons (they render at mismatched sizes across fonts).
- Filters on the home page are a plain GET form (works without JS);
  `app/static/js/filters.js` just auto-submits on change.

## Verifying changes

- Render every route with Flask's test client (all pathway slugs, `/`,
  filter query strings, `/diplomas`, a 404).
- Screenshots: headless Chrome (`--headless=new --screenshot`) can't go
  narrower than about 500px. The maintainer's Mac is in dark mode, so pass
  `--blink-settings=preferredColorScheme=1` for light.
- Interactive checks (the theme menu): a small Node script that drives
  headless Chrome over the DevTools protocol (`--remote-debugging-port`,
  `Input.dispatchMouseEvent`/`dispatchKeyEvent`; Enter needs `text: "\r"`).
  Node's built-in `WebSocket` is enough, no packages.

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
- **Deploy now** (when the maintainer asks; otherwise just wait for the
  timer): the VM isn't reachable directly and refuses root. SSH through
  pve2 as a jump host (`ProxyCommand` to `root@<pve2>`; address in
  school-services-infra's `ansible/inventory.yml`) as `cyberlab@172.30.1.13`
  with `~/.ssh/claude-key`, then
  `sudo -n systemctl start cte-pathways-update.service`. It logs
  "Updated <old> -> <new> and restarted cte-pathways". The site is briefly
  down while it restarts, so retry a check that fails right after.
- Workflow the maintainer uses: review locally, then "commit, push, deploy".
  Don't push without being asked.
- Requests to update the site come in ad hoc from staff; quick, safe content
  edits are the common case.

## Decisions (2026-10-19)

- Structure: overview grouped by career area with filters (career area,
  where taught, counts toward Honor Grad) that work without JS; detail page
  per pathway; Diplomas & Honors page.
- Branding: district (farmcards.org) colors and cardinal logo.
- Theme: Auto/Light/Dark dropdown menu, not a cycling toggle.
- License: MIT.
- The Class of 2027 Honor Grad alternative ("2 AP classes/ Spanish 3/ Human
  Body Systems/Anatomy") is left off: it's ambiguous (one of these, or all?)
  and doesn't apply to junior high readers.

## Still open

- Grade levels for each course, and per-pathway certifications (neither is
  in the guide; sections stay hidden until filled in).
- Level 3 of Information Technology & Security is "Cybersecurity Security"
  in the guide, likely a typo for "Cybersecurity". Left as written until
  confirmed.
- Pathway `summary`/`careers` and the "Words to know" definitions were
  drafted by Claude; the maintainer approved publishing them but staff may
  want to revise.
- Who besides the maintainer requests/approves content changes.
