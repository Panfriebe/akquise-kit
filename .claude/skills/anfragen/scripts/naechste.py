"""Die nächsten Leads für Kontaktanfragen aus der Kalt-Liste, in Versandreihenfolge.

    python3 .claude/skills/anfragen/scripts/naechste.py 12        # die nächsten 12 (versandbereite zuerst, dann Namenssuche)
    python3 .claude/skills/anfragen/scripts/naechste.py --alle    # alle Zeilen mit Status "neu", gruppiert

Versandbereit heißt: Status "neu", eine echte Profil-URL (linkedin.com/in/<name>).
Zeilen mit Sales-Navigator-ID, Suchlink oder leerer URL brauchen vorher eine
Namenssuche im normalen LinkedIn. Reihenfolge innerhalb der Gruppen: geprüfte
Zeilen zuerst, dann Stufe A vor B vor Reserve, dann Zeilennummer. "Qualifikation
offen" steht bei Zeilen, deren Notiz "noch prüfen" enthält.
"""

import re
import sys

import _pfad  # noqa: F401
from kaltliste import lies_zeilen, profil_url, url_art

RANG = {"A": 0, "B": 1, "Reserve": 2, "": 3}


def stufe(z):
    m = re.search(r"\*\*(A|B)\??\*\*", z["notiz"])
    if m:
        return m.group(1)
    if re.search(r"\bReserve\b", z["notiz"]):
        return "Reserve"
    return ""


def offen(z):
    return bool(re.search(r"noch prüfen|zu prüfen", z["notiz"], re.I))


def zeile_drucken(z):
    art = url_art(z["linkedin"])
    url = profil_url(z["linkedin"]) if art == "profil" else f"({art}) {z['linkedin'][:70]}"
    flags = []
    if offen(z):
        flags.append("Qualifikation offen")
    if z["groesse"]:
        flags.append(z["groesse"])
    print(f"#{z['nr']:>3}  {stufe(z) or '-':<7} {z['firma'][:22]:<22} {z['person'][:40]:<40} {url}")
    if flags:
        print(f"      {' | '.join(flags)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    _, zeilen = lies_zeilen()
    neu = [z for z in zeilen if z["status"] == "neu" and z["firma"] and z["person"]]
    neu.sort(key=lambda z: (offen(z), RANG[stufe(z)], int(z["nr"])))
    bereit = [z for z in neu if url_art(z["linkedin"]) == "profil"]
    suche = [z for z in neu if url_art(z["linkedin"]) != "profil"]

    if sys.argv[1] == "--alle":
        print(f"Versandbereit ({len(bereit)}):")
        for z in bereit:
            zeile_drucken(z)
        print(f"\nNamenssuche nötig ({len(suche)}):")
        for z in suche:
            zeile_drucken(z)
        return

    n = int(sys.argv[1])
    auswahl = (bereit + suche)[:n]
    print(f"Nächste {len(auswahl)} von {len(neu)} neuen Leads ({len(bereit)} versandbereit):\n")
    for z in auswahl:
        zeile_drucken(z)
    if len(auswahl) < n:
        print(f"\nNur {len(auswahl)} Leads mit Person vorhanden. Nachschub per /leads.")


if __name__ == "__main__":
    main()
