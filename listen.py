import speech_recognition as sr
from voice_state import log, set_voice_state

recognizer = sr.Recognizer()

def zuhoeren(wake_only=False):
    """Hört entweder im aktiven Modus oder unsichtbar auf das Wake-Word."""
    standby_message = "STANDBY // SAGE JARVIS"
    if wake_only:
        set_voice_state("idle", standby_message)
    else:
        set_voice_state("listening", "ICH HÖRE ZU")
    try:
        with sr.Microphone() as source:
            log("Mikrofon aktiv – ich höre zu...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio, language="de-DE")
        log("Du: " + text)
        if wake_only:
            set_voice_state("idle", standby_message)
        else:
            set_voice_state("thinking", "ANALYSIERE DEINE ANFRAGE")
        return text.lower()

    except sr.UnknownValueError:
        set_voice_state("idle", standby_message if wake_only else "")
        return ""

    except Exception as e:
        log(e)
        set_voice_state("idle", standby_message if wake_only else "")
        return ""
        
if __name__ == "__main__":
    zuhoeren()
