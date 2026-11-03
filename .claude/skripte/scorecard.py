"""Zählt die Tageswerte aus der Kalt-Liste und trägt sie in die Scorecard ein.

    python3 .claude/skripte/scorecard.py                     # heute, nur zählen und anzeigen
    python3 .claude/skripte/scorecard.py --eintragen
    python3 .claude/skripte/scorecard.py 2026-11-10 --eintragen --notiz "..."

Gezählt wird pro Firma, nicht pro Person (die Kalt-Liste kennt nur den letzten
Kontakt pro Firma). Bereits gefüllte Felder werden nicht überschrieben, außer
mit --ueberschreiben. Fehlt die Zeile für das Datum, wird sie angelegt.
"""

import argparse
from datetime import date

from kaltliste import lies_scorecard, lies_zeilen, schreibe_scorecard, scorecard_zeile

# Spaltenname in der Scorecard -> Status in der Kalt-Liste mit letztem Kontakt am Datum
ZAEHLUNG = {"anfragen": "angefragt", "dms": "dm", "follow-ups": "dm",
            "antworten": "antwort", "gespräche": "gespräch", "angebote": "angebot"}


def zaehle(datum):
    _, zeilen = lies_zeilen()
    heute = [z for z in zeilen if z["letzter_kontakt"] == datum]
    werte = {k: sum(z["status"] == s for z in heute) for k, s in ZAEHLUNG.items()}
    # Follow-up und DM teilen den Status "dm": Follow-up ist eine DM mit "Follow-up" in der Notiz
    werte["follow-ups"] = sum(z["status"] == "dm" and "follow-up" in z["notiz"].lower() for z in heute)
    werte["dms"] = sum(z["status"] == "dm" for z in heute) - werte["follow-ups"]
    return werte


def main():
    p = argparse.ArgumentParser()
    p.add_argument("datum", nargs="?", default=date.today().isoformat())
    p.add_argument("--eintragen", action="store_true")
    p.add_argument("--ueberschreiben", action="store_true")
    p.add_argument("--notiz", default="")
    a = p.parse_args()

    werte = zaehle(a.datum)
    print(f"{a.datum}: " + ", ".join(f"{k} {v}" for k, v in werte.items()))
    if not a.eintragen:
        return

    text, spalten, tage = lies_scorecard()
    c, i = scorecard_zeile(text, spalten, tage, a.datum)
    for k, v in werte.items():
        if k in spalten and v and (a.ueberschreiben or not c[spalten[k]]):
            c[spalten[k]] = str(v)
    if a.notiz and "notiz" in spalten:
        alt = c[spalten["notiz"]].strip()
        c[spalten["notiz"]] = (alt.rstrip(".") + ". " if alt else "") + a.notiz.strip()
    text[i] = "| " + " | ".join(c) + " |"
    schreibe_scorecard(text)
    print("In die Scorecard eingetragen.")


if __name__ == "__main__":
    main()
