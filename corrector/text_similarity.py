"""
Text Similarity Module
Uses TF-IDF vectorization and cosine similarity to compare texts.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os


def _ensure_nltk_data():
    """Download required NLTK data if not present."""
    for resource in ["punkt", "punkt_tab", "stopwords"]:
        try:
            if resource == "stopwords":
                nltk.data.find("corpora/stopwords")
            else:
                nltk.download(resource, quiet=True)
        except LookupError:
            nltk.download(resource, quiet=True)


_ensure_nltk_data()


class TextSimilarity:
    """Provides text preprocessing and similarity comparison utilities."""

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = TfidfVectorizer()

    def preprocess(self, text):
        """Lowercase, remove punctuation, remove stopwords."""
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in self.stop_words and t.isalpha()]
        return " ".join(tokens)

    def cosine_sim(self, text1, text2):
        """Compute cosine similarity between two texts using TF-IDF."""
        t1 = self.preprocess(text1)
        t2 = self.preprocess(text2)

        if not t1.strip() or not t2.strip():
            return 0.0

        try:
            tfidf_matrix = self.vectorizer.fit_transform([t1, t2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
        except ValueError:
            return 0.0

    def keyword_match_score(self, text, keywords):
        """Calculate what fraction of keywords appear in the text."""
        if not keywords:
            return 0.0

        text_lower = text.lower()
        matched = sum(1 for kw in keywords if kw.lower() in text_lower)
        return matched / len(keywords)
