"""Prüft eine Akquise-Nachricht gegen die Formregeln aus Sales/Nachrichtenregeln.md.

    python3 .claude/skills/dm/scripts/pruefe.py "Hallo Max, ich habe gesehen, dass ..."
    echo "Hallo Max, ..." | python3 .claude/skills/dm/scripts/pruefe.py
    python3 .claude/skills/dm/scripts/pruefe.py --follow-up "Hallo Max, ..."

Exit 0 wenn alles passt, 1 bei Fehlern. Warnungen ändern den Exit-Code nicht.
Länge, Satzzahl, Anrede, Fachwörter, Themenwörter und Referenz kommen aus
Sales/einstellungen.json. Der Prüfer sieht nur die Form. Ob das Detail belegt
ist und zur Firma passt, prüft er nicht.
"""

import re
import sys

import _pfad  # noqa: F401
from kaltliste import einstellungen

VERBOTENE_ZEICHEN = {
    "!": "Ausrufezeichen",
    ":": "Doppelpunkt",
    "–": "Gedankenstrich (en-dash)",
    "—": "Gedankenstrich (em-dash)",
    ";": "Semikolon",
}

FLOSKELN = [
    "danke fürs vernetzen", "danke für die vernetzung", "danke für das vernetzen",
    "danke für die annahme", "spannend", "spannender", "tolle", "toller", "beeindruckend",
    "großartig", "ich hoffe", "ich würde mich freuen", "gerne", "gern ", "kurz vorstellen",
    "ich bin ", "mein name", "ich helfe", "wir helfen", "lösung", "lösungen",
    "nur zur sicherheit", "falls du es übersehen hast", "falls es untergegangen ist",
    "wollte nur", "kostenlos und unverbindlich", "unverbindlich", "kein risiko",
    "melde dich", "meld dich", "lass uns", "calendly", "mehrwert", "synergie",
]

# Versprechen, die ohne Zugang zu Daten des Kunden nicht belegbar sind.
UNBELEGBAR = [
    "welche fragen eure kunden stellen", "was eure kunden fragen",
    "eure häufigsten fragen", "eure tickets analysier", "anteil eurer",
    "eure daten auswert", "eure zahlen auswert",
]


def saetze(text):
    t = text
    t = re.sub(r"\bz\. ?B\.", "zB", t)
    t = re.sub(r"\bca\.", "ca", t)
    t = re.sub(r"\bbzw\.", "bzw", t)
    t = re.sub(r"\bu\. ?a\.", "ua", t)
    t = re.sub(r"\d+\.\d+", "N", t)          # 10.000
    t = re.sub(r"\d+\.", "N", t)             # 1. Grades
    t = re.sub(r"\b[A-ZÄÖÜ]\.", "X", t)      # Initialen
    teile = [s for s in re.split(r"[.?!]+(?:\s+|$)", t.strip()) if s.strip()]
    return len(teile)


def pruefe(text, e, follow_up=False):
    fehler, warnungen = [], []
    text = text.strip()
    max_zeichen = e["max_zeichen"]
    max_saetze = 1 if follow_up else e["max_saetze"]

    n = len(text)
    if n > max_zeichen:
        fehler.append(f"{n} Zeichen, erlaubt sind {max_zeichen}")
    elif n > max_zeichen - 20:
        warnungen.append(f"{n} Zeichen, knapp an der Grenze von {max_zeichen}")

    s = saetze(text)
    if s > max_saetze:
        fehler.append(f"{s} Sätze, erlaubt sind {max_saetze}")

    for z, name in VERBOTENE_ZEICHEN.items():
        if z in text:
            fehler.append(f"{name} ({z!r}) enthalten")
    if " - " in text:
        fehler.append("Bindestrich mit Leerzeichen als Gedankenstrich benutzt")
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
        fehler.append("Emoji enthalten")

    if not re.match(r"^(Hallo|Hi|Moin|Servus|Guten Tag) [A-ZÄÖÜ][\wäöüß-]+(?: [A-ZÄÖÜ][\wäöüß-]+)?,", text):
        fehler.append("Beginnt nicht mit „Hallo [Vorname],“ (oder Hi, Moin, Servus, Guten Tag)")
    if not text.endswith("?"):
        fehler.append("Endet nicht mit einer Frage")

    low = text.lower()
    for f in FLOSKELN:
        if f in low:
            fehler.append(f"Floskel „{f.strip()}“")
    for u in UNBELEGBAR:
        if u in low:
            fehler.append(f"Unbelegbares Versprechen „{u}“ (braucht Zugang zu Daten des Kunden)")

    anrede = (e.get("anrede") or "du").lower()
    rest = low.split(",", 1)[-1]
    if anrede == "du" and re.search(r"\b(sie|ihnen|ihre[rsnm]?)\b", rest):
        warnungen.append("Klingt nach Sie-Form, Einstellung ist Du")
    if anrede == "sie" and re.search(r"\b(du|dir|dich|dein[esrnm]*|euch|euer|eure[rsnm]?)\b", rest):
        warnungen.append("Klingt nach Du-Form, Einstellung ist Sie")

    for w in e.get("fachwoerter") or []:
        if re.search(rf"\b{re.escape(w.lower())}", low):
            warnungen.append(f"Fachwort „{w}“, der Kunde benutzt es nicht (Profil.md)")

    themen = [t.lower() for t in (e.get("themenwoerter") or [])]
    if themen and not any(t in low for t in themen):
        warnungen.append("Kein Bezug zum Schmerz erkennbar (keins der Themenwörter aus den Einstellungen). "
                         "Das Detail muss zum Schmerz passen, nicht nur zur Firma")

    if not follow_up and not re.search(r"(habe|hab) gesehen|gesehen, dass|ist mir aufgefallen|habe gelesen", low):
        warnungen.append("Kein „ich habe gesehen, dass ...“, ist das Detail wirklich recherchiert?")

    for r in e.get("referenzwoerter") or []:
        if r.lower() in low:
            warnungen.append(f"Referenz „{r}“ in der Nachricht, laut Regel erst nach dem Ja")

    if re.search(r"\b(montag|dienstag|mittwoch|donnerstag|freitag|\d{1,2} uhr|termin|\d{2} minuten|call)\b", low):
        warnungen.append("Termin oder Zeitangabe in der Nachricht, laut Regel erst nach dem Ja")

    return n, s, fehler, warnungen


def main():
    args = sys.argv[1:]
    follow_up = "--follow-up" in args
    args = [a for a in args if a != "--follow-up"]
    text = " ".join(args) if args else sys.stdin.read()
    text = " ".join(text.split())

    n, s, fehler, warnungen = pruefe(text, einstellungen(), follow_up)
    print(f"{n} Zeichen, {s} Sätze")
    for f in fehler:
        print(f"FEHLER: {f}")
    for w in warnungen:
        print(f"Warnung: {w}")
    if not fehler:
        print("Prüfer ok" + (" (mit Warnungen)" if warnungen else ""))
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
