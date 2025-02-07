import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def parse_html(soup):
    data = []
    data.append(soup.find('title').text)
    data.append(soup.find('h3', class_="asiasanat").text)
    return data

if __name__ == "__main__":
    url = "https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250017"
    soup = fetch_content(url)
    #print(soup.prettify())
    print(parse_html(soup))