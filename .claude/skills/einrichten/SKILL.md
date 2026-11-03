---
name: einrichten
description: Richtet das Akquise-Kit beim ersten Start ein. Prüft Programme und Abos (Claude Code, Chrome mit Claude-Extension, LinkedIn-Login, Python, Obsidian), fragt dann in kurzen Runden nach Angebot, Zielgruppe (ICP), belegten Schmerzen, Referenz, Ton und Rhythmus, und legt daraus Sales/Profil.md, Kalt-Liste, Scorecard, Nachrichtenregeln und einstellungen.json an. Immer nutzen bei "/einrichten", "einrichten", "Setup", "loslegen", "erster Start" oder wenn Sales/Profil.md fehlt. Auch zum Nachbessern einzelner Teile ("Profil ändern", "Tagesziel ändern").
---

# Einrichten: Vom leeren Ordner zur ersten Kalt-Liste

Das Kit funktioniert nur, wenn Zielgruppe, Schmerz und Angebot der Person gehören, die es benutzt. Nachrichten aus fremden Schmerzen klingen generisch und verbrennen Leads. Deshalb fragt dieser Skill, statt Vorlagen zu kopieren, und trägt nur ein, was die Person wirklich gesagt hat.

Alle Pfade relativ zum Vault-Ordner (der Ordner mit `.claude/` und `_Vorlagen/`). Die Daten landen in `Sales/`, das nicht im Git liegt. Updates per `/aktualisieren` fassen `Sales/` nie an.

## Grundhaltung beim Fragen

- **Eine Runde nach der anderen**, höchstens vier Fragen pro Runde, mit `AskUserQuestion`, wo Auswahl sinnvoll ist, sonst im Gespräch. Niemals alle Fragen auf einmal.
- **Jede Frage begründen** in einem Satz, damit die Person weiß, wofür die Antwort gebraucht wird.
- **Fakten statt Annahmen.** Ein Schmerz ohne Quelle („ein Kunde hat gesagt ...", „im Gespräch mit ...") wird als Hypothese eingetragen, nicht als belegt. Das sagen, nicht verschweigen.
- **Nichts erfinden.** Fehlende Antworten bleiben als Platzhalter stehen, mit dem Hinweis, dass `/dm` ohne sie nicht arbeitet.
- **Die Person darf abkürzen.** Wer sagt „das reicht erst mal", bekommt den Rest als offene Punkte am Ende.

## Ablauf

### 0. Stand prüfen

Wenn `Sales/Profil.md` schon existiert: fragen, ob alles neu oder nur ein Teil (Angebot, Zielgruppe, Schmerzen, Ton, Rhythmus) geändert werden soll. Nur den Teil neu fragen und in den Dateien ersetzen.

### 1. Programme und Abos

Nacheinander prüfen und das Ergebnis als Tabelle zeigen (vorhanden, fehlt, optional). Nur fragen, was sich nicht selbst prüfen lässt.

| Was | Prüfung | Pflicht |
|---|---|---|
| Python 3 | `python3 --version` (ab 3.9) | ja, die Skripte brauchen es. Auf dem Mac ist es dabei, sonst Xcode Command Line Tools: `xcode-select --install` |
| Git | `git --version` | ja, für `/aktualisieren` |
| Chrome mit Extension „Claude in Chrome" | Browser-Tools laden (`ToolSearch` mit `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__find`), dann `tabs_context_mcp`. Fehler oder kein Tool: Extension fehlt. Anleitung: chrome.google.com/webstore nach „Claude in Chrome" suchen, installieren, in Claude Code anmelden | ja, `/anfragen` und `/leads` klicken damit |
| LinkedIn eingeloggt | neuen Tab mit `https://www.linkedin.com/feed/` öffnen. Login-Seite: die Person bitten, sich in Chrome einzuloggen, nichts von hier aus eingeben | ja |
| LinkedIn Sales Navigator | fragen | nein, hilft bei der Lead-Suche |
| Obsidian | `ls /Applications/Obsidian.app` | nein, alles sind Markdown-Dateien. Empfehlung: diesen Ordner als Vault öffnen, dann liest sich die Kalt-Liste als Tabelle |
| Claude-Abo | fragen (Pro oder Max). Mit Pro kann das Tageslimit vor Ende eines Akquise-Blocks erreicht sein, weil Browser-Schritte viele Tokens kosten | Hinweis, keine Pflicht |

Fehlt etwas Pflichtiges: die Installationsschritte nennen und mit dem Rest weitermachen. Am Ende steht es in den offenen Punkten.

### 2. Angebot

Fragen, mit Begründung „daraus entsteht das Traumergebnis in der Nachricht":

1. Was verkaufst du, in zwei Sätzen, so wie du es einem Kunden am Telefon sagen würdest?
2. Was hat der Kunde danach, in seinen Worten? (Traumergebnis, kein Feature)
3. Gibt es einen Kunden oder ein Projekt, das du als Referenz nennen darfst? Wie genau darfst du es nennen (Name, Branche, Stadt)? Nur, was schriftlich erlaubt ist.
4. Was kannst du einem Lead nach dem Ja in unter 30 Minuten gratis geben, ohne Zugang zu seinen Systemen? (Geschenk für das Gespräch oder Follow-up)

### 3. Zielgruppe (ICP)

Begründung: „Die Kalt-Liste wird nur mit Firmen gefüllt, die hier reinpassen."

1. Branche oder Art der Firma (so konkret, dass man sie auf LinkedIn filtern kann)
2. Größe in Beschäftigten laut LinkedIn-Firmenseite (zum Beispiel 11 bis 50)
3. Region (Länder oder Städte)
4. Welche Person in der Firma? Rolle laut LinkedIn-Headline (Gründer, Geschäftsführer, Head of ...)
5. Wen ausschließen? (Konzerne, Agenturen, Händler, Wettbewerber)

### 4. Schmerzen

Begründung: „Die erste Nachricht nennt genau einen belegten Schmerz in den Worten des Kunden. Was nicht belegt ist, trifft nicht."

1. Nenne bis zu drei Dinge, die diese Kunden wirklich drücken. Pro Schmerz: Wie hat der Kunde es gesagt oder gezeigt? Woher weißt du das (Gespräch, Mail, Projekt, Datum)?
2. Welcher davon ist der Grundschmerz, in einem Satz, wie der Kunde ihn sagen würde?
3. Was hältst du für wichtig, was der Kunde aber nicht als Kaufgrund nennt? (Technik, Datenschutz, Zeitersparnis beim Tippen)
4. Welche Wörter benutzt der Kunde nicht, die du aber ständig benutzt? (Fachwörter, diese bekommen eine Warnung im Prüfer)
5. Welche Wörter zeigen, dass ein Detail zum Schmerz gehört? (zum Beispiel „Support", „Bewertung", „Einarbeitung", „Angebot", „Rechnung"; diese werden Themenwörter im Prüfer)

Schmerz ohne Quelle: eintragen unter Hypothesen und sagen, mit welcher Frage im nächsten Kundengespräch er belegt werden könnte.

### 5. Ton

1. Du oder Sie in der ersten Nachricht? (Branche entscheidet, bei Gründern meist Du)
2. Ein bis zwei Sätze, wie die Person spricht, wenn sie einem Bekannten erklärt, was sie macht. Das wird das Tonbeispiel, an dem `/dm` sich orientiert.

### 6. Rhythmus

1. An welchen Wochentagen ist Akquise-Zeit, und wann am Tag? (ein fester Block, sonst wird er verschoben)
2. Tagesziel Kontaktanfragen (Empfehlung 20 bis 25, Wochenlimit bleibt etwa 100 in 7 Tagen)
3. Bis wann läuft die erste Runde, und woran wird am Ende gemessen, ob es sich gelohnt hat? (zum Beispiel „bis DATUM mindestens 6 Erstgespräche")

### 7. Dateien anlegen

Erst jetzt schreiben. `Sales/` anlegen, wenn es fehlt. Aus `_Vorlagen/` kopieren und die Platzhalter in Großbuchstaben (`ANGEBOT`, `SCHMERZ_1`, `DATUM`, ...) durch die Antworten ersetzen. Mehrere Schmerzen: Tabellenzeilen ergänzen. Leere Antworten: Platzhalter stehen lassen und unten in „Offene Punkte" aufführen.

- `Sales/Profil.md` aus `_Vorlagen/Profil.md`
- `Sales/Kalt-Liste.md` aus `_Vorlagen/Kalt-Liste.md` (nur `DATUM`)
- `Sales/Scorecard.md` aus `_Vorlagen/Scorecard.md` (`DATUM`, `ZEITRAUM`, `TAGESZIEL`, `PRUEFPUNKT`)
- `Sales/Nachrichtenregeln.md` aus `_Vorlagen/Nachrichtenregeln.md` (`DATUM`; Regel 1 und 7 an Tagesziel und Follow-up-Tage anpassen, falls abweichend)
- `Sales/einstellungen.json` aus `_Vorlagen/einstellungen.json`: `tagesziel`, `akquise_tage` (0 = Montag), `anrede`, `fachwoerter`, `themenwoerter`, `referenzwoerter` (Name des Referenzkunden und seine Stadt, damit der Prüfer warnt, wenn er in der ersten Nachricht auftaucht)

Danach prüfen, dass die Skripte laufen:

```
python3 .claude/skripte/faellig.py
python3 .claude/skills/anfragen/scripts/tageszahl.py
python3 .claude/skills/leads/scripts/bedarf.py
```

Alle drei müssen ohne Fehler durchlaufen (leere Liste ist in Ordnung).

### 8. Ausgabe

```
**Eingerichtet:** Profil, Kalt-Liste, Scorecard, Regeln, Einstellungen in Sales/
**Programme:** Python ok, Chrome-Extension ok, LinkedIn eingeloggt, Obsidian fehlt (optional)
**Offene Punkte:** Schmerz 2 ist Hypothese (Beleg fehlt), Referenz noch nicht schriftlich erlaubt
**Nächster Schritt:** /leads füllt die Kalt-Liste. Danach jeden Akquise-Tag /heute.
```

## Regeln

- **Nichts in `_Vorlagen/` ändern.** Das sind die Vorlagen für alle, sie kommen mit Updates.
- **Keine Secrets in den Vault.** Keine Passwörter, keine API-Keys, auch nicht in `einstellungen.json`.
- **Keine Schmerzen erfinden**, auch nicht aus allgemeinem Wissen über die Branche. Hypothese heißt Hypothese.
