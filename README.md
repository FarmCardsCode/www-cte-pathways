# CTE Pathways

Informational site for the district's Career and Technical Education
pathways: what each pathway is, which courses it includes and in what order,
and what students earn for completing it. Built for junior high students and
teachers planning ahead.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app wsgi run --debug
```

Then open http://127.0.0.1:5000.

## Updating content

Each pathway is a JSON file in `app/content/pathways/`. Edit or add a file,
commit, and push to `main`. The server picks it up automatically (see
`deploy/README.md`). Set `"published": false` to keep a draft out of the site.

## Deployment

See [`deploy/README.md`](deploy/README.md).
