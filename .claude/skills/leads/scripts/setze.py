"""Ändert Felder einer Zeile der Kalt-Liste.

    python3 .claude/skills/leads/scripts/setze.py 12 website=beispiel.de "groesse=11 bis 50 (LinkedIn)" linkedin=linkedin.com/in/max-muster
    python3 .claude/skills/leads/scripts/setze.py 12 status=angenommen
    python3 .claude/skills/leads/scripts/setze.py 12 "notiz+=Website geprüft 2026-11-10, Shopify, 2. Grad"
    python3 .claude/skills/leads/scripts/setze.py 12 "notiz-=noch prüfen"     # Teilstring aus der Notiz entfernen

Felder: firma, website, person, linkedin, detail, groesse, branche, quelle, status,
letzter_kontakt, follow_up, notiz. "feld=wert" ersetzt, "notiz+=text" hängt an,
"notiz-=text" entfernt. Status muss einer von: neu, angefragt, angenommen, dm,
antwort, gespräch, angebot, nein.
"""

import re
import sys

import _pfad  # noqa: F401
from kaltliste import SPALTEN, STATUS, als_zeile, lies_zeilen, schreibe


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    nr, aenderungen = sys.argv[1], sys.argv[2:]
    text, zeilen = lies_zeilen()
    z = next((z for z in zeilen if z["nr"] == nr), None)
    if not z:
        sys.exit(f"Zeile {nr} nicht in der Kalt-Liste.")

    for a in aenderungen:
        m = re.match(r"(\w+)(\+=|-=|=)(.*)", a, re.S)
        if not m or m.group(1) not in SPALTEN or m.group(1) == "nr":
            sys.exit(f"Unverständlich oder kein Feld: {a}")
        feld, op, wert = m.group(1), m.group(2), m.group(3).strip().replace("|", "/")
        if feld == "status" and wert not in STATUS:
            sys.exit(f"Unbekannter Status '{wert}'. Erlaubt: {', '.join(STATUS)}")
        if op == "=":
            z[feld] = wert
        elif op == "+=":
            alt = z[feld].strip()
            z[feld] = (alt.rstrip(".") + ". " if alt else "") + wert
        else:
            z[feld] = re.sub(r"\s*\.?\s*" + re.escape(wert) + r"\.?", "", z[feld]).strip()
        print(f"#{nr} {feld}: {z[feld][:120]}")

    text[z["_index"]] = als_zeile(z)
    schreibe(text)


if __name__ == "__main__":
    main()
