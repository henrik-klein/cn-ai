# Campus Assistant: Cloud-native AI

LLM-based assistant for HTWG Konstanz students, built step by step in the
Cloud-native AI course (WS 2026/27). The model is a swappable component:
which model is used is defined by configuration only, never in code.

## Exercises

| Exercise                       | Topic                                                  | Status      |
|--------------------------------|--------------------------------------------------------|-------------|
| [Übung 1](uebung_1/README.md)  | Model server setup, sampling, structured classification | Done        |
| [Übung 2](uebung_2/README.md)  | Versioned prompts, prompt attacks, knowledge retrieval  | Done        |

Each exercise README links its solutions and lists its scripts.

## Requirements

- Docker with Compose v2
- ~3 GB of free disk space for the models

## Quick start

Each exercise is a self-contained project with its own `compose.yaml` and `.env`.
Run all commands from inside the exercise folder:

```bash
cd uebung_1   # or any other exercise
cp .env.example .env
docker compose up --build app
```

The first start downloads the models, which takes a few minutes. Run a specific
script with:

```bash
docker compose run --rm app <script>.py
```

Stop an exercise with `docker compose down` before starting another one, since
they all use port 11434.

## Architecture

All exercises share these services. Additions are listed in the exercise README.

| Service        | Purpose                                                            |
|----------------|--------------------------------------------------------------------|
| `ollama`       | Local model server, exposes an OpenAI-compatible API on port 11434 |
| `modell-laden` | One-shot job that pulls the models, then exits                     |
| `app`          | Python client that sends requests to the model server              |

The models `llama3.2:3b` and `qwen2.5:0.5b` are used throughout. They are stored
in a Docker volume and survive restarts.

`app/` is mounted into the container, so code changes take effect immediately.
Rebuild only after changing `requirements.txt` or the `Dockerfile`.

## Configuration

All settings live in `.env`:

| Variable       | Description                       | Default                  |
|----------------|-----------------------------------|--------------------------|
| `LLM_BASE_URL` | OpenAI-compatible API endpoint    | `http://ollama:11434/v1` |
| `LLM_MODEL`    | Model name                        | `llama3.2:3b`            |
| `LLM_API_KEY`  | API key (not required for Ollama) | `nicht-noetig`           |

To switch models, change `LLM_MODEL`. No code changes or rebuild needed.
See `.env.example` for the Academic Cloud (GWDG) configuration.
