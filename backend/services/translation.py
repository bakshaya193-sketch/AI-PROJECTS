"""
Language detection and translation service.
Uses langdetect for detection and deep-translator for translation.
"""


def detect_language(text: str) -> str:
    """
    Detect language of text. Returns ISO 639-1 code (e.g. 'en', 'es').
    Defaults to 'en' for short or ambiguous text to avoid misdetection.
    """
    # Too short to reliably detect — default to English
    if len(text.strip()) < 20:
        return "en"

    try:
        from langdetect import detect, detect_langs
        # Get probabilities for all detected languages
        langs = detect_langs(text)

        if not langs:
            return "en"

        top = langs[0]

        # Only trust detection if confidence is high enough
        if top.prob < 0.85:
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
