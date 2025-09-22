import pickle
import json
import math
import os
from django.conf import settings


def load_json_safely(file_path):
    """Load JSON file if it exists and is not empty, else return empty dict."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_doc_vectors():
    """
    Build/update document vectors using lnc weighting:
      - l: log term frequency (1 + log10(tf))
      - n: no IDF for documents
      - c: cosine normalization
    Only new documents are processed.
    """

    # ----------------------------
    # Step 1: Load postings
    # ----------------------------
    postings_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "postings.pkl"
    )
    with open(postings_path, "rb") as f:
        postings = pickle.load(f)

    # ----------------------------
    # Step 2: Load existing vectors
    # ----------------------------
    docvec_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "doc_vectors.json"
    )
    doc_vectors = load_json_safely(docvec_path)

    already_indexed_docs = set(doc_vectors.keys())

    # ----------------------------
    # Step 3: Collect term freqs for only new docs
    # ----------------------------
    doc_termfreqs = {}
    for term, data in postings.items():
        for docid, tf in data["postings"]:
            if docid in already_indexed_docs:
                continue  # skip already processed docs
            if docid not in doc_termfreqs:
                doc_termfreqs[docid] = {}
            doc_termfreqs[docid][term] = tf

    if not doc_termfreqs:
        print("No new documents to normalize.")
        return

    # ----------------------------
    # Step 4: Apply log scaling + cosine normalization
    # ----------------------------
    for docid, termfreqs in doc_termfreqs.items():
        weights = {term: 1 + math.log10(tf) for term, tf in termfreqs.items()}
        length = math.sqrt(sum(w**2 for w in weights.values()))
        normalized = {term: w/length for term, w in weights.items()}
        doc_vectors[docid] = normalized

    # ----------------------------
    # Step 5: Save updated vectors
    # ----------------------------
    with open(docvec_path, "w", encoding="utf-8") as f:
        json.dump(doc_vectors, f, indent=2)

    print(f" Document vectors updated! Normalized {len(doc_termfreqs)} new docs.")
