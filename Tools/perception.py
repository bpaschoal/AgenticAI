import base64
from dataclasses import dataclass
from playwright.sync_api import sync_playwright
from typing import Optional


@dataclass
class Perception:
    dom: str
    screenshot: str  # base64-encoded PNG


def _screenshot_and_dom(page) -> tuple[str, str]:
    page.wait_for_timeout(300)
    png = page.screenshot()
    dom = page.content()
    return dom, base64.b64encode(png).decode()


def capture_perception(start_url: Optional[str] = None, width: int = 1280, height: int = 800) -> Perception:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": width, "height": height})

    try:
        if start_url:
            page.goto(start_url, wait_until="domcontentloaded")

        dom, screenshot = _screenshot_and_dom(page)
        return Perception(dom=dom, screenshot=screenshot)
    finally:
        browser.close()
        pw.stop()
