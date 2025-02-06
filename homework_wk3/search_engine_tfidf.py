from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  # for tfidf functions later
import numpy as np
import re

# Boolean search: Operators

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

stemmer = PorterStemmer()

# d. Wildcard searches: Let the users search on incomplete terms, such as hous* (easiest) or *ing (similar to previous case) or h*ing (hardest). Read Chapter 3 of the book to learn more about this topic.
### comment: I get a "nothing to repeat at position 0" error when running this function 
def wildcard(string:str):
    new_string = re.sub("*", r"\w*", string)
    new_string = re.sub("?", r".{1}", new_string)
    return new_string
    
# wildcards = {"*": r"\w*", "?": r".{1}"}  # wildcard replacements: \w* = word characters zero or more times, .{1} = any character exactly once

# 4 The most likely reason why not all words are indexed is the default token pattern used by CountVectorizer: r'\b\w\w+\b' This pattern only matches words with two or more alphanumeric characters. See changed token_pattern when initalizing CountVectorizer at the top of the page

# 5
def extract_wiki_articles(file: str): 
    """returns a list of strings"""
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    articles = text.split("</article>")
    cleaned_articles = []
    for article in articles:
        
        cleaned_articles.append(re.sub(r"<.*>", "", article))
        
    return cleaned_articles

# 2a&b (Stemming & exact matches) 
# NEW: Two Document Setup Functions

### document setup with CountVectorizer
# setup index with stemming (for tokens not enclosed in quotes)

def document_setup_stem(documents: list):
    cv = CountVectorizer(lowercase=True, tokenizer=stem_tokenizer, token_pattern=None, binary=True)
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T  # rows represent tokens
    t2i = cv.vocabulary_
    return td_matrix, t2i

# setup index without stemming (for exact-match tokens in quotes)
def document_setup_exact(documents: list):
    cv = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b', binary=True)
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T  # rows represent tokens
    t2i = cv.vocabulary_
    return td_matrix, t2i

# tokenizer that applies stemming
def stem_tokenizer(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [stemmer.stem(token) for token in tokens]

### document setup with TfIdfVectorizer > not sure whether it can be this simple? 
def get_tfidf(documents: list):
    """Returns a tuple with the TfIdf matrix and the vocabulary"""
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm=None) # logarithmic word frequency, idf, no normalization
    matrix = tfv.fit_transform(documents).todense().T
    return matrix, tfv.vocabulary_

#a function that asks user what document they want to use. 
def user_document_select():
    pass

def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    return user_input

def input_checker(user_input):
    if user_input == "quit" or user_input == "":
           print("Exit")
           return False
    return True

# 2a&b (Stemming & exact matches) 
# NEW: Query Processing Functions

# Process the query into a list of tuples (token, exact)
def process_query(query):
    tokens = []
    # this regex finds either "something in quotes" or individual words.
    pattern = r'"(.*?)"|(\w+)'
    for match in re.finditer(pattern, query):
        if match.group(1):  # if token is in double quotes => exact match
            tokens.append((match.group(1).lower(), True))
        elif match.group(2):  # otherwise, token is to be stemmed
            tokens.append((match.group(2).lower(), False))
    return tokens

# rewrite query into a Python expression for eval()
def rewrite_query(query, t2i_stem, t2i_exact):
    tokens = process_query(query)
    token_expressions = []
    for token, exact in tokens:
        # check for boolean operators (using dictionary d)
        if token in d:
            token_expressions.append(d[token])
        else:
            if exact:
                # for exact token, use exact index
                if token not in t2i_exact:
                    token_expressions.append('np.zeros((1, len(documents)), dtype=int)')
                else:
                    token_expressions.append(f'td_matrix_exact[{t2i_exact[token]}]')
            else:
                # for non-exact token, stem it and look up in the stem index
                stemmed = stemmer.stem(token)
                if stemmed not in t2i_stem:
                    token_expressions.append('np.zeros((1, len(documents)), dtype=int)')
                else:
                    token_expressions.append(f'td_matrix_stem[{t2i_stem[stemmed]}]')
    return " ".join(token_expressions)
       
#Modification of former rewrite_token() from course material that handles words not in documents
# check t2i variable: refers to a variable that is only in the main function

# OLD: avoid_operators and rewrite_query functions are replaced by the above
'''
def avoid_operators(t, t2i):
   if t in d:
       return d[t]
   if t not in t2i:
       return 'np.zeros((1, len(documents)), dtype=int)'
   
   return f'td_matrix[{t2i[t]}]'

def rewrite_query(query, t2i):
   return " ".join(avoid_operators(t, t2i) for t in query.split())


def retrieve_matches(query, documents, td_matrix, t2i):
    hits_matrix = eval(rewrite_query(query, t2i))
    hits_list = list(hits_matrix.nonzero()[1])
    return hits_list
'''

def retrieve_matches(query, documents, td_matrix_stem, t2i_stem, td_matrix_exact, t2i_exact):
    # Create the evaluable query expression
    query_expression = rewrite_query(query, t2i_stem, t2i_exact)
    try:
        # Evaluate the expression. (Note that 'documents' is used in the dummy np.zeros expression.)
        hits_matrix = eval(query_expression)
    except Exception as e:
        print("Error evaluating query:", e)
        return []
    hits_list = list(hits_matrix.nonzero()[1])
    return hits_list

### w 3 part 1, optional
def boolean_or_tfidf():
    """determines whether to use boolean search or tfidf-based search"""
    pass
        
def print_retrieved(hits_list, documents):
    if not hits_list:  
           print("No matching document")
           
    else:
        print()
        print(f"Found {len(hits_list)} matches:")
        
        print_limit = 2 # Determines max number of lines printed
        
        if len(hits_list) > print_limit:
            print(f"Here are the first {print_limit} results:")
            
            e_list = list(enumerate(hits_list))
            for i in range(print_limit):
                print()
                print('%.250s' % "Matching doc #{:d}: {:s}".format(e_list[i][0], documents[e_list[i][1]])) # '%.250s' Number here determines max length of printout per line   
                    
        else:        
            for i, doc_idx in enumerate(hits_list):
                print()
                print( '%.250s' % "Matching doc #{:d}: {:s}".format(i, documents[doc_idx])) # '%.250s' Number here determines max length of printout per line

### comment: the main function's structure is pretty much of (function(function(a))), which makes it difficult to follow
### response, by Akseli: I do not agree that it's difficult to follow, but then I did write it and this tends to be my preference for organising main functions. I do feel the functions and variables are quite clearly labled and the logic is not complicated. Using functions like this also allows the expansion of functionality without having to touch, or clutter main() all that much, and to have that functionality be portable, should it be applicable to some other issue. For example, if we want to check for somehting other than just the word quit "quit", we can just add it to the input_checker() function. The main logic of the programme in general does not need to know which conditions trigger an exit, it just gets told to exit. I, for example, wanted the programme to exit on an empty input as well as "quit", as it makes testing slightly less cumbersome, and also it means we don't have to account for what to do with an empty query. The point of main(), to me, is to be the overall layout of the programme as it runs, with as little specifis as possible.
def main():
    ### DOCUMENTS: Use the documents variable to determine which data you want to use. Please do not change documents variable elsewhere.
    documents = extract_wiki_articles(small_wiki) # Assign whatever list of strings you want to use as documents to this variable, comment this line if you don't want to use the small wiki
    #documents = extract_wiki_articles(large_wiki) # Assign whatever list of strings you want to use as documents to this variable, comment this line if you don't want to use the large_wiki
    # documents = example_documents # uncomment this line to use example_documents
    ### END OF DOCUMENTS:
    
    ### SETUP
    # Build two indices: one for stemming (non-exact tokens) and one for exact matches.
    td_matrix_stem, t2i_stem = document_setup_stem(documents)
    td_matrix_exact, t2i_exact = document_setup_exact(documents)
    ### END OF SETUP
    
    while True:
        user_input = user_query()
        if input_checker(user_input) == False:
            break
        hits_list = retrieve_matches(user_input, documents, td_matrix_stem, t2i_stem,                                  td_matrix_exact, t2i_exact)
        print_retrieved(hits_list, documents)

### comment: the main function could be written in a more functional fashion (=! object oriented) which would
### response, by Akseli: I do not see that this is in any practical sense a better solution. The programme being this small, there is little difference between these two versions as regrads what these main functions actually do, but with a more a more functional approach (as in, the main() function is a function that runs the programme which is a series of functions) to organising a programme like this, we can add and modify functions as we please, which will make things easier as the programme gets more complicated. In addition to my comment to the main() function, this is a good example for why I prefer my way. The user_query() function, in addition to simply asking input, also adds some empty lines to make it more readable on the command line. We can modify this function with various formatting, for example, without cluttering the main() function.
def new_main():
    while True:
    #   data = analyze_data(data) > analyze data here so it doesn't have to be done every time
    # response, by Akseli: This seems incorrect to me. If placed here, it's in the loop, so it will get done every time anyway, and it's before user input, which means it's done even when the user intends to quit. In main(), data only gets analysed if it has to be.
        user_input = input("Please Enter your query, type 'quit' to exit: ")
        if user_input == "quit":
            print("Exit")
            break
        else: 
         #   results = retrieve_matches(user_input, data)
        #    print(results)
            pass

### TF-IDF AND COSINE SIMILARITY FUNCTIONS         
# Document setup using TfidfVectorizer
def tf_document_setup(documents):
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2") 
    tf_matrix = tfv.fit_transform(documents).T.todense() 
    return tfv, tf_matrix

# Compute cosine similarity scores
def tf_retrieve_matches(query, tfv, tf_matrix):
    query_tf = tfv.transform([query]).todense()  # Convert query to tf-idf vector
    scores = np.dot(query_tf, tf_matrix)  # Compute cosine similarity score
    return scores

#Works to a limited extent: prints rank, score, and document id. Print formatting needs work. 
def tf_print_retrieved(scores, documents):
    if np.all(scores == 0):  
        print("No matching document")
    else:
        print()
        ranked_scores_and_doc_ids = sorted([(score, doc_idx) for doc_idx, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True) # Rank the documents by similarity score
        
        print(f"Found {len(ranked_scores_and_doc_ids)} matches:")
        
        print_limit = 2  # Max number of results to display
        #e_list = enumerate(ranked_scores_and_doc_ids)
        
        if len(ranked_scores_and_doc_ids) > print_limit:
            print(f"Here are the first {print_limit} results:")
        
            for rank, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids[:print_limit]):
                print()
                print(f"{rank} - {score} - {doc_idx}") # Needs formatting
                #print('%.250s' % "Matching doc #{:d}: {:s}".format(e_list[i][0], documents[e_list[i][1]])) # '%.250s' Number here determines max length of printout per line   
                    
        else:        
            for rank, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
                print()
                print(f"{rank} - {score} - {doc_idx}") # Needs formatting
                #print( '%.250s' % "Matching doc #{:d}: {:s}".format(i, documents[doc_idx])) # '%.250s' Number here determines max length of printout per line

# this function works exactly like the main function, but uses tfidf functions in place of the boolean stuff, used for testing   
def tfidf_test():
    #documents = ["This is a silly silly silly example",
    #         "A better example",
    #         "Nothing to see here nor here nor here",
    #         "This is a great example and a long example too"]
    small_wiki = "../wiki_files/enwiki-20181001-corpus.100-articles.txt"
    documents = extract_wiki_articles(small_wiki)
    tfv, tf_matrix  = tf_document_setup(documents)
    
    while True:
        user_input = user_query()
        if not input_checker(user_input):
            break
        scores = tf_retrieve_matches(user_input,tfv, tf_matrix)
        tf_print_retrieved(scores, example_documents)
### END OF TF-IDF AND COSINE SIMILARITY FUNCTIONS        


if __name__ == "__main__":
### DATA: I moved these variables here as the program is supposed to work with any data - Liisa

    example_documents = ["This is a silly example",
                "A better example",
                "Nothing to see here",
                "This is a great and long example"]

    ### These paths only work if you run the program from the same directory with the wiki_files folder. 
    # Akseli: fixed. Now point to parent folder and should be accessible from anywhere.
    small_wiki = "../wiki_files/enwiki-20181001-corpus.100-articles.txt" 
    large_wiki = "../wiki_files/enwiki-20181001-corpus.1000-articles.txt"

### END OF DATA
    
    main()
    #tfidf_test() # Comment main and uncomment this to test tf-idf