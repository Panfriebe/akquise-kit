---
name: anfragen
description: Verschickt die heutigen LinkedIn-Kontaktanfragen per Chrome (claude-in-chrome) und rechnet vorher aus, wie viele es heute sein dürfen (Tagesziel aus den Einstellungen, Wochenfenster ca. 100 in 7 Tagen, Vorrat in der Kalt-Liste). Immer nutzen bei "Anfragen raus", "heutige Anfragen", "vernetzen", "wie viele Anfragen heute", "Kontaktanfragen schicken" oder "/anfragen", auch ohne Zahl. Nicht für DMs oder Follow-ups (dafür /dm) und nicht für die Lead-Suche (dafür /leads).
---

# Anfragen: Heutige LinkedIn-Kontaktanfragen verschicken

LinkedIn lässt nur etwa 100 Kontaktanfragen in 7 Tagen zu. Wer das Limit reißt, kann tagelang gar nichts schicken, und wiederholte Verstöße gefährden das Konto. Deshalb rechnet dieser Skill zuerst, dann klickt er. Und er klickt im normalen LinkedIn, nie im Sales Navigator, weil der Navigator-Button eine Notiz einfügt. Anfragen gehen **immer ohne Notiz** raus, das recherchierte Detail gehört in die DM nach der Annahme (Annahmequote ohne Notiz ist in der Praxis nicht schlechter, und das Detail bleibt für die DM unverbraucht).

Alle Pfade relativ zum Vault-Ordner. Skripte in `.claude/skills/anfragen/scripts/`, Kalt-Liste und Scorecard in `Sales/`, Tagesziel in `Sales/einstellungen.json`.

## Was reinkommt

`/anfragen` ohne Zahl heißt: so viele, wie die Rechnung erlaubt. `/anfragen 12` heißt höchstens 12, die Rechnung deckelt trotzdem. Mit dem Aufruf ist der Versand freigegeben. Nachfragen nur, wenn die Tageszahl 0 ist, Chrome nicht eingeloggt ist, oder LinkedIn ein Limit meldet.

## Ablauf

### 1. Tageszahl rechnen

```
python3 .claude/skills/anfragen/scripts/tageszahl.py
```

Liest die Scorecard (Anfragen der letzten 7 Tage inklusive heute) und die Kalt-Liste (Vorrat) und druckt `HEUTE MÖGLICH: n`. Diese Zahl ist die Obergrenze, auch wenn mehr genannt wurde. Bei 0 nichts verschicken und den Grund nennen (Tagesziel erreicht oder Wochenlimit voll, dazu, wie viele morgen aus dem Fenster fallen).

Wenn LinkedIn in einer früheren Sitzung ein Limit gemeldet hat, steht das in der Scorecard-Notiz. Dann `wochenlimit` in `Sales/einstellungen.json` senken (zum Beispiel auf 80) und es sagen.

### 2. Leads wählen

```
python3 .claude/skills/anfragen/scripts/naechste.py 12
```

Druckt die nächsten Leads in Versandreihenfolge: versandbereite zuerst (echte Profil-URL `linkedin.com/in/<name>`), danach Zeilen, deren Person bekannt ist, aber die URL eine Sales-Navigator-ID (`ACwAA…`), ein Suchlink oder leer ist. Zeilen mit „Qualifikation offen" kommen zuletzt. Wenn weniger als die Tageszahl zusammenkommt, zuerst die halbfertigen Zeilen per Namenssuche nehmen (Schritt 4), und am Ende sagen, dass Nachschub per `/leads` fehlt.

Eine Person pro Firma. Wer in der Notiz als „kein LinkedIn" oder „passiv" vermerkt ist, zählt nicht.

### 3. Chrome vorbereiten

Alle Browser-Tools in einem ToolSearch-Aufruf laden:

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_close_mcp
```

Dann `tabs_context_mcp`, danach einen **neuen Tab** anlegen (keinen bestehenden Tab übernehmen). `https://www.linkedin.com/feed/` öffnen. Erscheint die Login-Seite, abbrechen und bitten, sich in Chrome einzuloggen. Nichts von hier aus einloggen.

### 4. Pro Lead: öffnen, prüfen, vernetzen

Für jeden Lead der Reihe nach, nicht parallel:

1. **Profil öffnen.** Versandbereite Zeile: die Profil-URL aus dem Skript. Sonst Namenssuche: `navigate` auf `https://www.linkedin.com/search/results/people/?keywords=<Vorname Nachname> <Firma>`, 2 Sekunden warten, dann `find` mit „Profil-Links der Suchergebnisse mit Name, Headline und Grad (href)". Das liefert Name, Headline und die echte Profil-URL in einem Aufruf, ohne `get_page_text` (das druckt bei Profilen alle Beiträge, Hunderte Zeilen). Die Person nehmen, deren Headline die Firma nennt. Wenn keine passt, Zeile überspringen (Schritt 5, Grund „kein Profil gefunden"). ID-URLs (`/in/ACwAA…`) gar nicht erst probieren, direkt Namenssuche.
2. **Person prüfen:** Profil per `navigate` öffnen, 2 Sekunden warten, dann ein `find` mit „Name, Headline, Grad und Ort im Profilkopf sowie die Buttons Vernetzen, Folgen, Ausstehend, Nachricht, Mehr" plus ein Screenshot (scale 0.5). Name stimmt mit der Spalte Person überein, die Headline nennt die Firma, Grad ist 2 oder 3. Stimmt eins davon nicht, überspringen. Nicht raten, nicht den Namensvetter nehmen.
3. **Status des Buttons lesen** (aus dem `find`-Ergebnis von Schritt 2):
   - „Vernetzen" (englisch „Connect") sichtbar: weiter mit 4.
   - „Folgen" („Follow") als Hauptbutton: den Drei-Punkte-Button „Mehr" rechts daneben **per Koordinate aus dem Screenshot** klicken (der `find`-Ref „Mehr" trifft oft den Toolbar-Button und öffnet nichts), 1 Sekunde warten, dann `find` „Menüeintrag Vernetzen im aufgeklappten Dropdown" und den Ref klicken. Nie „Folgen" statt Vernetzen klicken.
   - „Ausstehend" („Pending"): Anfrage läuft schon. Markieren mit `--ausstehend`, zählt nicht als heute.
   - „Nachricht" („Message") als Hauptbutton und 1. Grad: schon vernetzt. Status per `setze.py <Nr> status=angenommen` setzen und es sagen, damit die DM kommt.
   - Vernetzen verlangt eine E-Mail-Adresse: überspringen, Grund „nur mit E-Mail".
4. **„Vernetzen" klicken** (Ref aus `find`), 1,5 Sekunden warten, Screenshot. Der Dialog heißt „Eine Nachricht zu Ihrer Einladung hinzufügen?" (englisch „Add a note to your invitation?") mit den Buttons „Nachricht hinzufügen" und **„Ohne Notiz senden"** (englisch „Send without a note"). `find` sieht diesen Dialog oft nicht, deshalb den Screenshot prüfen und den rechten blauen Button per Koordinate klicken. Nur klicken, wenn der Screenshot den Dialog zeigt, sonst trifft der Klick die Seite dahinter. Nie „Nachricht hinzufügen". Wenn kein Dialog kommt und sofort „Ausstehend" steht, ist die Anfrage raus.
5. **Bestätigung prüfen:** Toast „Einladung gesendet" („Invitation sent") oder Button wechselt auf „Ausstehend". Erst dann zählt die Anfrage. Zeilennummer in der laufenden Liste notieren.
6. **Limit-Warnung:** Meldet LinkedIn „wöchentliches Einladungslimit erreicht", „You've reached the weekly invitation limit" oder verlangt eine Sicherheitsprüfung, **sofort aufhören**. Gesendete Anfragen bis dahin normal nachtragen, in der Scorecard-Notiz den Wortlaut festhalten, die Person informieren.

Tempo: ein Profil nach dem anderen, ein Tab. `browser_batch` ist erlaubt und spart Zeit, aber nur für Schritte, deren Ergebnis feststeht (Senden-Klick, warten, Screenshot, dann schon die Namenssuche des nächsten Leads). Nie den Dialog-Klick in denselben Batch wie den Vernetzen-Klick legen, ohne den Screenshot dazwischen gesehen zu haben. Mehr als die Tageszahl geht nicht raus, auch wenn Leads übrig sind.

Erfahrungswert: 12 Anfragen in etwa 40 Browser-Aufrufen, pro Lead 3 bis 4 (Suche, Profil, Vernetzen, Senden).

### 5. Nachtragen

Kalt-Liste, alle gesendeten Zeilen in einem Aufruf, gefundene Profil-URLs gleich mit:

```
python3 .claude/skills/anfragen/scripts/markiere.py 5 6 7 --url 5=linkedin.com/in/max-muster
python3 .claude/skills/anfragen/scripts/markiere.py 8 --uebersprungen "nur mit E-Mail"
python3 .claude/skills/anfragen/scripts/markiere.py 9 --ausstehend
```

Setzt Status `angefragt`, letzten Kontakt auf heute, Follow-up nach den Einstellungen und den Notiz-Zusatz „Anfrage ohne Notiz per Browser <Datum>". Übersprungene behalten ihren Status und bekommen den Grund in die Notiz. Was beim Prüfen nebenbei belegt wurde (Rolle laut Headline, Grad, Größe), per `setze.py` aus `/leads` nachtragen.

Scorecard, Anfragen-Zelle und Notiz für heute (legt die Tageszeile an, wenn sie fehlt):

```
python3 .claude/skills/anfragen/scripts/tageszahl.py --eintragen --notiz "12 Anfragen ohne Notiz per Browser, Zeilen 5 bis 17, 8 übersprungen (nur mit E-Mail). Wochenfenster 82 von 100"
```

Zum Schluss `python3 .claude/skripte/faellig.py` laufen lassen und erwähnen, was sonst heute fällig ist (Annahmen, DMs, Follow-ups), ohne es zu erledigen.

### 6. Ausgabe

Kurz, ohne Lesen übernehmbar:

```
**Verschickt:** 12 von 12 möglich. Zeilen 5, 6, 7, …
**Übersprungen:** 8 (nur mit E-Mail), 10 (Profil passt nicht zur Firma)
**Wochenfenster:** 82 von 100, morgen fallen 20 raus
**Vorrat:** 2 versandbereit, 14 ungeprüft. Nachschub per /leads nötig.
**Heute sonst fällig:** 3 DMs an Annahmen, 2 Follow-ups
```

## Regeln, die nie fallen

- **Keine Notiz.** Nicht vorschlagen, nicht einfügen, auch nicht „nur dieses Mal".
- **Nicht über Sales Navigator senden.** Dort hängt der Button eine Notiz an.
- **Nicht mehr als die Tageszahl.** Das Wochenfenster ist die harte Grenze, nicht der Vorrat.
- **Keine DM hier.** Wer annimmt, bekommt die Nachricht über `/dm`.
- **Nur belegte Personen.** Name und Firma müssen auf dem Profil zusammenpassen.
- **Nichts in der Scorecard erfinden.** Gezählt wird, was LinkedIn bestätigt hat.
- **Eigenes Konto, eigenes Risiko.** LinkedIn verbietet Automatisierung in seinen Nutzungsbedingungen. Das Tempo bleibt menschlich (ein Profil nach dem anderen, Pausen), und bei jeder Warnung ist sofort Schluss.
