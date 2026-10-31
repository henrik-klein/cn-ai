# Reflexion

## 1. Warum steht das Modell in `.env` und nicht im Code?

So bleibt das Modell austauschbar: Ein Wechsel ist eine Zeile in `.env` statt einer Codeänderung, und derselbe Code läuft unverändert lokal oder in der Cloud. Außerdem gehört der API-Key als Secret nicht ins Repository.

## 2. Welche Temperature habt ihr in `einordnen.py` gewählt, und warum?

Ich habe `temperature=0` gewählt, weil die Einordnung keine Kreativität braucht und dieselbe Mail immer dasselbe Ergebnis liefern soll. Korrekt wird das Modell dadurch aber nicht, nur vorhersagbar.

## 3. Was garantiert `response_format` mit Schema, und was nicht?

Das Schema garantiert die Form: Das Modell kann nur gültiges JSON mit den richtigen Feldern und erlaubten Werten erzeugen. Den Inhalt garantiert es nicht, denn `"null"` als Text oder eine erfundene Frist sind trotzdem gültige Strings.

## 4. Wann lokales Modell, wann Cloud-Dienst?

**Lokal**, wenn sensible Daten das eigene System nicht verlassen dürfen und keine Kosten pro Token anfallen sollen.

**Cloud**, wenn Qualität und Geschwindigkeit wichtiger sind: Große Modelle laufen dort auf GPUs, und man muss keine eigene Hardware betreiben.