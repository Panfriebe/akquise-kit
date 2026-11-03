# CLAUDE.md: Akquise-Kit

Ordner für LinkedIn-Akquise mit Claude Code. Die Befehle liegen als Skills in `.claude/skills/`, die Daten der Person in `Sales/`. `Sales/` liegt nicht im Git.

## Struktur

```
Sales/Profil.md             Angebot, Zielgruppe (ICP), belegte Schmerzen, Käufersprache, Referenz, Ton. Einzige Quelle für Nachrichten
Sales/Kalt-Liste.md         eine Zeile pro Firma, die Skripte lesen und schreiben die Tabelle
Sales/Scorecard.md          Tageswerte, gezählt wird „raus"
Sales/Nachrichtenregeln.md  die Regeln für jede Nachricht, der Prüfer kontrolliert die Form
Sales/einstellungen.json    Tagesziel, Wochenlimit, Akquise-Tage, Anrede, Fachwörter, Themenwörter, Referenzwörter
_Vorlagen/                  Vorlagen, aus denen /einrichten Sales/ erzeugt. Nicht bearbeiten
.claude/skripte/            gemeinsame Helfer (kaltliste.py, faellig.py, scorecard.py, website.py)
.claude/skills/             einrichten, heute, leads, anfragen, dm, aktualisieren
```

## Konventionen

- **Sprache Deutsch.** Keine langen Gedankenstriche (em-dash, en-dash), auch nicht in Nachrichten.
- **Fakten statt Annahmen.** Größe, Rolle, Branche nur eintragen, wenn belegt (LinkedIn-Firmenseite, Impressum, Website). Sonst „noch prüfen" in die Notiz. Schmerzen ohne Quelle sind Hypothesen.
- **Keine Secrets im Ordner.** Keine Passwörter, keine API-Keys, keine Logins. Einloggen passiert in Chrome.
- **Die Kalt-Liste ist die Wahrheit.** Status, Datum und Notiz werden nur über die Skripte oder bewusst per Hand geändert. Nichts raten, nichts aus dem Gedächtnis ergänzen.
- **Nichts verschicken ohne Aufruf.** `/anfragen` ist die Freigabe für Kontaktanfragen. DMs gehen nur raus, wenn die Person es ausdrücklich sagt.
- **Datumsformat ISO** `YYYY-MM-DD`.
- **Vor fachlicher Arbeit** `Sales/Profil.md` lesen. Fehlt die Datei oder enthält sie Platzhalter in Großbuchstaben, `/einrichten` vorschlagen.

## Skripte aufrufen

Immer aus dem Vault-Ordner heraus, mit relativem Pfad, zum Beispiel `python3 .claude/skripte/faellig.py`. Die Skripte finden ihre Dateien selbst. Jedes Skript zeigt mit `--help` oder ohne Argumente seine Verwendung.
