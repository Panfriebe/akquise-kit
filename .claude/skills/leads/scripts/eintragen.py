"""Hängt neue Leads an die Kalt-Liste an oder ergänzt die Aussortiert-Liste.

    python3 .claude/skills/leads/scripts/eintragen.py leads.json              # Liste von Objekten mit den Spalten der Kalt-Liste
    python3 .claude/skills/leads/scripts/eintragen.py leads.json --probe      # nur anzeigen, nichts schreiben
    python3 .claude/skills/leads/scripts/eintragen.py --aussortiert "Foo (zu groß, 120)" "Bar (Händler)"

JSON-Felder: firma (Pflicht), person (Pflicht), website, linkedin, detail,
groesse, branche, quelle, status (Standard "neu"), notiz. Dubletten (Firma oder
Domain schon in der Liste oder unter Aussortiert) werden übersprungen.
Die Zeilennummer vergibt das Skript.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import _pfad  # noqa: F401
from dublette import kern
from kaltliste import SPALTEN, als_zeile, lies_zeilen, schreibe, tabellen_ende


def main():
    p = argparse.ArgumentParser()
    p.add_argument("json", nargs="?")
    p.add_argument("--probe", action="store_true")
    p.add_argument("--aussortiert", nargs="+")
    a = p.parse_args()

    text, zeilen = lies_zeilen()

    if a.aussortiert:
        voll = "\n".join(text)
        m = re.search(r"^## Aussortiert.*?$", voll, re.M)
        if not m:
            sys.exit("Abschnitt '## Aussortiert' nicht in der Kalt-Liste gefunden.")
        heute = date.today().isoformat()
        marker = f"Geprüft {heute}: "
        for i, z in enumerate(text):
            if z.startswith(marker):
                text[i] = z.rstrip(".") + ", " + ", ".join(a.aussortiert) + "."
                break
        else:
            start = voll[:m.end()].count("\n") + 1
            ende = next((i for i in range(start, len(text)) if text[i].startswith("## ")), len(text))
            while ende > start and not text[ende - 1].strip():
                ende -= 1
            if ende > start and text[ende - 1].strip() and not text[ende - 1].startswith("Geprüft "):
                text.insert(ende, "")
                ende += 1
            text.insert(ende, marker + ", ".join(a.aussortiert) + ".")
        if not a.probe:
            schreibe(text)
        print(f"Aussortiert ergänzt: {', '.join(a.aussortiert)}")
        return

    if not a.json:
        print(__doc__)
        sys.exit(1)
    daten = json.loads(Path(a.json).read_text(encoding="utf-8"))
    if isinstance(daten, dict):
        daten = [daten]

    bekannt = "\n".join(text).lower()
    bekannt_norm = re.sub(r"[^a-z0-9äöüß\n]+", " ", bekannt).replace("\n", " ")
    naechste = max((int(z["nr"]) for z in zeilen), default=0) + 1
    letzte = tabellen_ende(text)
    neue = []
    for d in daten:
        firma, person = str(d.get("firma", "")).strip(), str(d.get("person", "")).strip()
        if not firma or not person:
            print(f"Übersprungen (firma oder person fehlt): {d}")
            continue
        schluessel = [kern(firma)] + ([kern(d["website"])] if d.get("website") else [])
        dup = [s for s in schluessel if s and f" {s} " in f" {bekannt_norm} "]
        if dup:
            print(f"Dublette, übersprungen: {firma} ({', '.join(dup)} steht schon in der Kalt-Liste)")
            continue
        z = {s: str(d.get(s, "")).strip().replace("|", "/") for s in SPALTEN}
        z["nr"] = str(naechste)
        z["status"] = z["status"] or "neu"
        if "Recherche" not in z["notiz"]:
            z["notiz"] = (z["notiz"].rstrip(".") + ". " if z["notiz"] else "") + f"Recherche {date.today().isoformat()}"
        neue.append(z)
        naechste += 1
        bekannt_norm += " " + " ".join(schluessel)

    for z in neue:
        print(als_zeile(z))
    if a.probe or not neue:
        print(f"\n{len(neue)} Zeilen (Probe, nichts geschrieben)." if a.probe else "\nNichts eingetragen.")
        return
    for k, z in enumerate(neue):
        text.insert(letzte + 1 + k, als_zeile(z))
    schreibe(text)
    print(f"\n{len(neue)} Zeilen eingetragen: {neue[0]['nr']} bis {neue[-1]['nr']}.")


if __name__ == "__main__":
    main()
