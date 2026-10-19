#!/usr/bin/env bash
# Fast-forward this checkout to the latest main on GitHub and restart the
# site if anything changed. Run as root by cte-pathways-update.timer (see
# install-auto-update.sh); git itself runs as whoever owns the checkout.
#
# Everything lives inside main() so bash parses the whole script before the
# merge below can rewrite this file on disk.

main() {
  set -euo pipefail

  local repo owner service url branch old new
  repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  owner="$(stat -c %U "$repo")"
  service="${SERVICE:-cte-pathways}"
  # HTTPS works while the repo is public; if it is private, set REPO_URL to
  # the SSH URL and give the checkout owner a read-only deploy key
  url="${REPO_URL:-https://github.com/FarmCardsCode/www-cte-pathways.git}"

  as_owner() { runuser -u "$owner" -- env GIT_TERMINAL_PROMPT=0 "$@"; }

  cd "$repo"

  branch="$(as_owner git symbolic-ref --short HEAD)"
  if [ "$branch" != "main" ]; then
    echo "Checkout is on '$branch', not main - skipping" >&2
    exit 1
  fi

  as_owner git fetch --quiet "$url" main
  old="$(as_owner git rev-parse HEAD)"
  new="$(as_owner git rev-parse FETCH_HEAD)"
  [ "$old" = "$new" ] && exit 0

  # --ff-only refuses rather than creating a merge if someone committed on
  # the server; git also refuses if local edits would be overwritten
  as_owner git merge --ff-only --quiet FETCH_HEAD
  systemctl restart "$service"
  echo "Updated ${old:0:7} -> ${new:0:7} and restarted $service"
}

main "$@"
exit
