from django.shortcuts import render
from django.http import JsonResponse, Http404, FileResponse
from django.conf import settings
import os
from . import query  # your query.py
def open_document(request, filename):
    """
    Serve a .txt document from CORPUS_DIR if it exists.
    Automatically appends .txt if missing, and removes trailing slash.
    """
    # Remove any trailing slash
    filename = filename.rstrip("/")

    # Add .txt if missing
    if not filename.endswith(".txt"):
        filename += ".txt"

    # Build the absolute path
    corpus_dir = os.path.join(settings.BASE_DIR, "searchapp", "CORPUS")
    filepath = os.path.join(corpus_dir, filename)

    # Check if file exists
    if not os.path.exists(filepath):
        raise Http404(f"Document '{filename}' not found at {filepath}.")

    # Serve the file
    return FileResponse(open(filepath, "rb"), as_attachment=False, content_type="text/plain")

def search_view(request):
    query_string = request.GET.get("query", "").strip()
    top_docs = []

    if query_string:
        # Run your ranking function
        query_vec, top_docs = query.process_query_and_rank(query_string, top_k=5)

        # Also run the part that generates query_point.json
        query.main(query_string)

    # If it's an AJAX request, return JSON
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"results": top_docs})

    # Otherwise render the page normally
    return render(request, "searchapp/home.html", {
        "results": top_docs,
        "query": query_string,
    })


def home(request):
    return render(request, "searchapp/home.html")