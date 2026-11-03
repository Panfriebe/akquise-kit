"""Trägt verschickte Kontaktanfragen in die Kalt-Liste ein.

    python3 .claude/skills/anfragen/scripts/markiere.py 5 6 7                       # Status angefragt, letzter Kontakt heute, Follow-up nach Einstellung
    python3 .claude/skills/anfragen/scripts/markiere.py 5 --url 5=linkedin.com/in/max-muster   # gefundene Profil-URL mit eintragen
    python3 .claude/skills/anfragen/scripts/markiere.py 8 --uebersprungen "Profil nur mit E-Mail"  # nur Notiz, Status bleibt
    python3 .claude/skills/anfragen/scripts/markiere.py 9 --ausstehend              # Anfrage war schon ausstehend, zählt nicht als heute
    python3 .claude/skills/anfragen/scripts/markiere.py 6 --datum 2026-11-10

Schreibt nur Zeilen mit Status "neu" (sonst --erzwingen). Notiz-Zusatz
standardmäßig "Anfrage ohne Notiz per Browser <Datum>".
"""

import argparse
import sys
from datetime import date

import _pfad  # noqa: F401
from kaltliste import als_zeile, einstellungen, lies_zeilen, plus_werktage, schreibe


def ergaenze(notiz, zusatz):
    notiz = notiz.strip()
    return (notiz.rstrip(".") + ". " if notiz else "") + zusatz.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("nrs", nargs="+")
    p.add_argument("--datum", default=date.today().isoformat())
    p.add_argument("--url", action="append", default=[], help="NR=URL, mehrfach möglich")
    p.add_argument("--notiz", help="eigener Notiz-Zusatz statt des Standards")
    p.add_argument("--uebersprungen", help="Grund; Status bleibt, nur Notiz")
    p.add_argument("--ausstehend", action="store_true", help="war schon ausstehend, kein heutiges Datum")
    p.add_argument("--erzwingen", action="store_true")
    a = p.parse_args()
    e = einstellungen()

    urls = dict(u.split("=", 1) for u in a.url)
    text, zeilen = lies_zeilen()
    nach_nr = {z["nr"]: z for z in zeilen}
    fehlt = [n for n in a.nrs if n not in nach_nr]
    if fehlt:
        sys.exit(f"Nicht in der Kalt-Liste: {', '.join(fehlt)}")

    for n in a.nrs:
        z = nach_nr[n]
        if z["status"] != "neu" and not a.erzwingen and not a.uebersprungen:
            print(f"#{n} {z['firma']}: Status ist '{z['status']}', nicht 'neu'. Übersprungen (sonst --erzwingen).")
            continue
        if n in urls:
            z["linkedin"] = urls[n].strip()
        if a.uebersprungen:
            z["notiz"] = ergaenze(z["notiz"], f"Übersprungen {a.datum}: {a.uebersprungen}")
            print(f"#{n} {z['firma']}: Notiz ergänzt, Status bleibt '{z['status']}'.")
        elif a.ausstehend:
            z["status"] = "angefragt"
            z["notiz"] = ergaenze(z["notiz"], f"Anfrage war am {a.datum} schon ausstehend (Datum unbekannt)")
            print(f"#{n} {z['firma']}: angefragt (ausstehend, ohne Datum).")
        else:
            z["status"] = "angefragt"
            z["letzter_kontakt"] = a.datum
            z["follow_up"] = plus_werktage(a.datum, e["follow_up_werktage"]).isoformat()
            z["notiz"] = ergaenze(z["notiz"], a.notiz or f"Anfrage ohne Notiz per Browser {a.datum}")
            print(f"#{n} {z['firma']}: angefragt {a.datum}, Follow-up {z['follow_up']}.")
        text[z["_index"]] = als_zeile(z)

    schreibe(text)


if __name__ == "__main__":
    main()
