# AgenticAI

An exploration of Agentic AI patterns and frameworks using local LLMs with Ollama.

## Overview

AgenticAI is a project designed to study and implement agentic AI systems. It leverages local language models through Ollama to create autonomous agents that can perform complex tasks. The project demonstrates how to build extensible AI agents with clean code organization and professional report generation.

## Features

- Local LLM execution using Ollama
- Automatic JSON and HTML report generation
- Task-based agent workflows
- Clean, modular code architecture
- Easy-to-extend agent and task definitions

## Prerequisites

- Python 3.8+ (Check with: `python --version`)
- Ollama (installed via official script or package manager)
- pip (Python package manager)

### Checking Your Python Installation

```bash
# Check Python version
python --version  # Should be 3.8 or higher

# Check pip
pip --version

# If using global installation, verify pip points to correct Python:
which python
which pip
```

## Installation

### 1. Install Ollama

**On Linux/Mac (Development Container):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**On Windows:**
Download the Ollama app from [ollama.ai](https://ollama.ai)

### 2. Install Python Dependencies

#### Option A: Using Virtual Environment (Recommended)
```bash
cd /workspaces/AgenticAI
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Option B: Global Installation (Without venv)
If you prefer to install dependencies globally, run:

```bash
# Core dependencies for agentic.py
pip install crewai crewai-tools litellm python-dotenv

# Additional dependencies (installed automatically with crewai)
pip install openai pydantic aiohttp beautifulsoup4
```

**All Required Packages:**
- **crewai** - Agent framework for building AI crews
- **crewai-tools** - Tools for agents (web scraping, etc.)
- **litellm** - LLM interface library (supports Ollama, OpenAI, etc.)
- **openai** - OpenAI Python client (required by crewai)
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation using Python type hints
- **aiohttp** - Async HTTP client
- **beautifulsoup4** - HTML/XML parsing
- **requests** - HTTP library
- **tiktoken** - Token counting library
- **instructor** - Structured data extraction from LLMs
- **chromadb** - Vector database for embeddings
- **pyfunctional** - Functional programming utilities

**Quick install without venv:**
```bash
pip install crewai crewai-tools litellm openai python-dotenv
```

## Quick Start

### Step 1: Start Ollama Server

Open a terminal and run:
```bash
ollama serve
```

### Step 2: Download a Model

In another terminal, download the Llama 3 model:
```bash
ollama pull llama3
```

You can also use other models like `llama2`, `neural-chat`, `mistral`, etc.

### Step 3: Run the Agent

Execute the main script:
```bash
python agentic.py
```

This will:
- Create a Tech Researcher agent that analyzes AI trends
- Display results in the terminal
- Generate `research_results.json` - Structured JSON data
- Generate `research_results.html` - Beautifully formatted HTML report

## Project Structure

```
AgenticAI/
├── agentic.py              # Tech researcher agent
├── study.py                # UX auditor agent (uses CrewAI)
├── report.py               # Report generation module
├── research_results.json   # Generated JSON report (agentic.py)
├── research_results.html   # Generated HTML report (agentic.py)
├── ux_fix_report.html      # Generated UX audit report (study.py)
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── .git/                   # Git repository
```

## File Descriptions

### agentic.py
Initial agent implementation that:
- Initializes the Ollama connection
- Defines the research task
- Generates AI responses
- Orchestrates report generation
- Outputs: `research_results.json` and `research_results.html`

**Run with:**
```bash
python agentic.py
```

### study.py
Advanced multi-agent system using **CrewAI**:
- **Senior UX Auditor Agent** - Analyzes website usability issues
- **UI/UX Developer Agent** - Provides HTML/CSS fixes for identified issues
- Creates interactive crew workflows
- Outputs: `ux_fix_report.html`

**Run with:**
```bash
python study.py
```

**Requires CrewAI installation:**
```bash
pip install crewai crewai-tools
```

### report.py
Report generation module with utilities for:
- `save_to_json()` - Exports results in JSON format
- `save_to_html()` - Creates styled HTML reports
- `generate_report()` - Coordinates both exports

## Generated Output Files

### research_results.json
Contains structured data:
```json
{
  "task": "Analyze the top 3 AI trends for 2025",
  "model": "Llama3 (Local via Ollama)",
  "timestamp": "2025-01-24 16:45:30",
  "response": "...",
  "status": "success"
}
```

### research_results.html
Professional HTML report with:
- Gradient styling and modern design
- Metadata display (task, model, timestamp)
- Formatted research results
- Responsive mobile design

## Code Example

```python
import ollama
from report import generate_report

# Create and execute a task
prompt = "Analyze the top 3 AI trends for 2025"

response = ollama.generate(
    model="llama3",
    prompt=prompt,
    stream=False
)

# Generate both JSON and HTML reports
generate_report(
    response_text=response['response'],
    task="Analyze AI trends",
    model="Llama3 (Local via Ollama)"
)
```

## Extending the Project

### Adding New Agent Tasks

1. Modify the `prompt` variable in `agentic.py`
2. Update the task description
3. Run the script - reports auto-generate

### Customizing Reports

Edit `report.py` to:
- Change HTML styling in `save_to_html()`
- Add new JSON fields in `generate_report()`
- Implement new export formats

## Troubleshooting

### Import Module Not Found When Using Global Installation

If you see errors like `ModuleNotFoundError: No module named 'crewai'`:

```bash
# Verify the module is installed
pip list | grep crewai

# Reinstall if needed
pip install --upgrade crewai crewai-tools

# Check which Python your script uses
python -c "import sys; print(sys.executable)"

# Run script with explicit Python path
/usr/local/python/3.12.1/bin/python study.py
```

### Python Version Mismatch

If you have multiple Python versions, ensure pip installs to the correct one:

```bash
# Install to Python 3.12 specifically
python3.12 -m pip install crewai crewai-tools

# Run with same Python version
python3.12 study.py
```

### Ollama Connection Error
```
Make sure Ollama is running: ollama serve
```
- Ensure Ollama server is running on port 11434
- Check connection: `curl http://localhost:11434/api/tags`
- Verify model is installed: `ollama list`

### Model Not Found
```bash
ollama pull llama3
ollama list  # Verify installation
```

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Memory Issues
- Use smaller models like `neural-chat` or `orca-mini`
- Check available disk space: `df -h`
- Monitor memory usage during inference

## Available Ollama Models

Popular models you can pull:
- `llama3` - Meta's Llama 3 model (8B)
- `llama2` - Meta's Llama 2 model (7B)
- `mistral` - Mistral AI model (7B)
- `neural-chat` - Intel's Neural Chat model
- `orca-mini` - Small, efficient model
- `dolphin-mixtral` - Mixtral-based model

## Learning Resources

- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Models Library](https://ollama.ai/library)
- [LLM Agent Patterns](https://en.wikipedia.org/wiki/Intelligent_agent)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and contribute improvements to this project! 

### Ideas for Enhancement
- Add more agent types (Summarizer, Translator, etc.)
- Implement conversation memory
- Add database storage for reports
- Create a web interface
- Support for multiple LLM providers