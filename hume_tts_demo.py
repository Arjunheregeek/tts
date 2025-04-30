from pipecat.processors.frame_processor import FrameProcessor
from pipecat.frames.frames import TTSTextFrame, AudioRawFrame, EndFrame
from pipecat.services.hume.tts import HumeTTSService
from pipecat.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask
from pipecat.pipeline.runner import PipelineRunner
import wave
import asyncio

class TextGenerator(FrameProcessor):
    def __init__(self, texts):
        super().__init__()
        self.texts = texts

    async def process(self, frame):
        for text in self.texts:
            yield TTSTextFrame(text)
        yield EndFrame()

class AudioSaver(FrameProcessor):
    def __init__(self, filename, sample_rate=16000, channels=1, sample_width=2):
        super().__init__()
        self.filename = filename
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width
        self.audio_data = b""

    async def process(self, frame):
        if isinstance(frame, AudioRawFrame):
            self.audio_data += frame.audio
        elif isinstance(frame, EndFrame):
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.sample_width)
                wf.setframerate(self.sample_rate)
                wf.writeframes(self.audio_data)

async def main():
    api_key = "your_hume_api_key"  # Replace with your actual Hume API key
    voice_description = "A friendly and expressive voice"
    sample_texts = [
        "Hello, this is a test of Hume TTS with Pipecat.",
        "How are you today? I hope you're doing great!"
    ]

    text_gen = TextGenerator(sample_texts)
    tts = HumeTTSService(api_key, voice_description)
    audio_saver = AudioSaver("output.wav")

    pipeline = Pipeline([text_gen, tts, audio_saver])
    task = PipelineTask(pipeline)
    runner = PipelineRunner()
    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())