"""Prüft Firmen-Websites: Titel, Impressum (Geschäftsführer, Ort, HRB), erkennbare Tools.

    python3 .claude/skripte/website.py beispiel.de andere-firma.com
    python3 .claude/skripte/website.py beispiel.de --json leads.json   # Vorschlag für eintragen.py

Domains, die schon in der Kalt-Liste stehen (auch unter "Aussortiert"), werden
übersprungen. Größe und LinkedIn-Profil prüft das Skript nicht, dafür gibt es
den Suchlink in der Ausgabe.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from kaltliste import KALTLISTE

TOOLS = {
    "Gorgias": r"gorgias",
    "Zendesk": r"zdassets\.com|zendesk\.com",
    "Freshdesk": r"freshdesk|freshchat|freshworks",
    "Intercom": r"intercom(cdn)?\.(io|com)|widget\.intercom",
    "HubSpot": r"hs-scripts\.com|hubspot",
    "Zoho": r"zohodesk|salesiq\.zoho",
    "Trengo": r"trengo",
    "Tidio": r"tidio",
    "Userlike": r"userlike",
    "Calendly": r"calendly\.com",
    "Shopify": r"cdn\.shopify\.com|Shopify\.theme",
    "WooCommerce": r"woocommerce",
    "Shopware": r"shopware",
    "WordPress": r"wp-content",
    "Webflow": r"webflow",
    "Personio": r"personio",
    "Trustpilot": r"trustpilot",
    "Trusted Shops": r"trustedshops",
}

GF_MUSTER = re.compile(
    r"(?:Vertretungsberechtigte[rn]?\s+)?(?:Gesch[äa]ftsf[üu]hr(?:er|erin|ung|ende)"
    r"|Vertreten\s+durch(?:\s+die\s+Gesch[äa]ftsf[üu]hr\w*)?|Inhaber(?:in)?|Managing\s+Directors?)"
    r"\s*[:\-]?\s*(.{3,120})", re.I)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def hole(url, frist=15):
    ende = time.monotonic() + frist
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=8) as r:
            teile, groesse = [], 0
            while groesse < 1_500_000 and time.monotonic() < ende:
                stueck = r.read(65536)
                if not stueck:
                    break
                teile.append(stueck)
                groesse += len(stueck)
            return b"".join(teile).decode("utf-8", "ignore"), r.geturl()
    except Exception:
        return "", url


def als_text(roh):
    roh = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", roh)
    roh = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|span)>", "\n", roh)
    t = html.unescape(re.sub(r"<[^>]+>", " ", roh))
    return "\n".join(z.strip() for z in t.split("\n") if z.strip())


def impressum_url(roh, basis):
    for m in re.finditer(r'href="([^"]+)"', roh):
        h = m.group(1)
        if re.search(r"impressum|imprint|legal-notice|legal_notice", h, re.I):
            return urllib.parse.urljoin(basis, html.unescape(h))
    return None


def namen(text):
    gefunden = []
    for m in GF_MUSTER.finditer(text):
        rest = m.group(1).split("\n")[0]
        rest = re.split(r"(?i)registergericht|handelsregister|amtsgericht|hrb|sitz|telefon|e-?mail|ust", rest)[0]
        for n in re.split(r",|;|\bund\b|&|/", rest):
            n = re.sub(r"\(.*?\)|Dr\.|Prof\.|Herr|Frau", "", n)
            n = re.sub(r"(?i)^.*?\b(gesch[äa]ftsf[üu]hr\w*|vertreten durch( die)?|inhaber\w*)\b\s*:?", "", n).strip(" .:-")
            w = n.split()
            if 2 <= len(w) <= 4 and all(x[0].isupper() for x in w) and not re.search(r"GmbH|UG|AG|KG|\d", n):
                if n not in gefunden:
                    gefunden.append(n)
    return gefunden[:3]


def pruefe(domain):
    domain = re.sub(r"^https?://", "", domain.strip()).strip("/").lower()
    roh, final = hole(f"https://{domain}")
    if not roh:
        return {"domain": domain, "fehler": "nicht erreichbar"}

    titel = re.search(r"<title[^>]*>(.*?)</title>", roh, re.I | re.S)
    tools = [t for t, m in TOOLS.items() if re.search(m, roh, re.I)]
    warenkorb = bool(re.search(r"warenkorb|/cart\b|add-to-cart|checkout", roh, re.I))

    imp_roh = ""
    url = impressum_url(roh, final)
    kandidaten = [url] if url else []
    kandidaten += [f"https://{domain}{p}" for p in ("/impressum", "/pages/impressum", "/imprint", "/legal-notice")]
    for k in kandidaten:
        imp_roh, _ = hole(k)
        if re.search(r"Gesch[äa]ftsf[üu]hr|Vertreten durch|Inhaber", imp_roh, re.I):
            break
    imp = als_text(imp_roh)
    gf = namen(imp)
    plz = re.search(r"\b(\d{4,5})\s+([A-ZÄÖÜ][\wäöüß\-]+(?:\s(?:am|an der|bei|im)\s[\wäöüß\-]+)?)", imp)
    hrb = re.search(r"HRB\s?\d+", imp)
    return {
        "domain": domain, "titel": html.unescape(titel.group(1).strip())[:80] if titel else "",
        "tools": tools, "warenkorb": warenkorb, "gf": gf,
        "ort": plz.group(2) if plz else "", "hrb": hrb.group(0) if hrb else "",
    }


def kern(domain):
    d = re.sub(r"^https?://", "", domain.lower()).strip("/").replace("www.", "")
    teile = d.split(".")
    return teile[-2] if len(teile) > 1 else d


def suchlink(name, domain):
    q = urllib.parse.quote(f"{name} {kern(domain)}")
    return f"linkedin.com/search/results/people/?keywords={q}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("domains", nargs="+")
    p.add_argument("--json", help="Vorschlag für eintragen.py in diese Datei schreiben")
    a = p.parse_args()

    liste = KALTLISTE.read_text(encoding="utf-8").lower() if KALTLISTE.exists() else ""
    neu = [d for d in dict.fromkeys(a.domains) if kern(d) not in liste]
    print(f"{len(a.domains)} Domains, {len(a.domains) - len(neu)} schon in der Kalt-Liste, prüfe {len(neu)} …\n", file=sys.stderr)

    with ThreadPoolExecutor(8) as ex:
        ergebnisse = list(ex.map(pruefe, neu))

    vorschlaege = []
    for e in ergebnisse:
        if "fehler" in e:
            print(f"--  {e['domain']:<28} {e['fehler']}")
            continue
        gf = ", ".join(e["gf"]) or "GF nicht gefunden"
        print(f"{e['domain']:<28} {e['titel'][:40]:<40}")
        print(f"    Tools: {', '.join(e['tools']) or '-'}   Shop: {'ja' if e['warenkorb'] else 'nein'}   "
              f"Ort: {e['ort'] or '-'}   {e['hrb']}")
        print(f"    GF lt. Impressum: {gf}")
        if e["gf"]:
            print(f"    Profil suchen: {suchlink(e['gf'][0], e['domain'])}")
        vorschlaege.append({
            "firma": kern(e["domain"]), "website": e["domain"],
            "person": ", ".join(e["gf"]) + (" (GF lt. Impressum)" if e["gf"] else ""),
            "linkedin": suchlink(e["gf"][0], e["domain"]) if e["gf"] else "",
            "detail": ", ".join(e["tools"]), "groesse": "", "branche": "",
            "quelle": f"website.py {date.today().isoformat()}, Impressum",
            "notiz": f"{e['ort']}. {e['hrb']}. Größe und Profil noch prüfen".strip(". "),
        })
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(vorschlaege, f, ensure_ascii=False, indent=1)
        print(f"\n{len(vorschlaege)} Vorschläge in {a.json} (prüfen, dann eintragen.py).", file=sys.stderr)


if __name__ == "__main__":
    main()
