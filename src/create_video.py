import os, json, subprocess, requests, random
from datetime import datetime
from pathlib import Path

PEXELS_API_KEY = os.environ["PEXELS_API_KEY"]
WATERMARK_TEXT = os.environ.get("WATERMARK_TEXT", "Kopfgewitter")

VIDEO_TERMS = [
    "woman crying emotional close up",
    "person walking alone rain",
    "couple breaking up emotional",
    "woman looking window sad",
    "man emotional breakdown crying",
    "person sitting alone night",
    "emotional woman portrait tears",
    "cinematic emotional people",
]

def download_background_video(output_path, duration):
    term = random.choice(VIDEO_TERMS)
    print(f"🎬 Suche Video: '{term}'")
    headers = {"Authorization": PEXELS_API_KEY}
    r = requests.get("https://api.pexels.com/videos/search", headers=headers,
        params={"query": term, "orientation": "portrait", "size": "medium", "per_page": 15})
    if r.status_code != 200:
        raise Exception(f"Pexels Fehler: {r.status_code}")
    videos = r.json().get("videos", [])
    if not videos:
        raise Exception("Keine Videos gefunden")
    suitable = [v for v in videos if v.get("duration", 0) >= max(duration, 15)]
    video = random.choice(suitable if suitable else videos)
    files = sorted(video["video_files"], key=lambda x: x.get("width", 0), reverse=True)
    video_url = files[0]["link"]
    print("⬇️ Lade Video herunter...")
    resp = requests.get(video_url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Hintergrundvideo: {output_path}")
    return output_path

def create_video(background_path, audio_path, subtitles_path, output_path, duration):
    print("🎞️ Erstelle Video mit FFmpeg...")
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", background_path, "-i", audio_path,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"eq=brightness=-0.05:contrast=1.1,"
        f"subtitles={subtitles_path}:force_style='FontName=Arial Black,FontSize=80,Bold=1,"
        f"PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=1,Outline=4,Shadow=2,"
        f"Alignment=2,MarginL=50,MarginR=50,MarginV=300',"
        f"drawtext=text='{WATERMARK_TEXT}':fontfile=/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf:"
