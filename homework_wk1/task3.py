import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://arthousecinemaniagara.fi/fi/tulossa'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
soup = soup.find("div", {"id": "posterlist"})


movies = []

for movie in soup.find_all("a", {'class': 'row posterlistbox'}):
   title = movie('h1')
   text = movie("div", {'class': 'posterlist-text'})

   

   movies.append({   
      'title': title,
      'description': text
      }
   )
  
  



movies_df = pd.DataFrame(movies)
print(movies_df)