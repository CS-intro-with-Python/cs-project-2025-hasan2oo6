from typing import Any, Dict, List, Optional
from cf_api import user_status, problem_key

def build_scoreboard(
    handles: List[str],
    problems: List[Dict[str, Any]],
    start_time_unix: int,
    end_time_unix: Optional[int] = None
) -> List[Dict[str, Any]]:
    prob_keys = {problem_key(p["contestId"], p["index"]): p for p in problems}
    standings: List[Dict[str, Any]] = []

    for h in handles:
        subs = sorted(user_status(h), key=lambda s: s["creationTimeSeconds"])

        wrong = {k: 0 for k in prob_keys}
        solved_time = {k: None for k in prob_keys}  # minutes from start

        for s in subs:
            t = s["creationTimeSeconds"]
            if t < start_time_unix:
                continue
            if end_time_unix is not None and t > end_time_unix:
                continue

            pr = s.get("problem", {})
            cid = pr.get("contestId")
            idx = pr.get("index")
            if cid is None or idx is None:
                continue

            k = problem_key(int(cid), str(idx))
            if k not in prob_keys:
                continue
            if solved_time[k] is not None:
                continue

            verdict = s.get("verdict")
            if verdict == "OK":
                solved_time[k] = int((t - start_time_unix) // 60)
            else:
                if verdict not in ("COMPILATION_ERROR",):
                    wrong[k] += 1

        solved = 0
        penalty = 0
        per_problem = []

        for k in prob_keys:
            st = solved_time[k]
            w = wrong[k]
            if st is not None:
                solved += 1
                penalty += st + 20 * w
                per_problem.append({"solved": True, "time": st, "wrong": w})
            else:
                per_problem.append({"solved": False, "time": None, "wrong": w})

        standings.append({
            "handle": h,
            "solved": solved,
            "penalty": penalty,
            "problems": per_problem
        })

    standings.sort(key=lambda x: (-x["solved"], x["penalty"], x["handle"].lower()))
    return standings
