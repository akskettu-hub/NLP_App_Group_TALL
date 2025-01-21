# This is and empty python file for initial commit purposes
#what happens if I add a line
import requests
from bs4 import BeautifulSoup

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

#Fetches info on when the wether report was las updated. 
def report_updated(soup):
    header_panel = soup.find('div', class_="row local-weather-header-panel mx-0 mb-3 pt-3")
    elements = header_panel.find_all('span')

    rows = []
    for element in elements:
        text = element.text
        rows.append(text)
    
    last_updated = rows[0] + rows[1]
    
    return last_updated

url = "https://www.ilmatieteenlaitos.fi/saa/espoo"
soup = fetch_content(url)
data = report_updated(soup)

print(data)