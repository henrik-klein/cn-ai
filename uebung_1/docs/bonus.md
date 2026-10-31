# Zusatz: Ausgaben inhaltlich absichern

## Umsetzung

- **Validator `null_text_to_none`** (`mode="before"`): `"null"`, `"None"` und `""` werden bei `studiengang` und `frist` zu echtem `None`.
- **Validator `known_program_only`**: `studiengang` ist nur gültig, wenn es in `DEGREE_PROGRAMS` (`AIN`, `WIN`, `MSI`) steht, sonst `None`.
- **Fristprüfung in `einordnen()`**: Steht die erkannte Frist nicht wörtlich in der Mail, wird sie auf `None` gesetzt und eine Warnung ausgegeben. Die Prüfung passiert im Code, nicht im Modell.
- **Messung in `auswerten()`**: Anliegen und Studiengang werden exakt verglichen, die Frist zählt als richtig, wenn die erwartete Frist im Ergebnis enthalten ist.

---

## Ergebnis

| Stand   | Alle drei Felder richtig (`llama3.2:3b`) |
| ------- | ---------------------------------------: |
| Vorher  |                                   4 von 8 |
| Nachher |                                   6 von 8 |

### Änderungen

| # | Mail                 | Vorher                     | Nachher             |
| -: | -------------------- | -------------------------- | ------------------- |
| 4 | eduroam              | `"null"` als Text          | echtes `null` ✓     |
| 5 | MSI Klausurabmeldung | Frist `bis zum 15.04.2024` | Frist `null` ✓      |

```text
Warning: deadline 'bis zum 15.04.2024' not found in mail
```

### Weiterhin falsch

| # | Mail             | Fehler                                 |
| -: | ---------------- | -------------------------------------- |
| 7 | IEEE Xplore      | Anliegen `pruefung` statt `bibliothek` |
| 8 | Prompt-Injection | Studiengang `WIN` erfunden             |

---

## Auswertung

Die Validatoren und die Fristprüfung fangen **Formfehler** und **erfundene Werte** ab, die nicht in der Mail stehen. Mail 8 zeigt aber die Grenze: `WIN` ist ein gültiges Kürzel aus der Liste. Die Whitelist erkennt nur **unbekannte** Kürzel, nicht erfundene gültige. Dafür müsste man, wie bei der Frist, prüfen, ob der Studiengang in der Mail vorkommt. Das ist bei abgeleiteten Werten wie „Angewandte Informatik“ → `AIN` (Mail 7) aber nicht per einfachem Textvergleich möglich. Falsche Anliegen wie bei Mail 7 lassen sich durch Validierung gar nicht erkennen, da `pruefung` ein erlaubter Wert ist.