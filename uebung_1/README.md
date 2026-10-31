# Übung 1: Model server, sampling and classification

Setup, configuration and architecture are described in the [main README](../README.md).

## Solutions

- [Aufgabe 1](docs/task1.md): Setup, latency measurements and model answers
- [Aufgabe 2](docs/task2.md): Comparison of `llama3.2:3b` and `qwen2.5:0.5b`
- [Aufgabe 3](docs/task3.md): Sampling across temperatures and token counts
- [Aufgabe 4](docs/task4.md): Structured classification of student emails
- [Bonus](docs/bonus.md): Validating the content of model outputs
- [Reflection](docs/reflection.md): Reflection on the exercise

## Usage

`docker compose up --build app` answers a default question and prints latency
metrics. Run any script in `app/` against the configured model:

```bash
cd uebung_1
docker compose run --rm app hallo_llm.py "How do I register for an exam?"
docker compose run --rm app sampling.py
docker compose run --rm app tokens.py
docker compose run --rm app einordnen.py
```

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
