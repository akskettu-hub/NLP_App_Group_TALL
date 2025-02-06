from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re

# Boolean search operator replacements
d = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

# Create a PorterStemmer instance
stemmer = PorterStemmer()

# --- 1. Two simple document setup functions ---

# Tokenizer that applies stemming
def stem_tokenizer(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [stemmer.stem(token) for token in tokens]

# Setup index with stemming (for tokens not enclosed in quotes)
def document_setup_stem(documents: list):
    cv = CountVectorizer(lowercase=True, tokenizer=stem_tokenizer, token_pattern=None, binary=True)
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T  # Transposed so that rows represent tokens
    t2i = cv.vocabulary_
    return td_matrix, t2i

# Setup index without stemming (for exact-match tokens in quotes)
def document_setup_exact(documents: list):
    cv = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b', binary=True)
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T  # Transposed so that rows represent tokens
    t2i = cv.vocabulary_
    return td_matrix, t2i

# --- 2. Simple Query Parser ---

# Process the query into a list of tuples (token, exact)
def process_query(query):
    tokens = []
    # This regex finds either "something in quotes" or single words.
    pattern = r'"(.*?)"|(\w+)'
    for match in re.finditer(pattern, query):
        if match.group(1):  # Token in double quotes: exact match
            tokens.append((match.group(1).lower(), True))
        elif match.group(2):  # Normal token: to be stemmed
            tokens.append((match.group(2).lower(), False))
    return tokens

# --- 3. Rewrite the query into a Python expression for eval() ---

def rewrite_query(query, t2i_stem, t2i_exact):
    tokens = process_query(query)
    token_expressions = []
    for token, exact in tokens:
        # Check if the token is a boolean operator
        if token in d:
            token_expressions.append(d[token])
        else:
            if exact:
                # Look up the token in the exact index
                if token not in t2i_exact:
                    token_expressions.append('np.zeros((1, len(documents)), dtype=int)')
                else:
                    token_expressions.append(f'td_matrix_exact[{t2i_exact[token]}]')
            else:
                # For non-exact tokens, stem it and search in the stem index.
                stemmed = stemmer.stem(token)
                if stemmed not in t2i_stem:
                    token_expressions.append('np.zeros((1, len(documents)), dtype=int)')
                else:
                    token_expressions.append(f'td_matrix_stem[{t2i_stem[stemmed]}]')
    return " ".join(token_expressions)

# --- 4. Main function that puts everything together ---

def main():
    # Example documents; in a real application, you could use extract_wiki_articles() or similar.
    documents = [
        "This is a silly example",
        "A better example",
        "Nothing to see here",
        "This is a great and long example",
        "House houses housing are all related."
    ]

    # Build two indices: one with stemming and one without (exact)
    td_matrix_stem, t2i_stem = document_setup_stem(documents)
    td_matrix_exact, t2i_exact = document_setup_exact(documents)

    while True:
        user_input = input("\nPlease enter your query (or type 'quit' to exit): ")
        if user_input.lower() == "quit" or user_input.strip() == "":
            print("Exiting")
            break

        # Rewrite the query into an evaluatable expression.
        # Note: The variable 'documents' is used in the np.zeros expression.
        query_expression = rewrite_query(user_input, t2i_stem, t2i_exact)

        # Use eval() to evaluate the query expression and get the hits vector.
        # The expression might look something like: td_matrix_stem[3] & td_matrix_exact[7]
        hits_matrix = eval(query_expression)
        hits_list = list(hits_matrix.nonzero()[1])

        if not hits_list:
            print("No matching document")
        else:
            print(f"\nFound {len(hits_list)} matching document(s):")
            for idx in hits_list:
                print(f"Doc #{idx}: {documents[idx]}")

if __name__ == "__main__":
    main()
