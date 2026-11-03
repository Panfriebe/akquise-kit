"""Gemeinsame Helfer: Kalt-Liste, Scorecard und Einstellungen lesen und schreiben.

Alle Skill-Skripte importieren von hier. Pfade sind relativ zum Vault-Ordner
(der Ordner, der `.claude/` und `Sales/` enthält).
"""

import json
import re
from datetime import date, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SALES = VAULT / "Sales"
KALTLISTE = SALES / "Kalt-Liste.md"
SCORECARD = SALES / "Scorecard.md"
PROFIL = SALES / "Profil.md"
REGELN = SALES / "Nachrichtenregeln.md"
EINSTELLUNGEN = SALES / "einstellungen.json"

SPALTEN = ["nr", "firma", "website", "person", "linkedin", "detail", "groesse",
           "branche", "quelle", "status", "letzter_kontakt", "follow_up", "notiz"]

STATUS = ["neu", "angefragt", "angenommen", "dm", "antwort", "gespräch", "angebot", "nein"]

STANDARD = {
    "tagesziel": 20,              # Kontaktanfragen pro Akquise-Tag
    "wochenlimit": 100,           # LinkedIn lässt etwa 100 Anfragen in 7 Tagen zu
    "akquise_tage": [0, 1, 2, 3, 4],  # 0 = Montag ... 4 = Freitag
    "follow_up_werktage": 3,
    "max_zeichen": 300,
    "max_saetze": 2,
    "anrede": "du",               # "du" oder "Sie"
    "fachwoerter": [],            # Wörter, die der Kunde nicht benutzt (Warnung im Prüfer)
    "themenwoerter": [],          # Wörter, die zeigen, dass das Detail zum Schmerz passt
    "referenzwoerter": [],        # Referenzkunde, erst nach dem Ja nennen
}


def einstellungen():
    """Einstellungen aus Sales/einstellungen.json, fehlende Werte aus STANDARD."""
    werte = dict(STANDARD)
    if EINSTELLUNGEN.exists():
        try:
            werte.update(json.loads(EINSTELLUNGEN.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{EINSTELLUNGEN} ist kein gültiges JSON: {e}")
    return werte


def pruefe_dateien():
    fehlt = [str(p.relative_to(VAULT)) for p in (KALTLISTE, SCORECARD) if not p.exists()]
    if fehlt:
        raise SystemExit("Fehlt: " + ", ".join(fehlt) + ". Zuerst /einrichten ausführen.")


def zellen(zeile):
    return [z.strip() for z in zeile.strip().strip("|").split("|")]


def lies_zeilen():
    """Alle Firmen-Zeilen der Kalt-Liste als Dicts, mit Zeilenindex in der Datei."""
    pruefe_dateien()
    text = KALTLISTE.read_text(encoding="utf-8").split("\n")
    zeilen = []
    for i, z in enumerate(text):
        if not z.startswith("|"):
            continue
        c = zellen(z)
        if len(c) != len(SPALTEN) or not c[0].isdigit():
            continue
        d = dict(zip(SPALTEN, c))
        d["_index"] = i
        zeilen.append(d)
    return text, zeilen


def schreibe(text):
    KALTLISTE.write_text("\n".join(text), encoding="utf-8")


def als_zeile(d):
    return "| " + " | ".join(str(d.get(s, "")).replace("|", "/") for s in SPALTEN) + " |"


def tabellen_ende(text):
    """Index der letzten Tabellenzeile der Kalt-Liste (oder der Kopfzeile, wenn leer)."""
    letzte = None
    for i, z in enumerate(text):
        if z.startswith("|"):
            letzte = i
        elif letzte is not None and z.startswith("## "):
            break
    return letzte


def url_art(zelle):
    """Was in der LinkedIn-Spalte steht: profil, id, navigator, suche oder leer.

    profil    linkedin.com/in/<name-slug>, direkt im normalen LinkedIn aufrufbar
    id        linkedin.com/in/ACwAA… (Sales-Navigator-Kennung, oft nicht aufrufbar)
    navigator linkedin.com/sales/lead/…
    suche     linkedin.com/search/results/people/?keywords=…
    leer      nichts oder nur ein Vermerk wie "(in LinkedIn suchen)"
    """
    u = (zelle or "").strip().lower()
    if not u or u.startswith("("):
        return "leer"
    if "search/results" in u:
        return "suche"
    if "/sales/" in u:
        return "navigator"
    m = re.search(r"linkedin\.com/in/([^/?\s)]+)", u)
    if not m:
        return "leer"
    return "id" if re.match(r"ac[ow]aa", m.group(1)) else "profil"


def profil_url(zelle):
    """Erste linkedin.com/in/-Adresse der Zelle als vollständige URL, sonst leer."""
    m = re.search(r"(?:[a-z]{2}\.)?linkedin\.com/in/[^/?\s)]+", (zelle or "").strip(), re.I)
    return "https://www." + re.sub(r"^[a-z]{2}\.", "", m.group(0)) + "/" if m else ""


def plus_werktage(d, n):
    """Datum n Werktage später (Sa und So übersprungen). d als date oder ISO-String."""
    if isinstance(d, str):
        d = date.fromisoformat(d)
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


# Scorecard ---------------------------------------------------------------

def lies_scorecard():
    """Scorecard als (text, spalten, tage). tage: Datum -> {"zellen", "_index"}."""
    pruefe_dateien()
    text = SCORECARD.read_text(encoding="utf-8").split("\n")
    spalten, tage = {}, {}
    for i, z in enumerate(text):
        if not z.startswith("|"):
            continue
        c = zellen(z)
        if not spalten and c and c[0].lower() == "datum":
            spalten = {name.lower(): k for k, name in enumerate(c)}
            spalten["_index"] = i
            continue
        if spalten and len(c) >= len(spalten) - 1 and re.match(r"\d{4}-\d{2}-\d{2}$", c[0]):
            tage[c[0]] = {"zellen": c, "_index": i}
    if not spalten:
        raise SystemExit(f"Keine Tabelle mit Spalte 'Datum' in {SCORECARD.name}.")
    return text, spalten, tage


def zahl(zelle):
    m = re.match(r"\d+", (zelle or "").strip())
    return int(m.group(0)) if m else 0


def scorecard_zeile(text, spalten, tage, datum):
    """Zellen für ein Datum; legt die Zeile am Tabellenende an, wenn sie fehlt."""
    if datum in tage:
        return tage[datum]["zellen"], tage[datum]["_index"]
    d = date.fromisoformat(datum)
    n = len(spalten) - 1
    c = [""] * n
    c[0] = datum
    if "tag" in spalten:
        c[spalten["tag"]] = "Mo Di Mi Do Fr Sa So".split()[d.weekday()]
    if "woche" in spalten:
        c[spalten["woche"]] = f"KW {d.isocalendar()[1]}"
    # hinter die letzte Datumszeile, sonst direkt hinter die Trennzeile des Kopfs
    letzte = max((t["_index"] for t in tage.values()), default=spalten["_index"] + 1)
    text.insert(letzte + 1, "| " + " | ".join(c) + " |")
    tage[datum] = {"zellen": c, "_index": letzte + 1}
    for t in tage.values():
        if t["_index"] > letzte + 1 and t is not tage[datum]:
            t["_index"] += 1
    return c, letzte + 1


def schreibe_scorecard(text):
    SCORECARD.write_text("\n".join(text), encoding="utf-8")
