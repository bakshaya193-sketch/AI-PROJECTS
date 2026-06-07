"""
Language detection and translation service.
Uses langdetect for detection and deep-translator for translation.
"""


def detect_language(text: str) -> str:
    """
    Detect language of text. Returns ISO 639-1 code (e.g. 'en', 'es').
    Biased toward English because short phrases are very easy to misdetect
    (e.g. langdetect reading "will i get a refund?" as Welsh).
    """
    cleaned = text.strip()

    # Short text is unreliable to detect — default to English
    if len(cleaned) < 30:
        return "en"

    try:
        from langdetect import detect_langs, DetectorFactory
        DetectorFactory.seed = 0  # make detection deterministic

        langs = detect_langs(cleaned)
        if not langs:
            return "en"

        top = langs[0]

        # Require high confidence before switching away from English
        if top.prob < 0.90:
            return "en"

        return str(top.lang)

    except Exception:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text from source_lang to English."""
    if source_lang == "en":
        return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate text from English back to the target language."""
    if target_lang == "en":
        return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text


LANGUAGE_NAMES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "zh": "Chinese", "ja": "Japanese",
    "ko": "Korean", "ar": "Arabic", "hi": "Hindi", "ru": "Russian",
}


def get_language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, code.upper())
