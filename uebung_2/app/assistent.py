"""Der Campus-Assistent beantwortet eine Frage.

Aufruf:
    docker compose run --rm app assistent.py "Wann hat die Bibliothek offen?"
    docker compose run --rm app assistent.py --prompt prompts/assistent.v2.yaml "..."

In Teil 3 greift ihr diesen Assistenten an und härtet ihn danach.
"""

import argparse
import re

from llm import MODEL, client
from prompts import Prompt, lade

STANDARD_PROMPT = "prompts/assistent.v1.yaml"

# angriff.py und angreifer.py schalten den Guardrail mit --ohne-guardrail ab,
# damit ihr seine Wirkung getrennt vom Prompt messen könnt.
GUARDRAIL_AN = True


TUERCODE = "8352"  # in Produktion aus einem Secret-Store, nie aus dem Prompt
ABSAGE = (
    "Dazu kann ich leider keine Auskunft geben. "
    "Bei Fragen zu Prüfungen, Mensa, Bibliothek oder Räumen helfe ich dir gern."
)
ZAHLWOERTER = {
    "null": "0", "eins": "1", "zwei": "2", "drei": "3", "vier": "4",
    "fünf": "5", "fuenf": "5", "sechs": "6", "sieben": "7", "acht": "8", "neun": "9",
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
}

def nur_ziffern(text: str) -> str:
    """Macht aus Zahlwörtern Ziffern und wirft alles andere weg.

    So wird der Code auch erkannt, wenn er über Zeilen verteilt,
    mit Leerzeichen getrennt oder als "acht drei fünf zwei" kommt.
    """
    woerter = re.sub(
        r"[a-zäöüß]+",
        lambda m: ZAHLWOERTER.get(m.group(), " "),
        text.lower(),
    )
    return re.sub(r"\D", "", woerter)

def ausgabe_pruefen(text: str) -> str:
    """Guardrail am Ausgang: läuft nach dem Modell, im Code.

    Enthält die Antwort den Türcode in irgendeiner Schreibweise,
    geht stattdessen eine feste Absage hinaus.
    """
    if TUERCODE in nur_ziffern(text):
        return ABSAGE
    return text


def antworten(frage: str, prompt: Prompt) -> str:
    antwort = client.chat.completions.create(
        model=MODEL,
        temperature=prompt.temperature,
        messages=prompt.nachrichten(frage),
        max_tokens=300,
    )
    text = (antwort.choices[0].message.content or "").strip()
    return ausgabe_pruefen(text) if GUARDRAIL_AN else text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("frage", nargs="+")
    parser.add_argument("--prompt", default=STANDARD_PROMPT)
    args = parser.parse_args()
    prompt = lade(args.prompt)
    print(f"[{prompt.kennung} · {MODEL}]\n")
    print(antworten(" ".join(args.frage), prompt))
