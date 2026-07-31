from typing import Dict, Any


class Reviewer:
    def review(self, exec_result: Dict[str, Any], objective: str) -> Dict[str, Any]:
        # Simple heuristic: if a task_completed action was returned, accept it.
        actions = exec_result.get("actions", [])
        for a in actions:
            if a.get("action") == "task_completed":
                return {"success": True, "result": a.get("result")}

        # otherwise, try to match objective keywords in DOM
        dom = exec_result.get("dom", "") or ""
        # if the objective asks for 'text of the first link', try to extract it
        if "first link" in objective.lower():
            import re

            m = re.search(r"<a[^>]*>(.*?)</a>", dom, re.I | re.S)
            if m:
                text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
                return {"success": True, "result": text}

        return {"success": False, "reason": "no matching result"}
