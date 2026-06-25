import json, re
from datetime import datetime

def text_to_subtitle_chunks(text, total_duration):
    clean_text = re.sub(r'[👉💔❤️🫀]', '', text)
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    all_words = []
    for line in lines:
        all_words.extend(line.split())
    if not all_words:
        return []
    chunks = []
    i = 0
    while i < len(all_words):
        chunks.append(' '.join(all_words[i:i+2]))
        i += 2
    time_per_chunk = total_duration / len(chunks)
    result = []
    for idx, chunk in enumerate(chunks):
        start = idx * time_per_chunk
        end = start + time_per_chunk * 0.9
        words = chunk.split()
        result.append({"index": idx, "start": round(start, 3), "end": round(end, 3),
            "text": chunk, "highlighted": words[-1] if words else ""})
    return result

def generate_ass_subtitles(chunks, output_path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,78,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,5,80,80,600,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def to_time(s):
        h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
        return f"{h}:{m:02d}:{sec:05.2f}"
    
    events = []
    for chunk in chunks:
        start = to_time(chunk["start"]); end = to_time(chunk["end"])
        words = chunk["text"].split(); highlighted = chunk["highlighted"]
        normal = ' '.join(w for w in words if w != highlighted)
        if normal:
            line = f"Dialogue: 0,{start},{end},Default,,0,0,0,,{normal} {{\\c&H1C1CFF&\\3c&H1C1CFF&}}{highlighted}{{\\c&HFFFFFF&\\3c&H000000&}}"
        else:
            line = f"Dialogue: 0,{start},{end},Default,,0,0,0,,{{\\c&H1C1CFF&\\3c&H1C1CFF&}}{highlighted}{{\\c&HFFFFFF&\\3c&H000000&}}"
        events.append(line)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + '\n'.join(events))
    print(f"✅ Untertitel: {output_path} ({len(chunks)} Chunks)")
    return output_path

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"output/text_{today}.json", encoding="utf-8") as f:
        data = json.load(f)
    chunks = text_to_subtitle_chunks(data["text"], 50.0)
    generate_ass_subtitles(chunks, f"output/subtitles_{today}.ass")
