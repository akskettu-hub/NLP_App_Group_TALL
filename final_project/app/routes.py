from flask import Flask, request, render_template, jsonify
import json
from app import app
from app.neural_search import neural_search, load_documents as load_neural_documents
from app.tfidf import tf_document_setup, retrieve_matches, tf_get_results, load_documents as load_tfidf_documents


file_path = 'data/en_sample_database.json'
documents = load_neural_documents(file_path)

# For the TF-IDF search, prepare the TF-IDF matrix and vectorizer
tf_matrix, tfv = tf_document_setup(documents)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form.get('query', '')
    search_type = request.form.get('search_type', 'neural') # neural as default search type
    if not user_query:
        return render_template('index.html', error="Please enter a search term.")
    if search_type == 'neural':
        # Neural search expects an English query
        results = neural_search(documents, user_query)
    elif search_type == 'tfidf':
        # TF-IDF search: compute similarity scores then convert to a JSON-like structure
        scores = retrieve_matches(user_query, tf_matrix, tfv)
        results = tf_get_results(scores, documents)
        '''
    elif search_type == 'boolean':
        # Boolean search: assume boolean_search returns a JSON-like list of results
        results = boolean_search(documents, user_query)
        '''
    else:
        results = []
    
    return render_template('index.html', results=results, query=user_query)