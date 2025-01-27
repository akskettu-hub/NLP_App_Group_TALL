from sklearn.feature_extraction.text import CountVectorizer


documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]


# use the CountVectorizer class to create a term-document matrix of our data
cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)

print("Term-document matrix: (?)\n")
print(sparse_matrix)


#print a dense version of this matrix
dense_matrix = sparse_matrix.todense()

print("Term-document matrix: (?)\n")
print(dense_matrix)

#transpose the matrix, so that the rows and columns change places
td_matrix = dense_matrix.T   # .T transposes the matrix

print("Term-document matrix:\n")
print(td_matrix)

# ordered list of terms
print("\nIDX -> terms mapping:\n")
print(cv.get_feature_names_out())

# double-check
terms = cv.get_feature_names_out()

print("First term (with row index 0):", terms[0])
print("Third term (with row index 2):", terms[2])

#map the other way around, from term to index
print("\nterm -> IDX mapping:\n")
print(cv.vocabulary_) # note the _ at the end


#.vocabulary_ (with a trailing underscore) is a Python dictionary
print("Row index of 'example':", cv.vocabulary_["example"])
print("Row index of 'silly':", cv.vocabulary_["silly"])



#simple searches
t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
print("Query: example")
print(td_matrix[t2i["example"]])

# AND
print("Query: example AND great")
print("example occurs in:                            ", td_matrix[t2i["example"]])
print("great occurs in:                              ", td_matrix[t2i["great"]])
print("Both occur in the intersection (AND operator):", td_matrix[t2i["example"]] & td_matrix[t2i["great"]])

# OR
print("Query: is OR see")
print("is occurs in:                            ", td_matrix[t2i["is"]])
print("see occurs in:                           ", td_matrix[t2i["see"]])
print("Either occurs in the union (OR operator):", td_matrix[t2i["is"]] | td_matrix[t2i["see"]])

# NOT
print("Query: NOT this")
print("this occurs in:                     ", td_matrix[t2i["this"]])
print("this does not occur in (complement):", 1 - td_matrix[t2i["this"]]) # 1 - x changes 1 to 0 and 0 to 1

# MORE COMPLEX
print("Query: ( example AND NOT this ) OR nothing")
print("example occurs in:                  ", td_matrix[t2i["example"]])
print("this does not occur in:             ", 1 - td_matrix[t2i["this"]])
print("example AND NOT this:               ", td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]]))
print("nothing occurs in:                  ", td_matrix[t2i["nothing"]])
print("( example AND NOT this ) OR nothing:", 
      (td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]])) | td_matrix[t2i["nothing"]])


# query parser
# Operators and/AND, or/OR, not/NOT become &, |, 1 -
# Parentheses are left untouched
# Everything else is interpreted as a term and fed through td_matrix[t2i["..."]]

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    print()

test_query("example AND NOT nothing")
test_query("NOT example OR great")
test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
test_query("( not example or great ) and nothing") # ... or all small letters
test_query("not example and not nothing")

#sparse matrix
print(sparse_matrix)

#convert the sparse matrix to CSC format
print(sparse_matrix.tocsc())

#we want a term-document matrix, so let's transpose:
print(sparse_matrix.T)

#so-called inverted index:
sparse_td_matrix = sparse_matrix.T.tocsr()
print(sparse_td_matrix)

#redefine the rewrite_token() function
def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

test_query("NOT example OR great")

#Show retrieved documents
hits_matrix = eval(rewrite_query("NOT example OR great"))
print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
print("The coordinates of the non-zero elements:", hits_matrix.nonzero())  

#extract array and convert it from a NumPy array to an ordinary Python list:
hits_list = list(hits_matrix.nonzero()[1])
print(hits_list)

#retrieve the matching documents

for doc_idx in hits_list:
    print("Matching doc:", documents[doc_idx])

#enumerate the documents
for i, doc_idx in enumerate(hits_list):
    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))


### HOMEWORK
# 1. Ask the user to type the query. Make this run in a loop, so that the user can run as many queries they like. Also come up with some user input that tells the program to quit, such as an empty string or a specific keyword. Type your code here: 

# a) Ask the user to type the query (issue #11): 

input = input("Please type in one of the following words: and, better, example, great, here, is, long, nothing, see, silly, this, to: ")
print(td_matrix[t2i[input]])

# 2.Your search application should print the contents of the retrieved documents. (A vector consisting of ones and zeros won't do!) If there are too many matching documents, maybe you want to show only the top n documents. (Still you could print out how many matching documents there are in total.) If the documents are long, maybe you want to truncate the output to the m first words or characters only. Type your code here: 

# Akseli's notes: These two functions do the following. retrieve_matches() takes the query string and returns a hit list of found matches using the functions defined in the course material. Function print_retrieved() takes this hit list and prints the contents of the documents that matched. The variable print limit determines how many search results we want to print. In future we might add a feature that only prints a certain number of character's but since I'm just using the documents in the course materials, it's not a problem currently. It can easily be altered later.

def retrieve_matches(query):
    hits_matrix = eval(rewrite_query(query))
    hits_list = list(hits_matrix.nonzero()[1])
    return hits_list
        
def print_retrieved(hits_list):
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

# 3. If you just copy the code from the tutorial, your program will crash if you enter a word (term) that does not occur in any document in the collection. Modify your program to work correctly also in the case that a term is unknown. Type your code here: 

# 4. Have you noticed that not all words in the toy data were actually indexed by the code in the tutorial? Which ones? Would you like to index all words containing alpha-numerical characters? Can you solve that? Type your code here: 

# 5. This task is important. You need to index some "real" documents from a text file. When you run your program, it should start by reading document contents from a file and index these documents. After this, the user should be able to type queries and retrieve matching documents. Initially, you can use our example data sets: One contains 100 articles extracted from English Wikipedia and the other contains 1000 articles extracted from English Wikipedia (with topics mostly starting with the letter A). When you read these files, you need to produce a list of strings, such that an entire article (document) is in one string. You can locate the boundaries between two articles from the </article> tag, which always occurs on a line of its own in the file. The text is UTF-8 encoded. Type your code here: 

# 6. If you like, you can use some other data, for instance a Wikipedia dump for some other language, such as Finnish: https://linguatools.org/tools/corpora/wikipedia-monolingual-corpora/. First you need to download a Wikipedia XML file. Then you need to uncompress it with bunzip2. Then you need to convert the XML format to plain text using the Perl script xml2txt.pl, which is available for download on the web page. You need to use the option -articles in order to preserve the article tags: perl xml2txt.pl -articles INPUT_FILE.xml OUTPUT_FILE.txt. Type your code here: 
