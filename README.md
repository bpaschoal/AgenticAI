# AgenticAI

An exploration of Agentic AI patterns and frameworks using local LLMs with Ollama.

## Overview

AgenticAI is a project designed to study and implement agentic AI systems. It leverages local language models through Ollama to create autonomous agents that can perform complex tasks. The project demonstrates how to build extensible AI agents with clean code organization and professional report generation.

## Features

- 🤖 Local LLM execution using Ollama
- 📊 Automatic JSON and HTML report generation
- 🎯 Task-based agent workflows
- 🏗️ Clean, modular code architecture
- 📁 Easy-to-extend agent and task definitions

## Prerequisites

- Python 3.8+
- Ollama (installed via official script or package manager)
- pip or conda

## Installation

### 1. Install Ollama

**On Linux/Mac (Development Container):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**On Windows:**
Download the Ollama app from [ollama.ai](https://ollama.ai)

### 2. Install Python Dependencies

```bash
cd /workspaces/AgenticAI
pip install ollama litellm python-dotenv
```

The following packages will be installed:
- **ollama** - Python client for Ollama
- **litellm** - LLM interface library
- **python-dotenv** - Environment variable management

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
├── agentic.py              # Main agent implementation
├── report.py               # Report generation module
├── research_results.json   # Generated JSON report
├── research_results.html   # Generated HTML report
├── README.md               # Project documentation
└── .git/                   # Git repository
```

## File Descriptions

### agentic.py
Main agent implementation that:
- Initializes the Ollama connection
- Defines the research task
- Generates AI responses
- Orchestrates report generation

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

### Ollama Connection Error
```
⚠️ Make sure Ollama is running: ollama serve
```
- Ensure Ollama server is running on port 11434
- Check connection: `curl http://localhost:11434/api/tags`

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