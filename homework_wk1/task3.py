import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://arthousecinemaniagara.fi/fi/tulossa'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
soup = soup.find("div", {"id": "posterlist"})


movies = []

for movie in soup.find_all("a", {'class': 'row posterlistbox'}):
   title = movie.find('h1').get_text(strip=True)
   text = movie.find("div", {'class': 'posterlist-text'}).get_text(strip=True)

   

   movies.append({   
      'title': title,
      'description': text
      }
   )
  
  



movies_df = pd.DataFrame(movies)
print(movies_df)