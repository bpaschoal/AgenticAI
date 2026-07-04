from crewai import Agent, LLM
from Tools import navigate_visually 


def create_visual_navigation_agent(llm: LLM) -> Agent:
    return Agent(
        role="Web navigation specialist",
        goal="Execute tasks in websites and apps observing the screen and deciding the necessary actions",
        backstory="You know how to operate any visual interface without depending on fixed layout rules.",
        tools=[navigate_visually],
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )