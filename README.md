# AI Agents with an Orchestrator (CrewAI + Ollama)

## What is an AI Agent?

An AI agent is a system that uses a language model (LLM) not just to answer questions, but to **make decisions and take actions** autonomously. Unlike a regular chatbot, an agent can:

- Analyze a goal and plan the steps to reach it
- Call external tools (APIs, databases, searches, code)
- Evaluate the results and decide the next step
- Repeat this cycle until the task is solved

In short: the agent reasons, acts, observes the result, and adjusts course.

## Why an "orchestrator"?

When a task is complex, a single agent doing everything on its own tends to get confused, slow, or inefficient. That's where the **orchestrator** comes in: a "coordinator" agent that doesn't do the heavy lifting directly, but decides **who does what**.

Think of it as a conductor: it doesn't play any instrument, but it makes sure each musician (specialized agent) comes in at the right time.

### How it works in practice

```
User → Orchestrator → decides which agent(s) to trigger
                ├── Research Agent
                ├── Coding Agent
                ├── Data Agent
                └── Writing Agent
         ← Orchestrator gathers the results and responds
```

The orchestrator is responsible for:

1. **Interpreting** the user's request
2. **Breaking** the task into smaller subtasks
3. **Delegating** each subtask to the most suitable specialized agent
4. **Consolidating** the responses into a coherent result

## When is this architecture worth it?

| Scenario | Single agent | Orchestrator + subagents |
|---|---|---|
| Simple, direct task | ✅ Ideal | Unnecessary |
| Task with multiple distinct steps | ⚠️ May get confused | ✅ Ideal |
| Needs specialization (e.g. code + research + data) | ❌ Limited | ✅ Ideal |
| Needs parallelism | ❌ Sequential | ✅ Can run in parallel |

## Typical components

- **LLM** — the "brain" that reasons and decides
- **Tools** — functions the agent can call (search, math, APIs)
- **Memory** — context of what has already been done in the conversation/task
- **Orchestrator** — control layer that manages multiple agents/tools
- **Subagents** — agents specialized in a specific function

---

## About this project

This repository is a concrete implementation of that architecture: a **visual web
navigation** system with an orchestrator in CrewAI running in hierarchical mode.

**Everything runs locally — nothing leaves your machine.** There is no API key and
no usage cost:

- The **reasoning/routing** (the CrewAI "manager") runs via **Ollama** with the
  `llama3.1` model.
- The **visual navigation agent** also runs on **Ollama**, with a vision model
  (`qwen2.5vl`) that looks at the screenshot and decides the next click.

In other words, the CrewAI orchestrator receives the task, decides when to trigger
the navigation agent, and consolidates the result — exactly as described in the
conceptual section above.

---

# Installation

## Summary — what needs to be installed

| # | Item | What for |
|---|---|---|
| 1 | **Python 3.10+** | Runs the project |
| 2 | **Ollama** | Runtime that serves the models locally |
| 3 | Model **`llama3.1`** (via Ollama) | Reasoning/routing (CrewAI manager) |
| 4 | Model **`qwen2.5vl`** (via Ollama) | Vision: decides the clicks in the navigation loop |
| 5 | **Python dependencies** (`crewai`, `crewai-tools`, `playwright`, `ollama`) | Project libraries |
| 6 | **Chromium browser** (via Playwright) | Browser the agent controls |

**Hardware requirements:** ~8 GB of free RAM minimum (~8B-parameter models),
16 GB+ recommended. Reserve 5-10 GB of disk per model pulled in Ollama (there are
two models here). A GPU helps a lot with speed, but is not required.

---

## 1. Install Python 3.10+

### Linux
On most distributions Python is already installed. Check the version:
```bash
python3 --version
```
If it's lower than 3.10 (or missing), install it (Debian/Ubuntu):
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip
```

### Windows
Download the installer from https://www.python.org/downloads/ and, **on the first
installer screen, check the "Add Python to PATH" box**. Then verify in PowerShell:
```powershell
python --version
```

---

## 2. Install Ollama

Ollama runs as a background service, exposing an API at `http://localhost:11434`.

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download and run the installer from https://ollama.com/download
(it also works via WSL2, using the Linux instructions above).

### Check that it's running (Linux and Windows)
```bash
ollama --version
```
If the service doesn't start on its own, start it manually in a separate terminal:
```bash
ollama serve
```

---

## 3. Pull the models used by the project

There are **two** models. With Ollama installed, run (same on Linux and Windows):
```bash
ollama pull llama3.1      # reasoning/routing (CrewAI manager)
ollama pull qwen2.5vl     # vision (decides the clicks in navigation)
```

- **Change the reasoning model:** edit the string in `main.py`
  (`llama3.2` is lighter; `mistral` also works):
  ```python
  llm_local = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
  ```
- **Change the vision model:** set the `OLLAMA_VISION_MODEL` environment variable
  (the default is `qwen2.5vl`). For click-coordinate grounding, `qwen2.5vl` is
  usually much better than `llama3.2-vision`.

---

## 4. Set up the Python environment and install the dependencies

First create and activate a virtual environment (in the project folder):

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
> If PowerShell blocks the activation script, run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and activate again.
> On the classic Command Prompt (cmd), use: `.venv\Scripts\activate.bat`

With the environment activated (the prompt shows `(.venv)`), install the
dependencies (same on both systems):
```bash
pip install -r requirements.txt
```

---

## 5. Install the Playwright browser

The navigation agent controls a Chromium via Playwright. Install it (same on Linux
and Windows, with `.venv` activated):
```bash
playwright install chromium
```
On Linux, if system libraries are missing, Playwright helps install them:
```bash
playwright install-deps chromium     # (may require sudo)
```

---

## 6. Run the project

Make sure Ollama is running (`ollama serve`) and `.venv` is activated. Then:
```bash
python main.py          # Windows
python3 main.py         # Linux/macOS
```

The `Crew` will run the visual navigation agent to interact with websites according
to the task described in `main.py`.

### Optional environment variables

| Variable | Default | What for |
|---|---|---|
| `OLLAMA_VISION_MODEL` | `qwen2.5vl` | Chooses the navigation vision model |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server address |

To set them (example with the vision model):
```bash
export OLLAMA_VISION_MODEL="qwen2.5vl"     # Linux/macOS
setx OLLAMA_VISION_MODEL "qwen2.5vl"       # Windows (applies from the next terminal on)
```

---

## 7. Adding a new agent

1. Create `Agents/new_agent.py` with a function `create_new_agent(llm) -> Agent`.
2. If it needs a new action, create the tool in `Tools/` with `@tool`.
3. Register the import in `Agents/__init__.py`.
4. In `main.py`, instantiate it and add it to the `Crew`'s `agents=[...]` list.

No other file needs to change — the CrewAI manager discovers the new agent
automatically from the list and decides when to delegate to it based on the
`role`/`goal`/`backstory` you write.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `Connection refused` on port 11434 | Ollama isn't running — run `ollama serve` |
| `model not found` | Model wasn't pulled — run `ollama pull llama3.1` and `ollama pull qwen2.5vl` |
| Very slow or hanging responses | Model too big for the available RAM/GPU — try `llama3.2` |
| Tool-calling not supported error | Not every Ollama model supports tool use — check the model page at ollama.com/library |
| Inaccurate clicks in navigation | Weak vision model — prefer `qwen2.5vl` via `OLLAMA_VISION_MODEL` |
| Browser doesn't open (navigation agent) | Run `playwright install chromium` again (and `playwright install-deps chromium` on Linux) |
| `command not found: playwright` / `pip` | The `.venv` isn't activated — activate it before running |
