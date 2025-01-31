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
        print(hits_list)

        for doc_idx in hits_list:
            print("Matching doc:", documents[doc_idx])    
loop()
