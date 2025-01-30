from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re


documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]

cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'\b\w+\b') ### changed token_pattern as part of homework #4
sparse_matrix = cv.fit_transform(documents)

#print a dense version of this matrix
dense_matrix = sparse_matrix.todense()

#transpose the matrix, so that the rows and columns change places
td_matrix = dense_matrix.T   # .T transposes the matrix

t2i = cv.vocabulary_ 

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

#HOMEWORK

# 1 - 3 
def loop():
    while True:
        user_query = input("Please Enter your query, type 'quit' to exit: ")
        if user_query == "quit":
           print("Exit")
           break
        hits_matrix = eval(rewrite_query(user_query))
       
        print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
        print("The coordinates of the non-zero elements:", hits_matrix.nonzero())  
       
        hits_list = list(hits_matrix.nonzero()[1])
        if not hits_list:  
           print("No matching document")
        else:
           for doc_idx in hits_list:
               print("Matching doc:", documents[int(doc_idx)]) 

        print(f"Found {len(hits_list)} matches:")
    
        print_limit = 2
    
        if len(hits_list) > print_limit:
            print(f"Here are the first {print_limit} results:")
        
            e_list = list(enumerate(hits_list))
            for i in range(print_limit):
                print("Matching doc #{:d}: {:s}".format(e_list[i][0], documents[e_list[i][1]]))
                
        else:        
            for i, doc_idx in enumerate(hits_list):
                print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))

        
loop()

# 4 The most likely reason why not all words are indexed is the default token pattern used by CountVectorizer: r'\b\w\w+\b' This pattern only matches words with two or more alphanumeric characters. See changed token_pattern when initalizing CountVectorizer at the top of the page

# 5

def extract_articles(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    articles = text.split("</article>")
    cleaned = []
    for article in articles:
        
        cleaned.append(re.sub(r"<.*>", "", article))
        
    return cleaned

small = "wiki_files/enwiki-20181001-corpus.100-articles.txt"
large = "wiki_files/enwiki-20181001-corpus.1000-articles.txt"



