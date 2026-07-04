# Agentes de IA com Orquestrador

## O que é um Agente de IA?

Um agente de IA é um sistema que usa um modelo de linguagem (LLM) não apenas para responder perguntas, mas para **tomar decisões e executar ações** de forma autônoma. Diferente de um chatbot comum, um agente pode:

- Analisar um objetivo e planejar os passos para alcançá-lo
- Chamar ferramentas externas (APIs, bancos de dados, buscas, código)
- Avaliar os resultados e decidir o próximo passo
- Repetir esse ciclo até resolver a tarefa

Em resumo: o agente raciocina, age, observa o resultado e ajusta a rota.

## Por que "orquestrador"?

Quando uma tarefa é complexa, um único agente fazendo tudo sozinho tende a ficar confuso, lento ou ineficiente. É aí que entra o **orquestrador**: um agente "coordenador" que não executa o trabalho pesado diretamente, mas decide **quem faz o quê**.

Pense nele como um maestro: não toca nenhum instrumento, mas garante que cada músico (agente especializado) entre na hora certa.

### Como funciona na prática

```
Usuário → Orquestrador → decide qual(is) agente(s) acionar
                ├── Agente de Pesquisa
                ├── Agente de Código
                ├── Agente de Dados
                └── Agente de Escrita
         ← Orquestrador junta os resultados e responde
```

O orquestrador é responsável por:

1. **Interpretar** a solicitação do usuário
2. **Dividir** a tarefa em subtarefas menores
3. **Delegar** cada subtarefa ao agente especializado mais adequado
4. **Consolidar** as respostas em um resultado coerente

## Quando vale a pena usar essa arquitetura?

| Cenário | Agente único | Orquestrador + subagentes |
|---|---|---|
| Tarefa simples e direta | ✅ Ideal | Desnecessário |
| Tarefa com múltiplas etapas distintas | ⚠️ Pode confundir | ✅ Ideal |
| Necessidade de especialização (ex: código + pesquisa + dados) | ❌ Limitado | ✅ Ideal |
| Precisa de paralelismo | ❌ Sequencial | ✅ Pode rodar em paralelo |

## Componentes típicos

- **LLM** — o "cérebro" que raciocina e decide
- **Ferramentas (tools)** — funções que o agente pode chamar (busca, cálculo, APIs)
- **Memória** — contexto do que já foi feito na conversa/tarefa
- **Orquestrador** — camada de controle que gerencia múltiplos agentes/ferramentas
- **Subagentes** — agentes especializados em uma função específica

## Resumo

Um agente de IA age de forma autônoma para cumprir objetivos. Quando a tarefa é grande demais para um agente só, um **orquestrador** entra em cena para dividir o trabalho entre agentes especializados e juntar os resultados no final — trazendo mais organização, escalabilidade e qualidade ao processo.
