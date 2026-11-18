
from io import BytesIO

from streamlit_mic_recorder import speech_to_text
from gtts import gTTS


def capture_voice_question(language):
    """
    Capture a farmer's voice and convert it into text.
    Supports English and Kannada.
    """

    speech_language = (
        "en-IN" if language == "English" else "kn-IN"
    )

    start_prompt = (
        "Start speaking" if language == "English"
        else "ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ"
    )

    stop_prompt = (
        "Stop recording" if language == "English"
        else "ರೆಕಾರ್ಡಿಂಗ್ ನಿಲ್ಲಿಸಿ"
    )

    question = speech_to_text(
        start_prompt=start_prompt,
        stop_prompt=stop_prompt,
        just_once=True,
        language=speech_language,
        key=f"krishimitra_voice_{language}"
    )

    return question


def generate_speech_audio(text, language):
    """
    Convert an answer into spoken audio.
    Supports English and Kannada.
    """

    speech_language = (
        "en" if language == "English" else "kn"
    )

    audio_buffer = BytesIO()

    tts = gTTS(
        text=text,
        lang=speech_language
    )

    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer
