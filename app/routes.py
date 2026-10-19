from flask import Blueprint, render_template, abort
from pathlib import Path
import json

bp = Blueprint("main", __name__)

PATHWAYS_DIR = Path(__file__).resolve().parent / "content" / "pathways"

def load_pathways():
    pathways = []

    if not PATHWAYS_DIR.exists():
        return pathways

    for file_path in PATHWAYS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                pathway = json.load(f)

            # Skip unpublished drafts
            if not pathway.get("published", False):
                continue

            # Basic required fields check
            required_fields = ["slug", "title", "summary", "courses"]
            if not all(field in pathway for field in required_fields):
                continue

            pathways.append(pathway)

        except (json.JSONDecodeError, ValueError):
            # Skip malformed files
            continue

    pathways.sort(key=lambda p: p["title"])

    return pathways

def get_pathway_by_slug(slug):
    for pathway in load_pathways():
        if pathway["slug"] == slug:
            return pathway
    return None

@bp.get("/")
def index():
    return render_template("index.html", pathways=load_pathways())

@bp.get("/pathways/<slug>")
def pathway_detail(slug):
    pathway = get_pathway_by_slug(slug)
    if pathway is None:
        abort(404)
    return render_template("pathway.html", pathway=pathway)
