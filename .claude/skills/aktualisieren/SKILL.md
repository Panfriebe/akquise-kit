---
name: aktualisieren
description: Holt die neueste Fassung des Akquise-Kits (Skills, Skripte, Vorlagen) aus dem Git-Repository, ohne die eigenen Daten in Sales/ anzufassen, und sagt, was sich geändert hat. Immer nutzen bei "/aktualisieren", "Update", "neue Version", "Kit aktualisieren", "gibt es was Neues".
---

# Aktualisieren: Neue Skills und Skripte holen

Das Kit wird weiterentwickelt. Die eigenen Daten (`Sales/`) liegen nicht im Git und bleiben bei jedem Update unverändert. Geholt werden nur `.claude/`, `_Vorlagen/`, `README.md` und `CLAUDE.md`.

## Ablauf

1. Stand merken: `git -C <Vault> rev-parse --short HEAD`
2. Holen: `git -C <Vault> pull --ff-only`
3. Fehler „not a git repository": Der Ordner wurde als Zip geladen. Dann sagen, dass Updates nur per Git gehen, und anbieten, das Repo neu zu klonen und `Sales/` hinüberzukopieren.
4. Fehler wegen lokaler Änderungen in Kit-Dateien (jemand hat eine Vorlage oder einen Skill direkt bearbeitet): nicht überschreiben. Zeigen, welche Dateien betroffen sind (`git status --short`), und fragen, ob die eigenen Änderungen verworfen werden dürfen. Eigene Anpassungen gehören in `Sales/`, nicht in `_Vorlagen/`.
5. Änderungen zeigen: `git -C <Vault> log --oneline <alt>..HEAD` und die Dateiliste `git diff --stat <alt> HEAD`.
6. Wenn `_Vorlagen/Nachrichtenregeln.md` oder `_Vorlagen/einstellungen.json` neue Felder haben, die in `Sales/` fehlen: nennen und anbieten, sie zu ergänzen. Nie ungefragt in `Sales/` schreiben.

## Ausgabe

```
**Aktualisiert:** 3 Commits (a1b2c3 → d4e5f6)
- anfragen: Dialog „Ohne Notiz senden" auch auf Englisch erkannt
- dm: neue Floskeln im Prüfer
**Deine Daten:** unverändert (Sales/)
**Zu tun:** einstellungen.json hat ein neues Feld „pause_tage", soll ich es mit dem Standard ergänzen?
```
