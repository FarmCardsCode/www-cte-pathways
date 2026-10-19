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

Status (2026-10-19): **new project, nothing built beyond a starter scaffold.** The first
session should settle the open questions below with the user before building
out pages.

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

- `app/content/pathways/<slug>.json`: one file per pathway. The schema in
  `example-pathway.json` is a **draft**: refine it with the user once real
  pathway data is in hand.
- Files with `"published": false` are skipped, so drafts can sit in the repo.
- Never invent real course numbers, certifications, or requirements. Use
  only what the user provides, and leave clear `TODO` placeholders otherwise.

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

- **Nothing is hosted yet.** Long-term hosting is pending district IT
  approval (the maintainer's IT request sheet, 2026-10-19). There is no
  public URL. Don't hardcode any domain.
- **Repo:** public on GitHub, `FarmCardsCode/www-cte-pathways`, the only
  remote. Kept on GitHub (not the maintainer's Forgejo) because pve2's
  guests can reach GitHub but not Forgejo, and public means the server pulls
  over HTTPS with no key.
- **Server:** its own dedicated VM, `508` `cte` at `172.30.1.13` on pve2's
  svcpub network, not shared with farmcardscode.org (blast radius), with its
  own Cloudflare tunnel `cte-pathways`. Drafted in
  `~/Code/school-services-infra` (commit `a990e2f`): catalog entry in
  `ansible/vars/servers.yml` (enabled; unpublished until approval), role
  `ansible/tasks/server-roles/cte.yml`, and **`docs/cte-pathways.md`, the
  source of truth for hosting**. Built and checked 2026-10-19 (serves
  this repo at 127.0.0.1:8000, update timer running), not published.
- **Deploys:** the role clones this repo and runs this repo's
  `deploy/auto-update.sh` on a 5-minute timer, so pushing to `main` is the
  deploy. Keep `main` deployable at all times. The timer doesn't reinstall
  dependencies: if `requirements.txt` changes, the role must be re-run. The
  role writes its own systemd units; `deploy/cte-pathways.service` and
  `deploy/install-auto-update.sh` are only the by-hand fallback.
- **Open: the district hostname.** A plain CNAME from the district's DNS to
  the tunnel won't work (a tunnel only routes hostnames in the same
  Cloudflare account). Options (Cloudflare for SaaS custom hostname, the
  district running the subdomain on Cloudflare, or just
  `cte.farmcardscode.org`) are in `docs/cte-pathways.md` in
  school-services-infra. It decides what to ask district IT for.
- Requests to update the site come in ad hoc from staff; quick, safe content
  edits are the common case.

## Open questions for the first session

1. Which pathways exist, and which are actually taught at each school?
   (Get the official list/course guide from the user.)
2. What does "completing" a pathway earn here: state completer status,
   specific certifications, dual credit, graduation endorsements?
3. Page structure: one page per pathway plus an overview/comparison page?
   Search or filter (by career area, school, grade)?
4. Branding: district/school name, colors, logo. Are we allowed to use them?
5. Who besides the maintainer needs to request or approve content changes?
6. License for the repo (farmcardscode.org uses MIT).
