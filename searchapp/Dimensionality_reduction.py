from sklearn.decomposition import PCA
import numpy as np
import json
import os
from django.conf import settings


def load_json_safely(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def reduce_dimension():
    # Build absolute paths
    docvec_path  = os.path.join(settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "doc_vectors.json")
    docpoints_path = os.path.join(settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "doc_points.json")

    with open(docvec_path, "r", encoding="utf-8") as f:
        doc_vectors = json.load(f)

    # Convert dict into matrix
    doc_ids = list(doc_vectors.keys())
    terms = list({t for vec in doc_vectors.values() for t in vec})  # all terms
    term_index = {t: i for i, t in enumerate(terms)}

    X = np.zeros((len(doc_ids), len(terms)))
    for i, docid in enumerate(doc_ids):
        for term, val in doc_vectors[docid].items():
            X[i, term_index[term]] = val

    # Reduce to 3D
    pca = PCA(n_components=3)
    X_3d = pca.fit_transform(X)

    # Store results
    doc_points = []
    for i, docid in enumerate(doc_ids):
        x, y, z = X_3d[i]
        doc_points.append({"doc": docid, "x": float(x), "y": float(y), "z": float(z)})

    with open(docpoints_path, "w", encoding="utf-8") as f:
        json.dump(doc_points, f, indent=2)

    print("3D document points saved to doc_points.json")


def place_query(query_vec, top_docs):
    """
    Position query in 3D space near its top matching docs.
    Uses already reduced doc_points.json.
    """
    # Build absolute path
    docpoints_path = os.path.join(settings.BASE_DIR, "searchapp", "static", "searchapp", "json_files", "doc_points.json")

    with open(docpoints_path, "r", encoding="utf-8") as f:
        doc_points = {p["doc"]: p for p in json.load(f)}

    coords = []
    weights = []
    for docID, score in top_docs:
        if docID in doc_points:
            p = doc_points[docID]
            coords.append([p["x"], p["y"], p["z"]])
            weights.append(score)

    if not coords:
        return np.zeros(3)

    coords = np.array(coords)
    weights = np.array(weights)
    weights = weights / weights.sum()  # normalize

    # Weighted centroid
    query_3d = np.average(coords, axis=0, weights=weights)
    return query_3d
