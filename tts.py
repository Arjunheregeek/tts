import requests
import json
import os
from playsound import playsound

# PlayHT API credentials (replace with your own)
USER_ID = ""
API_KEY = ""

# API endpoint
url = "https://api.play.ht/api/v2/tts"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "X-User-ID": USER_ID,
    "Content-Type": "application/json"
}

# Payload
payload = {
    "text": "Hello, this is a test of text-to-speech!",
    "voice": "s3://voice-cloning-zero-shot/df99adce-967f-11ee-b0ae-5b0203ec4b42/voice.mp3",  # Example voice
    "output_format": "mp3",
    "sample_rate": "24000"
}

# Make the API request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if request was successful
if response.status_code == 200:
    # Save the audio file
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio file saved as output.mp3")
    
    # Play the audio file
    playsound("output.mp3")
    print("Playing audio...")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Clean up
if os.path.exists("output.mp3"):
    os.remove("output.mp3")
    print("Cleaned up audio file")
