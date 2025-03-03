import json
#from ntest import embedd_doc, cosine_similarities, neural_search, neural_search_results
class LexDatabase:
    def __init__(self, file_path):
        with open(file_path, encoding="utf-8") as json_file:
            data = json.load(json_file) 
        
        self.data = data
        self.doc_dict = self.documents_dict()
        self.contents = self.text_contents(self.doc_dict)
        self.embeddings = []
        
    def documents(self): # Handles loading documents originally from neural search and modified
        documents = []
        
        for year, cases in self.data.items():
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
                #Akseli's note, this does not get all the contents of these fields, btw.
                for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu", "Lower Courts", "Decision of the Supreme Court", "Appeal to the Supreme Court"]: # Added current headings
                    if section in case_info and "Contents" in case_info[section]:
                        text_content.append(f"\n{section}:")
                        text_content.extend(case_info[section]["Contents"])
                
                
                documents.append("\n".join(text_content))

        return documents
    
    def documents_dict(self): # This returns the documents in dict format in a list if that is easier for some applications
        documents = []
        
        
        for year in self.data.keys():
            for case in self.data[year].keys():
                    
                doc = {}
                
                doc["Title"] = self.data[year][case]['Title']
                    
                doc['Link'] = self.data[year][case]['Metadata']['Link']
                doc['Diaarinumero'] = self.data[year][case]['Metadata']['Diaarinumero:']
                doc['Antopäivä'] = self.data[year][case]['Metadata']['Antopäivä:']
                
                doc['Description'] = ' '.join(self.data[year][case]["Description"])
                
                for section in ["Lower Courts", "Appeal to the Supreme Court", "Decision of the Supreme Court"]:
                    
                    doc[section] = ""
                    for subsection in self.data[year][case][section].keys():
                        for item in self.data[year][case][section][subsection]:
                            doc[section] += item
                            
            documents.append(doc)

        return documents
    
    def add_document_embeddings(self, embeddings):
        for item in embeddings:
            self.embeddings.append(item)
        
    
    def text_contents(self, documents): #return text contents and title
        contents = []
        for doc in documents:
            data = []
            data.append(doc["Title"])
            #text = ""
            #text += documents[doc]["Description"]
            data.append(doc["Description"])
            
            contents.append(data)
        return contents    
        pass

if __name__ == "__main__":
    file_path = '../data/database.json'
    db = LexDatabase(file_path)
    docs = db.documents_dict()
    
    print(docs[0])
    contents = db.text_contents(docs)
    print(contents[0])
    #print(db.contents[0])
    #db.add_document_embeddings(embedd_doc(db.contents))
    
    print(db.embeddings[0])
    query = "fraud"
    
    #sim = cosine_similarities(db.embeddings, query)
    
    #print(sim[:10]) 
    
    #sim = cosine_similarities1(db.contents, query)
    
    #print(sim[:10]) 
    
    #docs_old = db.documents()
    
    #neural_search(docs_old)
    #result = neural_search_results(sim, db.doc_dict)
    
    #print(result)
    
