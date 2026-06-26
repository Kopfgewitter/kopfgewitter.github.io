import os, json, requests, subprocess, base64
from datetime import datetime
from pathlib import Path

ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "onwK4e9ZLuTAKqWW03F9")

def generate_voice(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.30,
            "similarity_boost": 0.85,
            "style": 0.75,
            "use_speaker_boost": True
        }
    }
    print("🎙️ Generiere Voiceover mit Timestamps...")
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        raise Exception(f"ElevenLabs Fehler {r.status_code}: {r.text}")

    response_data = r.json()

    # Audio speichern
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    audio_bytes = base64.b64decode(response_data["audio_base64"])
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    print(f"✅ Voiceover: {output_path}")

    # Timestamps verarbeiten — Satz-Timestamps berechnen
    alignment = response_data.get("alignment", {})
    chars = alignment.get("characters", [])
    char_times = alignment.get("character_start_times_seconds", [])

    # Text in Sätze aufteilen
    sentences = [s.strip() for s in text.split("\n") if s.strip()]
    sentence_timestamps = []

    if chars and char_times:
        full_text = "".join(chars)
        search_start = 0
        for sentence in sentences:
            idx = full_text.find(sentence, search_start)
            if idx != -1 and idx < len(char_times):
                start_time = char_times[idx]
                sentence_timestamps.append({
                    "text": sentence,
                    "start": round(start_time, 3)
                })
                search_start = idx + len(sentence)
            else:
                sentence_timestamps.append({
                    "text": sentence,
                    "start": None
                })

    # Timestamps speichern
    timestamps_path = output_path.replace(".mp3", "_timestamps.json")
    with open(timestamps_path, "w", encoding="utf-8") as f:
        json.dump(sentence_timestamps, f, ensure_ascii=False, indent=2)
    print(f"✅ Timestamps: {timestamps_path}")

    return output_path

def get_audio_duration(audio_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"output/text_{today}.json", encoding="utf-8") as f:
        data = json.load(f)
    generate_voice(data["text"], f"output/voice_{today}.mp3")
