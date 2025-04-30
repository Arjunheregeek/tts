import base64
import requests
from pipecat.processors.frame_processor import FrameProcessor  # Updated import
from pipecat.frames.frames import TTSTextFrame, AudioRawFrame, EndFrame  # Already updated

class HumeTTSService(FrameProcessor):  # Updated base class
    def __init__(self, api_key, voice_description="A friendly and expressive voice"):
        super().__init__()
        self.api_key = "WxWH28kegyxp3h04RDAGKyFolCNbGMvTtpbxR88wsRKoD9if"
        self.voice_description = voice_description

    async def process(self, frame):
        if isinstance(frame, TTSTextFrame):
            text = frame.text
            audio_bytes = self._generate_speech(text)
            return AudioRawFrame(audio_bytes)
        return frame

    def _generate_speech(self, text):
        url = "https://api.hume.ai/v0/tts/synthesize"  # Verify with Hume's docs
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice": {
                "description": self.voice_description
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        audio_base64 = data["audio"]  # Adjust key based on actual API response
        audio_bytes = base64.b64decode(audio_base64)
        return audio_bytes