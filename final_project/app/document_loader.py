# app/document_loader.py

import json

def load_documents(file_path):
    documents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
## This loop works on the sample database, but need to be modified if the keys change as the dadtabase develops
## The metadata and link parts are left out but can be added if needed
    for year, cases in data.items():
        for case_info in cases.values():  
            text_content = []
            
            if "Title" in case_info:
                text_content.append("Title:")  
                text_content.append(case_info["Title"])
            
            if "Description" in case_info:
                text_content.append("Description:")
                text_content.extend(case_info["Description"])
            
            for section in ["Asian käsittely alemmissa oikeuksissa", "Muutoksenhaku Korkeimmassa oikeudessa", "Korkeimman oikeuden ratkaisu"]:
                if section in case_info and "Contents" in case_info[section]:
                    text_content.append(f"\n{section}:")
                    text_content.extend(case_info[section]["Contents"])
            
            documents.append("\n".join(text_content))

    return documents



