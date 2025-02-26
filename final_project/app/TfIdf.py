import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import re

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
            
            for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu"]:
                if section in case_info and "Contents" in case_info[section]:
                    text_content.append(f"\n{section}:")
                    text_content.extend(case_info[section]["Contents"])
            
            
            documents.append("\n".join(text_content))

    return documents
# Document setup using TfidfVectorizer
def tf_document_setup(documents):
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2") 
    tf_matrix = tfv.fit_transform(documents).T.todense() 
    return tf_matrix, tfv
'''
def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    print()
    return user_input


def input_checker(user_input):
    if user_input == "quit" or user_input == "":
           print("Exit")
           return False
    return True
'''
# Compute cosine similarity scores
def retrieve_matches(query, tf_matrix, tfv):
    query_tf = tfv.transform([query]).todense()  # Convert query to tf-idf vector
    scores = np.dot(query_tf, tf_matrix)  # Compute cosine similarity score
    return scores

def extract_field(document, field_name):
    """Extract a field from a structured document string."""
    match = re.search(rf"{field_name}: (.+)", document)
    return match.group(1) if match else "N/A"

def tf_get_results(scores, documents):
    results = []
    if np.all(scores == 0):
        return results

    ranked_scores_and_doc_ids = sorted(
        [(score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0],
        reverse=True
    )

    for rank, (score, i) in enumerate(ranked_scores_and_doc_ids):
        matched_doc = documents[i]
        
        results.append({
            "rank": rank + 1,
            "title": extract_field(matched_doc, "Title"),
            "link": extract_field(matched_doc, "Link"),
            "diaarinumero": extract_field(matched_doc, "Diaarinumero"),
            "antopaiva": extract_field(matched_doc, "Antopäivä"),
            "description": matched_doc[:500] + "...",  # Truncate for display
            "score": float(score)
        })
    import json
    print(json.dumps(results, indent=2))
    return results
    
  

def tf_print_retrieved(scores, documents):
    if np.all(scores == 0):  
        print("No matching document")
    else:
        ranked_scores_and_doc_ids = sorted([(score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True) # Rank the documents by similarity score
        
        print(f"Found {len(ranked_scores_and_doc_ids)} matches:")
        
        print_limit = 500  # Change the number here to determine the output length
        for rank, (score, i) in enumerate(ranked_scores_and_doc_ids):
            matched_doc = documents[i]
            limit_doc = matched_doc[:print_limit]  
            
            limit_doc += "..."  
            
            print(f"\nMatching doc #{rank + 1}:")
            print(limit_doc) 
            print(f"(score: {score:.4f})")  


'''         
def main():
    while True:
        user_input = user_query()
        if not input_checker(user_input):
            break
        scores = retrieve_matches(user_input, tf_matrix, tfv)
        results = tf_get_results(scores, documents)
      
        import json
        print(json.dumps(results, indent=2))
        # tf_print_retrieved(scores, documents)

if __name__ == "__main__":
    file_path = '../data/en_sample_database.json'
    documents = load_documents(file_path)
    tf_matrix, tfv = tf_document_setup(documents)  
    main()
    '''  