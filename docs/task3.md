# Aufgabe 3

## Aufgabe 3.1: Sampling

### 3.1.1

**Prompt:** „Erfinde einen Namen für ein neues Gericht in der Mensa. Antworte nur mit dem Namen.“

| Temperature | Verschiedene Antworten (5 Durchläufe) |
| ----------: | ------------------------------------: |
|         0.0 |                                     1 |
|         0.7 |                                     4 |
|         1.2 |                                     5 |

#### Temperature 0.0

| Anzahl | Antwort        |
| -----: | -------------- |
|     5× | „Sonnenblume“ |

#### Temperature 0.7

| Anzahl | Antwort                       |
| -----: | ----------------------------- |
|     2× | „Sonnenblume“                 |
|     1× | „Kulturauslese“               |
|     1× | „Sonnenblume Sunset“          |
|     1× | „Sonnenblumenfleischkugeln“   |

#### Temperature 1.2

| Anzahl | Antwort                                     |
| -----: | ------------------------------------------- |
|     1× | „Sunblaze“                                  |
|     1× | „Zukunftsblum“                              |
|     1× | „Sonnenbrater“                              |
|     1× | „Schwarzwaldberry-Burgunder-Gläserling“     |
|     1× | Schnitzelpuffer-Paprika                     |

### 3.1.2

In unseren Läufen lieferte Temperature 0 jeweils fünfmal dieselbe Antwort. **Garantiert ist das aber nicht.**

- Bei Temperature 0 wird zwar immer das wahrscheinlichste Token gewählt, doch die Berechnung mit Gleitkommazahlen ist nicht exakt reproduzierbar.
- Je nach Hardware, paralleler Ausführung oder Batching mit anderen Anfragen weichen die Logits minimal ab.
- Liegen zwei Tokens fast gleichauf, kann das den Gewinner ändern, und alle folgenden Tokens bauen auf dieser Abweichung auf.

Ein fester Seed oder Caching verringern das, garantieren aber nichts.

### 3.1.3

**Prompt:** „Ist die HTWG Konstanz eine private oder staatliche Hochschule? Antworte mit einem Satz.“

| Temperature | Verschiedene Antworten (5 Durchläufe) |
| ----------: | ------------------------------------: |
|         0.0 |                                     1 |
|         0.7 |                                     3 |
|         1.2 |                                     5 |

#### Temperature 0.0

| Anzahl | Antwort                                                                       |
| -----: | ----------------------------------------------------------------------------- |
|     5× | Die Hochschule für Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule. |

#### Temperature 0.7

| Anzahl | Antwort                                                                                         |
| -----: | ----------------------------------------------------------------------------------------------- |
|     2× | Die HTWG Konstanz ist eine staatliche Hochschule.                                               |
|     2× | Die Hochschule für Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule.       |
|     1× | Die HTWG Konstanz (Hochschule für Technik und Wirtschaft Konstanz) ist eine staatliche Hochschule. |

#### Temperature 1.2

| Anzahl | Antwort                                                                                                                         |
| -----: | ------------------------------------------------------------------------------------------------------------------------------- |
|     1× | Die Hochschule für Technologie, Wirtschaft und Gesellschaft (HTWG) Konstanz ist eine staatliche Hochschule, die 1992 aus dem Bildungszentrum der |
|     1× | Die Hochschule für Technik und Wirtschaft (HTWG) in Konstanz ist eine staatliche Hochschule.                                    |
|     1× | Die HTWG Konstanz ist eine staatliche Hochschule.                                                                               |
|     1× | Die Hochschule für Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule.                                       |
|     1× | Die Hochschule Technik und Wirtschaft (HTWG) Konstanz ist eine staatliche Hochschule.                                           |

#### Auswertung

Der Kern der Antwort („staatlich“) ist bei allen Temperaturen **richtig**.

- Schon bei **Temperature 0** ist aber der ausgeschriebene Name falsch („Hochschule für Technik und Wirtschaft“ statt „Hochschule Konstanz Technik, Wirtschaft und Gestaltung“).
- Erst bei **1,2** kommen weitere Fehler dazu: ein erfundenes „Gesellschaft“ und eine unbelegte Gründungsgeschichte.

Fehler bei Temperature 0 sind die wahrscheinlichste Ausgabe des Modells und kommen daher **aus den Trainingsdaten**. Fehler, die erst bei hoher Temperature auftreten, entstehen **durch das Sampling** unwahrscheinlicher Tokens, auf denen das Modell dann weiter aufbaut.

---

## Aufgabe 3.2: Tokens

```bash
docker compose run --rm app tokens.py
```

### 3.2.1

```text
Deutsch    63 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 14 Tokens mehr (+29%).
```

### 3.2.2

```text
Deutsch    52 Tokens für 8 Wörter
Englisch   44 Tokens für 16 Wörter

Deutsch braucht 8 Tokens mehr (+18%).
```

#### Auswertung

Mit langen Komposita braucht Deutsch für **8 Wörter 52 Tokens**, Englisch für denselben Inhalt in **16 Wörtern 44 Tokens**.

- **Absolut und prozentual** ist der Unterschied kleiner als beim ersten Text, weil der kürzere Satz den festen Overhead des Chat-Formats stärker gewichtet.
- **Pro Wort** ist er aber deutlich größer: Der Tokenizer ist auf Englisch optimiert und zerlegt lange zusammengesetzte Wörter wie „Rückmeldegebührenüberweisungsbestätigung“ in viele Teile, während häufige englische Wörter meist ein einzelnes Token sind.

Da pro Token abgerechnet und gerechnet wird, sind deutsche Anfragen **teurer und langsamer**, als die Wortzahl vermuten lässt.
