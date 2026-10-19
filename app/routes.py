from flask import Blueprint, render_template, abort, request
from pathlib import Path
import json

bp = Blueprint("main", __name__)

CONTENT_DIR = Path(__file__).resolve().parent / "content"
PATHWAYS_DIR = CONTENT_DIR / "pathways"

def load_json(name):
    with open(CONTENT_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def load_pathways():
    pathways = []

    if not PATHWAYS_DIR.exists():
        return pathways

    area_slugs = {area["slug"] for area in load_json("career_areas.json")}

    for file_path in PATHWAYS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                pathway = json.load(f)

            # Skip unpublished drafts
            if not pathway.get("published", False):
                continue

            # Basic required fields check
            required_fields = ["slug", "title", "summary", "career_area", "levels"]
            if not all(field in pathway for field in required_fields):
                continue
            if pathway["career_area"] not in area_slugs:
                continue

            pathways.append(pathway)

        except (json.JSONDecodeError, ValueError):
            # Skip malformed files
            continue

    pathways.sort(key=lambda p: p["title"])

    return pathways

def get_pathway_by_slug(pathways, slug):
    for pathway in pathways:
        if pathway["slug"] == slug:
            return pathway
    return None

def group_by_area(pathways):
    """Career areas in content order, each with its pathways (empty areas dropped)."""
    groups = []
    for area in load_json("career_areas.json"):
        members = [p for p in pathways if p["career_area"] == area["slug"]]
        if members:
            groups.append({**area, "pathways": members})
    return groups

def shared_courses(pathway, pathways):
    """For each level, the other pathways that use one of the same courses.

    Lets a student see that, say, Introduction to Agriculture also starts
    Animal Systems and Plant Systems, so they can switch after Level 1.
    """
    shared = {}
    for level in pathway["levels"]:
        courses = set(level["options"])
        others = [
            p for p in pathways
            if p["slug"] != pathway["slug"]
            and any(
                l["level"] == level["level"] and courses & set(l["options"])
                for l in p["levels"]
            )
        ]
        if others:
            shared[level["level"]] = others
    return shared

# Filter values for the "Where it's taught" select.
WHERE_CHOICES = {
    "fhs": lambda p: not p.get("partners"),
    "nwti": lambda p: "NWTI" in p.get("partners", []),
    "nwacc": lambda p: "NWACC" in p.get("partners", []),
}

@bp.app_context_processor
def inject_site():
    return {"site": load_json("site.json")}

@bp.get("/")
def index():
    pathways = load_pathways()
    areas = load_json("career_areas.json")

    filters = {
        "area": request.args.get("area", ""),
        "where": request.args.get("where", ""),
        "honors": request.args.get("honors", ""),
    }
    shown = pathways
    if filters["area"] in {a["slug"] for a in areas}:
        shown = [p for p in shown if p["career_area"] == filters["area"]]
    if filters["where"] in WHERE_CHOICES:
        shown = [p for p in shown if WHERE_CHOICES[filters["where"]](p)]
    if filters["honors"] == "yes":
        shown = [p for p in shown if p.get("h2")]

    return render_template(
        "index.html",
        groups=group_by_area(shown),
        areas=areas,
        filters=filters,
        filtered=any(filters.values()),
        shown_count=len(shown),
        total_count=len(pathways),
    )

@bp.get("/pathways/<slug>")
def pathway_detail(slug):
    pathways = load_pathways()
    pathway = get_pathway_by_slug(pathways, slug)
    if pathway is None:
        abort(404)
    area = next(a for a in load_json("career_areas.json") if a["slug"] == pathway["career_area"])
    related = [
        p for p in pathways
        if p["career_area"] == pathway["career_area"] and p["slug"] != slug
    ]
    return render_template(
        "pathway.html",
        pathway=pathway,
        area=area,
        shared=shared_courses(pathway, pathways),
        related=related,
    )

@bp.get("/diplomas")
def diplomas():
    return render_template("diplomas.html", content=load_json("diplomas.json"))

@bp.app_errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
