"""Wie viele neue Leads die Kalt-Liste für die nächsten Akquise-Tage braucht.

    python3 .claude/skills/leads/scripts/bedarf.py             # nächste 3 Akquise-Tage
    python3 .claude/skills/leads/scripts/bedarf.py --tage 5

Vorrat = Zeilen mit Status "neu". Davon zählt nur "versandbereit" (echte
Profil-URL, Qualifikation nicht offen) als fertig. Halbfertige Zeilen
(Sales-Navigator-ID, Suchlink, "noch prüfen") sind der schnellste Nachschub:
erst die fertig machen, dann neu suchen. Akquise-Tage und Tagesziel stehen in
Sales/einstellungen.json.
"""

import argparse
import re
from datetime import date, timedelta

import _pfad  # noqa: F401
from kaltliste import einstellungen, lies_zeilen, url_art


def offen(z):
    return bool(re.search(r"noch prüfen|zu prüfen", z["notiz"], re.I))


def naechste_tage(ab, n, akquise_tage):
    tage, d = [], ab
    while len(tage) < n:
        d += timedelta(days=1)
        if d.weekday() in akquise_tage:
            tage.append(d)
    return tage


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tage", type=int, default=3)
    a = p.parse_args()
    e = einstellungen()

    _, zeilen = lies_zeilen()
    neu = [z for z in zeilen if z["status"] == "neu" and z["firma"]]
    bereit = [z for z in neu if url_art(z["linkedin"]) == "profil" and not offen(z)]
    ohne_url = [z for z in neu if url_art(z["linkedin"]) != "profil" and not offen(z)]
    ungeprueft = [z for z in neu if offen(z)]
    naechste_nr = max((int(z["nr"]) for z in zeilen), default=0) + 1

    tage = naechste_tage(date.today(), a.tage, e["akquise_tage"] or [0, 1, 2, 3, 4])
    wochen = max(1, (tage[-1] - date.today()).days // 7 + 1)
    bedarf = min(a.tage * e["tagesziel"], e["wochenlimit"] * wochen)
    fehlen = max(0, bedarf - len(bereit))

    print(f"Vorrat (Status neu): {len(neu)}")
    print(f"  versandbereit (Profil-URL, geprüft): {len(bereit)}")
    print(f"  Person bekannt, Profil-URL fehlt (ID oder Suchlink): {len(ohne_url)}")
    print(f"  ungeprüft (Website, Passung oder Größe offen): {len(ungeprueft)}"
          + (f", Zeilen {ungeprueft[0]['nr']} bis {ungeprueft[-1]['nr']}" if ungeprueft else ""))
    print(f"Nächste freie Zeile: {naechste_nr}")
    print()
    print(f"Nächste {a.tage} Akquise-Tage: " + ", ".join(f"{'Mo Di Mi Do Fr Sa So'.split()[d.weekday()]} {d:%d.%m.}" for d in tage))
    print(f"Bedarf bei {e['tagesziel']} pro Tag (gedeckelt durch {e['wochenlimit']} in 7 Tagen): {bedarf}")
    print(f"FEHLEN: {fehlen} versandbereite Leads")
    if fehlen:
        schnell = len(ohne_url) + len(ungeprueft)
        print(f"Schnellster Weg: {min(fehlen, schnell)} aus den halbfertigen Zeilen fertig machen"
              + (f", danach {fehlen - schnell} neu suchen." if fehlen > schnell else "."))
    else:
        print("Vorrat reicht. Trotzdem halbfertige Zeilen fertig machen, wenn Zeit ist.")


if __name__ == "__main__":
    main()
