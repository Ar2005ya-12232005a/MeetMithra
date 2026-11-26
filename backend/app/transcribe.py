from pathlib import Path

from groq import Groq

from .config import settings

STT_MODEL = "whisper-large-v3-turbo"
# A short Roman-script Hinglish prompt nudges Whisper to write Hinglish in English letters.
HINGLISH_HINT = "Namaste, aaj ki meeting budget aur campaign ke baare mein hai. Theek hai, final karte hain."
MAX_MB = 24  # Groq's free upload limit is about 25 MB


def transcribe(audio_path: str) -> list[dict]:
    """Audio file -> [{start_sec, end_sec, text}]."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    size_mb = path.stat().st_size / 1_000_000
    if size_mb > MAX_MB:
        raise ValueError(f"Audio is {size_mb:.0f} MB, over the {MAX_MB} MB limit. Use a shorter clip.")

    client = Groq(api_key=settings.groq_api_key or None)
    resp = client.audio.transcriptions.create(
        file=(path.name, path.read_bytes()),
        model=STT_MODEL,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=HINGLISH_HINT,
        temperature=0,
    )

    raw = resp.segments if hasattr(resp, "segments") else resp["segments"]
    segments = []
    for s in raw:
        get = (lambda k: s[k]) if isinstance(s, dict) else (lambda k: getattr(s, k))
        text = get("text").strip()
        if text:
            segments.append({"start_sec": float(get("start")), "end_sec": float(get("end")), "text": text})
    return segments