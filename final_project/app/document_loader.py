import json

class LexDatabase:
    def __init__(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file) 
        
        self.data = data
        
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
                
                for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu", "Lower Courts", "Decision of the Supreme Court", "Appeal to the Supreme Court"]:
                    if section in case_info and "Contents" in case_info[section]:
                        text_content.append(f"\n{section}:")
                        text_content.extend(case_info[section]["Contents"])
                
                
                documents.append("\n".join(text_content))

        return documents
    
if __name__ == "__main__":
    file_path = '../data/en_sample_database.json'
    db = LexDatabase(file_path)
    docs = db.documents()
    
    
    
