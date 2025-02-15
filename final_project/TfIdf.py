
"""


████████╗ █████╗ ██╗     ██╗     
╚══██╔══╝██╔══██╗██║     ██║     
   ██║   ███████║██║     ██║     
   ██║   ██╔══██║██║     ██║     
   ██║   ██║  ██║███████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝

TF-IDF based search.
Assumes a dataset with at least doc_name and doc_text values.
"""


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import numpy as np
import os


data = {"doc_name": [],
        "doc_text": []}


def setup_vectorizer():
    global vectorizer
    vectorizer = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")

def vectorize_data(data):
    vect_data = vectorizer.fit_transform(data['doc_text']).T.tocsr()
    return vect_data

def vectorize_query(query: str):
    vect_query = vectorizer.transform([query]).tocsc()
    return vect_query

def get_hits(query, data):
    """Returns cosine similarities"""
    return np.dot(query, data)

def rank(hits):
    try: 
        return sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
    except:
        print("No search results.")

def print_ranked(ranked_hits):
    print("Search results in order of relevance:")
    for score, id in ranked_hits:
        print(f'{data['doc_name'][id]}, score {score:.3f}')


## setting up data for testing

def dir_to_df(folder: dir, extension=".txt"):
    """Returns a pandas DataFrame with the name and text of all files in a folder (default filetype=.txt)"""
    data = {"doc_name": [],
            "doc_text": []}
    for file in os.scandir(folder): # iterates through the fodler
        filename = os.fsdecode(file) 
        if file.is_file() and filename.endswith(extension):
            data["doc_name"].append(filename.split("/")[-1])
            f = open(file, "r", encoding="utf-8", errors="ignore")
            content = f.read()
            data["doc_text"].append(content)
            f.close()
    df = pd.DataFrame.from_dict(data)
    return df        

## ui for testing

def ui():
    while True:
        print("Enter your query, or type 'exit' to quit.")
        query = input(">>> ")
        if query == "exit":
            break
        else:
            query_v = vectorize_query(query)
            results = get_hits(query_v, data_v)
            try: 
                ranked = rank(results)
                print_ranked(ranked)
            except:
                print("No search results.")
                continue


if __name__== "__main__":


    ## setting up data ###

    folder = "gutenberg"
    data = dir_to_df(folder)


    ### vectorize data

    setup_vectorizer()
    data_v = vectorize_data(data)

    ### query and vectorize query
    ### get results

    ui()

