# demo_playht_integration.py

import os
import asyncio
import wave
from pathlib import Path

import aiohttp
from loguru import logger

from pipecat.services.elevenlabs.tts import output_format_from_sample_rate
from pipecat.services.playht.tts import PlayHTHttpTTSService  # adjust import path
from pipecat.frames.frames import (
    TTSStartedFrame,
    TTSAudioRawFrame,
    TTSStoppedFrame,
)

# Configure your Play.ht credentials and voice
PLAYHT_API_KEY = os.getenv("PLAYHT_API_KEY", "ak-d59ad68203ac4e75ba9f61eb0208789c")
PLAYHT_USER_ID = os.getenv("PLAYHT_USER_ID", "IMDBa26u92UeN8BKEw3J33LJk4R2")
VOICE_URL      = "s3://voice-cloning-zero-shot/53f08752-037b-4b9a-ae62-a3935aa60714/original/manifest.json"  # e.g. a voice identifier URL or ID

# Output settings
SAMPLE_RATE = 24000  # desired sample rate
OUTPUT_WAV = Path("output_playht.wav")

async def run_playht_demo(text: str):
    async with aiohttp.ClientSession() as session:
        tts = PlayHTHttpTTSService(
            api_key=PLAYHT_API_KEY,
            user_id=PLAYHT_USER_ID,
            voice_url=VOICE_URL,
            sample_rate=SAMPLE_RATE,
            protocol="http",
        )

        pcm_chunks = []

        async for frame in tts.run_tts(text):
            if isinstance(frame, TTSStartedFrame):
                logger.info("PlayHT TTS started")
            elif isinstance(frame, TTSAudioRawFrame):
                pcm_chunks.append(frame.audio)
            elif isinstance(frame, TTSStoppedFrame):
                logger.info("PlayHT TTS stopped")
                break
            # ignore None frames

        if pcm_chunks:
            with wave.open(str(OUTPUT_WAV), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                for chunk in pcm_chunks:
                    wf.writeframes(chunk)
            logger.success(f"Wrote PlayHT audio to {OUTPUT_WAV}")
        else:
            logger.error("No PlayHT audio received — check your API key, user ID, and network.")

if __name__ == "__main__":
    text_to_speak = (
        "Hello from PlayHT integration demo via Pipecat!"
    )
    asyncio.run(run_playht_demo(text_to_speak))
