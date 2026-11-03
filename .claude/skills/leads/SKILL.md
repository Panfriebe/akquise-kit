---
name: leads
description: Füllt die Kalt-Liste für die nächsten Akquise-Tage mit versandbereiten Leads auf (Firmen nach dem ICP aus Sales/Profil.md, Person mit echter LinkedIn-Profil-URL). Rechnet den Bedarf, macht zuerst halbfertige Zeilen fertig, sucht dann neue Kandidaten (LinkedIn und Sales Navigator in Chrome, Verzeichnisse, Websites) und trägt sie ein. Immer nutzen bei "Leads vorbereiten", "Leads für morgen", "Kalt-Liste auffüllen", "Nachschub", "neue Firmen suchen", "Sales Navigator" oder "/leads". Nicht zum Verschicken (dafür /anfragen) und nicht für Nachrichten (dafür /dm).
---

# Leads: Kalt-Liste für die nächsten Tage vorbereiten

Jeder Akquise-Tag braucht so viele Leads wie das Tagesziel, die sich ohne Nachdenken anfragen lassen. Was den Versand am Tag bremst, ist nie das Klicken, sondern fehlende Profil-URLs und unklare Firmen. Deshalb liefert dieser Skill nicht „Kandidaten", sondern **versandbereite Zeilen**: Person belegt, echte Profil-URL, Firma passt zum ICP, Größe laut LinkedIn-Firmenseite.

Alle Pfade relativ zum Vault-Ordner. Skripte in `.claude/skills/leads/scripts/`, ICP und Stufen in `Sales/Profil.md`, Quellen-Rezepte in `references/quellen.md`.

## Was reinkommt

`/leads` ohne Zahl deckt die nächsten 3 Akquise-Tage (aus `einstellungen.json`). `/leads 40` heißt 40 versandbereite Zeilen zusätzlich. „Leads für Donnerstag" heißt ein Tag. Niemand muss zuschauen, das Ergebnis steht in der Kalt-Liste.

## Was eine Zeile versandbereit macht

Zuerst `Sales/Profil.md` lesen, Abschnitt Zielgruppe. Die Tabelle dort ist der Filter.

| Feld | Muss | Beleg |
|---|---|---|
| Firma, Website | passt zur Zielgruppe im Profil, kein Ausschluss | Website, Impressum |
| Person | Vorname Nachname, Rolle laut Profil | LinkedIn-Profil oder Impressum |
| LinkedIn-URL | `linkedin.com/in/<name-slug>`, keine `ACwAA…`-ID, kein Suchlink | Profil im normalen LinkedIn geöffnet |
| Größe | laut LinkedIn-Firmenseite im Bereich aus dem Profil | Firmenseite, Info |
| Branche, Region | laut Profil | Impressum oder Firmenseite |
| Detail | ein belegter Aufhänger für die spätere DM, falls beim Prüfen gefunden (Tool, Stellenanzeige, Post) | URL |
| Notiz | Ort, Stufe `**A?**` oder `**B?**` oder `Reserve`, Grad, Quelle, Datum | |

## Ablauf

### 1. Bedarf rechnen

```
python3 .claude/skills/leads/scripts/bedarf.py
python3 .claude/skills/leads/scripts/bedarf.py --tage 5
```

Druckt den Vorrat in drei Gruppen (versandbereit, Profil-URL fehlt, ungeprüft), den Bedarf und `FEHLEN: n`. Die halbfertigen Gruppen sind der schnellste Nachschub, weil die Person schon da ist.

### 2. Halbfertige Zeilen fertig machen

Zuerst die Zeilen „Profil-URL fehlt", dann „ungeprüft". Pro Zeile:

1. **Website prüfen**, wenn offen:
   ```
   python3 .claude/skripte/website.py <domain> <domain2>
   ```
   liefert Titel, erkennbare Tools, Geschäftsführer und Ort laut Impressum. „nicht erreichbar" oder kein Treffer zur Zielgruppe heißt: aussortieren.
2. **Größe und Sitz** auf der LinkedIn-Firmenseite in Chrome prüfen (`linkedin.com/company/<name>/about/`, Felder „Beschäftigte" und „Hauptsitz"). Außerhalb des Bereichs: Status `nein` mit Grund, oder `Reserve`, wenn knapp.
3. **Profil-URL holen.** Namenssuche im normalen LinkedIn: `https://www.linkedin.com/search/results/people/?keywords=<Vorname Nachname> <Firma>`, die Person mit der Firma in der Headline öffnen, die URL aus der Adresszeile nehmen. Im Sales Navigator führt auf der Lead-Seite das Menü „…" mit „Auf LinkedIn.com anzeigen" direkt zum Profil. ID-URLs (`/in/ACwAA…`) nie stehen lassen.
4. **Eintragen:**
   ```
   python3 .claude/skills/leads/scripts/setze.py 12 website=beispiel.de "groesse=11 bis 50 (LinkedIn)" linkedin=linkedin.com/in/max-muster "notiz-=noch prüfen" "notiz+=geprüft 2026-11-10, 2. Grad"
   python3 .claude/skills/leads/scripts/setze.py 15 status=nein "notiz+=geprüft 2026-11-10: Konzern, 400 Beschäftigte"
   ```
   Der Teil `notiz-=noch prüfen` ist Pflicht, sonst bleibt die Zeile als ungeprüft markiert.

Mehrere Zeilen hintereinander: Websites gesammelt an `website.py` geben (ein Aufruf, mehrere Domains), Firmenseiten und Profile dann nacheinander in einem Chrome-Tab.

### 3. Neue Kandidaten suchen

Erst wenn die halbfertigen Zeilen den Bedarf nicht decken. Rezepte und Filter in `references/quellen.md`. Hauptweg ist die Personensuche auf LinkedIn (mit Sales Navigator, wenn vorhanden) in Chrome (Tools wie in `/anfragen` Schritt 3 laden, neuer Tab, eingeloggt sein).

Pro Ergebnisseite `get_page_text`, daraus Name, Rolle, Firma, Ort und die Profil-URL ziehen. Alle Firmen und Namen der Seite in einem Aufruf gegen die Liste prüfen:

```
python3 .claude/skills/leads/scripts/dublette.py "Beispiel GmbH" "Max Muster" beispiel.de
```

Was „neu" ist, wird wie in Schritt 2 geprüft (Website, Größe, Profil-URL) und dann als JSON-Datei im Scratchpad gesammelt und angehängt:

```
python3 .claude/skills/leads/scripts/eintragen.py <scratchpad>/leads.json --probe
python3 .claude/skills/leads/scripts/eintragen.py <scratchpad>/leads.json
```

JSON ist eine Liste von Objekten mit `firma`, `person`, `website`, `linkedin`, `detail`, `groesse`, `branche`, `quelle`, `notiz`. Das Skript vergibt die Nummer, setzt Status `neu`, hängt „Recherche <Datum>" an und überspringt Dubletten. Kandidaten, die durchfallen, ohne je in der Tabelle gewesen zu sein, kommen mit Grund in den Abschnitt Aussortiert:

```
python3 .claude/skills/leads/scripts/eintragen.py --aussortiert "Foo (zu groß, 400)" "Bar (Agentur)"
```

Wer die Prüfung nicht in dieser Sitzung schafft, kommt trotzdem rein, mit `notiz` „noch prüfen", damit die Person nicht verloren geht. Besser halbfertig in der Liste als nur im Browser.

### 4. Ausgabe

```
**Bedarf:** 60 für Mi, Do, Fr. Vorher 2 versandbereit.
**Fertig gemacht:** 18 Zeilen (12 bis 29), davon 3 aussortiert (15 Konzern, 20 Agentur, 24 nicht erreichbar)
**Neu eingetragen:** 12 Zeilen (30 bis 41), Quelle LinkedIn-Suche „Geschäftsführer Steuerberatung Hamburg"
**Jetzt versandbereit:** 29. Fehlen noch 31. Nächster Schritt: Zeilen 42 bis 55 prüfen.
```

Danach `python3 .claude/skills/leads/scripts/bedarf.py` noch einmal zeigen, damit die Zahl stimmt.

## Regeln

- **Fakten statt Annahmen:** Größe nur von der LinkedIn-Firmenseite oder aus einem Beleg, nicht geschätzt. Was nicht belegt ist, bleibt als „noch prüfen" markiert.
- **Vor jedem Eintrag Dublette prüfen,** auch gegen Aussortiert. Eine Firma, die dort steht, wird nicht erneut geprüft.
- **Eine Person pro Firma.** Zweitkontakte in die Notiz, nicht als eigene Zeile.
- **Keine Anfrage aus diesem Skill.** Vernetzen macht `/anfragen` mit der Tagesrechnung.
- **Keine Secrets, keine privaten Daten** über das hinaus, was Impressum und LinkedIn öffentlich zeigen. Telefonnummern nur aus dem Impressum.
- **Sales Navigator nur lesen.** Keine InMails, keine Anfragen, keine Notizen von dort.
- **Firmenseiten und Suchen nicht per Skript in Serie abrufen.** Das sieht LinkedIn als Bot. Ein Tab, eine Seite nach der anderen.
