# CTE Pathways

Informational site for Farmington High School's Career and Technical
Education pathways: what each pathway is, which courses it includes and in
what order, and what students earn for completing it. Built for junior high
students and teachers planning ahead. Live at https://cte.farmcardscode.org.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app wsgi run --debug
```

Then open http://127.0.0.1:5000.

## Updating content

All content is JSON in `app/content/`; templates don't need to change for
content edits.

| File | What it holds |
| --- | --- |
| `pathways/<slug>.json` | One pathway: title, career area, summary, careers, classes by level (`options` with more than one entry shows "Choose one"), `h2` (counts toward Honor Graduate), partner schools (`NWTI`, `NWACC`) |
| `career_areas.json` | Career areas, their order, and icon names |
| `diplomas.json` | Honor Graduate, Diploma of Merit/Distinction rules, glossary |
| `site.json` | School name, partner names, application note |

Edit or add a file, commit, and push to `main`. The server picks it up
within about 5 minutes (see `deploy/README.md`). Set `"published": false`
to keep a draft pathway out of the site.

## Deployment

See [`deploy/README.md`](deploy/README.md).
