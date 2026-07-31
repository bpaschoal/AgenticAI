import base64
from typing import Any, Dict, List
from playwright.sync_api import sync_playwright


class Executor:
    def __init__(self, width: int = 1280, height: int = 800):
        self.width = width
        self.height = height

    def _screenshot_and_dom(self, page):
        page.wait_for_timeout(300)
        png = page.screenshot()
        dom = page.content()
        return dom, base64.b64encode(png).decode()

    def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": self.width, "height": self.height})

        result: Dict[str, Any] = {"dom": "", "screenshot": "", "actions": []}

        try:
            for step in plan:
                action = step.get("action")
                if action == "open_url":
                    url = step.get("url")
                    page.goto(url, wait_until="domcontentloaded")
                    result["actions"].append({"action": "open_url", "url": url})
                elif action == "inspect_dom":
                    result["actions"].append({"action": "inspect_dom"})
                elif action == "task_completed":
                    # nothing to execute in the browser; we return the declared result
                    result["actions"].append({"action": "task_completed", "result": step.get("result")})
                else:
                    result["actions"].append({"action": "unknown", "detail": step})

            dom, screenshot = self._screenshot_and_dom(page)
            result["dom"] = dom
            result["screenshot"] = screenshot
            return result
        finally:
            browser.close()
            pw.stop()
