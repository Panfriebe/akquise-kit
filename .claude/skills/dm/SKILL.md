---
name: dm
description: Schreibt Akquise-Nachrichten an Leads aus der Kalt-Liste. LinkedIn-DM nach Annahme der Kontaktanfrage, Follow-up nach drei Werktagen, Antwort auf eine Rückmeldung. Immer nutzen, wenn eine Nachricht an einen Lead gewünscht ist, auch bei "schreib dem mal", "was schicke ich Zeile 17", "Follow-up für Max", "hat angenommen" oder "/dm". Nicht für LinkedIn-Posts, Profiltexte oder Kontaktanfragen.
---

# DM: Akquise-Nachricht für einen Lead

Akquise lebt von Nachrichten, die ein Fremder in fünf Sekunden liest und mit Ja beantworten kann. Jede Nachricht, die generisch klingt, verbrennt einen Lead, den die Recherche eine halbe Stunde gekostet hat. Deshalb entsteht hier keine Nachricht aus dem Kopf, sondern aus drei Dingen: dem Lead in der Kalt-Liste, einem belegten Detail, das zum Schmerz passt, und dem Schmerz aus `Sales/Profil.md` in Käufersprache.

Alle Pfade relativ zum Vault-Ordner. Skripte in `.claude/skills/dm/scripts/`.

## Was reinkommt

Ein Lead (Zeilennummer, Firmenname oder Personenname) und meist die Art der Nachricht. Wenn die Art fehlt, folgt sie aus dem Status in der Kalt-Liste: `angenommen` heißt erste DM, `dm` ohne Antwort und Follow-up-Datum erreicht heißt Follow-up, `antwort` heißt Antwort auf das, was die Person geschrieben hat (dann den Wortlaut erfragen, falls nicht in der Notiz).

## Ablauf

### 1. Lead laden

```
python3 .claude/skills/dm/scripts/lead.py 17
python3 .claude/skills/dm/scripts/lead.py Beispielfirma
```

Druckt die Zeile mit allen Feldern. Wichtig daraus: Vorname und Rolle, Detail, Stufe, was in der Notiz an Recherche steht, welche Nachrichten schon rausgingen. Wenn der Lead nicht gefunden wird, nachfragen, nicht raten.

### 2. Regeln und Profil laden

Drei Dateien lesen, in dieser Reihenfolge. Sie sind die einzige Quelle für Ton, Schmerz und Angebot. Der Skill wiederholt sie nicht, damit es nur eine Fassung gibt.

- `Sales/Nachrichtenregeln.md`: die zehn Regeln, Vorlagen für erste Nachricht und Follow-up, was nach dem Ja kommt.
- `Sales/Profil.md`: Grundschmerz, belegte Schmerzen, Käufersprache, Wörter, die der Kunde nicht benutzt, Referenz, Geschenk, Tonbeispiel.
- `Sales/einstellungen.json`: Anrede, Längen.

Steht im Profil noch ein Platzhalter in Großbuchstaben (`SCHMERZ_1`, `GRUNDSCHMERZ`), aufhören und `/einrichten` vorschlagen. Ohne belegten Schmerz entsteht hier keine Nachricht.

### 3. Detail belegen

Das Detail in der Nachricht muss zwei Bedingungen erfüllen: Es passt nur auf diese Firma, und es hat mit dem Schmerz zu tun. „Ihr habt 37 Mio. Umsatz" erfüllt die zweite nicht. Wenn die Kontaktanfrage ausnahmsweise mit Notiz ging, stand dort meist schon ein Detail, dann braucht die DM ein anderes.

Quellen, die in unter 10 Minuten belegbar sind, per WebFetch oder Chrome:

- Website der Firma: Seiten Kontakt, FAQ, Hilfe, Karriere, Über uns
- Stellenanzeigen (eigene Seite, LinkedIn Jobs, Stepstone): was die Firma gerade sucht, sagt, wo es klemmt
- LinkedIn-Posts der Person oder der Firma aus den letzten Wochen
- Bewertungen (Google, Trustpilot, Kununu, Trusted Shops): Anzahl, wiederkehrende Themen, ob die Firma antwortet
- Pressemitteilungen, Podcasts, Interviews mit der Person

Jedes Detail bekommt eine Quelle (URL und was dort steht). Was nicht belegt ist, kommt nicht in die Nachricht. Wenn gar nichts Belegbares zu finden ist, das sagen und keine Nachricht ohne Detail schreiben, sondern fragen, ob stattdessen angerufen wird.

### 4. Schmerz wählen

Aus `Sales/Profil.md` den Schmerz nehmen, zu dem das Detail passt. Entscheidung in einem Satz begründen. Kein Angebot, kein Geschenk, kein Termin in der ersten Nachricht (Regel 3 und 4). Das Geschenk aus dem Profil ist für das Gespräch oder das Follow-up.

### 5. Schreiben und prüfen

Zwei Entwürfe, die sich im Detail oder im Einstieg unterscheiden, nicht nur in Wörtern. Jeden Entwurf durch den Prüfer schicken:

```
python3 .claude/skills/dm/scripts/pruefe.py "Hallo Max, ich habe gesehen, dass ..."
python3 .claude/skills/dm/scripts/pruefe.py --follow-up "Hallo Max, ist meine Frage von Montag bei dir angekommen?"
```

Der Prüfer kennt die Formregeln (Länge, Satzzahl, verbotene Zeichen, Floskeln, Fachwörter, Anrede, unbelegbare Versprechen) und meldet jeden Verstoß. Er prüft keine Inhalte, ob das Detail stimmt und zur Firma passt, bleibt Aufgabe des Schreibenden. Entwürfe mit Fehlern werden überarbeitet, nicht mit Hinweis ausgeliefert.

Stil: so wie das Tonbeispiel im Profil. Direkt, ohne Anlauf, ohne Lob für die Firma, Frage am Ende, die man mit Ja beantworten kann. Follow-ups sind ein Satz, der die Frage wiederholt, ohne Druck und ohne „nur zur Sicherheit".

### 6. Ausgabe

Immer dieses Format, damit es ohne Lesen übernommen werden kann:

```
## [Vorname Nachname], [Firma] (Zeile [Nr])

**Lage:** [ein Satz, z. B. 40 offene Stellen auf der Karriereseite, davon 3 im Kundenservice]
**Schmerz:** [Nummer und Kurzname aus dem Profil], weil [ein Satz]

**Belege**
- [Detail]: [URL], [was dort steht]

**Entwurf A** ([n] Zeichen, Prüfer ok)
[Text]

**Entwurf B** ([n] Zeichen, Prüfer ok)
[Text]

**Nach dem Versand in die Kalt-Liste:**
python3 .claude/skills/leads/scripts/setze.py [Nr] status=dm letzter_kontakt=[heute] follow_up=[heute plus Werktage] "notiz+=DM gesendet [heute]"
```

Nichts wird verschickt und nichts in die Kalt-Liste geschrieben. Das macht die Person selbst, oder sie sagt ausdrücklich „trag das ein" oder „schick das so" (dann per Chrome im LinkedIn-Nachrichtenfenster, Text einfügen, Screenshot prüfen, senden, danach den `setze.py`-Befehl ausführen).

## Regeln

- **Kein Schmerz, keine Nachricht.** Lieber nachfragen als eine generische Nachricht schreiben.
- **Keine Zahl ohne Beleg.** Zahlen nur mit URL oder schriftlicher Bestätigung.
- **Referenz erst nach dem Ja.** Der Prüfer warnt, wenn sie in der ersten Nachricht steht.
- **Eine Linie, 50 Stück.** Den Aufbau der ersten Nachricht nicht pro Lead neu erfinden. Nur das Detail und der Vorname wechseln.
