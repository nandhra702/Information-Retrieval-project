import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import os
import pickle
from django.conf import settings

# Tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def load_pickle_safely(file_path):
    """Load pickle file if it exists and is not empty, else return empty dict."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}
    with open(file_path, "rb") as f:
        return pickle.load(f)


def process_file(file_path):
    """
    Process a single text file.
    Cleans tokens and stores them in tokens.pkl.
    """
    # Get file name (without .txt extension)
    file_name = os.path.basename(file_path)
    file_name = file_name[:-4]

    # 1. Read text
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. Tokenize + clean
    words = word_tokenize(text)
    tokens = []
    for w in words:
        w = w.lower().strip(string.punctuation)
        if w and w.isalpha() and w not in stop_words:
            tokens.append(lemmatizer.lemmatize(w))

    # Build absolute path for tokens.pkl
    tokens_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "tokens.pkl"
    )

    # 3. Load existing pickle (or empty dict)
    data = load_pickle_safely(tokens_path)

    # 4. Update with this file’s tokens
    data[file_name] = tokens

    # 5. Save back to pickle
    with open(tokens_path, "wb") as f:
        pickle.dump(data, f)

    print("✅ Tokens saved successfully!")
    return tokens


def simple_tokenize(text):
    """
    Tokenize a string into a list of cleaned tokens.
    Does NOT write to tokens.pkl.
    """
    words = word_tokenize(text)
    tokens = []
    for w in words:
        w = w.lower().strip(string.punctuation)
        if w and w.isalpha() and w not in stop_words:
            tokens.append(lemmatizer.lemmatize(w))
    return tokens
