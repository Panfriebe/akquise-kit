# Quellen für neue Leads, nach Aufwand sortiert

Welche Quelle die beste ist, hängt von der Zielgruppe in `Sales/Profil.md` ab. Hier nachtragen, was wie viel gebracht hat (Datum, Zahl), damit die nächste Suche dort anfängt.

## 1. LinkedIn-Personensuche (ohne Sales Navigator)

`https://www.linkedin.com/search/results/people/?keywords=<Rolle> <Branche> <Ort>`, dann Filter „Standorte" und „Aktuelle Unternehmen". Ergebnis liefert Name, Headline, Ort und die echte Profil-URL. Die Firmengröße steht nicht dabei, die kommt von der Firmenseite (`linkedin.com/company/<name>/about/`).

Suchwörter aus dem Profil ableiten: Rolle (`Geschäftsführer OR Gründer OR Inhaber OR CEO`), Branche in der Sprache des Kunden, Region.

## 2. LinkedIn Sales Navigator, Lead-Suche

Wenn vorhanden, die ergiebigste Quelle. Lead-Suche, nicht Account-Suche:

| Filter | Wert |
|---|---|
| Geografie | Länder oder Städte aus dem Profil |
| Unternehmensgröße | Bereich aus dem Profil |
| Karrierestufe | Inhaber/Partner, CXO (je nach Zielperson) |
| Branche | pro Durchlauf eine, sonst sind die Treffer gemischt |
| Stichwörter (Titel) | `Gründer OR Geschäftsführer OR Founder OR CEO OR Inhaber OR Owner` |

**Was den Ertrag erhöht:**

- **Suche speichern.** Der Navigator zeigt dann unter „Gespeicherte Suchen" nur neue Treffer seit dem letzten Mal. Eine gespeicherte Suche pro Branche.
- **Bereits angesehene Leads ausblenden** (Filter „Bisherige Lead-Aktivität", Option „Angesehen" ausschließen).
- **Spotlight „Hat in den letzten 30 Tagen auf LinkedIn gepostet"**: aktive Leute nehmen Anfragen eher an und antworten eher.
- **Lead-Liste im Navigator anlegen** und Treffer dort speichern. Das ist die Dublettensperre innerhalb des Navigators, die Kalt-Liste bleibt die Wahrheit.
- **Ähnliche Leads:** Auf der Lead-Seite eines guten Treffers „Ähnliche Leads anzeigen".
- **Account-Suche als zweiter Weg:** Firmen filtern (Hauptsitz, Größe, Branche), dann pro Firma „Mitarbeitende" mit Karrierestufe.

**Pro Treffer mitnehmen:** Name, Rolle, Firma, Ort, Unternehmensgröße (steht auf der Lead-Seite), und über das Menü „…" den Link „Auf LinkedIn.com anzeigen" für die echte Profil-URL. Die Navigator-URL (`/sales/lead/ACwAA…`) ist für den Versand unbrauchbar.

**Nicht tun:** Dort vernetzen (fügt eine Notiz ein), InMail schicken, Notizen am Lead speichern.

## 3. Halbfertige Zeilen in der Kalt-Liste

Vor jeder neuen Suche. `bedarf.py` zeigt, wie viele Zeilen nur eine Profil-URL oder eine Website-Prüfung brauchen. Pro Zeile 3 bis 5 Minuten, kein Suchaufwand.

## 4. Umgekehrter Weg: Firmennamen sammeln, dann die Person suchen

Branchenlisten, Rankings („Top 100 ..."), Messe-Ausstellerlisten, Verbandsmitglieder, Kundenlogos von Dienstleistern der Branche, Fallstudien („<Firma> Erfolgsgeschichte"). Namen mit `dublette.py` filtern, auf der LinkedIn-Firmenseite die Größe lesen, dann die Person suchen. Bringt oft mehr als die Stichwortsuche, wenn die Branche auf LinkedIn unscharf ist.

## 5. Website-Prüfung in Serie

`python3 .claude/skripte/website.py a.de b.de c.de --json leads.json` prüft Impressum (Geschäftsführer, Ort), erkennbare Tools und ob es einen Shop gibt. Die JSON-Datei ist ein Vorschlag für `eintragen.py`, vorher Größe und Profil-URL ergänzen.

## 6. Verzeichnisse und Bewertungsportale

Kununu (Mitarbeiterzahl), Trusted Shops und Trustpilot (Firmen mit vielen Bewertungen), OMR Reviews und Capterra (Rezensenten nennen Firma und Größe), Branchenverzeichnisse, IHK-Listen, Handelsregister-Suche (handelsregister.de) für Rechtsform und Geschäftsführer. Eher zum Belegen als zum Finden.

## Prüf-Reihenfolge pro Kandidat (so bleibt es unter 5 Minuten)

1. `dublette.py` mit Firma und Name
2. Website: passt zur Zielgruppe, Impressum (Sitz, Rechtsform), `website.py` für Tools und Geschäftsführer
3. LinkedIn-Firmenseite: Beschäftigte, Hauptsitz
4. Profil der Person im normalen LinkedIn: Headline nennt die Firma, Grad notieren
5. Eintragen mit Stufe: `**A?**` alles passt, `**B?**` ein Haken, `Reserve` zu klein oder Profil passiv
