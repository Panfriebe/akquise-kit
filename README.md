# Akquise-Kit: LinkedIn-Akquise mit Claude Code

Ein Ordner, der deine Kalt-Liste führt, Kontaktanfragen auf LinkedIn verschickt, Nachrichten nach festen Regeln schreibt und dir jeden Morgen sagt, was ansteht. Die Arbeit macht Claude Code in deinem Chrome, mit deinem LinkedIn-Konto. Du gibst die Zielgruppe, den Schmerz des Kunden und dein Angebot vor, alles andere ist vorbereitet.

Du brauchst keine Programmierkenntnisse. Du tippst Befehle wie `/heute` in ein Chat-Fenster.

## Was du brauchst

| Was | Wofür | Kosten |
|---|---|---|
| **Claude Code** (Desktop-App für Mac oder Windows) | das Chat-Fenster, in dem alles läuft. Download: https://claude.ai/download, dann „Claude Code" | Claude-Abo Pro oder Max. Pro reicht zum Start. Mit Max kommst du an einem Akquise-Tag nicht ans Limit |
| **Google Chrome** mit der Extension **„Claude in Chrome"** | damit Claude in deinem LinkedIn klicken kann. Im Chrome Web Store nach „Claude in Chrome" suchen | kostenlos |
| **LinkedIn**, in Chrome eingeloggt | dein eigenes Konto. Alles läuft über dein Profil | dein bestehendes Konto |
| **LinkedIn Sales Navigator** | hilft bei der Suche nach neuen Firmen | optional, ab ca. 80 EUR im Monat |
| **Obsidian** | zeigt die Kalt-Liste als Tabelle. Download: https://obsidian.md | optional, kostenlos |

Python und Git sind auf dem Mac dabei. Falls nicht, sagt dir die Einrichtung, was zu tun ist.

## Einrichtung (einmalig, etwa 30 Minuten)

1. **Claude Code öffnen** und einen neuen, leeren Ordner wählen, zum Beispiel `Dokumente/Akquise`. (In der Desktop-App: „Open folder". Im Terminal: in den Ordner wechseln und `claude` tippen.)
2. **Diesen Satz in das Chat-Fenster einfügen:**

   ```
   Hol dir das Akquise-Kit von https://github.com/Panfriebe/akquise-kit in diesen Ordner (git clone, Inhalt direkt hier hinein) und starte danach /einrichten.
   ```

3. **Fragen beantworten.** Claude prüft zuerst, ob Chrome, die Extension und LinkedIn bereit sind, und fragt dann in kurzen Runden nach deinem Angebot, deiner Zielgruppe, den Schmerzen deiner Kunden und deinem Rhythmus. Antworte so, wie du es einem Kollegen am Telefon sagen würdest. Was du nicht weißt, lässt du offen.
4. **Fertig.** Deine Antworten stehen in `Sales/Profil.md`. Du kannst sie jederzeit dort ändern oder `/einrichten` noch einmal aufrufen.

Wenn du Obsidian nutzt: Obsidian öffnen, „Ordner als Vault öffnen", den Akquise-Ordner wählen.

## Jeder Akquise-Tag

Fester Block im Kalender, zum Beispiel 9 bis 11 Uhr. Dann in Claude Code:

| Befehl | Was passiert |
|---|---|
| `/heute` | Tagesplan: wer hat geantwortet, wer braucht eine Nachricht, wie viele Anfragen sind heute erlaubt, fehlt Nachschub |
| `/dm 14` | schreibt zwei Entwürfe für die Nachricht an Zeile 14 der Kalt-Liste. Du kopierst einen davon in LinkedIn, oder sagst „schick das so" |
| `/anfragen` | verschickt die heutigen Kontaktanfragen in deinem Chrome, ohne Notiz, und trägt alles ein |
| `/leads` | füllt die Kalt-Liste mit neuen Firmen und Personen, die zu deiner Zielgruppe passen |
| `/aktualisieren` | holt neue Versionen des Kits. Deine Daten bleiben unverändert |

Am Ende des Blocks: „trag die Scorecard ein". Nach vier Wochen siehst du in `Sales/Scorecard.md`, was funktioniert hat.

## Was im Ordner liegt

```
Sales/                    deine Daten, nur bei dir (Profil, Kalt-Liste, Scorecard, Regeln, Einstellungen)
_Vorlagen/                Vorlagen für die Einrichtung, nicht bearbeiten
.claude/skills/           die Befehle (/einrichten, /heute, /leads, /anfragen, /dm, /aktualisieren)
.claude/skripte/          Hilfsprogramme, die die Kalt-Liste lesen und schreiben
CLAUDE.md                 Regeln, die Claude in diesem Ordner einhält
```

Du musst in `.claude/` und `_Vorlagen/` nichts anfassen. Wenn du Regeln ändern willst, ändere `Sales/Nachrichtenregeln.md` und `Sales/Profil.md`.

## Was du wissen musst

- **Dein Konto, dein Risiko.** LinkedIn verbietet automatisierte Aktionen in seinen Nutzungsbedingungen. Das Kit arbeitet deshalb in menschlichem Tempo, hält das Wochenlimit von etwa 100 Anfragen ein und hört bei jeder Warnung sofort auf. Eine Sperre ist trotzdem möglich. Wer das nicht will, lässt `/anfragen` die Liste nur vorbereiten und klickt selbst.
- **Keine Nachricht ohne belegten Schmerz.** Das Kit schreibt keine Nachricht, solange in `Sales/Profil.md` kein Schmerz mit Quelle steht. Das ist Absicht. Generische Nachrichten bekommen keine Antwort.
- **Claude verschickt nur, was du freigibst.** `/dm` schreibt Entwürfe. `/anfragen` verschickt erst, wenn du es aufrufst.
- **Keine Passwörter in den Ordner.** Der Ordner ist ein normaler Ordner auf deinem Rechner. Logins passieren in Chrome, nicht in Claude.
- **Was zählt, ist „raus".** Die Scorecard zählt Anfragen und Nachrichten, die rausgegangen sind. Antworten kannst du nicht steuern, das Volumen schon.

## Wenn etwas nicht geht

Schreib es Claude im Chat, so wie es ist („die Extension findet LinkedIn nicht", „das Skript meldet einen Fehler"). Meistens löst es das selbst. Wenn nicht, schick die Fehlermeldung an die Person, von der du das Kit hast.
