"""
Dataset Preprocessing Script
─────────────────────────────
Preprocesses the Jigsaw Toxic Comment Classification dataset.

Usage:
    python scripts/preprocess_data.py

Input:  ml/data/train.csv  (download from Kaggle)
Output: ml/data/processed_train.csv
"""

import os
import sys
import re
import string
import pandas as pd
import numpy as np

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

print("=" * 60)
print("  Toxicity Dataset Preprocessor")
print("=" * 60)


def download_nltk_resources():
    """Download required NLTK resources."""
    import nltk
    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
    for r in resources:
        nltk.download(r, quiet=True)


def clean_text(text):
    """Full text preprocessing pipeline."""
    if not isinstance(text, str):
        return ''

    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    # Keep negation words
    negation = {'no', 'not', 'nor', 'never', 'neither', 'none', 'nobody', 'nothing'}
    stop_words -= negation

    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', ' ', text)
    # Remove HTML
    text = re.sub(r'<.*?>', ' ', text)
    # Remove non-alpha
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize, remove stopwords, lemmatize
    try:
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(t) for t in tokens
                  if t not in stop_words and len(t) > 2]
    except Exception:
        tokens = [t for t in text.split() if len(t) > 2]

    return ' '.join(tokens)


def create_synthetic_dataset(n_samples=5000):
    """
    Create a synthetic dataset for demo purposes
    when the Kaggle dataset is not available.
    """
    print("\n⚠️  Creating synthetic dataset for demonstration...")

    toxic_templates = [
        "You are such a stupid {noun}, nobody likes you",
        "I hate you so much, you {adj} piece of trash",
        "Kill yourself you worthless {noun}",
        "You are the ugliest {noun} I have ever seen",
        "Shut up you dumb {noun}, your opinion is garbage",
        "You are a complete moron and {adj} idiot",
        "I will hurt you if you don't stop {verb}",
        "Everyone hates you because you are so {adj}",
        "Get lost you pathetic excuse for a {noun}",
        "You disgust me with your {adj} attitude",
    ]

    clean_templates = [
        "I think this is a great idea worth exploring",
        "Could you please help me understand this better?",
        "I respectfully disagree with your perspective",
        "Thank you for sharing your thoughts on this",
        "I appreciate your contribution to the discussion",
        "This is an interesting point, let me think about it",
        "I see your viewpoint, though I have a different opinion",
        "Great work on this project, well done!",
        "Can we discuss this topic more constructively?",
        "I enjoy learning from different perspectives",
    ]

    nouns = ['person', 'human', 'individual', 'creature', 'thing']
    adjs = ['terrible', 'horrible', 'awful', 'worthless', 'pathetic']
    verbs = ['talking', 'posting', 'writing', 'commenting', 'existing']

    import random
    random.seed(42)

    texts, labels = [], []

    for _ in range(n_samples // 2):
        template = random.choice(toxic_templates)
        text = template.format(
            noun=random.choice(nouns),
            adj=random.choice(adjs),
            verb=random.choice(verbs)
        )
        texts.append(text)
        labels.append(1)

    for _ in range(n_samples // 2):
        texts.append(random.choice(clean_templates))
        labels.append(0)

    df = pd.DataFrame({'comment_text': texts, 'toxic': labels})
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def main():
    download_nltk_resources()

    input_path = os.path.join(DATA_DIR, 'train.csv')
    output_path = os.path.join(DATA_DIR, 'processed_train.csv')

    os.makedirs(DATA_DIR, exist_ok=True)

    # Load or create dataset
    if os.path.exists(input_path):
        print(f"\n📂 Loading dataset from: {input_path}")
        df = pd.read_csv(input_path)
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")

        # Jigsaw dataset format
        text_col = 'comment_text'
        label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

        if text_col not in df.columns:
            print(f"❌ Expected column '{text_col}' not found. Columns: {list(df.columns)}")
            sys.exit(1)

        # Use first 50k samples for speed
        df = df.head(50000)

    else:
        print(f"\n⚠️  Dataset not found at: {input_path}")
        print("   Download from: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge")
        df = create_synthetic_dataset(5000)

    print(f"\n🔄 Preprocessing text ({len(df)} samples)...")

    # Clean text
    df['cleaned_text'] = df['comment_text'].apply(clean_text)

    # Remove empty cleaned texts
    df = df[df['cleaned_text'].str.len() > 5].reset_index(drop=True)

    # Binary toxic label (any category = toxic)
    label_cols_present = [c for c in ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'] if c in df.columns]
    if label_cols_present:
        df['is_toxic'] = (df[label_cols_present].sum(axis=1) > 0).astype(int)
    else:
        df['is_toxic'] = df.get('toxic', 0)

    print(f"\n📊 Class Distribution:")
    toxic_count = df['is_toxic'].sum()
    clean_count = len(df) - toxic_count
    print(f"   Toxic:     {toxic_count:,} ({toxic_count/len(df)*100:.1f}%)")
    print(f"   Non-toxic: {clean_count:,} ({clean_count/len(df)*100:.1f}%)")

    # Save processed data
    cols_to_save = ['comment_text', 'cleaned_text', 'is_toxic'] + label_cols_present
    cols_to_save = [c for c in cols_to_save if c in df.columns]
    df[cols_to_save].to_csv(output_path, index=False)

    print(f"\n✅ Preprocessed data saved to: {output_path}")
    print(f"   Final shape: {df.shape}")
    print("\n🎯 Next step: Run python scripts/train_model.py")


if __name__ == '__main__':
    main()
