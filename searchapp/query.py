import os
import math
import json
import pickle
from collections import Counter
from django.conf import settings  # ✅ needed for BASE_DIR
from . import Dimensionality_reduction
from . import tokenizing  # must expose simple_tokenize()


def process_query_and_rank(query_string, top_k=5):
    """
    Process a query using ltc weighting and rank corpus docs using cosine similarity.
    Reads tokens.pkl, postings.pkl, and doc_vectors.json.
    Does NOT write to them.
    """

    # ----------------------------
    # 1. Load corpus stats
    # ----------------------------
    tokens_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "tokens.pkl"
    )
    postings_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "pickle_files", "postings.pkl"
    )
    docvec_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "doc_vectors.json"
    )

    with open(tokens_path, "rb") as f:
        documents = pickle.load(f)

    with open(postings_path, "rb") as f:
        postings = pickle.load(f)

    with open(docvec_path, "r") as f:  # ✅ json needs text mode
        doc_vectors = json.load(f)

    N = len(documents)  # total docs
    df_dict = {term: len(postings[term]) for term in postings}

    # ----------------------------
    # 2. Tokenize query
    # ----------------------------
    query_tokens = tokenizing.simple_tokenize(query_string)
    tf_raw = Counter(query_tokens)

    # ----------------------------
    # 3. Build ltc weights
    # ----------------------------
    query_vec = {}
    for term, tf in tf_raw.items():
        tf_weight = 1 + math.log(tf, 10)
        idf = math.log(N / df_dict[term], 10) if term in df_dict and df_dict[term] > 0 else 0.0
        query_vec[term] = tf_weight * idf

    # normalize
    norm = math.sqrt(sum(w**2 for w in query_vec.values()))
    if norm > 0:
        for term in query_vec:
            query_vec[term] /= norm

    # ----------------------------
    # 4. Cosine similarity with docs
    # ----------------------------
    scores = {}
    for docID, d_vec in doc_vectors.items():
        score = 0.0
        for term, q_w in query_vec.items():
            if term in d_vec:
                score += q_w * d_vec[term]
        if score > 0:
            scores[docID] = score

    # sort and pick top-k
    top_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    return query_vec, top_docs


# ----------------------------
# MAIN for testing
# ----------------------------
def main(string):
    query = string
    query_vec, top_docs = process_query_and_rank(query, top_k=5)

    print("\n🔎 Query Vector (normalized ltc):")
    for term, weight in query_vec.items():
        print(f"{term}: {weight:.4f}")

    print("\n📄 Top matching documents:")
    for docID, score in top_docs:
        print(f"Doc {docID}: {score:.4f}")

    # Position query
    query_vec_3d = Dimensionality_reduction.place_query(query_vec, top_docs)

    query_json = {
        "x": float(query_vec_3d[0]),
        "y": float(query_vec_3d[1]),
        "z": float(query_vec_3d[2]),
        "doc": "New_query",
    }

    # ✅ build query_point.json path dynamically
    query_point_path = os.path.join(
        settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "query_point.json"
    )
    with open(query_point_path, "w", encoding="utf-8") as f:
        json.dump(query_json, f, indent=2)

    


if __name__ == "__main__":
    main("test query")
