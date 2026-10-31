# Aufgabe 1

## Setup

```bash
docker compose up --build app
```

**Ollama** dient als Model Server. Wir laden zwei Modelle in das Volume:

| Modell         | ID             | Größe  | Geladen           |
| -------------- | -------------- | ------ | ----------------- |
| `qwen2.5:0.5b` | `a8b0c5157701` | 397 MB | About an hour ago |
| `llama3.2:3b`  | `a80c4f17acd5` | 2.0 GB | About an hour ago |

### Ausgabe

```text
app-1  | Modell:              llama3.2:3b @ http://ollama:11434/v1
app-1  | Time to First Token: 13852 ms
app-1  | Gesamtdauer:         20481 ms
app-1  | Zeichen Antwort:     332
```

Das Laden des Modells in den RAM und die Analyse der Frage (Prefill) dauern ca. **13 Sekunden**, die Antwort selbst wird innerhalb von ca. **7 Sekunden** generiert.

---

## Frage 1

```bash
docker compose run --rm app hallo_llm.py "Wie melde ich mich zu einer Prüfung an?"
```

| Aufruf         | Time to First Token | Gesamtdauer | Zeichen Antwort |
| -------------- | ------------------: | ----------: | --------------: |
| Erster Aufruf  |            46855 ms |    64358 ms |             360 |
| Danach         |             2048 ms |     7765 ms |             309 |

### Antwort 1

> Um dich zu einer Prüfung anzumelden, kannst du die folgenden Schritte ausprobieren:
>
> 1. Besuche die Prüfungsinformationen in der Studien- und Prüfungseinrichtung, um alle möglichen Prüfungsstellen, -termine und -arten zu finden.
> 2. Suche nach Prüfungsmeldedaten oder deinen persönlichen Prüfungsmeldedaten und melde dich dann an und deine Prüfungsmeldung an.

### Antwort 2

> Um dich zu einer Prüfung anzumelden, kannst du folgende Schritte unternehmen:
>
> 1. Besuche die Prüfungsseit einer der HT-Weggrenen.
> 2. Informiere dich in der Prüfungsvorlesung und/oder online über Anforderungen und Pflichten der Prüfung.
>
> Du findest mehr Informationen hier: www.htwk.de/de/pruefungen

---

## Frage 2

```bash
docker compose run --rm app hallo_llm.py "Ist die HTWG Konstanz eine private oder eine staatliche Hochschule?"
```

```text
Time to First Token: 4339 ms
Gesamtdauer:         12396 ms
Zeichen Antwort:     201
```

### Antwort

> Hallo!
>
> Die Hochschule für Technologie, Wirtschaft und Gestaltung Konstanz (HTWG) in Konstanz ist sowohl eine staatliche als auch eine private Hochschule. Der Begriff "stiftungsräumig" ist oft genannt.

---

## Frage 3

```bash
docker compose run --rm app hallo_llm.py "Wie lange kann ich ein Buch in der Bibliothek ausleihen?"
```

```text
Time to First Token: 2151 ms
Gesamtdauer:         20917 ms
Zeichen Antwort:     651
```

### Antwort

> Eine gute Frage!
>
> Der Ausleihtermin hängt von dem Buch und der jeweiligen Bibliothekskarte ab. Die HTWG-Konstanz hat eine folgende Leihfrist:
>
> - Standardausleihtermin: 21 Tage (ab dem Ablauf der Leihfrist kann man das Buch wieder ausleihen)
> - Studenten mit Bibliothekskarte als "Student an der HTWG Konstanz" können bis 2 Mal pro Jahr bis zum 2. Arbeitstag des zweiten Semester jeweils 30 Tage lang ausleihen.
> - Um eine Ausleihe zu verlängern, muss man sich bei der Bibliothek melden.
>
> Bitte beachte, dass es auch Möglichkeiten zur Ausleiheitsverlängerung für ein weiteres Mal gibt, wenn man die gesetzlichen Mindestausleihterminer nicht erreicht hat.
