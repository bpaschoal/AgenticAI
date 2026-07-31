import re
from typing import Any, Dict, List
from Tools.perception import Perception


class Planner:

    def plan(self, perception: Perception, objective: str) -> List[Dict[str, Any]]:
        # If the objective contains an explicit URL, use open_url
        url_match = re.search(r"https?://[\w\.-/]+", objective)
        if url_match:
            return [{"action": "open_url", "url": url_match.group(0)}]

        # try to find first href in DOM
        href_match = re.search(r"<a[^>]+href=[\"']([^\"']+)[\"']?[^>]*>(.*?)</a>", perception.dom, re.I | re.S)
        if href_match:
            href, text = href_match.group(1), re.sub(r"<[^>]+>", "", href_match.group(2)).strip()
            return [{"action": "open_url", "url": href}, {"action": "task_completed", "result": text or href}]

        # No explicit action found; request current DOM for inspection
        return [{"action": "inspect_dom"}]
