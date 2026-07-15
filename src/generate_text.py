import anthropic, json, random
from datetime import datetime, date
from pathlib import Path

THEMEN_KATEGORIEN = {
    "einseitige_liebe": [
        "wenn du immer derjenige bist der schreibt",
        "wenn Liebe einseitig wird und du es zu spät merkst",
        "wenn du mehr gibst als du bekommst",
        "wenn du für jemanden kämpfst der dich nicht vermisst",
        "wenn deine Nachrichten auf gelesen bleiben",
        "wenn du weißt dass du zu viel bist für jemanden der zu wenig gibt",
        "wenn du hoffst dass sie sich ändern aber es nie passiert",
        "wenn du der einzige bist der noch an uns glaubt",
        "wenn Liebe sich anfühlt wie betteln",
        "wenn du liebst ohne geliebt zu werden",
        "wenn du bemerkst dass du ersetzt wurdest",
        "wenn jemand dich nur braucht wenn er einsam ist",
        "wenn du weißt dass du mehr verdienst aber nicht gehst",
    ],
    "verlust_und_loslassen": [
        "stilles Loslassen nach zu viel Schmerz",
        "wenn man jemanden verliert der einen als selbstverständlich sah",
        "der Moment wo man aufhört zu kämpfen",
        "wenn du jemanden liebst aber loslassen musst",
        "wenn eine Beziehung stirbt bevor sie endet",
        "wenn loslassen sich schlimmer anfühlt als bleiben",
        "wenn du jemanden vermisst der noch lebt",
        "wenn du weißt es ist vorbei aber dein Herz es nicht akzeptiert",
        "wenn du Erinnerungen löschst um weiterzumachen",
        "wenn das letzte Gespräch nicht so war wie du es wolltest",
        "wenn du nicht weißt ob du trauern sollst weil nichts offiziell war",
        "wenn jemand geht ohne zu erklären warum",
        "wenn du aufhörst zu warten und es sich wie Verrat anfühlt",
    ],
    "modernes_dating": [
        "wenn jemand dich ghostet nach allem was ihr geteilt habt",
        "wenn Gefühle per Nachricht beendet werden",
        "wenn jemand dich auf Abstand hält aber nicht loslässt",
        "wenn man nicht zusammen ist aber auch nicht getrennt",
        "wenn Social Media zeigt dass er ohne dich weitermacht",
        "wenn jemand sagt er braucht Zeit aber postet täglich Stories",
        "wenn du nicht weißt was ihr seid",
        "wenn jemand dich behandelt als wärst du eine Option",
        "wenn du auf eine Antwort wartest die nie kommt",
        "wenn jemand dich nur nachts braucht",
        "wenn Emojis mehr sagen als echte Worte",
        "wenn jemand dich daten will aber keine Beziehung",
        "wenn du nicht weißt ob du zu viel erwartest",
        "wenn jemand perfekt klingt aber nie da ist",
    ],
    "selbstverlust": [
        "wenn man sich für jemanden verändert der es nicht verdient",
        "sich selbst verlieren um jemand anderen glücklich zu machen",
        "wenn du nicht mehr weißt wer du ohne diese Person bist",
        "wenn du deine eigenen Bedürfnisse ignorierst für andere",
        "wenn du dich klein machst damit jemand anderes groß wirkt",
        "wenn du dich selbst nicht mehr erkennst",
        "wenn du merkst dass du dich verändert hast um zu gefallen",
        "wenn du deine Träume aufgibst für jemand anderen",
        "wenn du dich entschuldigst für Dinge die keine Entschuldigung verdienen",
        "wenn andere bestimmen wer du sein sollst",
        "wenn du vergisst was du dir selbst versprochen hast",
        "wenn du dich selbst am wenigsten liebst",
    ],
    "einsamkeit_und_overthinking": [
        "die Einsamkeit mitten unter Menschen",
        "Overthinking und nicht abschalten können",
        "wenn du nachts nicht schlafen kannst wegen Gedanken",
        "wenn du lächelst aber innerlich weinst",
        "wenn du das Gefühl hast niemand versteht dich wirklich",
        "wenn du Gespräche im Kopf führst die nie stattfinden",
        "wenn du um 3 Uhr nachts allein mit deinen Gedanken bist",
        "wenn du alles analysierst bis es keinen Sinn mehr macht",
        "wenn du Worte bereust die du gesagt oder nicht gesagt hast",
        "wenn du dir vorstellst wie es wäre wenn alles anders wäre",
        "wenn du Angst hast zu fühlen weil Fühlen wehtut",
        "wenn du nicht weißt warum du traurig bist aber es trotzdem bist",
        "wenn du funktionierst aber nicht lebst",
        "wenn du Menschen brauchst aber Nähe Angst macht",
    ],
    "unsichtbarkeit": [
        "das Gefühl unsichtbar zu sein obwohl man alles gibt",
        "wenn Menschen dich erst wertschätzen wenn es zu spät ist",
        "wenn du der Einzige bist der sich Mühe gibt",
        "wenn dein Schmerz von niemandem gesehen wird",
        "wenn du für alle da bist aber niemand für dich",
        "wenn du redest aber niemand zuhört",
        "wenn du fehlst aber niemand fragt wo du bist",
        "wenn du hilfst aber niemand fragt wie es dir geht",
        "wenn du stark sein musst weil niemand deine Schwäche aushält",
        "wenn du merkst dass du ersetzbar bist",
        "wenn du dich anstrengst aber es nicht gesehen wird",
        "wenn du weinst aber alleine damit bist",
    ],
    "toxische_muster": [
        "wenn jemand dich immer wieder zurückzieht und dann loslässt",
        "wenn Entschuldigungen nichts ändern",
        "wenn du weißt dass es falsch ist aber trotzdem bleibst",
        "wenn Hoffnung dich in einer schlechten Situation hält",
        "wenn jemand dich liebt aber trotzdem verletzt",
        "wenn du immer wieder verzeihst obwohl du es nicht solltest",
        "wenn jemand sagt er liebt dich aber es sich nicht so anfühlt",
        "wenn du Ausreden für jemandes Verhalten erfindest",
        "wenn du weißt wie es endet aber trotzdem anfängst",
        "wenn du dich für jemandes schlechtes Verhalten verantwortlich fühlst",
        "wenn du glückliche Momente festhalten willst weil du weißt sie vergehen",
        "wenn du immer wieder zurückgehst egal was passiert ist",
    ],
    "heilung_und_wahrheit": [
        "wenn du merkst dass du dich selbst vernachlässigt hast",
        "der Moment wo du aufhörst um Liebe zu betteln",
        "wenn du verstehst dass nicht alle bleiben sollen",
        "wenn Schmerz dich stärker macht als du wolltest",
        "wenn du lernst dass Einsamkeit besser ist als falsche Gesellschaft",
        "wenn du aufhörst zu erklären wer du bist",
        "wenn du merkst dass du ohne ihn funktionierst",
        "wenn du dir selbst gibst was du anderen gegeben hast",
        "wenn Loslassen sich wie Befreiung anfühlt",
        "wenn du aufhörst jemanden zu suchen der nicht gesucht werden will",
        "wenn du lernst nein zu sagen ohne dich zu erklären",
        "wenn du merkst dass du genug bist",
    ],
    "valentinstag_liebeskummer": [
        "wenn Valentinstag dich daran erinnert wer nicht mehr da ist",
        "wenn alle Herzen posten und du dich leerer fühlst als sonst",
        "wenn der 14. Februar nur ein Tag wie jeder andere sein soll aber es nicht ist",
        "wenn du siehst wie glücklich andere Paare heute sind",
        "wenn Valentinstag dich an das Versprechen erinnert das nie gehalten wurde",
    ],
    "silvester_neuanfang": [
        "wenn das neue Jahr beginnt aber der Schmerz vom letzten bleibt",
        "wenn du dir wünschst loszulassen aber die Uhr einfach nur weiterläuft",
        "wenn alle Vorsätze fassen und du dir nur wünschst wieder ganz zu sein",
        "wenn Silvester dich daran erinnert mit wem du es letztes Jahr verbracht hast",
        "wenn ein neues Jahr anfängt und du innerlich noch im alten feststeckst",
    ],
    "weihnachten_einsamkeit": [
        "wenn alle von Familie sprechen und du dich am einsamsten fühlst",
        "wenn Weihnachten zeigt wer wirklich für dich da ist",
        "wenn der leere Stuhl am Tisch lauter ist als jedes Lied",
        "wenn Feiertage dich daran erinnern was du verloren hast",
        "wenn alle Lichter brennen aber es in dir dunkel bleibt",
    ],
    "muttertag_vatertag": [
        "wenn dieser Tag an jemanden erinnert der nicht mehr anrufen kann",
        "wenn du siehst wie andere feiern und du nur schweigst",
        "wenn ein Feiertag zur schwersten Erinnerung des Jahres wird",
    ],
    "schulstart_neuanfang": [
        "wenn ein neuer Abschnitt beginnt aber du innerlich noch nicht bereit bist",
        "wenn alle über Neuanfänge sprechen und du dich noch am alten Ende festhältst",
        "wenn ein neues Kapitel beginnen soll aber du das letzte nicht abgeschlossen hast",
    ],
}

# Feiertage/Anlässe: (Monat, Tag) -> Kategorie, gilt für ±3 Tage um das Datum
SAISONALE_ANLAESSE = {
    (2, 14): "valentinstag_liebeskummer",
    (12, 24): "weihnachten_einsamkeit",
    (12, 25): "weihnachten_einsamkeit",
    (12, 26): "weihnachten_einsamkeit",
    (12, 31): "silvester_neuanfang",
    (1, 1): "silvester_neuanfang",
    (5, 12): "muttertag_vatertag",
    (6, 15): "muttertag_vatertag",
    (9, 1): "schulstart_neuanfang",
}

# Wochentag-Gewichtung: 0=Montag ... 6=Sonntag
WOCHENTAG_KATEGORIEN = {
    6: ["einsamkeit_und_overthinking", "unsichtbarkeit"],  # Sonntag – Vorabend-Melancholie
    0: ["heilung_und_wahrheit", "selbstverlust"],          # Montag – Neuanfang-Gedanken
}

HOOK_TYPEN = [
    "Kontrast-Hook: Zwei kurze Sätze die sich direkt widersprechen — Satz 1 zeigt was du für andere tust, Satz 2 zeigt was du dafür zurückbekommst. Maximal 4 Wörter pro Satz.",
    "Rollentausch-Hook: Du tust etwas für andere — niemand tut es für dich. Zwei Sätze, knallharter Bruch dazwischen. Keine Erklärung, nur der Fakt.",
    "Stille-Hook: Eine Handlung die jeder kennt, gefolgt vom Fehlen der erwarteten Reaktion. Struktur: 'Du X. Niemand Y zurück.'",
    "Realitäts-Ohrfeige: Ein Satz der eine Illusion zerstört, brutal direkt, ohne Vorwarnung. Maximal 5 Wörter.",
    "Wiederholungs-Hook: Drei kurze Parallelsätze die das gleiche Muster zeigen, dann ein vierter Satz der bricht und wehtut.",
]

CTAS = [
    "Die Person an die du jetzt denkst. Schick es ihr. 💔",
    "Schick das. Ohne Text. Sie weiß es.",
    "Wer kam dir gerade in den Kopf? 💔",
    "Schreib 💔 wenn du weißt für wen das ist.",
    "Schick das der Person die du vermisst aber nicht mehr schreibst.",
    "Einfach schicken. Kein Text nötig. 💔",
    "Die Person ohne die du einschläfst. Schick es ihr.",
    "Schreib 🖤 wenn dich das gerade trifft.",
]

FOLLOW_TRIGGER = [
    "Mach das Plus weg. 🖤",
    "Lass ein Follow da wenn dich das trifft. 🖤",
    "Ein Follow kostet nichts. 🖤",
    "Drück auf Folgen. Du weißt warum. 🖤",
    "Folge uns. Einmal drücken. 🖤",
    "Das Plus oben rechts. Drück drauf. 🖤",
    "Folge uns für mehr davon. 🖤",
    "Drück Folgen wenn dich das gerade trifft. 🖤",
]

def get_saisonale_kategorie(heute=None):
    """Prüft ob heute (±3 Tage) ein Anlass ist. Gibt Kategorie zurück oder None."""
    if heute is None:
        heute = date.today()
    for (monat, tag), kategorie in SAISONALE_ANLAESSE.items():
        try:
            anlass_datum = date(heute.year, monat, tag)
        except ValueError:
            continue
        differenz = abs((heute - anlass_datum).days)
        if differenz <= 3:
            return kategorie
    return None

def get_heutiges_thema():
    heute = date.today()
    wochentag = heute.weekday()

    # 1. Priorität: Saisonale Anlässe (30% Chance auch an Feiertagen normalen Content zu zeigen)
    saison_kategorie = get_saisonale_kategorie(heute)
    if saison_kategorie and saison_kategorie in THEMEN_KATEGORIEN and random.random() < 0.7:
        kategorie = saison_kategorie
        thema = random.choice(THEMEN_KATEGORIEN[kategorie])
        return kategorie, thema

    # 2. Priorität: Wochentag-Gewichtung (40% Chance bevorzugte Kategorie zu nutzen)
    if wochentag in WOCHENTAG_KATEGORIEN and random.random() < 0.4:
        kategorie = random.choice(WOCHENTAG_KATEGORIEN[wochentag])
        thema = random.choice(THEMEN_KATEGORIEN[kategorie])
        return kategorie, thema

    # 3. Standard: normale Kategorien (ohne saisonale, die kommen nur zu ihrer Zeit)
    standard_kategorien = [k for k in THEMEN_KATEGORIEN.keys() if k not in SAISONALE_ANLAESSE.values()]
    kategorie = random.choice(standard_kategorien)
    thema = random.choice(THEMEN_KATEGORIEN[kategorie])
    return kategorie, thema

def generate_text():
    client = anthropic.Anthropic()
    kategorie, thema = get_heutiges_thema()
    hook_typ = random.choice(HOOK_TYPEN)
    cta = random.choice(CTAS)
    follow_trigger = random.choice(FOLLOW_TRIGGER)
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""Du bist Kopfgewitter — der emotionalste deutsche TikTok-Account für Menschen die zu viel fühlen und zu viel denken.

Thema: "{thema}"

HOOK — ERSTE ZWEI SEKUNDEN ENTSCHEIDEN ALLES:
Stil: {hook_typ}

PFLICHT-STRUKTUR für den Hook (erste 1-2 Sätze):
- Satz 1: Was DU für andere tust (max. 4 Wörter)
- Satz 2: Was DU dafür zurückbekommst — meist: nichts (max. 4 Wörter)
- Der Kontrast muss in unter 2 Sekunden Lesezeit erfassbar sein
- Keine abstrakten Aussagen — nur konkrete, bildhafte Handlungen
- Test: Würde jemand beim ersten Lesen sofort nicken? Wenn nein, neu schreiben

VERBOTEN:
- Hooks die Nachdenken erfordern um den Sinn zu verstehen
- Mehr als 5 Wörter im ersten Satz
- Metaphern oder bildliche Sprache im Hook (erst ab Satz 3 erlaubt)
- "Das wusstest du..." / "Wusstest du dass..." / lange Einleitungen
- Jegliche Unterbrechung des emotionalen Flows in den ersten 10 Sekunden — kein CTA, kein Follow-Hinweis, keine Werbung direkt nach dem Hook

ERFOLGREICHE HOOK-BEISPIELE (nachgewiesen hohe Retention):
"Du hälst alle zusammen. Dich hält niemand."
"Du fehlst. Aber niemand sucht dich."
"Du gibst Ozean. Und bekommst Pfützen zurück."
"Du schreibst. Gelesen. Keine Antwort."
"3 Uhr nachts. Alle schlafen. Nur du nicht."
"Er liebt dich nicht. 💔"

STRUKTUR — GENAU IN DIESER REIHENFOLGE:
1. Hook (1-2 Sätze) — sofort der härteste Kontrast, null Kontext, maximal 2 Sekunden Lesezeit
2. Aufbau (3-4 Sätze) — konkrete Alltagsbilder die jeder kennt, Wunde vertiefen, ungebrochener emotionaler Flow
3. Wendepunkt (1 Satz) — die brutalste Wahrheit oder die Erkenntnis die wehtut
4. CTA: "{cta}"
5. Follow-Trigger: "{follow_trigger}"

POLARISIERUNGS-REGELN:
- Jeder Satz löst eine eigene Emotion aus
- Kein Satz darf austauschbar sein
- Beim zweiten Lesen trifft es noch härter
- Konkret schreiben — niemals abstrakt
- 1-2 Emojis erlaubt — nur 💔 oder 🖤, nie mehr
- Der emotionale Spannungsbogen von Hook bis Wendepunkt darf durch nichts unterbrochen werden

TECHNISCHE REGELN:
- 55-70 Wörter gesamt
- Max 6 Wörter pro Satz (Hook: max 4-5 Wörter)
- Nur "du/dich" — niemals "man"
- Jeder Satz eine eigene Zeile
- Kein Hashtag

Gib NUR den fertigen Text zurück."""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip()
    result = {"date": today, "kategorie": kategorie, "topic": thema, "text": text}
    with open(f"output/text_{today}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Text generiert | Kategorie: {kategorie} | Thema: {thema}")
    print(text)
    return result

if __name__ == "__main__":
    generate_text()
