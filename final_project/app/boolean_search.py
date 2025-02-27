from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import re
import json
import numpy as np
from nltk.stem import SnowballStemmer # for Finnish stemming


stemmer = SnowballStemmer("finnish")

def load_documents(file_path):
    documents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
## updated funtion per Friday's discussion
    for year, cases in data.items():
        for case_info in cases.values():  
            text_content = []
            
            if "Title" in case_info:
                text_content.append(f"Title: {case_info['Title']}")  
            
            if "Metadata" in case_info:
                metadata = case_info["Metadata"]
                if "Link" in metadata:
                    text_content.append(f"Link: {metadata['Link']}")
                if "Diaarinumero:" in metadata:
                    text_content.append(f"Diaarinumero: {metadata['Diaarinumero:']}")
                if "Antopäivä:" in metadata:
                    text_content.append(f"Antopäivä: {metadata['Antopäivä:']}")
            
            if "Description" in case_info:
                text_content.append("Description:")
                text_content.extend(case_info["Description"])
            
            ### Suppose we want what's in the "content" entries:
            '''
            for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu"]:
                if section in case_info and "Contents" in case_info[section]:
                    text_content.append(f"\n{section}:")
                    text_content.extend(case_info[section]["Contents"])
            '''
            
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
    
    return td_matrix, t2i

'''

def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    print()
    return user_input
'''
#Modification of former rewrite_token() from course material that handles words not in documents
def avoid_operators(t, t2i):
   if t in d:
       return d[t]
   if t not in t2i:
       return 'np.zeros((1, len(documents)), dtype=int)'
   
   return f'td_matrix[{t2i[t]}]'

def rewrite_query(query, t2i):
    query = query.lower()
    return " ".join(avoid_operators(t, t2i) for t in query.split())

'''
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

'''
def extract_case_info(doc):
    case_info = {
        "Title": "N/A",
        "Link": "N/A",
        "Case Number": "N/A",
        "Date": "N/A",
        "Description": "N/A"
    }

    # Extract the  Title
    title_match = re.search(r"^Title:\s*(.*)", doc, re.MULTILINE)
    if title_match:
        case_info["Title"] = title_match.group(1).strip()

    # Extract the Link
    link_match = re.search(r"^Link:\s*(.*)", doc, re.MULTILINE)
    if link_match:
        case_info["Link"] = link_match.group(1).strip()


    # Extract the Case  Number
    case_number_match = re.search(r"^Diaarinumero:\s*(.*)", doc, re.MULTILINE)
    if case_number_match:
        case_info["Case Number"] = case_number_match.group(1).strip()

    # Extract the Date
    date_match = re.search(r"^Antopäivä:\s*(.*)", doc, re.MULTILINE)
    if date_match:
        case_info["Date"] = date_match.group(1).strip()

    # Extract the Description
    description_match = re.search(r"^Description:\s*(.*)", doc, re.MULTILINE)
    if description_match:
        case_info["Description"] = description_match.group(1).strip()

    return case_info


def retrieve_matches(query, td_matrix, t2i, documents):
    # Check for exact match (quoted string)
    if query.startswith('"') and query.endswith('"'):
        query = query[1:-1]
        return exact_match(query, documents)
    
    # Process normal query (Boolean search or similar)
    hits_matrix = eval(rewrite_query(query, t2i))  # Evaluates the query and retrieves the matching documents
    hits_list = list(hits_matrix.nonzero()[1])  # Extract indices of matching documents

    # Initialize an empty list to store results
    results = []

    # Now, process each document from the retrieved hits
    for i in hits_list:
        document = documents[i]  # Get the document text based on index
        # Extract structured case info using the extract_case_info function
        case_info = extract_case_info(document)
        # Add the score (from the hits_matrix) to the case_info dictionary
        case_info["score"] = hits_matrix[0, i]
        # Append the structured case info to the results list
        results.append(case_info)

    return results


def exact_match(query, documents):   
    pattern = re.compile(r'\b' + query + r'\b', re.IGNORECASE)  # match the exact query aas a whole
    
    matching_docs = []
    for i, doc in enumerate(documents):
        if pattern.search(doc):
            matching_docs.append(i)
    
    return matching_docs



        
def print_retrieved(hits_list, documents):
    if not hits_list:  
        print("No matching document")
    else:
        print(f"Found {len(hits_list)} matches:")
        
        print_limit = 30 # Change the number here to determine the output length
        
        for i, doc_idx in enumerate(hits_list):
            matched_doc = documents[doc_idx]
            
           # print(f"\nMatching doc #{i + 1}:")
            
            limit_doc = matched_doc[:print_limit]  
            
            if len(matched_doc) > print_limit:
                limit_doc += " ..."  
            
            #print(limit_doc)

'''
            
def main():

    while True:
        user_input = user_query()
        if input_checker(user_input) == False:
            break
        hits_list = retrieve_matches(user_input)
        print_retrieved(hits_list)
                

if __name__ == "__main__":
    file_path = 'en_sample_database.json'
    documents = load_documents(file_path)
    documents = documents
    setup = document_setup(documents) 
    td_matrix = setup[0]
    t2i = setup[1]
    main()
'''