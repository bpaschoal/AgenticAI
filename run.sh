#!/usr/bin/env bash
# Setup + run (everything local via Ollama).
# Usage: ./run.sh          -> sets up (if needed) and runs
#        ./run.sh setup     -> only prepares the environment
set -euo pipefail
cd "$(dirname "$0")"

# Reasoning/routing model: light default (~2 GB) for machines with little RAM.
# Accepts OLLAMA_ROUTER_MODEL with or without the "ollama/" prefix (used by main.py).
ROUTER_MODEL="${OLLAMA_ROUTER_MODEL:-llama3.2:3b}"
ROUTER_MODEL="${ROUTER_MODEL#ollama/}"
VISION_MODEL="${OLLAMA_VISION_MODEL:-qwen2.5vl}"

# 1. Virtual environment
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
# install-deps needs sudo; skip it if it fails
playwright install-deps chromium 2>/dev/null || \
  echo "(skipped install-deps — run 'sudo playwright install-deps chromium' if Chromium complains about libs)"
playwright install chromium

# 3. Start Ollama in the background only if it isn't already running
if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama not found. Install it: curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi
if ! curl -sf localhost:11434 >/dev/null 2>&1; then
  echo "Starting 'ollama serve' in the background (log at /tmp/ollama.log)..."
  ollama serve > /tmp/ollama.log 2>&1 &
  for _ in $(seq 1 30); do
    curl -sf localhost:11434 >/dev/null 2>&1 && break
    sleep 1
  done
fi

# 4. Models (after serve; skips the ones that already exist)
ollama pull "$ROUTER_MODEL"
ollama pull "$VISION_MODEL"

# 5. Run (unless it's setup only)
if [ "${1:-}" = "setup" ]; then
  echo "Setup complete. Run './run.sh' to execute."
  exit 0
fi
# CrewAI (in main.py) expects the model with the "ollama/" prefix; ensure that
# regardless of whether OLLAMA_ROUTER_MODEL was passed with or without it.
export OLLAMA_ROUTER_MODEL="ollama/${ROUTER_MODEL}"
python3 main.py
