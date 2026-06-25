import os, subprocess, requests, random
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
    
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "eq=brightness=-0.05:contrast=1.1,"
        "subtitles=" + subtitles_path + ":force_style="
        "'FontName=Arial,FontSize=80,Bold=1,"
        "PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
        "BorderStyle=1,Outline=4,Shadow=2,"
        "Alignment=2,MarginL=50,MarginR=50,MarginV=500',"
        "drawtext=text='" + WATERMARK_TEXT + "':"
        "fontfile=/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf:"
        "fontsize=52:fontcolor=white@0.6:x=(w-text_w)/2:y=80:"
        "shadowcolor=black@0.5:shadowx=2:shadowy=2"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", background_path,
        "-i", audio_path,
        "-vf", vf,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-t", str(duration),
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-3000:])
        raise Exception("FFmpeg fehlgeschlagen")
    size = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"✅ Video: {output_path} ({size:.1f} MB)")
    return output_path

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    from generate_voice import get_audio_duration
    duration = get_audio_duration(f"output/voice_{today}.mp3")
    download_background_video(f"output/background_{today}.mp4", duration)
    create_video(
        f"output/background_{today}.mp4",
        f"output/voice_{today}.mp3",
        f"output/subtitles_{today}.ass",
        f"output/final_{today}.mp4",
        duration
    )
