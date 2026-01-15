import time
import random
from datetime import datetime
from typing import List, Dict, Any, Tuple

from flask import Flask, render_template, request, redirect, url_for

from db import init_db, create_contest, get_contest, list_contests, start_contest
from cf_api import problemset_problems, solved_problem_keys, problem_key
from scoring import build_scoreboard

app = Flask(__name__)
# Initialize DB once at startup
init_db()
app.logger.info("App started, DB initialized")

def fmt(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")

def parse_handles(s: str) -> List[str]:
    parts = []
    for x in s.replace("\n", " ").replace(",", " ").split():
        x = x.strip()
        if x:
            parts.append(x)
    seen = set()
    out = []
    for h in parts:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out

def matches_tags(problem_tags: List[str], need_tags: List[str], mode: str) -> bool:
    if not need_tags:
        return True
    pt = set(t.lower() for t in problem_tags)
    nt = set(t.lower() for t in need_tags)
    if mode == "any":
        return len(pt & nt) > 0
    return nt.issubset(pt)

def parse_groups(text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    groups = []
    errors = []
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    for i, ln in enumerate(lines, start=1):
        parts = ln.split()
        if len(parts) < 4:
            errors.append(f"Group line {i}: format is: k min_rating max_rating tag_mode tags... (or '-' for no tags)")
            continue
        try:
            k = int(parts[0]); minr = int(parts[1]); maxr = int(parts[2])
        except ValueError:
            errors.append(f"Group line {i}: k/min/max must be integers.")
            continue
        mode = parts[3].lower()
        if mode not in ("any", "all"):
            errors.append(f"Group line {i}: tag_mode must be 'any' or 'all'.")
            continue
        tags = parts[4:]
        if len(tags) == 1 and tags[0] == "-":
            tags = []
        groups.append({"k": k, "min": minr, "max": maxr, "mode": mode, "tags": [t.lower() for t in tags]})
    return groups, errors


@app.get("/")
def index():
    contests = list_contests()
    return render_template("index.html", contests=contests, errors=[], warnings=[])

@app.post("/create")
def create():
    errors, warnings = [], []

    handles = parse_handles(request.form.get("handles", ""))
    if not handles:
        errors.append("Please enter at least one Codeforces handle.")
        return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

    duration_minutes = int(request.form.get("duration_minutes", "120"))

    groups_text = (request.form.get("groups", "") or "").strip()

    all_problems = problemset_problems()

    valid_tags = set()
    for p in all_problems:
        for t in p.get("tags", []):
            valid_tags.add(t.lower())

    solved = solved_problem_keys(handles)
    chosen = []
    used = set()

    if groups_text:
        groups, parse_errs = parse_groups(groups_text)
        if parse_errs:
            errors.extend(parse_errs)
            return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

        invalid = []
        for g in groups:
            for t in g["tags"]:
                if t not in valid_tags:
                    invalid.append(t)
        invalid = list(dict.fromkeys(invalid))
        if invalid:
            errors.append("Invalid tag(s) in groups: " + ", ".join(invalid))
            return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

        for gi, g in enumerate(groups, start=1):
            k_need = g["k"]
            minr, maxr = g["min"], g["max"]
            tags, mode = g["tags"], g["mode"]

            candidates = []
            for p in all_problems:
                cid = p.get("contestId"); idx = p.get("index"); rating = p.get("rating")
                if cid is None or idx is None or rating is None:
                    continue
                if p.get("type") != "PROGRAMMING":
                    continue

                r = int(rating)
                if not (minr <= r <= maxr):
                    continue

                pk = problem_key(int(cid), str(idx))
                if pk in solved or pk in used:
                    continue

                if not matches_tags(p.get("tags", []), tags, mode):
                    continue

                candidates.append(p)

            if len(candidates) < k_need:
                warnings.append(
                    f"Group {gi}: requested {k_need}, found only {len(candidates)} "
                    f"(rating {minr}-{maxr}, tags: {', '.join(tags) if tags else '-'})"
                )

            random.shuffle(candidates)
            pick = candidates[:min(k_need, len(candidates))]
            for p in pick:
                pk = problem_key(int(p["contestId"]), str(p["index"]))
                used.add(pk)
                chosen.append(p)

        if not chosen:
            errors.append("No problems found for your groups. Try wider rating ranges or fewer/other tags.")
            return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

    else:
        num_problems = int(request.form.get("num_problems", "7"))
        min_rating = int(request.form.get("min_rating", "800"))
        max_rating = int(request.form.get("max_rating", "1700"))
        tag_mode = (request.form.get("tag_mode", "any") or "any").lower()
        tags = [t.lower() for t in (request.form.get("tags", "") or "").replace(",", " ").split() if t.strip()]

        invalid = [t for t in tags if t not in valid_tags]
        if invalid:
            errors.append("Invalid tag(s): " + ", ".join(sorted(set(invalid))))
            return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

        candidates = []
        for p in all_problems:
            cid = p.get("contestId"); idx = p.get("index"); rating = p.get("rating")
            if cid is None or idx is None or rating is None:
                continue
            if p.get("type") != "PROGRAMMING":
                continue

            r = int(rating)
            if not (min_rating <= r <= max_rating):
                continue

            pk = problem_key(int(cid), str(idx))
            if pk in solved:
                continue

            if not matches_tags(p.get("tags", []), tags, tag_mode):
                continue

            candidates.append(p)

        if len(candidates) < num_problems:
            warnings.append(f"Requested {num_problems} problems, found only {len(candidates)}. Try wider filters.")

        random.shuffle(candidates)
        chosen = candidates[:min(num_problems, len(candidates))]

        if not chosen:
            errors.append("No problems found. Try wider rating or remove tags.")
            return render_template("index.html", contests=list_contests(), errors=errors, warnings=warnings)

    cid = create_contest(int(time.time()), duration_minutes, handles, chosen)
    app.logger.info(f"Created contest {cid} with {len(chosen)} problems for handles={handles}")
    return redirect(url_for("contest_page", contest_id=cid))

@app.get("/contest/<int:contest_id>")
def contest_page(contest_id: int):
    c = get_contest(contest_id)
    if not c:
        return "Contest not found", 404

    now = int(time.time())
    standings = None
    finished = False
    end_time = None

    if c["start_time"] is not None:
        end_time = int(c["start_time"]) + int(c["duration_minutes"]) * 60
        finished = now >= end_time
        standings = build_scoreboard(c["handles"], c["problems"], int(c["start_time"]), end_time)

    c_view = dict(c)
    c_view["start_time_fmt"] = fmt(c["start_time"])
    c_view["end_time_fmt"] = fmt(end_time) if end_time is not None else None
    return render_template("contest.html", contest=c_view, standings=standings, finished=finished)

@app.post("/contest/<int:contest_id>/start")
def contest_start(contest_id: int):
    c = get_contest(contest_id)
    if not c:
        return "Contest not found", 404
    if c["start_time"] is None:
        start_contest(contest_id, int(time.time()))
        app.logger.info(f"Started contest {contest_id}")
    return redirect(url_for("contest_page", contest_id=contest_id))

import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
