"""
Here the orchestrator is no longer a file of ours -- it's CrewAI itself running
in Process.hierarchical. In this mode, CrewAI automatically creates a "manager"
agent that reads the task, decides which agent to delegate to (based on each
one's role/goal/backstory) and aggregates the result. It's exactly the role that
orchestrator.py used to play by hand before.

Prerequisites (everything local, nothing leaves your machine):
    pip install crewai 'crewai[tools]' playwright ollama
    playwright install chromium
    ollama pull llama3.2:3b     # reasons/routes (the CrewAI "manager") -- light
    ollama pull qwen2.5vl       # vision: decides the clicks in the navigation loop
    ollama serve                # make sure it's running on localhost:11434
"""

import os

from crewai import Task, Crew, Process, LLM
from Agents import create_visual_navigation_agent

# Local LLM via Ollama -- it's the one that reasons and decides the routing.
# Default is a small model (~2.5 GB) that runs on machines with little RAM;
# switch it via OLLAMA_ROUTER_MODEL (e.g. "ollama/llama3.1" if you have >=8 GB free).
router_model = os.environ.get("OLLAMA_ROUTER_MODEL", "ollama/llama3.2:3b")
llm_local = LLM(model=router_model, base_url="http://localhost:11434")

nav_agent = create_visual_navigation_agent(llm_local)
# new_agent = create_new_agent(llm_local)   <- that's all it takes to add one more

task = Task(
    description=(
        "Go to example.com and tell me the text of the link shown on the page."
    ),
    expected_output="A direct, objective answer about what was asked.",
    # no fixed `agent=`: the manager decides who runs it, at runtime
)

crew = Crew(
    agents=[nav_agent],
    tasks=[task],
    process=Process.hierarchical,
    manager_llm=llm_local,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nFinal answer:", result)
