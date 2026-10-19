# Campus Assistant: Cloud-native AI

LLM-based assistant for HTWG Konstanz students, built step by step in the
Cloud-native AI course (WS 2026/27). The model is a swappable component:
which model is used is defined by configuration only, never in code.

## Architecture

| Service        | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| `ollama`       | Local model server, exposes an OpenAI-compatible API on port 11434      |
| `modell-laden` | One-shot job that pulls `llama3.2:3b` and `qwen2.5:0.5b`, then exits    |
| `app`          | Python client that sends requests to the model server                   |

Models are stored in the `ollama-modelle` volume and survive restarts.

## Requirements

- Docker with Compose v2
- ~3 GB of free disk space for the models

## Quick start

```bash
cp .env.example .env
docker compose up --build app
```

The first start downloads the models (~2.4 GB), which takes a few minutes.
The app then answers a default question and prints latency metrics.

## Configuration

All settings live in `.env`:

| Variable       | Description                          | Default                    |
|----------------|--------------------------------------|----------------------------|
| `LLM_BASE_URL` | OpenAI-compatible API endpoint       | `http://ollama:11434/v1`   |
| `LLM_MODEL`    | Model name                           | `llama3.2:3b`              |
| `LLM_API_KEY`  | API key (not required for Ollama)    | –                          |

To switch models, change `LLM_MODEL`. No code changes or rebuild needed.
See `.env.example` for the Academic Cloud (GWDG) configuration.

## Usage

Run any script in `app/` against the configured model:

```bash
docker compose run --rm app hallo_llm.py "How do I register for an exam?"
docker compose run --rm app sampling.py
docker compose run --rm app tokens.py
docker compose run --rm app einordnen.py
```

`app/` is mounted into the container, so code changes take effect immediately.
Rebuild only after changing `requirements.txt` or the `Dockerfile`.

## Exercise notes

- [Aufgabe 1](docs/task1.md): Setup, latency measurements and model answers
- [Aufgabe 2](docs/task2.md): Comparison of `llama3.2:3b` and `qwen2.5:0.5b`
- [Aufgabe 3](docs/task3.md): Sampling across temperatures and token counts
- [Aufgabe 4](docs/task4.md): Structured classification of student emails
- [Bonus](docs/bonus.md): Validating the content of model outputs
- [Reflection](docs/reflection.md): Reflection on the exercise

## Project structure

```
.
├── compose.yaml
├── .env.example
├── docs/
│   ├── task1.md         # notes and results for Aufgabe 1
│   ├── task2.md         # model comparison for Aufgabe 2
│   ├── task3.md         # sampling and tokens for Aufgabe 3
│   ├── task4.md         # email classification for Aufgabe 4
│   ├── bonus.md         # content validation of model outputs
│   └── reflection.md    # reflection on the exercise
└── app/
    ├── llm.py           # shared client, reads config from env
    ├── hallo_llm.py     # single request with TTFT measurement
    ├── sampling.py      # answer variance across temperatures
    ├── tokens.py        # token count German vs. English
    ├── einordnen.py     # structured classification of student emails
    └── mails.json       # test emails for einordnen.py
```