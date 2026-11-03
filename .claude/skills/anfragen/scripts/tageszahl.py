"""Wie viele LinkedIn-Kontaktanfragen heute rausgehen dürfen, und Eintrag in die Scorecard.

    python3 .claude/skills/anfragen/scripts/tageszahl.py                 # heute: Tagesziel, Wochenfenster, Vorrat
    python3 .claude/skills/anfragen/scripts/tageszahl.py 2026-11-10      # anderes Datum
    python3 .claude/skills/anfragen/scripts/tageszahl.py --eintragen --notiz "12 Anfragen ohne Notiz per Browser, Zeilen 5 bis 17"
    python3 .claude/skills/anfragen/scripts/tageszahl.py --eintragen --anzahl 13 --notiz "..."   # wenn mehr Personen als Zeilen

Rechnung: heute möglich = min(Tagesziel minus heute schon raus, Wochenlimit minus
Anfragen der letzten 7 Tage inklusive heute). Tagesziel und Wochenlimit stehen in
Sales/einstellungen.json. Die Tageswerte kommen aus der Scorecard, der Vorrat aus
der Kalt-Liste. --eintragen zählt die Zeilen mit Status "angefragt" und letztem
Kontakt heute und schreibt die Zahl in die Spalte Anfragen (legt die Zeile an,
wenn sie fehlt).
"""

import argparse
from datetime import date, timedelta

import _pfad  # noqa: F401
from kaltliste import (einstellungen, lies_scorecard, lies_zeilen, schreibe_scorecard,
                       scorecard_zeile, url_art, zahl)


def vorrat():
    _, zeilen = lies_zeilen()
    neu = [z for z in zeilen if z["status"] == "neu" and z["firma"]]
    bereit = [z for z in neu if url_art(z["linkedin"]) == "profil"]
    suche = [z for z in neu if url_art(z["linkedin"]) != "profil" and z["person"]]
    return bereit, suche


def main():
    p = argparse.ArgumentParser()
    p.add_argument("datum", nargs="?", default=date.today().isoformat())
    p.add_argument("--eintragen", action="store_true")
    p.add_argument("--anzahl", type=int, help="gesendete Anfragen, falls abweichend von den Zeilen")
    p.add_argument("--notiz", default="")
    a = p.parse_args()
    e = einstellungen()

    heute = date.fromisoformat(a.datum)
    text, spalten, tage = lies_scorecard()
    if "anfragen" not in spalten:
        raise SystemExit("Scorecard hat keine Spalte 'Anfragen'.")
    sp = spalten["anfragen"]

    if a.eintragen:
        _, zeilen = lies_zeilen()
        n = a.anzahl if a.anzahl is not None else sum(
            z["status"] == "angefragt" and z["letzter_kontakt"] == a.datum for z in zeilen)
        c, i = scorecard_zeile(text, spalten, tage, a.datum)
        c[sp] = str(n)
        if a.notiz and "notiz" in spalten:
            alt = c[spalten["notiz"]].strip()
            c[spalten["notiz"]] = (alt.rstrip(".") + ". " if alt else "") + a.notiz.strip()
        text[i] = "| " + " | ".join(c) + " |"
        schreibe_scorecard(text)
        print(f"Scorecard {a.datum}: Anfragen = {n}" + (", Notiz ergänzt" if a.notiz else ""))
        return

    fenster = [(heute - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    im_fenster = {d: zahl(tage[d]["zellen"][sp]) if d in tage else 0 for d in fenster}
    summe = sum(im_fenster.values())
    heute_schon = im_fenster[a.datum]
    frei_woche = max(0, e["wochenlimit"] - summe)
    frei_tag = max(0, e["tagesziel"] - heute_schon)
    moeglich = min(frei_tag, frei_woche)
    bereit, suche = vorrat()

    print(f"Datum: {a.datum} ({'Mo Di Mi Do Fr Sa So'.split()[heute.weekday()]})")
    print(f"Wochenfenster {fenster[0]} bis {a.datum}: {summe} von {e['wochenlimit']}  "
          + "(" + ", ".join(f"{d[5:]}: {n}" for d, n in im_fenster.items() if n) + ")")
    print(f"Morgen fallen {im_fenster[fenster[0]]} aus dem Fenster (Anfragen vom {fenster[0]}).")
    print(f"Tagesziel {e['tagesziel']}, heute schon {heute_schon} raus.")
    print(f"Vorrat Kalt-Liste: {len(bereit)} versandbereit (Profil-URL), {len(suche)} nur per Namenssuche oder ID.")
    print()
    print(f"HEUTE MÖGLICH: {moeglich}")
    if moeglich == 0:
        grund = "Tagesziel erreicht" if frei_tag == 0 else "Wochenlimit erreicht"
        print(f"Grund: {grund}. Nichts verschicken.")
    elif len(bereit) < moeglich:
        print(f"Davon {len(bereit)} sofort, {moeglich - len(bereit)} brauchen Namenssuche oder Nachschub (/leads).")
    if heute.weekday() not in e["akquise_tage"]:
        print("Hinweis: Heute ist laut Einstellungen kein Akquise-Tag. Wer /anfragen aufruft, hat trotzdem entschieden.")


if __name__ == "__main__":
    main()
