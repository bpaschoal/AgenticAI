from crewai.tools import tool
from .visual_navigation_engine import VisualNavigationEngine


@tool("navigate_visually")
def navigate_visually(objective: str, context: str = "") -> str:
    """
    Opens a browser and executes a task by observing the screen and deciding
    on its own where to click/type -- without fixed selector rules. Use for
    unknown sites or apps, dynamic ones, or when you don't know the
    page structure beforehand.
    """
    engine = VisualNavigationEngine()
    return engine.execute(objective, context)