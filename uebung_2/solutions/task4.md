# Aufgabe 4

Modell `llama3.2:3b`, Embedding `granite-embedding:278m`, Qdrant, 14 Testfragen.

## 4.1 Alles in den Kontext

```bash
docker compose run --rm app alles.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app alles.py "Wo kann ich mein Auto abstellen?"
```

| Frage | Eingabe-Tokens | Dauer |
| --- | ---: | ---: |
| Klausur krank | 3.905 | 227,1 s |
| Auto abstellen | 3.898 | 20,0 s |

1. Bei beiden Aufrufen ist der Anfang des Prompts gleich: Anweisung plus komplette Wissensbasis. Nur die Frage am Ende unterscheidet sich. Ollama hält die Berechnung dieses Anfangs im Prompt-Cache, beim zweiten Aufruf muss es also nur die neuen Tokens der Frage rechnen. Das klappt nur, weil das feste Wissen vorne und die Frage hinten steht. Außerdem muss das Modell geladen bleiben: Nach 5 Minuten Leerlauf entlädt Ollama es, und der Cache ist weg. Ein früherer Versuch hat genau so 207 s gedauert.
2. Bei 2.000 Dateien wären es rund 370.000 Tokens pro Anfrage. Das passt nicht ins Kontextfenster von `llama3.2:3b` und kostet bei einer API etwa das Hundertfache pro Anfrage. Auf diesem Laptop würde schon der erste Aufruf Stunden dauern. Die Antwortqualität sinkt, weil das Modell die richtige Stelle in langem Kontext schlechter findet (Lost in the Middle, Context Rot).

## 4.2 Dateisuche

```bash
docker compose run --rm app datei_suche.py --woerter "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app datei_suche.py "Ich bin am Tag meiner Klausur krank. Was muss ich tun?"
docker compose run --rm app datei_suche.py --woerter "Wer sitzt in Raum F-201?"
```

1. Die Suche mit den Wörtern der Frage findet `beratung.md` (9), `bibliothek.md` (7) und `praxissemester.md` (4), aber nicht `pruefungsunfaehigkeit.md` (3). Die Treffer sind fast nur Wortteile: „tun“ in „Bera**tun**g“ und „S**tun**den“, „tag“ in „Mon**tag**“ und „Sams**tag**“. In der richtigen Datei stehen weder „krank“ noch „Klausur“, sondern „Prüfungstag“, „Attest“ und „Prüfungsunfähigkeit“.
2. Das Modell schlägt `Krankheit, Arzt, Medizin, Krankenhaus, Notdoktor, Notfall` vor. Davon trifft nur „Krankheit“, in `praxissemester.md`. Es hätte Fachbegriffe wie **Attest**, **Prüfungsunfähigkeit** oder **Rücktritt** wählen müssen. Selbst „Arzt“ verfehlt die Datei, denn dort steht „ärztliches“.
3. „f-201“ steht einmal in `praxissemester.md`, „raum“ dagegen in vielen Dateien und Wortteilen („Anmeldezeit**raum**“, „**Raum**nummer“). Jeder Treffer zählt gleich, also schlagen drei unspezifische Treffer den einen entscheidenden, und die Datei landet auf Rang 4. Die Bewertung müsste seltene Begriffe höher gewichten (IDF/BM25) und nur ganze Wörter zählen.
4. Claude Code hat (a) ein starkes Modell, das die Fachsprache kennt und gute Suchbegriffe wählt, und (b) eine Schleife: Es liest die Treffer, merkt, wenn sie nicht passen, und sucht mit neuen Begriffen, Regex oder Dateinamen weiter. Unser Aufbau sucht genau einmal.

## 4.3 RAG

```bash
docker compose run --rm app rag.py --index
docker compose run --rm app vergleich_wissen.py rag
```

1. `zerlege()` trennt an `## `-Überschriften, ohne Überschriften an Leerzeilen, und stellt jedem Abschnitt den Dokumenttitel voran.

| rag | Abschnitte | Kontext richtig | Antwort richtig | Tokens (Ø) | Dauer (Ø) |
| --- | ---: | ---: | ---: | ---: | ---: |
| ein Abschnitt pro Datei | 21 | 12/13 | 12/14 | 891 | 36,8 s |
| an Überschriften zerlegt | 48 | 12/13 | 13/14 | 567 | 24,6 s |

„Kontext richtig“ bleibt gleich, nur „F-201“ fehlt. „Antwort richtig“ steigt um eins: Bei „gestresst“ stand vorher die ganze `beratung.md` im Kontext, und das Modell fand die Stelle nicht. Jetzt bekommt es nur den passenden Abschnitt. Die Tokens sinken um 36 %.

2. In der Sammlung `campus` liegen 48 Punkte. Jeder besteht aus einem Vektor (768 Zahlen, Cosine) und dem Payload `datei` und `text`. `wissen.py` braucht den `text` als Kontext für das Modell und die `datei` für die Quellenangabe und die Messung „Kontext richtig“. Nebenbei: `indexed_vectors_count` ist 0. Unter 10.000 Punkten baut Qdrant keinen HNSW-Index und sucht exakt.
3. Mit `-k 1` kommt nur der Abschnitt über Krankheitstage aus `praxissemester.md` (0,719). Die Antwort ist falsch, aber billig (244 Tokens). Mit `-k 8` stehen alle drei Abschnitte von `pruefungsunfaehigkeit.md` im Kontext, dazu fünf unpassende. Das Modell vermischt sie und schickt die Studentin zur Psychosozialen Beratung (962 Tokens). Ein größeres k findet die richtige Stelle eher, bringt aber Rauschen und Kosten. k = 4 ist der bessere Kompromiss.

## 4.4 Vergleich

```bash
docker compose run --rm app vergleich_wissen.py
docker compose run --rm app vergleich_wissen.py alles
```

| Variante | Kontext richtig | Antwort richtig | Eingabe-Tokens (Ø) | Dauer (Ø) |
| --- | ---: | ---: | ---: | ---: |
| alles | 13/13 | 14/14 | 3904 | 30,6 s |
| woerter | 7/13 | 9/14 | 682 | 27,2 s |
| datei | 9/13 | 11/14 | 613 | 27,1 s |
| rag | 12/13 | 13/14 | 567 | 24,6 s |

Bei `alles` steckt im Durchschnitt der erste, ungecachte Aufruf (~4 min). Danach dauert jede Frage etwa 15–20 s.

1. Richtige Datei im Kontext, nach Fragetyp:

| Typ | alles | woerter | datei | rag |
| --- | ---: | ---: | ---: | ---: |
| direkt (4) | 4 | 3 | 4 | 4 |
| kennung (3) | 3 | 2 | 2 | 2 |
| umschrieben (6) | 6 | 2 | 3 | 6 |
| fehlt (1) | – | – | – | – |

`alles` gewinnt überall, weil keine Suche scheitern kann. Bei **direkten** Fragen reichen alle Suchen, `woerter` verliert nur „Ersatz-Campuskarte“, weil das Wort mit Bindestrich als ein Suchbegriff bleibt und so nicht im Text steht. Bei **Kennungen** finden alle § 17 und PA-12, aber keine Suche „F-201“: die Textsuche wegen der Zählung („raum“ gewinnt), RAG, weil eine Kennung im Embedding untergeht. Bei **umschriebenen** Fragen gewinnt RAG klar (6 gegen 2–3): Embeddings finden Bedeutung ohne gemeinsame Wörter, die Textsuche kennt keine Synonyme. Bei der Frage, deren Antwort **fehlt**, sagen alle Varianten richtig, dass sie keine Information haben.

2. In diesem Lauf gibt es keinen Fall mit richtiger Datei und falscher Antwort. Im ersten RAG-Lauf (ein Abschnitt pro Datei) aber schon: Bei „gestresst“ stand `beratung.md` im Kontext, die Antwort war trotzdem falsch. Das ist ein Fehler des Generators, nicht der Suche. Umgekehrt ist „Wie oft darf ich eine Prüfung schreiben?“ bei `woerter` und `datei` ohne richtige Datei als richtig gezählt, weil die Stichworte („drei“, „3“) leicht zufällig in einer Antwort vorkommen. Die getrennte Messung zeigt also, ob Suche oder Modell versagt, und dass die Stichwortprüfung grob ist.
3. Für diese Wissensbasis (~3.900 Tokens, ändert sich selten) würde ich `alles` mit Prompt-Caching nehmen: 14/14, keine Suche kann scheitern, und nach dem Cache ist es kaum langsamer. Umsteigen würde ich, sobald die Wissensbasis nicht mehr bequem ins Kontextfenster des Modells passt oder sich oft ändert, bei einem kleinen lokalen Modell schon bei einigen zehntausend Tokens. Dann auf eine hybride Suche: RAG mit Zerlegung als Basis (beste Suche hier, 12/13 bei den wenigsten Tokens) plus BM25 für Kennungen wie F-201, zusammengeführt per Reciprocal Rank Fusion.

## 4.5 Verbesserung: BM25

```bash
docker compose run --rm app vergleich_wissen.py woerter datei
```

| Variante | Kontext richtig | Antwort richtig | Tokens (Ø) | Dauer (Ø) |
| --- | ---: | ---: | ---: | ---: |
| woerter, Trefferzählung | 7/13 | 9/14 | 682 | 27,2 s |
| woerter, BM25 | **8/13** | 9/14 | **549** | 20,6 s |
| datei, Trefferzählung | 9/13 | 11/14 | 613 | 27,1 s |
| datei, BM25 | **10/13** | 11/14 | **531** | 27,2 s |

`suche_bm25()` in `datei_suche.py` ersetzt die reine Trefferzählung durch BM25: Es zählt nur ganze Wörter, gewichtet seltene Begriffe über die IDF höher, dämpft Wiederholungen und gleicht die Dateilänge aus. Mit `BM25 = False` bleibt die alte Suche aus TODO 4a verfügbar. Dadurch landet „F-201“ bei `woerter` jetzt auf Rang 1, und „Wie oft darf ich eine Prüfung schreiben?“ findet die richtige Datei. Weil keine Wortteile mehr treffen, kommen weniger unpassende Dateien in den Kontext (−20 % bzw. −13 % Tokens). Dafür verliert `woerter` die Frage „gestresst“, die vorher nur über Wortteile getroffen wurde. Synonyme („krank“ → „Attest“) löst auch BM25 nicht, dafür braucht es Embeddings.
