"""
Visual navigation engine, fully local: screenshot -> decide action -> execute ->
new screenshot. The "brain" that decides WHEN to call this tool runs on Ollama
via CrewAI; this internal vision loop also runs on Ollama, so nothing leaves the
machine.

Note: local vision models don't do reliable tool-calling, so instead of a tool
schema we ask the model for a single structured JSON action (Ollama's `format`)
and dispatch it ourselves. For click-coordinate grounding, qwen2.5vl is clearly
stronger than llama3.2-vision -- prefer it if you can pull it:
    ollama pull qwen2.5vl
Override the model with the OLLAMA_VISION_MODEL env var.
"""

import base64
import json
import os

from ollama import Client
from playwright.sync_api import sync_playwright

VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "qwen2.5vl")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
WIDTH, HEIGHT = 1280, 800

# The single action we ask the model to return each step. No tool-calling: the
# model just fills this JSON shape and we route on `action`.
ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["open_url", "click", "type", "press_key", "scroll", "task_completed"],
        },
        "url": {"type": "string"},
        "x": {"type": "integer"},
        "y": {"type": "integer"},
        "text": {"type": "string"},
        "key": {"type": "string"},
        "pixels": {"type": "integer"},
        "result": {"type": "string"},
    },
    "required": ["action"],
}

SYSTEM_PROMPT = (
    f"You operate a web browser by looking at screenshots. The screen is "
    f"{WIDTH}x{HEIGHT} pixels; coordinates start at (0,0) in the top-left.\n"
    "Each turn, look at the current screen and choose exactly ONE action, "
    "returning it as JSON matching the given schema:\n"
    '- open_url: navigate to a URL -> {"action":"open_url","url":"..."}\n'
    '- click: click at a point -> {"action":"click","x":123,"y":456}\n'
    '- type: type text in the focused element -> {"action":"type","text":"..."}\n'
    '- press_key: press a key (Enter, Tab...) -> {"action":"press_key","key":"Enter"}\n'
    '- scroll: scroll vertically by pixels -> {"action":"scroll","pixels":300}\n'
    '- task_completed: finish with the result -> {"action":"task_completed","result":"..."}\n'
    "Only output the JSON for the next single action."
)


class VisualNavigationEngine:
    def __init__(self, max_iterations: int = 15):
        self.max_iterations = max_iterations
        self._client = Client(host=OLLAMA_HOST)
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=False)
        self._page = self._browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})

    def open_url(self, url): self._page.goto(url, wait_until="domcontentloaded")
    def click(self, x, y): self._page.mouse.click(x, y)
    def type(self, text): self._page.keyboard.type(text, delay=20)
    def press_key(self, key): self._page.keyboard.press(key)
    def scroll(self, pixels): self._page.mouse.wheel(0, pixels)

    def _screenshot(self) -> str:
        self._page.wait_for_timeout(400)
        return base64.b64encode(self._page.screenshot()).decode()

    def _close(self):
        self._browser.close()
        self._pw.stop()

    def execute(self, objective: str, context: str = "") -> str:
        extra = f"\n\nAdditional context: {context}" if context else ""
        history: list[str] = []  # textual log of actions taken, keeps context bounded

        try:
            for _ in range(self.max_iterations):
                log = "\n".join(history) if history else "(none yet)"
                user_text = (
                    f"Objective: {objective}{extra}\n\n"
                    f"Actions taken so far:\n{log}\n\n"
                    "Current screen is attached. Decide the next single action."
                )
                response = self._client.chat(
                    model=VISION_MODEL,
                    format=ACTION_SCHEMA,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_text, "images": [self._screenshot()]},
                    ],
                )

                data = json.loads(response["message"]["content"])
                action = data.get("action")

                if action == "task_completed":
                    return data.get("result", "")
                if action not in ("open_url", "click", "type", "press_key", "scroll"):
                    history.append(f"Ignored invalid action: {data}")
                    continue

                params = {k: data[k] for k in ("url", "x", "y", "text", "key", "pixels") if k in data}
                getattr(self, action)(**params)
                history.append(f"{action}({params})")

            return "Did not complete within iteration limit."
        finally:
            self._close()
