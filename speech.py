import asyncio
import edge_tts
import os
from pygame import mixer
from voice_state import log, set_voice_state

async def _speak(text):
    communicate = edge_tts.Communicate(
        text,
        voice="de-DE-ConradNeural"
    )

    await communicate.save("jarvis.mp3")

    mixer.init()
    mixer.music.load("jarvis.mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        await asyncio.sleep(0.1)

    mixer.music.unload()
    os.remove("jarvis.mp3")

def sprechen(text):
    set_voice_state("speaking", "JARVIS ANTWORTET")
    log("Jarvis: " + text)
    try:
        asyncio.run(_speak(text))
    finally:
        set_voice_state("idle")