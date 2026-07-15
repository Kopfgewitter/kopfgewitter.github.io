import os, json, requests
from datetime import datetime
from pathlib import Path

ZERNIO_API_KEY = os.environ["ZERNIO_API_KEY"]
ZERNIO_TIKTOK_ACCOUNT_ID = os.environ["ZERNIO_TIKTOK_ACCOUNT_ID"]

KATEGORIE_HASHTAGS = {
    "einseitige_liebe":            "#liebeskummer #herzschmerz #zitate #wahreworte #gefühle",
    "verlust_und_loslassen":       "#liebeskummer #trennung #zitate #vermissen #herzschmerz",
    "modernes_dating":             "#liebeskummer #beziehung #zitate #herzschmerz #wahreworte",
    "selbstverlust":               "#gefühle #zitate #wahreworte #herzschmerz #sprüche",
    "einsamkeit_und_overthinking": "#gefühle #zitate #traurig #wahreworte #sprüche",
    "unsichtbarkeit":              "#gefühle #herzschmerz #zitate #traurig #wahreworte",
    "toxische_muster":             "#liebeskummer #beziehung #zitate #herzschmerz #trennung",
    "heilung_und_wahrheit":        "#wahreworte #zitate #gefühle #sprüche #herzschmerz",
}

def generate_caption(text_data):
    text = text_data["text"]
    kategorie = text_data.get("kategorie", "")
    hashtags = KATEGORIE_HASHTAGS.get(kategorie, "#liebeskummer #herzschmerz #zitate #gefühle #wahreworte")
    caption = f"{text}\n\n{hashtags}"
    return caption[:2200]

def post_to_tiktok(video_url, caption):
    print("📤 TikTok Upload über Zernio...")

    response = requests.post(
        "https://zernio.com/api/v1/posts",
        headers={
            "Authorization": f"Bearer {ZERNIO_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "content": caption,
            "mediaItems": [
                {"type": "video", "url": video_url}
            ],
            "platforms": [
                {
                    "platform": "tiktok",
                    "accountId": ZERNIO_TIKTOK_ACCOUNT_ID,
                    "platformSpecificData": {
                        "tiktokSettings": {
                            "privacy_level": "PUBLIC_TO_EVERYONE",
                            "allow_comment": True,
                            "allow_duet": True,
                            "allow_stitch": True,
                            "content_preview_confirmed": True,
                            "express_consent_given": True
                        }
                    }
                }
            ],
            "publishNow": True
        }
    )

    if response.status_code not in [200, 201]:
        raise Exception(f"Zernio TikTok Fehler {response.status_code}: {response.text}")

    result = response.json()
    print(f"🎉 Erfolgreich auf TikTok veröffentlicht! (ID: {result.get('post', {}).get('_id', 'N/A')})")
    return {"success": True, "post_id": result.get("post", {}).get("_id")}

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"output/text_{today}.json", encoding="utf-8") as f:
        data = json.load(f)
    caption = generate_caption(data)
    with open(f"output/result_instagram_{today}.json", encoding="utf-8") as f:
        ig_result = json.load(f)
    print("Hinweis: Für den Test brauchst du eine Cloudinary Video-URL")
