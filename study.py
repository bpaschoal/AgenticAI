from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool

# 1. Configuration: Connect to your local Ollama instance
# Ensure you have run `ollama pull llama3.2` in your terminal first
local_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

# 2. Tools: The "eyes" for our agents
scrape_tool = ScrapeWebsiteTool(website_url='https://sauce-demo.myshopify.com/') 

# 3. Agents: Defining the Roles
auditor = Agent(
    role='Senior UX Auditor',
    goal='Identify usability friction points regarding buttons, colors, and layout density.',
    backstory='You are a meticulous expert in accessibility. You find what is broken.',
    tools=[scrape_tool],
    llm=local_llm,
    verbose=True
)

developer = Agent(
    role='UI/UX Developer',
    goal='Propose specific HTML/CSS fixes for identified usability issues.',
    backstory='You are a creative coder who turns critiques into clean, functional solutions.',
    llm=local_llm,
    verbose=True
)

# 4. Tasks: The Workflow
audit_task = Task(
    description='Analyze the website and list the top 3 usability issues.',
    expected_output='A detailed list of 3 specific UX problems found on the page.',
    agent=auditor
)

fix_task = Task(
    description='Take the UX problems and create a detailed report that includes the problems and their code-based fixes. Format the output as structured text.',
    expected_output='A detailed report with specific UX issues found and their recommended HTML/CSS fixes.',
    agent=developer,
    context=[audit_task] # This passes the auditor's findings to the developer
)

# 5. The Crew: Bringing it all together
ux_crew = Crew(
    agents=[auditor, developer],
    tasks=[audit_task, fix_task],
    process=Process.sequential # Auditor finishes -> Developer starts
)

# Execute
results = ux_crew.kickoff()

# Extract the outputs from both tasks
audit_output = ux_crew.tasks[0].output.raw if ux_crew.tasks[0].output else "No audit data"
fix_output = ux_crew.tasks[1].output.raw if ux_crew.tasks[1].output else "No fix data"

# Create a proper HTML report
html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Auditoria UX</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 30px;
            border-left: 4px solid #764ba2;
            padding-left: 15px;
        }}
        .section {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            border-left: 4px solid #667eea;
            padding: 15px;
            overflow-x: auto;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        }}
        .timestamp {{
            color: #999;
            font-size: 0.9em;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Relatório de Auditoria UX - Análise Automática</h1>
        
        <h2>🔍 Problemas Identificados (Senior UX Auditor)</h2>
        <div class="section">
            <pre>{audit_output}</pre>
        </div>
        
        <h2>✅ Recomendações de Correção (UI/UX Developer)</h2>
        <div class="section">
            <pre>{fix_output}</pre>
        </div>
        
        <div class="timestamp">
            <p>Relatório gerado em: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Tecnologia: CrewAI + LLM Local (Ollama)</p>
        </div>
    </div>
</body>
</html>
"""

# Save the result to HTML file
with open('ux_fix_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Success! Check ux_fix_report.html for the results.")
print(f"📝 Audit findings: {len(audit_output)} characters")
print(f"🛠️ Fix recommendations: {len(fix_output)} characters")