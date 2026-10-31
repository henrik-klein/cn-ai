# Aufgabe 2

## Vergleich der Modelle

| Frage                 | Modell         | TTFT (ms) | Gesamt (ms) | Antwort brauchbar?                                        |
| --------------------- | -------------- | --------: | ----------: | --------------------------------------------------------- |
| Prüfungsanmeldung     | `llama3.2:3b`  |      2048 |        7765 | Nein, vage, verlinkt HTWK Leipzig                         |
| Prüfungsanmeldung     | `qwen2.5:0.5b` |       368 |        3890 | Nein, ergibt keinen Sinn                                  |
| HTWG privat/staatlich | `llama3.2:3b`  |      4339 |       12396 | Nein, „staatlich und privat“, falscher Name               |
| HTWG privat/staatlich | `qwen2.5:0.5b` |       427 |        3423 | Nein, „weder privat noch staatlich“, erfundene Begriffe   |
| Bibliothek Leihfrist  | `llama3.2:3b`  |      2151 |       20917 | Nein, Fristen erfunden                                    |
| Bibliothek Leihfrist  | `qwen2.5:0.5b` |       381 |        1296 | Nein, beantwortet die Frage nicht                         |

## Aufgabe 2.2

Keines der beiden Modelle antwortet richtig (die HTWG ist staatlich).

- **`llama3.2:3b`** formuliert flüssig und überzeugend, erfindet aber Details wie einen falschen Namen und „staatlich und privat“.
- **`qwen2.5:0.5b`** liefert offensichtlichen Unsinn („Hochschule der Verfassung“).

Das Wissen fehlt in den Trainingsdaten beider Modelle. Das größere Modell ist dabei sogar **gefährlicher**, weil seine falsche Antwort glaubwürdig klingt.
