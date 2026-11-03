"""Zeigt, was heute in der Kalt-Liste fällig ist.

    python3 .claude/skripte/faellig.py              # heute
    python3 .claude/skripte/faellig.py 2026-11-10   # anderes Datum
"""

import sys
from datetime import date

from kaltliste import lies_zeilen

AKTION = {
    "antwort": "ANTWORTEN",
    "angenommen": "DM schicken (/dm)",
    "dm": "Follow-up, ein Satz (/dm)",
    "angefragt": "Annahme prüfen",
}


def main():
    heute = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    _, zeilen = lies_zeilen()

    faellig = []
    for z in zeilen:
        status = z["status"]
        if status not in AKTION:
            continue
        # Antworten und Annahmen sind immer sofort fällig
        if status in ("antwort", "angenommen") or (z["follow_up"] and z["follow_up"] <= heute):
            faellig.append(z)

    reihenfolge = list(AKTION)
    faellig.sort(key=lambda z: (reihenfolge.index(z["status"]), z["follow_up"]))

    neu = sum(1 for z in zeilen if z["status"] == "neu" and z["firma"])
    print(f"Fällig am {heute}: {len(faellig)}   |   Noch nicht angefragt (neu): {neu}\n")
    for z in faellig:
        print(f"#{z['nr']:>3}  {AKTION[z['status']]:<28} {z['firma'][:22]:<22} {z['person'][:40]}")
    if not faellig:
        print("Nichts fällig. Annahmen auf LinkedIn prüfen und mit setze.py auf 'angenommen' setzen.")


if __name__ == "__main__":
    main()
