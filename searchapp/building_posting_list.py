import pickle
import json
import os
from collections import Counter
from django.conf import settings


def load_pickle_safely(file_path):
    """Load pickle file if it exists and is not empty, else return empty dict."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}
    with open(file_path, "rb") as f:
        return pickle.load(f)


def build_postings():
    """
    Update postings list only for new documents from tokens.pkl.
    - Each term gets a document frequency (df) and postings list [(docid, tf)].
    """

    # ----------------------------
    # Paths
    # ----------------------------
    tokens_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "tokens.pkl"
    )
    postings_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "postings.pkl"
    )
    postings_json_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "postings.json"
    )

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    documents = load_pickle_safely(tokens_path)   # tokens by doc
    postings = load_pickle_safely(postings_path)  # existing postings

    # ----------------------------
    # FIND ALREADY INDEXED DOCS
    # ----------------------------
    already_indexed_docs = {
        docid
        for term_data in postings.values()
        for docid, _ in term_data["postings"]
    }

    # ----------------------------
    # PROCESS ONLY NEW DOCS
    # ----------------------------
    new_docs = {docid: tokens for docid, tokens in documents.items()
                if docid not in already_indexed_docs}

    if not new_docs:
        print(" !! No new documents to index.")
        return

    for docid, tokens in new_docs.items():
        term_freqs = Counter(tokens)
        for term, tf in term_freqs.items():
            if term not in postings:
                postings[term] = {"df": 0, "postings": []}

            postings[term]["df"] += 1
            postings[term]["postings"].append((docid, tf))

    # ----------------------------
    # SAVE UPDATED POSTINGS
    # ----------------------------
    with open(postings_path, "wb") as f:
        pickle.dump(postings, f)

    with open(postings_json_path, "w", encoding="utf-8") as f:
        json.dump(postings, f, indent=2)

    print(f"Postings updated successfully! Indexed {len(new_docs)} new docs.")
