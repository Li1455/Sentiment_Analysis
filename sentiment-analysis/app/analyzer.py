import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.sia = SentimentIntensityAnalyzer()
        except LookupError:
            # Fallback if download failed or data missing
            import nltk
            nltk.download('vader_lexicon', quiet=True)
            self.sia = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> dict:
        """
        Analyzes the sentiment of the input text using NLTK's VADER.
        Raises TypeError if input is not a string.
        Raises ValueError if input is empty or whitespace-only.
        """
        # Basic validation
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")
        
        stripped_text = text.strip()
        if not stripped_text:
            raise ValueError("Input text cannot be empty or whitespace-only.")

        # VADER polarity analysis
        scores = self.sia.polarity_scores(text)
        compound = scores['compound']

        # Determine sentiment class based on compound score thresholds
        # Standard VADER thresholds:
        # positive: compound >= 0.05
        # negative: compound <= -0.05
        # neutral: otherwise
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Calculate a human-friendly confidence percentage
        # Since compound ranges from -1 to 1, we can compute a relative intensity
        # depending on the classified sentiment class.
        if sentiment == "Positive":
            confidence = compound  # 0.05 to 1.0
        elif sentiment == "Negative":
            confidence = abs(compound)  # 0.05 to 1.0
        else:
            # For neutral, we can express how close it is to absolute 0
            # relative to the 0.05 threshold.
            confidence = 1.0 - abs(compound) / 0.05  # 0.0 to 1.0

        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 4),
            "scores": {
                "positive": round(scores['pos'], 4),
                "negative": round(scores['neg'], 4),
                "neutral": round(scores['neu'], 4),
                "compound": round(compound, 4)
            }
        }
