import numpy as np
# We use a pretrained model from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
from sentence_transformers import SentenceTransformer
import json
import re # for exact match
from nltk.stem import SnowballStemmer # for Finnish stemming
import matplotlib.pyplot as plt

model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  # We can change it to a better model if we find one
stemmer = SnowballStemmer("finnish")

def test():
    string = ["test string is this I like beans", "another string", "yet morestrings clump "]
    doc_embeddings = model.encode(string)
    query_embedding = model.encode("beans")
    
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)
    print(cosine_similarities)
    
def embedd_doc(contents : list):
    embeddigns = []
    for doc in contents:
        doc_title = doc[0]
        doc_embedding = model.encode(doc[1])
        embeddigns.append((doc_title, doc_embedding))
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
    length_results = 3
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

if __name__ == "__main__":
    contents = [['KKO:2015:1', 'X Oy:n vastuuhenkilö A oli nostanut perusteettomien aliurakointilaskujen avulla yhtiöstä varoja ja hänet oli tuomittu yhtiön verotuksessa tehdystä törkeästä veropetoksesta hänen annettuaan yhtiön veroilmoituksissa vääriä tietoja veron määrään vaikuttavista seikoista. Osa varoista oli jäänyt A:lle ja A oli tuomittu myös henkilökohtaisessa verotuksessaan tekemästään veropetoksesta. Korkeimman oikeuden ratkaisusta ilmenevillä perusteilla katsottiin, ettei A:lla ollut niin sanotun itsekriminointisuojan perusteella oikeutta jättää ilmoittamatta X Oy:stä saamiaan varoja henkilökohtaisessa verotuksessaan. Jättäessään varat ilmoittamatta A syyllistyi törkeään veropetokseen. Ks. KKO:2011:35']]
    
    res = embedd_doc(contents)
    print(res)