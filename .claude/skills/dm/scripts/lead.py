"""Druckt eine Zeile der Kalt-Liste mit allen Feldern.

    python3 .claude/skills/dm/scripts/lead.py 17
    python3 .claude/skills/dm/scripts/lead.py Beispielfirma
    python3 .claude/skills/dm/scripts/lead.py Muster
"""

import sys

import _pfad  # noqa: F401
from kaltliste import SPALTEN, lies_zeilen

LABEL = {
    "nr": "Zeile", "firma": "Firma", "website": "Website", "person": "Person(en)",
    "linkedin": "LinkedIn", "detail": "Detail (Aufhänger)", "groesse": "Größe",
    "branche": "Branche", "quelle": "Quelle", "status": "Status",
    "letzter_kontakt": "Letzter Kontakt", "follow_up": "Follow-up", "notiz": "Notiz",
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    suche = " ".join(sys.argv[1:]).strip().lower()
    _, zeilen = lies_zeilen()

    if suche.isdigit():
        treffer = [z for z in zeilen if z["nr"] == suche]
    else:
        treffer = [z for z in zeilen
                   if suche in z["firma"].lower() or suche in z["person"].lower()]

    if not treffer:
        print(f"Kein Lead zu '{suche}' in der Kalt-Liste gefunden. Nachfragen, nicht raten.")
        sys.exit(2)
    if len(treffer) > 1:
        print(f"{len(treffer)} Treffer, bitte Zeilennummer nennen:")
        for z in treffer:
            print(f"  {z['nr']}: {z['firma']} ({z['person']})")
        sys.exit(3)

    z = treffer[0]
    for s in SPALTEN:
        print(f"{LABEL[s]}: {z[s] or '(leer)'}")
    if "mit notiz" in z["notiz"].lower():
        print("\nHinweis: Die Kontaktanfrage ging laut Notiz MIT Notiz raus. Die DM braucht ein anderes Detail.")


if __name__ == "__main__":
    main()
