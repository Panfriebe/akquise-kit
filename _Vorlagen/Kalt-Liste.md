---
typ: liste
stand: DATUM
---

# Kalt-Liste

> Zielgruppe und Stufen stehen in [[Profil]]. Eine Zeile pro Firma, eine Person pro Firma (Zweitkontakte in die Notiz).
> Status: `neu`, `angefragt`, `angenommen`, `dm`, `antwort`, `gespräch`, `angebot`, `nein`. Follow-up nach der Zahl Werktage aus `einstellungen.json`.
> Die Skripte lesen und schreiben diese Tabelle. Spalten nicht umbenennen, keine `|` in Zellen. Zeilen von Hand ergänzen ist in Ordnung, die Nummer muss eindeutig sein.

## Regeln

1. **Vor jedem Eintrag Dublette prüfen,** auch gegen Aussortiert (`dublette.py`).
2. **Fakten statt Annahmen:** Größe nur von der LinkedIn-Firmenseite oder aus einem Beleg. Was nicht belegt ist, bekommt „noch prüfen" in die Notiz.
3. **Kontaktanfragen ohne Notiz.** Das recherchierte Detail gehört in die DM nach der Annahme.
4. **Nicht über Sales Navigator vernetzen,** der Button dort hängt eine Notiz an. Profil im normalen LinkedIn öffnen.
5. **Wochenlimit:** etwa 100 Anfragen in 7 Tagen (rollierend). `/anfragen` rechnet das aus der [[Scorecard]].

## Liste

| Nr | Firma | Website | Person | LinkedIn | Detail | Größe | Branche | Quelle | Status | Letzter Kontakt | Follow-up | Notiz |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Aussortiert

Firmen, die geprüft wurden und nicht passen, mit Grund. Damit sie nicht noch einmal geprüft werden.
