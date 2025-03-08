from flask import Flask, request, render_template, jsonify, send_from_directory
import json
from app import app
from app.neural_search import neural_search, embedd_doc, cosine_similarities, neural_search_results
from app.tfidf import tf_document_setup, retrieve_matches, tf_get_results, tfidf_search_results
from app.boolean_search import load_documents as load_boolean_documents, document_setup as boolean_document_setup, retrieve_matches as boolean_retrieve_matches
from app.document_loader import LexDatabase
from app.chartgen import generate_chart

# Set up LexDatabase object
file_path = 'data/database.json'
db = LexDatabase(file_path)

documents = db.documents()
db.add_document_embeddings(embedd_doc(db.contents))  # Generates embeddings for the documents

generate_chart(db) # Generates the chart
# Load documents for all search types


# For the TF-IDF search, prepare the TF-IDF matrix and vectorizer
tf_matrix, tf_columns, tfv = tf_document_setup(db.contents)
#tf_matrix, tfv = tf_document_setup(documents)

# For Boolean search, prepare the Boolean matrix
# boolean_documents = load_boolean_documents(file_path)
boolean_td_matrix, boolean_t2i = boolean_document_setup(documents)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form.get('query', '').strip()
    search_type = request.form.get('search_type', 'neural') # Default to neural search

    if not user_query:
        return render_template('index.html', error="Please enter a search term.")
    
    results = []

    if search_type == 'neural':
        scores = cosine_similarities(db.embeddings, user_query)
        results = neural_search_results(scores, db.doc_dict) or []
        #results = neural_search(documents, user_query) or []
    elif search_type == 'tfidf':
        scores = retrieve_matches(user_query, tf_matrix, tfv)
        scores_and_titles = tf_get_results(scores, tf_columns)
        results = tfidf_search_results(scores_and_titles, db.doc_dict)
        #scores = retrieve_matches(user_query, tf_matrix, tfv)
        #results = tf_get_results(scores, documents)[:3]   or []
    elif search_type == 'boolean':
        # For boolean  search, use the retrieve_matches function from booleansearch.py
        results = boolean_retrieve_matches(user_query, boolean_td_matrix, boolean_t2i, documents)[:3]   or []

    

    print(f"Search Type: {search_type}, Query: {user_query}, Results: {results}")
    return render_template('index.html', results=results, query=user_query, search_type=search_type)

@app.errorhandler(500)
def internal_server_error(e):
    return send_from_directory('static/images', 'error_judge.jpg'), 500