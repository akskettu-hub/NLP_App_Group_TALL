import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
    
# Document setup using TfidfVectorizer, uses LexDatabase
def tf_document_setup(documents):
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    text_contents = [doc[1] for doc in documents]
    tf_columns = {i: doc[0]  for i, doc in enumerate(documents)} #returns a dict with the tf matrix column index and the associated case name
    tf_matrix = tfv.fit_transform(text_contents).T.todense() 
    return tf_matrix, tf_columns, tfv

# Compute cosine similarity scores
def retrieve_matches(query, tf_matrix, tfv):
    query_tf = tfv.transform([query]).todense()  # Convert query to tf-idf vector
    scores = np.dot(query_tf, tf_matrix)  # Compute cosine similarity score
    return scores
#
def tf_get_results(scores, tf_columns):
    results = []
    if np.all(scores == 0):
        return results
    
    scores_and_titles = sorted([(tf_columns[i], score) for i, score in enumerate(np.array(scores)[0]) if score > 0],
        reverse=True) 
    return scores_and_titles

def tfidf_search_results(scores_and_titles : tuple, docs):
    length_results = 3
    sim_results = scores_and_titles[:length_results]
    res_titles = [res[0] for res in sim_results]
    res_scores = [res[1] for res in sim_results]   
    res_docs = [doc for doc in docs if doc["Title"] in res_titles]
    
    results = []
    for i in range(len(sim_results) - 1):
        
        result ={}
        result["rank"] = i+1
        result["title"] = res_docs[i]["Title"]
        result["link"] = res_docs[i]["Link"]
        result["diaarinumero"] = res_docs[i]["Diaarinumero"]
        result["antopaiva"] = res_docs[i]["Antopäivä"]
        result["description"] = res_docs[i]['Description'][:250]
        result["score"] = float(res_scores[i])
        
        results.append(result)     
        
    return results

if __name__ == "__main__":
    """file_path = '../data/en_sample_database.json'
    documents = load_documents(file_path)
    tf_matrix, tfv = tf_document_setup(documents)  
    main()
      
    file_path = 'data/database.json'
    db = LexDatabase(file_path)"""
