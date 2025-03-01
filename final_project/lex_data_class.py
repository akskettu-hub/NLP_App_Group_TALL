import json

class Lex_Database:
    def __init__(self):
        with open("data/database.json") as json_file:
            data = json.load(json_file) 
        
        self.data = data
        
    def text_rage():
        pass
    
    