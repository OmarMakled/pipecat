import asyncio
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from pipecat.frames.frames import EndFrame, TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.local.audio import LocalAudioTransport
from pipecat.services.deepgram import DeepgramTTSService

load_dotenv(override=True)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")


async def main():
    transport = LocalAudioTransport(TransportParams(audio_out_enabled=True))

    tts_cartesia = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="79a125e8-cd45-4c13-8a67-188112f4dd22",
    )

    tts_deepgram = DeepgramTTSService(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        voice="aura-helios-en",
        sample_rate=24000
    )

    pipeline = Pipeline([tts_cartesia, tts_deepgram, transport.output()])

    task = PipelineTask(pipeline)

    async def say_something():
        await task.queue_frames([TTSSpeakFrame("Hello this is me, how is it going!"), EndFrame()])

    runner = PipelineRunner()

    await asyncio.gather(runner.run(task), say_something())


if __name__ == "__main__":
    asyncio.run(main())