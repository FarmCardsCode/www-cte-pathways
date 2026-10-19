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

Status: **new project, nothing built beyond a starter scaffold.** The first
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

- **Planned:** the district domain gets a subdomain (e.g.
  `cte.<district domain>`) pointing at the maintainer's server, pending
  approval through the district IT request. Until that's approved, there is
  no public URL. Don't hardcode any domain.
- Same server as farmcardscode.org: Proxmox VM 500, reached via jump host
  (`ssh -J jlong@10.64.62.201 jlong@172.30.1.100`), exposed through
  cloudflared. This site runs as its **own** systemd service on its own port,
  separate from farmcardscode.org, so neither can take down the other.
- `deploy/` has the service unit and an auto-update timer (copied from
  farmcardscode.org): once installed, pushing to `main` goes live within
  a few minutes. Keep `main` deployable at all times.
- If this repo stays private, the server needs a read-only GitHub deploy key
  and `REPO_URL` set to the SSH URL (see `deploy/README.md`).
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
