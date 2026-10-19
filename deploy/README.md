# Deploying

Live at https://cte.farmcardscode.org since 2026-10-19 (VM 508); long-term
hosting is still pending district IT approval. The plan is a
dedicated VM on `pve2`, provisioned from the server catalog in
`school-services-infra`, running this app under gunicorn with its own
Cloudflare tunnel. The district subdomain points at that tunnel only.

That role now exists, drafted and not yet run: VM `508` `cte`, role
`ansible/tasks/server-roles/cte.yml` in `school-services-infra`, documented
in its `docs/cte-pathways.md`. Use it. The steps below are only the by-hand
fallback.

## One-time server setup

On the VM (as a sudo user):

```sh
sudo useradd --system --home /srv/cte-pathways cte-pathways
sudo git clone https://github.com/FarmCardsCode/www-cte-pathways.git /srv/cte-pathways
sudo chown -R jlong:jlong /srv/cte-pathways          # checkout owner runs git
cd /srv/cte-pathways
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

sudo cp deploy/cte-pathways.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cte-pathways             # serves on 127.0.0.1:8000

sudo deploy/install-auto-update.sh 5min              # pull main every 5 min
```

If the repo is private, add a read-only deploy key for the checkout owner,
clone over SSH instead, and install the timer with
`sudo REPO_URL=git@github.com:FarmCardsCode/www-cte-pathways.git deploy/install-auto-update.sh 5min`.

Then create this VM's own tunnel, route the approved hostname to
`http://127.0.0.1:8000`, and have district IT point that hostname at the
tunnel.

## Day to day

Push to `main`; the timer fast-forwards the server and restarts the service.
To deploy immediately instead of waiting:

```sh
sudo systemctl start cte-pathways-update.service
journalctl -u cte-pathways-update -n 20      # what it did
```

Never edit files directly on the server: the update only fast-forwards, so
local changes there block every future deploy.
