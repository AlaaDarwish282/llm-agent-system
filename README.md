# LLM Agent System

A production-ready multi-agent AI system built with **LangGraph**, **LangChain**, and **OpenAI GPT-4o**. The system automatically classifies incoming tasks and routes them to specialized agents — a ResearcherAgent for information gathering and a CoderAgent for writing and executing Python code.

## Architecture

```
User Request
     │
     ▼
[Classifier Node]
     │
     ├──► [ResearcherAgent] ──► Web Search + LLM Synthesis
     │
     ├──► [CoderAgent] ──► Code Generation + Execution + Self-Correction
     │
     └──► [SynthesizerNode] ──► Final Answer
```

## Features

- 🤖 **Automatic task routing** via LangGraph state machine
- 🔍 **Web-augmented research** using Tavily Search API
- 💻 **Sandboxed code execution** with self-correction loop (up to 3 retries)
- 🧠 **Conversation memory** with configurable sliding window
- 🚀 **FastAPI REST interface** with Swagger docs at `/docs`
- 🐳 **Docker-ready** deployment

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/AlaaDarwish282/llm-agent-system.git
cd llm-agent-system
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Run
python main.py
```

Visit `http://localhost:8000/docs` for the interactive API.

## API Usage

```bash
curl -X POST http://localhost:8000/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{"task": "Research the latest advances in quantum computing and summarize key breakthroughs"}'
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph 0.1 |
| LLM Provider | OpenAI GPT-4o / Anthropic Claude |
| Web Search | Tavily API |
| API Server | FastAPI + Uvicorn |
| Runtime | Python 3.11 |
| Container | Docker |

## Project Structure

```
llm-agent-system/
├── agents/
│   ├── orchestrator.py    # LangGraph state machine
│   ├── researcher.py      # Web research agent
│   └── coder.py           # Code generation agent
├── tools/
│   ├── web_search.py      # Tavily search wrapper
│   └── code_executor.py   # Sandboxed Python executor
├── memory/
│   └── store.py           # Conversation memory
├── api/
│   └── routes.py          # FastAPI endpoints
├── config/
│   └── settings.py        # Environment config
├── main.py
├── requirements.txt
└── Dockerfile
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | required |
| `ANTHROPIC_API_KEY` | Anthropic API key | optional |
| `TAVILY_API_KEY` | Tavily search key | required |
| `MODEL_NAME` | LLM model to use | `gpt-4o` |
| `MAX_ITERATIONS` | Max agent iterations | `10` |

## License

MIT
