from flask import Flask, request, render_template, jsonify, send_from_directory
import json
from app import app
from app.neural_search import neural_search, load_documents as load_neural_documents
from app.tfidf import tf_document_setup, retrieve_matches, tf_get_results, load_documents as load_tfidf_documents
from app.boolean_search import load_documents as load_boolean_documents, document_setup as boolean_document_setup, retrieve_matches as boolean_retrieve_matches

# Load documents for all search types
file_path = 'data/en_sample_database.json'
documents = load_neural_documents(file_path)

# For the TF-IDF search, prepare the TF-IDF matrix and vectorizer
tf_matrix, tfv = tf_document_setup(documents)

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
        results = neural_search(documents, user_query) or []
    elif search_type == 'tfidf':
        scores = retrieve_matches(user_query, tf_matrix, tfv)
        results = tf_get_results(scores, documents)[:3]   or []
    elif search_type == 'boolean':
        # For boolean  search, use the retrieve_matches function from booleansearch.py
        results = boolean_retrieve_matches(user_query, boolean_td_matrix, boolean_t2i, documents)[:3]   or []

    

    print(f"Search Type: {search_type}, Query: {user_query}, Results: {results}")
    return render_template('index.html', results=results, query=user_query, search_type=search_type)

@app.errorhandler(500)
def internal_server_error(e):
    return send_from_directory('static/images', 'error_judge.jpg'), 500