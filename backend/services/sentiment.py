"""
Sentiment analysis service using TextBlob.
Returns positive / neutral / negative with a polarity score.
"""


def _ensure_nltk_data():
    """Download required NLTK data on first run."""
    import nltk
    for resource in ["punkt", "averaged_perceptron_tagger", "brown"]:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text.
    Returns dict with: sentiment, score, needs_escalation
    """
    try:
        _ensure_nltk_data()
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1.0 to 1.0

        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": round(polarity, 3),
            "needs_escalation": polarity < -0.5,
        }
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"sentiment": "neutral", "score": 0.0, "needs_escalation": False}


SENTIMENT_EMOJI = {
    "positive": "😊",
    "neutral": "😐",
    "negative": "😔",
}
