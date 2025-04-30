# list_voices.py
import os, requests

API_KEY = "sk_87a1421ec4fb9580defe37ab740d4c5afd0c725478fbd3d7"
url = "https://api.elevenlabs.io/v1/voices"

resp = requests.get(url, headers={"xi-api-key": API_KEY})
resp.raise_for_status()
voices = resp.json()["voices"]

print("Available voices:")
for v in voices:
    print(f" • {v['name']} ➔ {v['voice_id']}")
