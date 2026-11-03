---
name: heute
description: Zeigt zu Beginn jedes Akquise-Tags, was ansteht, in Reihenfolge. Antworten beantworten, DMs an neue Annahmen, fällige Follow-ups, wie viele Kontaktanfragen heute erlaubt sind, und ob Nachschub in der Kalt-Liste fehlt. Immer nutzen bei "/heute", "was steht an", "was muss ich heute machen", "Tagesplan", "los geht's" oder beim ersten Aufruf am Tag. Erledigt nichts selbst, nennt die Skills dafür.
---

# Heute: Der Tagesplan in einer Minute

Akquise scheitert selten am Können, meist daran, dass man morgens nicht weiß, womit man anfängt, und dann den Block verschiebt. Dieser Skill rechnet aus Kalt-Liste und Scorecard, was heute fällig ist, und gibt die Reihenfolge vor. Reihenfolge nach Wert: Wer geantwortet hat, ist am wärmsten, Anfragen sind am kältesten.

Alle Pfade relativ zum Vault-Ordner. Fehlt `Sales/Profil.md`, zuerst `/einrichten` vorschlagen und aufhören.

## Ablauf

1. **Annahmen abfragen.** Die Kalt-Liste weiß nicht von selbst, wer angenommen hat. Fragen: „Hat seit dem letzten Mal jemand die Kontaktanfrage angenommen oder geantwortet?" Wenn ja, pro Person `python3 .claude/skills/leads/scripts/setze.py <Nr> status=angenommen` (oder `status=antwort`). Wer es im Browser prüfen will: LinkedIn, „Mein Netzwerk", neue Kontakte mit der Kalt-Liste abgleichen (`dublette.py` mit den Namen).

2. **Drei Skripte laufen lassen**, in einem Aufruf:

```
python3 .claude/skripte/faellig.py
python3 .claude/skills/anfragen/scripts/tageszahl.py
python3 .claude/skills/leads/scripts/bedarf.py
```

3. **Tagesplan ausgeben**, kurz, in dieser Reihenfolge:

```
**Heute, [Wochentag Datum]**
1. Antworten: 2 (Zeilen 14, 27) → /dm 14
2. DMs an neue Annahmen: 3 (Zeilen 8, 19, 22) → /dm 8
3. Follow-ups fällig: 4 (Zeilen 3, 5, 9, 11) → /dm 3
4. Kontaktanfragen: 18 möglich (Wochenfenster 82 von 100, 20 versandbereit) → /anfragen
5. Nachschub: 12 versandbereite Leads fehlen für die nächsten 3 Tage → /leads
Am Ende des Blocks: python3 .claude/skripte/scorecard.py --eintragen
```

Punkte mit 0 weglassen. Wenn nichts fällig ist und die Liste leer ist, steht da nur `/leads`.

4. **Nicht erledigen.** Der Skill plant, die anderen Skills arbeiten. Erst auf Aufruf (`/dm 14`, `/anfragen`) weitermachen.

## Regeln

- **Kein Status raten.** Annahmen und Antworten nur eintragen, wenn die Person sie bestätigt hat oder der Browser sie zeigt.
- **Reihenfolge nicht umdrehen.** Antworten vor DMs vor Follow-ups vor Anfragen. Anfragen sind das Einzige, was sich verschieben lässt, ohne einen warmen Lead zu verlieren.
