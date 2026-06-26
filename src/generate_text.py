import anthropic, json, random
from datetime import datetime

TOPICS = [
    "jemanden verlieren der dich als selbstverständlich sah",
    "stilles Loslassen nach zu viel Schmerz",
    "Menschen die erst wertschätzen wenn es zu spät ist",
    "das Gefühl unsichtbar zu sein obwohl man alles gibt",
    "Overthinking und nicht abschalten können",
    "wenn man sich für jemanden verändert der es nicht verdient",
    "der Moment wo man aufhört zu kämpfen",
    "wenn Liebe einseitig wird",
    "sich selbst verlieren um jemand anderen glücklich zu machen",
    "die Einsamkeit mitten unter Menschen",
    "wenn du merkst dass du nicht mehr wichtig bist",
    "der Schmerz den niemand sieht",
    "wenn Schweigen mehr sagt als Worte",
    "Menschen die bleiben wenn es schwer wird",
    "das Gefühl morgens aufzuwachen und nichts zu fühlen",
]

HOOK_TYPEN = [
    "Direkt ins Gefühl — keine Ankündigung, sofort der schmerzhafte Moment",
    "Eine Situation beschreiben die jeder kennt aber niemand ausspricht",
    "Eine brutale Wahrheit die wehtut aber befreit",
    "Ein Satz der so präzise trifft dass man aufhört zu scrollen",
]

def generate_text():
    client = anthropic.Anthropic()
    topic = random.choice(TOPICS)
    hook_typ = random.choice(HOOK_TYPEN)
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""Du bist Kopfgewitter — ein emotionaler deutscher TikTok-Account der Menschen trifft die zu viel fühlen und zu viel denken.

Schreibe einen kurzen viralen TikTok-Text zum Thema: "{topic}"

HOOK-REGEL (die ersten 2 Sätze entscheiden alles):
Hook-Stil: {hook_typ}
NIEMALS mit "Das wusstest du..." oder "Wusstest du dass..." beginnen.
Der erste Satz muss so treffen dass man nicht weiterscrollen kann.

STRUKTUR:
1. Hook (2 Sätze) — sofort mitten ins Gefühl
2. Aufbau (3-4 Sätze) — kurz vertiefen, ein starkes Bild erzeugen
3. Ein Abschlusssatz der hängen bleibt
4. Ein einziger CTA — entweder Share-Trigger ODER Kommentar-Trigger

REGELN:
- Maximal 60-70 Wörter (20-25 Sekunden)
- Kurze kraftvolle Sätze (max 6 Wörter pro Satz)
- Immer "du/dich" — direkte Ansprache
- Jeder Satz eine eigene Zeile
- Kein Hashtag im Text
- Kein "Folge Kopfgewitter"
- Weniger ist mehr — jedes Wort muss sitzen

Gib NUR den fertigen Text zurück, nichts anderes."""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip()
    result = {"date": today, "topic": topic, "text": text}
    with open(f"output/text_{today}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Text generiert | Thema: {topic}")
    print(text)
    return result

if __name__ == "__main__":
    generate_text()
