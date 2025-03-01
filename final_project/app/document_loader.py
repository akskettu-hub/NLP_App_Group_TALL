import json

class LexDatabase:
    def __init__(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file) 
        
        self.data = data
        
    def documents(self): # Handles loading documents originally from neural search and modified
        documents = []
        
        
        for year in self.data.keys():
            for case in self.data[year].keys():
                  
                doc = {}
                
                doc["Title"] = self.data[year][case]['Title']
                    
                doc['Link'] = self.data[year][case]['Metadata']['Link']
                doc['Diaarinumero'] = self.data[year][case]['Metadata']['Diaarinumero:']
                doc['Antopäivä'] = self.data[year][case]['Metadata']['Antopäivä:']
                
                doc['Description'] = self.data[year][case]["Description"]
                
                for section in ["Lower Courts", "Appeal to the Supreme Court", "Decision of the Supreme Court"]:
                    
                    doc[section] = ""
                    for subsection in self.data[year][case][section].keys():
                        for item in self.data[year][case][section][subsection]:
                            doc[section] += item
                            
            documents.append(doc)

        return documents
    
    def descriptions(self, documents):
        desc = []
                
        for doc in documents:
            doc
        
        return desc
        
    
if __name__ == "__main__":
    file_path = 'data/database.json'
    db = LexDatabase(file_path)
    docs = db.documents()
    
    print(len(docs))
    print(json.dumps(docs[0], indent = 4, ensure_ascii=False))
    
    
    
    
