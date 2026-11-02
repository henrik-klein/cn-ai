# Reflexion

## 1. Gemessene vs. gefühlte Verbesserung

Gemessen heißt: gleiche Mails, gleiches Modell, feste Kriterien, und man sieht auch den Preis. v2 hat 4 Mails mehr komplett richtig, kostet aber 4,6-mal so viele Tokens. Der `Literal`-Fix fühlte sich nach Schutz an, hat an den Zahlen aber nichts geändert.

## 2. „Mit einem guten System-Prompt ist Prompt Injection gelöst.“

Nein. v2 hatte 0 % Verletzungen, aber 38 % Fehlablehnungen. v3 ist fast gleich und lässt die Mail-Injection trotzdem wieder durch. Und `einordnen.v2` hat `HACKED` übernommen, obwohl der Prompt das verbietet.

## 3. Welche Abwehr hat am meisten gebracht?

Der Guardrail am Ausgang (Systemebene): v1 ging von 80 % auf 13 % Verletzungen, ohne Fehlablehnungen. Zusammen mit v3, wo der Code gar nicht mehr im Prompt steht, kann er nicht mehr rausgehen. Gegen PWNED oder die gefälschte Mail hilft aber beides nicht.

## 4. Warum auch die Fehlablehnungsrate?

Wer alles ablehnt, hat 0 % Verletzungen, hilft aber niemandem. v2 hat 0 % Verletzungen, beantwortet aber nicht mal „Wie melde ich mich von einer Prüfung ab?“.

## 5. „RAG ist immer besser als Textsuche.“

Nicht immer. Bei umschriebenen Fragen findet RAG 6/6 Dateien, die Textsuche nur 2–3. „F-201“ findet RAG aber nicht, die Textsuche mit BM25 schon. Und bei unserer kleinen Wissensbasis war „alles“ mit 14/14 am besten, nur siebenmal so teuer.

## 6. Warum Kontext und Antwort getrennt?

Damit man sieht, ob die Suche oder das Modell schuld ist. Bei „gestresst“ war im ersten RAG-Lauf die richtige Datei da, die Antwort trotzdem falsch, also ein Modellfehler. Bei „Wie oft darf ich eine Prüfung schreiben?“ war es umgekehrt: falsche Datei, aber die Antwort zählte trotzdem als richtig.