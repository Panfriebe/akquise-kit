"""Prüft, ob Firmen, Domains oder Personen schon in der Kalt-Liste stehen (Tabelle oder Aussortiert).

    python3 .claude/skills/leads/scripts/dublette.py beispiel.de "Max Muster" "Andere Firma"

Ausgabe pro Begriff: "neu", "Zeile <Nr> (<Status>)" oder "aussortiert".
Verglichen wird der Kern (ohne www, ohne Endung, Kleinschreibung).
"""

import re
import sys

import _pfad  # noqa: F401
from kaltliste import lies_zeilen


def kern(s):
    s = re.sub(r"^https?://", "", s.strip().lower()).strip("/")
    s = s.replace("www.", "")
    if "." in s and " " not in s:
        teile = s.split(".")
        s = teile[-2] if len(teile) > 1 else s
    return re.sub(r"[^a-z0-9äöüß]+", " ", s).strip()


def main():
    begriffe = sys.argv[1:]
    if not begriffe:
        print(__doc__)
        sys.exit(1)
    text, zeilen = lies_zeilen()
    voll = "\n".join(text)
    m = re.search(r"^## Aussortiert.*?$(.*?)(?=^## |\Z)", voll, re.M | re.S)
    aussortiert = (m.group(1) if m else "").lower()
    aussortiert = re.sub(r"[^a-z0-9äöüß\n]+", " ", aussortiert)

    treffer_gesamt = 0
    for b in begriffe:
        k = kern(b)
        if not k:
            continue
        treffer = [z for z in zeilen if k in re.sub(r"[^a-z0-9äöüß]+", " ", (z["firma"] + " " + z["website"] + " " + z["person"]).lower())]
        if treffer:
            treffer_gesamt += 1
            print(f"{b:<30} Zeile " + ", ".join(f"{z['nr']} ({z['status']}, {z['firma']})" for z in treffer))
        elif f" {k} " in f" {aussortiert} ":
            treffer_gesamt += 1
            print(f"{b:<30} aussortiert (nicht erneut prüfen)")
        else:
            print(f"{b:<30} neu")
    print(f"\n{len(begriffe) - treffer_gesamt} von {len(begriffe)} neu.", file=sys.stderr)


if __name__ == "__main__":
    main()
