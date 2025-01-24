# Code for task 3, and therefore a little messy.
# Prints when weather was last updated on the FMI website and latest articles published on cracked.com (in dataframe format)
# Planned on extracting weather information but found that too tricky
# Demonstrates basics of webscraping

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

#Fetches info on when the weather report was las updated. 
def report_updated_FMI(soup):
    header_panel = soup.find('div', class_="row local-weather-header-panel mx-0 mb-3 pt-3")
    elements = header_panel.find_all('span')

    rows = []
    for element in elements:
        text = element.text
        rows.append(text)
    
    last_updated = rows[0] + rows[1]
    
    return last_updated

#Fetches latest articles from cracked.com and puts each article and its data into a dictonary for easy pandas dataframe.
def latest_cracked(soup):
    latest = soup.find('div', class_="right")
    articles = latest.find_all('article')
    
    text_articles = []
    for article in articles:
        title = article.find('h2').text
        date = article.find('time').text
        topic = article.find('label').text
        author = article.find('dd').a.text
        link = article.find('h2').a['href']
    
        text_articles.append({"Title" : title, "Date Published" : date, "Topic" : topic, "Author" : author, "Link" : link})
        
    return text_articles

def df_from_dict(list_dicts : dict):
    df = pd.DataFrame(list_dicts)
    df['Author'] = df['Author'].str.replace(",", "")
    return df
    

if __name__ == "__main__":
    url = "https://www.ilmatieteenlaitos.fi/saa/espoo"
    soup = fetch_content(url)
    data = report_updated_FMI(soup)

    print(data)
    
    url = "https://en.ilmatieteenlaitos.fi/local-weather/espoo"
    soup = fetch_content(url)
    data = report_updated_FMI(soup)

    print(data)
    
    url = "https://www.cracked.com/"
    cracked_soup = fetch_content(url)
    cracked_df = df_from_dict(latest_cracked(cracked_soup))
    
    print(cracked_df)