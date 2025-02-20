from flask import request, render_template
from app import app
from app.neural_search import neural_search
from app.document_loader import load_documents


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        
        # Load documents
        documents = load_documents('data/sample_database.json') 
        
        # Perform neural search
        results = neural_search(documents, query)

    return render_template("index.html", query=query, results=results)