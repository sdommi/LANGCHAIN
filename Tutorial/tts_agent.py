#!/usr/bin/env rye run python

import time
import asyncio
import os

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv

load_dotenv()

# gets OPENAI_API_KEY from your environment variables

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in .env")

openai = AsyncOpenAI(api_key=api_key)


async def main() -> None:
    start_time = time.time()

    async with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        response_format="pcm",  # similar to WAV, but without a header chunk at the start.
        input="""I see skies of blue and clouds of white
                The bright blessed days, the dark sacred nights
                And I think to myself What a wonderful world
                hey divya you are looks like lazy and try to be active and act as super aggresive a
                nd try to be active and act as super aggressive and try to be active and act as super aggressive poushya is smart and beatiful and vihaan better than everyone
                ofcourse he is smart but he is not listening to his parents and he is not doing 
                his work properly and he is not doing his work properly """ ,
    ) as response:
    
        print(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms")
        await LocalAudioPlayer().play(response)
        print(f"Time to play: {int((time.time() - start_time) * 1000)}ms")


if __name__ == "__main__":
    asyncio.run(main())