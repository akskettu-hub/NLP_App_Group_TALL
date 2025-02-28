import numpy as np
# We use a pretrained model from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
from sentence_transformers import SentenceTransformer
import json
import re # for exact match
from nltk.stem import SnowballStemmer # for Finnish stemming
import matplotlib.pyplot as plt

model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  # We can change it to a better model if we find one
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
            
            for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu"]:
                if section in case_info and "Contents" in case_info[section]:
                    text_content.append(f"\n{section}:")
                    text_content.extend(case_info[section]["Contents"])
            
            
            documents.append("\n".join(text_content))

    return documents

def neural_search(documents, user_input):
    doc_embeddings = model.encode(documents)  # Encode documents
    query_embedding = model.encode(user_input)  # Encode user input
    
    # Calculate cosine similarities and rank documents
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)  
    ranked_doc_indices = np.argsort(cosine_similarities)[::-1]  
    
    num_results = min(3, len(documents))  # Limit to top 3 results
    # print(f'\nYour query "{user_input}" matches {len(documents)} documents.')
    # print(f"Here are the top {num_results} results:\n")

    result_scores = []
    result_titles = []

    results = []

    for i in range(num_results):
        doc_idx = ranked_doc_indices[i]
        doc_content = documents[doc_idx].split("\n")
        
        # Initialize metadata variables
        metadata = {key: "" for key in ["Title", "Link", "Diaarinumero", "Antopäivä"]}
        descriptions = []

        for line in doc_content:
            if line.startswith("Title:"):
                metadata["Title"] = line.replace("Title:", "").strip()
            elif line.startswith("Link:"):
                metadata["Link"] = line.replace("Link:", "").strip()
            elif line.startswith("Diaarinumero:"):
                metadata["Diaarinumero"] = line.replace("Diaarinumero:", "").strip()
            elif line.startswith("Antopäivä:"):
                metadata["Antopäivä"] = line.replace("Antopäivä:", "").strip()
            elif line.startswith("Description:"):
                descriptions.extend(doc_content[doc_content.index(line) + 1:])  

        description = " ".join(descriptions)[:250]  ### change the number here to determine the output length

        # Store results for plotting
        result_scores.append(float(cosine_similarities[doc_idx]))  
        result_titles.append(metadata["Title"] if metadata["Title"] else "Unknown Title")
        '''
        # Print formatted result
        print(f"Matching doc #{i+1}:")
        for key in metadata:
            if metadata[key]:
                print(f"{key}: {metadata[key]}")
        if description:
            print(f"Description: {description}...")  
        
        print(f"(score: {cosine_similarities[doc_idx]:.2f})\n")
        '''

        results.append({
            "rank": i + 1,
            "title": metadata["Title"] if metadata["Title"] else "Unknown Title",
            "link": metadata["Link"],
            "diaarinumero": metadata["Diaarinumero"],
            "antopaiva": metadata["Antopäivä"],
            "description": description,
            "score": float(cosine_similarities[doc_idx])
        })
    # print(f"results:{results}")
    # return result_scores, result_titles  
    return results


'''    
def plotting(result_scores, result_titles):
    # Visualize the results
    plt.bar(result_titles, result_scores)
    plt.xlabel('Document')
    plt.ylabel('Match Score')
    plt.title('Top Search Results')
    plt.ylim(0.3)
    plt.show()
'''


def user_query():
    print()
    user_input = input("Please Enter your query, type 'quit' to exit: ")
    return user_input

# tokenizer that applies stemming
def stem_tokenizer(text):
    tokens = re.findall(r'\b\w+\b', text.lower())  
    return [stemmer.stem(token) for token in tokens]  

# Function to process the query (exact match for quoted phrases, stemming for other tokens)
def process_query(query):
    tokens = []
    # This regex finds either "something in quotes" or individual words
    pattern = r'"(.*?)"|(\w+)'
    for match in re.finditer(pattern, query):
        if match.group(1):  # If token is in double quotes => exact match
            tokens.append((match.group(1).lower(), True))
        elif match.group(2):  # Otherwise, token is to be stemmed
            tokens.append((match.group(2).lower(), False))
    return tokens

def input_checker(user_input):
    if user_input == "quit" or user_input == "":
        print("Exit")
        return False
    return True


'''
def main():

    file_path = '../data/en_sample_database.json'
    documents = load_documents(file_path)

    while True:
        user_input = user_query()
        if input_checker(user_input) == False: 
            break
            
        results, result_scores, result_titles = neural_search(documents, user_input)
        plotting(result_scores, result_titles)

        

# Run the main function
if __name__ == "__main__":
    main()
'''