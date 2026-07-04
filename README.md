# Agentic project (CrewAI + Ollama)

Sistema de navegação visual web com um orchestrator (CrewAI em modo hierárquico).
O raciocínio/roteamento roda localmente via Ollama; o agente de navegação visual
usa Claude só na etapa de visão.

## 1. Pré-requisitos

- Python 3.10 ou superior
- ~8 GB de RAM livres no mínimo (modelos de 8B parâmetros), 16 GB+ recomendado
- Espaço em disco: 5-10 GB por modelo baixado no Ollama

## 2. Instalar o Ollama

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Baixe o instalador em https://ollama.com/download (roda melhor via WSL2, se disponível).

### Verificar se está rodando
O Ollama roda como serviço em background, expondo uma API em `http://localhost:11434`.
```bash
ollama --version
```
Se o serviço não subir sozinho, inicie manualmente:
```bash
ollama serve
```

### Baixar o modelo usado no projeto
```bash
ollama pull llama3.1
```
Outras opções válidas: `llama3.2` (mais leve, roda em menos RAM) ou `mistral`.
Pra trocar o modelo, basta editar a string em `main.py`:
```python
llm_local = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
```

## 3. Configurar o ambiente Python

Crie e ative um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Instale o navegador usado pelo Playwright (necessário para o agente de navegação):
```bash
playwright install chromium
```

## 4. Configurar a chave da Anthropic (só para o agente de navegação visual)

O `navegador_visual_engine.py` usa a API da Anthropic para a parte de visão
(decidir onde clicar a partir do screenshot). Exporte sua chave como variável
de ambiente:
```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"     # Linux/macOS
setx ANTHROPIC_API_KEY "sua-chave-aqui"       # Windows
```
Se você não for usar o agente de navegação visual, pode remover essa
dependência e o arquivo correspondente sem afetar o resto do projeto.

## 5. Rodar o projeto

Com o Ollama rodando (`ollama serve`) e o ambiente virtual ativado:
```bash
python main.py
```

O `Crew` vai executar o agente de navegação visual (`agente_navegador`) para
interagir com websites conforme a tarefa descrita em `main.py`.

## 6. Adicionando um novo agente

1. Crie `agentes/novo_agente.py` com uma função `criar_agente_novo(llm) -> Agent`.
2. Se ele precisar de uma ação nova, crie a tool em `ferramentas/` com `@tool`.
3. Registre a importação em `agentes/__init__.py`.
4. No `main.py`, instancie e adicione à lista `agents=[...]` do `Crew`.

Nenhum outro arquivo precisa mudar — o manager do CrewAI descobre o novo
agente automaticamente pela lista e decide quando delegar pra ele com base
no `role`/`goal`/`backstory` que você escrever.

## Solução de problemas

| Sintoma | Causa provável |
|---|---|
| `Connection refused` na porta 11434 | Ollama não está rodando — rode `ollama serve` |
| Respostas muito lentas ou travando | Modelo grande demais para a RAM/GPU disponível — tente `llama3.2` |
| Erro de tool calling não suportado | Nem todo modelo do Ollama suporta tool use — confira a página do modelo em ollama.com/library |
| Navegador não abre (agente de navegação) | Rode `playwright install chromium` novamente |
| Erro de autenticação da Anthropic | Confira se `ANTHROPIC_API_KEY` está exportada na sessão atual do terminal |