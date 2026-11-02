"""Variante 1: File-based Retrieval, Dateien per Textsuche finden.

Aufruf:
    docker compose run --rm app datei_suche.py "Wann hat die Mensa offen?"
    docker compose run --rm app datei_suche.py --woerter "Wann hat die Mensa offen?"

So arbeiten Coding-Agenten wie Claude Code: kein Index, keine Embeddings.
Erst Suchbegriffe überlegen, dann mit grep suchen, dann die passenden
Dateien lesen. Die Suchbegriffe kommen entweder vom Modell (Standard)
oder mit --woerter einfach aus den Wörtern der Frage.
"""

import argparse
import math
import re
import time
from collections import Counter

from pydantic import BaseModel, Field

from einordnen import schema_von
from llm import MODEL, client
from prompts import lade
from wissen import Treffer, antworten, dokumente, zeigen

MAX_DATEIEN = 3
MAX_BEGRIFFE = 6
BM25 = True  # Teil 4.5: False = Trefferzählung aus TODO 4a

# Wörter, die in fast jedem Dokument stehen und nichts über das Thema sagen.
STOPPWOERTER = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einer",
    "und", "oder", "ich", "mein", "meine", "meinen", "mir", "mich", "wir",
    "ist", "sind", "bin", "hat", "habe", "kann", "darf", "muss", "wie", "was",
    "wo", "wer", "wann", "warum", "wofür", "noch", "mit", "für", "von", "bis",
    "auf", "aus", "bei", "zu", "zum", "zur", "im", "in", "am", "an", "es",
    "nicht", "viel", "kostet", "oft", "total",
}


class Suchbegriffe(BaseModel):
    begriffe: list[str] = Field(max_length=MAX_BEGRIFFE)


def woerter_der_frage(frage: str) -> list[str]:
    """Die naive Variante: jedes Wort der Frage ist ein Suchbegriff."""
    woerter = re.findall(r"[\wÄÖÜäöüß§-]+", frage.lower())
    return [w for w in woerter if w not in STOPPWOERTER and len(w) > 2]


def begriffe_vom_modell(frage: str) -> list[str]:
    """Das Modell überlegt sich Suchbegriffe, auch Synonyme und Fachwörter."""
    prompt = lade("prompts/suchbegriffe.v1.yaml")
    antwort = client.chat.completions.create(
        model=MODEL,
        temperature=prompt.temperature,
        messages=prompt.nachrichten(frage),
        response_format=schema_von(Suchbegriffe),
        max_tokens=100,
    )
    try:
        return Suchbegriffe.model_validate_json(antwort.choices[0].message.content or "").begriffe
    except ValueError:  # ungültiges JSON oder zu viele Begriffe
        return woerter_der_frage(frage)


def woerter(text: str) -> list[str]:
    """Zerlegt einen Text in ganze Wörter ("tag" trifft nicht "Montag")."""
    return re.findall(r"[\wäöüß§-]+", text.lower())


def suche(begriffe: list[str], max_dateien: int = MAX_DATEIEN) -> list[Treffer]:
    """Unser grep: findet die Dateien, in denen die Begriffe am häufigsten vorkommen.

    Groß- und Kleinschreibung spielt keine Rolle, und ein Begriff zählt
    auch als Teil eines längeren Worts ("karte" findet "Campuskarte").
    Jede Datei bekommt als Wert die Zahl ihrer Treffer. Zurück kommen die
    besten max_dateien Dateien mit ihrem ganzen Text, Dateien ohne Treffer
    nie.
    """
    # TODO 4a (Teil 4.2): Setzt die Suche um.
    #   - dokumente() liefert {dateiname: text} für alle Dateien.
    #   - Zählt für jede Datei, wie oft die Begriffe darin vorkommen,
    #     ohne auf Groß- und Kleinschreibung zu achten (str.lower, str.count).
    #   - Nur Dateien mit mindestens einem Treffer kommen in die Liste,
    #     als Treffer(datei, text, wert).
    #   - Sortiert absteigend nach wert und gebt die ersten max_dateien zurück.
    gefunden = []
    for datei, text in dokumente().items():
        klein = text.lower()
        wert = sum(klein.count(b.lower()) for b in begriffe)
        if wert > 0:
            gefunden.append(Treffer(datei, text, wert))
    gefunden.sort(key=lambda t: t.wert, reverse=True)
    return gefunden[:max_dateien]


def suche_bm25(
    begriffe: list[str], max_dateien: int = MAX_DATEIEN, k1: float = 1.5, b: float = 0.75
) -> list[Treffer]:
    """Bewertet die Dateien mit BM25 statt mit der reinen Trefferzahl.

    Seltene Begriffe zählen mehr, Wiederholungen in einer Datei werden
    gedämpft, und die Länge der Datei wird ausgeglichen.
    """
    texte = dokumente()
    zaehler = {datei: Counter(woerter(text)) for datei, text in texte.items()}
    laengen = {datei: sum(z.values()) for datei, z in zaehler.items()}
    n = len(texte)
    schnitt = sum(laengen.values()) / n
    suchwoerter = [wort for begriff in begriffe for wort in woerter(begriff)]

    gefunden = []
    for datei, text in texte.items():
        wert = 0.0
        for wort in suchwoerter:
            df = sum(wort in z for z in zaehler.values())
            idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
            tf = zaehler[datei][wort]
            wert += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * laengen[datei] / schnitt))
        if wert > 0:
            gefunden.append(Treffer(datei, text, wert))
    gefunden.sort(key=lambda t: t.wert, reverse=True)
    return gefunden[:max_dateien]


def abrufen(frage: str, nur_woerter: bool = False) -> tuple[list[Treffer], list[str], float]:
    start = time.perf_counter()
    begriffe = woerter_der_frage(frage) if nur_woerter else begriffe_vom_modell(frage)
    treffer = suche_bm25(begriffe) if BM25 else suche(begriffe)
    return treffer, begriffe, time.perf_counter() - start


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("frage", nargs="+")
    parser.add_argument("--woerter", action="store_true", help="Wörter der Frage statt Modell")
    args = parser.parse_args()
    frage = " ".join(args.frage)
    treffer, begriffe, sekunden = abrufen(frage, args.woerter)
    print(f"Suchbegriffe: {begriffe}")
    for t in treffer:
        print(f"  {t.wert:>4.0f}  {t.datei}")
    print()
    zeigen(antworten(frage, treffer, sekunden))
