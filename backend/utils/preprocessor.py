"""
Text preprocessing utilities for toxicity detection.
Handles cleaning, tokenization, stopword removal, stemming.
"""
import re
import string
import nltk

# Download required NLTK data (first-time only)
for pkg in ["stopwords", "punkt", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{pkg}" if pkg != "punkt" else f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Full preprocessing pipeline for a comment."""
    if not text or not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Remove special characters & digits
    text = re.sub(r"[^a-z\s]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    """Tokenize cleaned text."""
    return word_tokenize(text)


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def stem_tokens(tokens: list[str]) -> list[str]:
    return [stemmer.stem(t) for t in tokens]


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    return [lemmatizer.lemmatize(t) for t in tokens]


def preprocess(text: str, use_stemming: bool = False) -> str:
    """End-to-end preprocessing — returns a single cleaned string."""
    cleaned = clean_text(text)
    tokens  = tokenize(cleaned)
    tokens  = remove_stopwords(tokens)
    tokens  = lemmatize_tokens(tokens)
    if use_stemming:
        tokens = stem_tokens(tokens)
    return " ".join(tokens)
