"""
Aqui o orchestrator não é mais um arquivo nosso -- é o próprio CrewAI rodando
em Process.hierarchical. Nesse modo, o CrewAI cria automaticamente um agente
"manager" que lê a tarefa, decide para qual agente delegar (com base no role/
goal/backstory de cada um) e agrega o resultado. É exatamente o papel que o
orchestrator.py fazia na mão antes.

Pré-requisitos (tudo local, nada sai da máquina):
    pip install crewai 'crewai[tools]' playwright ollama
    playwright install chromium
    ollama pull llama3.1        # raciocina/roteia (o "manager" do CrewAI)
    ollama pull qwen2.5vl       # visão: decide os cliques no loop de navegação
    ollama serve                # garanta que está rodando em localhost:11434
"""

from crewai import Task, Crew, Process, LLM
from Agents import create_visual_navigation_agent

# LLM local via Ollama -- é ele quem raciocina e decide o roteamento
llm_local = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

agente_navegador = create_visual_navigation_agent(llm_local)
# agente_novo = criar_agente_novo(llm_local)   <- é só isso pra adicionar mais um

tarefa = Task(
    description=(
        "Vá até example.com e diga qual é o texto do link que aparece na página."
    ),
    expected_output="Uma resposta direta e objetiva sobre o que foi pedido.",
    # sem `agent=` fixo: o manager decide quem executa, em runtime
)

crew = Crew(
    agents=[agente_navegador],
    tasks=[tarefa],
    process=Process.hierarchical,
    manager_llm=llm_local,
    verbose=True,
)

if __name__ == "__main__":
    resultado = crew.kickoff()
    print("\nResposta final:", resultado)