# Aufgabe 1

## 1.1

`nachrichten()` setzt die Mail in den Prompt ein, der als `self` aus der YAML-Datei geladen wurde. Mit `str.format` würde Python im gesamten Prompt-Text jede geschweifte Klammer als Platzhalter deuten. In unseren Prompts stehen aber oft JSON-Beispiele mit geschweiften Klammern. Für diese gibt es kein passendes Argument, deshalb käme es zu einem `KeyError`. `replace` sucht dagegen nur genau die Zeichenkette `{eingabe}` und lässt den restlichen Prompt unverändert.

---

## 1.2

Sonst passen die Messwerte im README nicht mehr zum Prompt und lassen sich weder nachprüfen noch vergleichen.

---

## 1.3

```bash
docker compose run --rm app einordnen.py --prompt prompts/einordnen.v1.yaml
```

Mit `einordnen.v1` und `llama3.2:3b` stimmen **13 von 16** Anliegen und **8 von 16** komplette Einordnungen.
