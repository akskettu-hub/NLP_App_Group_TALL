from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  # for tfidf functions later
import numpy as np
import re
import json
from nltk.stem import SnowballStemmer # for Finnish stemming
stemmer = SnowballStemmer("finnish")
import matplotlib.pyplot as plt
def load_documents(file_path):
    documents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
## This loop works on the sample database, but need to be modified if the keys change as the dadtabase develops
## The metadata and link parts are left out but can be added if needed
    for year, cases in data.items():
        for case_info in cases.values():  
            text_content = []
            
            if "Title" in case_info:
                text_content.append("Title:")  
                text_content.append(case_info["Title"])
            
            if "Description" in case_info:
                text_content.append("Description:")
                text_content.extend(case_info["Description"])
            
            for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu"]:
                if section in case_info and "Contents" in case_info[section]:
                    text_content.append(f"\n{section}:")
                    text_content.extend(case_info[section]["Contents"])
            
            documents.append("\n".join(text_content))

    return documents

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

# 4 The most likely reason why not all words are indexed is the default token pattern used by CountVectorizer: r'\b\w\w+\b' This pattern only matches words with two or more alphanumeric characters. See changed token_pattern when initalizing CountVectorizer at the top of the page
def document_setup(documents):
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'\b\w+\b') ### changed token_pattern as part of homework #4
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_ 
    
    return (td_matrix, t2i)



def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    print()
    return user_input

#Modification of former rewrite_token() from course material that handles words not in documents
def avoid_operators(t):
   if t in d:
       return d[t]
   if t not in t2i:
       return 'np.zeros((1, len(documents)), dtype=int)'
   
   return f'td_matrix[{t2i[t]}]'

def rewrite_query(query):
   return " ".join(avoid_operators(t) for t in query.split())

def input_checker(user_input):
    if user_input == "quit" or user_input == "":
           print("Exit")
           return False
        


def stemming(documents):
    
    stemmed_documents = []
    for doc in documents:
        tokens = word_tokenize(doc)  # Tokenize the document
        stemmed_tokens = [stemmer.stem(word) for word in tokens]  # Apply stemming to each token
        stemmed_documents.append(" ".join(stemmed_tokens))  # Join the tokens back into a document
    
    return stemmed_documents

def input_checker(user_input):
    if user_input == "quit" or user_input == "":
        print("Exit")
        return False
    return True                
import re

# This is new. The old one for exact match doesn't work on this script
def exact_match(query, documents):   
    pattern = re.compile(r'\b' + query + r'\b', re.IGNORECASE) # match the exact query as a whole, with t
    
    matching_docs = []
    for i, doc in enumerate(documents):
        if pattern.search(doc):
            matching_docs.append(i)
    
    return matching_docs

# Modify the retrieve_matches function to use exact match
def retrieve_matches(query):
    # Check if the query begins and ends with " "
    if query.startswith('"') and query.endswith('"'):
        # Remove quotes and perform exact match search
        query = query[1:-1]
        return exact_match(query, documents)
    
    # Otherwise proceed with original query rewrite and operator processing
    hits_matrix = eval(rewrite_query(query))
    hits_list = list(hits_matrix.nonzero()[1])
    return hits_list

        
def print_retrieved(hits_list):
    if not hits_list:  
           print("No matching document")
           
    else:
        print(f"Found {len(hits_list)} matches:")
        
        print_limit = 2 # Determines max number of lines printed
        
        if len(hits_list) > print_limit:
            print(f"Here are the first {print_limit} results:")
            
            e_list = list(enumerate(hits_list))
            for i in range(print_limit):
                print()
                print('%.250s' % "Matching doc #{:d}: {:s}".format(e_list[i][0] + 1, documents[e_list[i][1]])) # '%.250s' Number here determines max length of printout per line
                
                    
        else:        
            for i, doc_idx in enumerate(hits_list):
                print()
                print( '%.250s' % "Matching doc #{:d}: {:s}".format(i + 1, documents[doc_idx])) # '%.250s' Number here determines max length of printout per line
            
def main():
    file_path = 'sample_database.json'
    documents = load_documents(file_path)
    documents = documents
    setup = document_setup(documents) 
    td_matrix = setup[0]
    t2i = setup[1]
    while True:
        user_input = user_query()
        if input_checker(user_input) == False:
            break
        hits_list = retrieve_matches(user_input)
        print_retrieved(hits_list)
                

if __name__ == "__main__":
    file_path = 'sample_database.json'
    documents = load_documents(file_path)
    documents = documents
    setup = document_setup(documents) 
    td_matrix = setup[0]
    t2i = setup[1]
    main()