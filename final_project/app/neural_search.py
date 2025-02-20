# please install: pip install sentence-transformers nltk matplotlib

## Dependencies for semantic/neural search:
import numpy as np
# We use a pretrained model from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
from sentence_transformers import SentenceTransformer
import re # for exact match
from nltk.stem import SnowballStemmer # for Finnish stemming


model = SentenceTransformer('all-MiniLM-L6-v2')  # We can change it to a better model if we find one
stemmer = SnowballStemmer("finnish")


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


# Neural search function
def neural_search(documents, user_input):
    # Process the query
    processed_query = process_query(user_input)

    # Construct the final query with stemming
    final_query = []
    for token, is_exact_match in processed_query:
        if is_exact_match:
            final_query.append(token)  # Exact match
        else:
            final_query.append(stemmer.stem(token))  # Apply stemming

    # Join processed tokens into a query string
    final_query_str = " ".join(final_query)

    # Encode the documents and processed query
    doc_embeddings = model.encode(documents)
    query_embedding = model.encode(final_query_str)

    # Calculate cosine similarities between query and documents
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)
    ranked_doc_indices = np.argsort(cosine_similarities)[::-1]  # Rank by descending similarity

    # Collect top 3 results
    num_results = min(3, len(documents))
    results = []
    for i in range(num_results):
        doc_idx = ranked_doc_indices[i]
        doc_content = documents[doc_idx].split("\n")
        title = doc_content[0].replace("Title:", "").strip()
        case_id = doc_content[1].strip()
        full_title = f"{case_id}{title}"
        results.append({
            "title": full_title,
            "score": float(cosine_similarities[doc_idx]),
            "snippet": documents[doc_idx][:50]
        })

    return results