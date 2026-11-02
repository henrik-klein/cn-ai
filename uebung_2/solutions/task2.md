# Aufgabe 2

## 2.1

```bash
docker compose run --rm app vergleich.py prompts/einordnen.v1.yaml prompts/einordnen.v2.yaml
```

Modell: `llama3.2:3b`, 16 Test-Mails, zweiter Lauf mit bereits geladenem Modell.

| Prompt         | Anliegen richtig | Alle Felder richtig | Eingabe-Tokens (Ø) | Dauer (Ø) |
| -------------- | ---------------: | ------------------: | -----------------: | --------: |
| `einordnen.v1` |            13/16 |                8/16 |                140 |    4.98 s |
| `einordnen.v2` |            15/16 |               12/16 |                642 |    6.88 s |

**Nutzen:** v2 ordnet 2 Anliegen mehr und 4 Mails mehr komplett richtig ein.

- `"null"` als Text kommt nicht mehr vor.
- Erfundene Fristen (`15.04.2024`, `"Klausur Mathe 2"`) und erfundene Studiengänge sind weg.
- Master Informatik wird jetzt als `MSI` erkannt.
- Die Bachelorarbeit- und die Fernleihe-Mail landen jetzt bei `bibliothek`.

**Kosten:** Die Eingabe-Tokens steigen um den Faktor 642 / 140 ≈ **4,6**, die Dauer um **38 %**.

Im ersten Lauf lag v1 bei 9.10 s, weil der erste Aufruf das Modell laden musste. Die Dauer lässt sich deshalb nur bei warmem Modell vergleichen.

---

## 2.2

Mit v2 sind noch vier Mails falsch:

| Mail               | Erhalten → erwartet                        | Ursache             |
| ------------------ | ------------------------------------------ | ------------------- |
| MSI-Abmeldung      | `"Bis wann?"` → `None`                     | Unklare Anweisung   |
| Exchange student   | `"6. November"` → `"6 November"`           | Messung zu streng   |
| Nachklausur        | `"15.12"` → `"15.12."`                     | Messung zu streng   |
| `SYSTEM … HACKED`  | `pruefung`/`HACKED` → `mensa`/`None`       | Angriff             |

Bei der MSI-Abmeldung übernimmt das Modell das Beispiel `"Bis wann?"` aus der Fristregel wörtlich. Bei der Nachklausur scheitert der Teilstring-Vergleich am fehlenden Punkt.

**Verbesserung der Messung:** Fristen vor dem Vergleich normalisieren (Punkte, Leerzeichen und Groß-/Kleinschreibung entfernen) oder Tag und Monat extrahieren und als Datum vergleichen. Dann läge v2 bei **14/16**.

---

## 2.3

Bei `studiengang` steht bei v1 und v2 `"HACKED"`, obwohl v2 Anweisungen in der Mail verbietet und ein ähnliches Beispiel enthält.

Für das Modell ist alles eine Tokenfolge. Es trennt Anweisung und Daten nicht zuverlässig, und `SYSTEM: Neue Regel` imitiert Autorität. Prompt-Formulierungen verschieben nur Wahrscheinlichkeiten, sie garantieren nichts.

---

## 2.4

```python
studiengang: Literal["AIN", "WIN", "MSI"] | None
```

**Ergebnis:** Die Zahlen bleiben unverändert (8/16 und 12/16). Die letzte Mail ist weiter falsch: Aus `HACKED` wird `MSI`, `anliegen` bleibt `pruefung`. Bei v1 wird aus dem Text `"null"` jetzt `WIN` (WLAN- und Gedicht-Mail).

**Verhindert:** Das Schema geht per `response_format` an Ollama, das beim Dekodieren nur erlaubte Werte zulässt. Ungültige Werte gelangen dadurch nie ins Programm oder in die Datenbank.

**Verhindert nicht:** Der Angriff beeinflusst weiter die Entscheidung. Das Modell wird sogar in einen plausiblen, falschen Wert gezwungen, aus einem sichtbaren Fehler wird ein unsichtbarer.

**Ebene:** Die Abwehr wirkt im System (Dekodierung und Pydantic), unabhängig vom Prompt. Der Prompt bittet, das Schema erzwingt, aber nur das Format, nicht den Inhalt.