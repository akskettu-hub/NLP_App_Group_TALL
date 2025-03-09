import numpy as np
from sentence_transformers import SentenceTransformer
from nltk.stem import SnowballStemmer # for Finnish stemming

model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  
stemmer = SnowballStemmer("finnish")

def embedd_doc(contents : list):
    print("Generating word embeddings. Please wait...")
    embeddigns = []
    for doc in contents:
        doc_title = doc[0]
        doc_embedding = model.encode(doc[1])
        embeddigns.append((doc_title, doc_embedding))
    print("Generation of word embeddings complete.")
    return embeddigns

def cosine_similarities(embeddings, query):
    doc_embeddings = [embedding[1] for embedding in embeddings]
    query_embedding = model.encode(query)
    cosine_similarities = np.dot(query_embedding, np.array(doc_embeddings).T)
    
    similarities = []
    for i in range(len(cosine_similarities)):
        similarities.append((embeddings[i][0], cosine_similarities[i]))
    
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_similarities

def neural_search_results(sorted_similarities, docs):
    length_results = 10
    sim_results = sorted_similarities[:length_results]
    res_titles = [res[0] for res in sim_results]
    res_scores = [res[1] for res in sim_results]   
    res_docs = [doc for doc in docs if doc["Title"] in res_titles]
    
    results = []
    for i in range( length_results):
        
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