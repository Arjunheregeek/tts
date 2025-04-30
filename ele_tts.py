# demo_elevenlabs_integration_fixed.py

import os
import asyncio
import wave
from pathlib import Path

import aiohttp
from loguru import logger

from pipecat.services.elevenlabs.tts import (
    ElevenLabsHttpTTSService,
    output_format_from_sample_rate,
)
from pipecat.frames.frames import (
    TTSStartedFrame,
    TTSAudioRawFrame,
    TTSStoppedFrame,
)

# Load your real ElevenLabs API key:
ELEVENLABS_API_KEY = "sk_87a1421ec4fb9580defe37ab740d4c5afd0c725478fbd3d7"
VOICE_ID            = "3gsg3cxXyFLcGIfNbM6C"
MODEL_ID            = "eleven_turbo_v2"
OUTPUT_WAV          = Path("output.wav")

async def run_demo(text: str):
    async with aiohttp.ClientSession() as session:
        tts = ElevenLabsHttpTTSService(
            api_key=ELEVENLABS_API_KEY,
            voice_id=VOICE_ID,
            aiohttp_session=session,
            model=MODEL_ID,
            sample_rate=24000,  # We'll use this for WAV header too
            params=ElevenLabsHttpTTSService.InputParams(
                stability=0.7,
                similarity_boost=0.8
            )
        )

        # Hack: manually set output_format from our SAMPLE_RATE
        SAMPLE_RATE = 24000
        tts._output_format = output_format_from_sample_rate(SAMPLE_RATE)

        pcm_chunks = []
        sample_rate = SAMPLE_RATE

        async for frame in tts.run_tts(text):
            if isinstance(frame, TTSStartedFrame):
                logger.info("TTS started")
            elif isinstance(frame, TTSAudioRawFrame):
                # Use the correct attribute for raw audio bytes
                pcm_chunks.append(frame.audio)
            elif isinstance(frame, TTSStoppedFrame):
                logger.info("TTS stopped")
                break
            # ignore None frames

        # Only write if we actually got audio
        if pcm_chunks:
            with wave.open(str(OUTPUT_WAV), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                for chunk in pcm_chunks:
                    wf.writeframes(chunk)
            logger.success(f"Wrote audio to {OUTPUT_WAV}")
        else:
            logger.error("No audio received—check your API key and network.")

if __name__ == "__main__":
    asyncio.run(run_demo("Zudu AI assistant introduces itself and learns about the user, Braem from Spice Blue, a contact center solution. Braem is interested in automating inbound calls with Zudu's AI voice technology. Zudu gathers Braem's email and offers to have their team follow up with more information."))
