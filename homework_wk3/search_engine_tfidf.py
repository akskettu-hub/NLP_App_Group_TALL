from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np 
import re



# Boolean search: Operators

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements


# d. Wildcard searches: Let the users search on incomplete terms, such as hous* (easiest) or *ing (similar to previous case) or h*ing (hardest). Read Chapter 3 of the book to learn more about this topic.
### comment: I get a "nothing to repeat at position 0" error when running this function 
def wildcard(string:str):
    new_string = re.sub("*", r"\w*", string)
    new_string = re.sub("?", r".{1}", new_string)
    return new_string
    
# wildcards = {"*": r"\w*", "?": r".{1}"}  # wildcard replacements: \w* = word characters zero or more times, .{1} = any character exactly once
    




# 4 The most likely reason why not all words are indexed is the default token pattern used by CountVectorizer: r'\b\w\w+\b' This pattern only matches words with two or more alphanumeric characters. See changed token_pattern when initalizing CountVectorizer at the top of the page


### document setup with CountVectorizer
def document_setup(documents: list):
    """Returns a tuple with the term-document matrix and the vocabulary"""
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'\b\w+\b') ### changed token_pattern as part of homework #4
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_ 
    
    return (td_matrix, t2i)


### document setup with TfIdfVectorizer > not sure whether it can be this simple? 
def get_tfidf(documents: list):
    """Returns a tuple with the TfIdf matrix and the vocabulary"""
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm=None) # logarithmic word frequency, idf, no normalization
    matrix = tfv.fit_transform(documents).todense().T
    return matrix, tfv.vocabulary_



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

#a function that asks user what document they want to use. 
def user_document_select():
    pass


def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    print()
    return user_input

#Modification of former rewrite_token() from course material that handles words not in documents
# check t2i variable: refers to a variable that is only in the main function
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

### w 3 part 1, optional
def boolean_or_tfidf():
    """determines whether to use boolean search or tfidf-based search"""
    pass


def retrieve_matches(query):
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
                print('%.250s' % "Matching doc #{:d}: {:s}".format(e_list[i][0], documents[e_list[i][1]])) # '%.250s' Number here determines max length of printout per line
                
                    
        else:        
            for i, doc_idx in enumerate(hits_list):
                print()
                print( '%.250s' % "Matching doc #{:d}: {:s}".format(i, documents[doc_idx])) # '%.250s' Number here determines max length of printout per line


### comment: the main function's structure is pretty much of (function(function(a))), which makes it difficult to follow
def main():
    while True:
        
        user_input = user_query()
        if input_checker(user_input) == False:
            break
        hits_list = retrieve_matches(user_input)
        print_retrieved(hits_list)



### comment: the main function could be written in a more functional fashion (=! object oriented) which would
def new_main():
    while True:
    #   data = analyze_data(data) > analyze data here so it doesn't have to be done every time
        user_input = input("Please Enter your query, type 'quit' to exit: ")
        if user_input == "quit":
            print("Exit")
            break
        else: 
         #   results = retrieve_matches(user_input, data)
        #    print(results)
            pass




if __name__ == "__main__":


### DATA: I moved these variables here as the program is supposed to work with any data - Liisa

    example_documents = ["This is a silly example",
                "A better example",
                "Nothing to see here",
                "This is a great and long example"]


    ### These paths only work if you run the program from the same directory with the wiki_files folder. 
    small_wiki = "/Users/liisa/Documents/Python/NPA Apps 2025/NLP_App_Group_TALL/homework_wk2/wiki_files/enwiki-20181001-corpus.100-articles.txt" 
    # large_wiki = "wiki_files/enwiki-20181001-corpus.1000-articles.txt"

    # documents = extract_wiki_articles(small_wiki) # Assign whatever list of strings you want to use as documents to this variable, comment this line if you don't want to use the small wiki
    documents = example_documents # uncomment this line to use example_documents

### END OF DATA

    ### These variables are referred to in some functions, so they need to be declared earlier if they are needed
    setup = document_setup(example_documents) 
    # setup = get_tfidf(example_documents)
    
    td_matrix = setup[0]
    t2i = setup[1]
    
    main()