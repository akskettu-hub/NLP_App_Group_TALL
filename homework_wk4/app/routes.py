from flask import render_template, request
from app import app
from search_engine_tfidf import extract_wiki_articles, retrieve_matches, print_retrieved, document_setup_stem, document_setup_exact 

# load documents globally when the app starts
documents = extract_wiki_articles("../wiki_files/enwiki-20181001-corpus.1000-articles.txt")
td_matrix_stem, t2i_stem = document_setup_stem(documents)
td_matrix_exact, t2i_exact = document_setup_exact(documents)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# route for handling the search query
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']  # get the search query from the form

        hits_list = retrieve_matches(query, documents, td_matrix_stem, t2i_stem, td_matrix_exact, t2i_exact)

        hits_list = [int(hit) for hit in hits_list]

        limited_docs = [doc[:250] for doc in documents]

        # render the results page with the hits
        return render_template('results.html', query=query, hits_list=hits_list, documents=documents, limited_docs=limited_docs)
 
    return render_template('index.html') 