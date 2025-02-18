from flask import render_template, request
from app import app
from app.TfIdf import vectorize_query, get_hits, rank, data_v, data


@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        query_v = vectorize_query(query)  
        hits = get_hits(query_v, data_v)  
        ranked_hits = rank(hits)  

        
        search_results = [
            {"doc_name": data["doc_name"][doc_id], "score": round(score, 3)}
            for score, doc_id in ranked_hits
        ]

    return render_template("index.html", query=query, results=search_results)