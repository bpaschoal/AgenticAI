#!/usr/bin/env bash
# Setup + execução (tudo local via Ollama).
# Uso: ./run.sh          -> setup (se preciso) e roda
#      ./run.sh setup     -> só prepara o ambiente
set -euo pipefail
cd "$(dirname "$0")"

VISION_MODEL="${OLLAMA_VISION_MODEL:-qwen2.5vl}"

# 1. Ambiente virtual
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Dependências Python
pip install --upgrade pip
pip install -r requirements.txt
# install-deps precisa de sudo; ignora se não der
playwright install-deps chromium 2>/dev/null || \
  echo "(pulei install-deps — rode 'sudo playwright install-deps chromium' se o Chromium reclamar de libs)"
playwright install chromium

# 3. Sobe o Ollama em background só se ainda não estiver rodando
if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama não encontrado. Instale: curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi
if ! curl -sf localhost:11434 >/dev/null 2>&1; then
  echo "Iniciando ollama serve em background (log em /tmp/ollama.log)..."
  ollama serve > /tmp/ollama.log 2>&1 &
  for _ in $(seq 1 30); do
    curl -sf localhost:11434 >/dev/null 2>&1 && break
    sleep 1
  done
fi

# 4. Modelos (depois do serve; pula os que já existem)
ollama pull llama3.1
ollama pull "$VISION_MODEL"

# 5. Roda (a menos que seja só setup)
if [ "${1:-}" = "setup" ]; then
  echo "Setup concluído. Rode './run.sh' para executar."
  exit 0
fi
python3 main.py
