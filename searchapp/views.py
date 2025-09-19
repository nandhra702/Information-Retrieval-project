from django.shortcuts import render
from django.http import JsonResponse
from . import query   # your query.py

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