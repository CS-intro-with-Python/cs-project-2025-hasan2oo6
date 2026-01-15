import requests
from typing import Any, Dict, List, Set, Tuple

CF = "https://codeforces.com/api"

def _get(method: str, params: dict) -> Any:
    r = requests.get(f"{CF}/{method}", params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "OK":
        raise RuntimeError(data.get("comment", "Codeforces API error"))
    return data["result"]

def problemset_problems() -> List[Dict[str, Any]]:
    res = _get("problemset.problems", {})
    return res["problems"]

def user_status(handle: str) -> List[Dict[str, Any]]:
    return _get("user.status", {"handle": handle})

def problem_key(contest_id: int, index: str) -> str:
    return f"{contest_id}-{index}"

def solved_problem_keys(handles: List[str]) -> Set[str]:
    solved: Set[str] = set()
    for h in handles:
        subs = user_status(h)
        for s in subs:
            if s.get("verdict") != "OK":
                continue
            pr = s.get("problem", {})
            cid = pr.get("contestId")
            idx = pr.get("index")
            if cid is None or idx is None:
                continue
            solved.add(problem_key(int(cid), str(idx)))
    return solved
