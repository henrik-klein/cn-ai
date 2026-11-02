# Übung 2: Versioned prompts, prompt attacks and knowledge retrieval

Setup, configuration and architecture are described in the [main README](../README.md).

## Solutions

- [Aufgabe 1](solutions/task1.md): Prompts as versioned artifacts
- [Aufgabe 2](solutions/task2.md): Improving and measuring the classification
- [Aufgabe 3](solutions/task3.md): Attacking and hardening the assistant
- [Aufgabe 4](solutions/task4.md): Knowledge retrieval with file search and RAG
- [Bonus](solutions/bonus.md): A model attacks the assistant
- [Reflection](solutions/reflection.md): Reflection on the exercise

## Additions to the shared setup

| Addition                 | Purpose                                                                |
|--------------------------|------------------------------------------------------------------------|
| `qdrant`                 | Vector database for RAG, dashboard at <http://localhost:6333/dashboard> |
| `granite-embedding:278m` | Embedding model, always runs locally on Ollama                         |
| `EMBED_MODEL`            | Name of the embedding model in `.env`                                  |

The models are stored in the volume `cnai-ollama-modelle`, so exercises from
Übung 2 onward download them only once.

## Usage

`docker compose up --build app` runs `einordnen.py`. Run any script in `app/`
against the configured model:

```bash
cd uebung_2
docker compose run --rm app assistent.py "Wann hat die Bibliothek offen?"
docker compose run --rm app angriff.py prompts/assistent.v1.yaml
docker compose run --rm app vergleich.py prompts/einordnen.v1.yaml
```

Build the RAG index once before using it:

```bash
docker compose run --rm app rag.py --index
docker compose run --rm app rag.py "Wann hat die Mensa offen?"
docker compose run --rm app vergleich_wissen.py
```

## Project structure

```
.
├── compose.yaml
├── .env.example
├── solutions/
│   ├── task1.md              # versioned prompts for Aufgabe 1
│   ├── task2.md              # classification comparison for Aufgabe 2
│   ├── task3.md              # attacks and defenses for Aufgabe 3
│   ├── task4.md              # knowledge retrieval for Aufgabe 4
│   ├── bonus.md              # a model attacks the assistant
│   └── reflection.md         # reflection on the exercise
└── app/
    ├── llm.py                # shared client, reads config from env
    ├── prompts.py            # loads versioned prompts
    ├── prompts/              # prompts as versioned YAML files
    ├── einordnen.py          # structured classification of student emails
    ├── vergleich.py          # compares prompt versions on the test emails
    ├── assistent.py          # campus assistant answers a question
    ├── angriff.py            # attacks the assistant, measures the defense
    ├── angreifer.py          # a model attacks the assistant
    ├── wissen.py             # shared building blocks for retrieval
    ├── alles.py              # variant 0: whole knowledge base as context
    ├── datei_suche.py        # variant 1: file-based retrieval
    ├── rag.py                # variant 2: retrieval via embeddings
    ├── vergleich_wissen.py   # compares the variants on the test questions
    ├── wissen/               # knowledge base (fictional documents)
    ├── mails.json            # test emails
    ├── angriffe.json         # attacks for angriff.py
    └── fragen.json           # test questions for vergleich_wissen.py
```
