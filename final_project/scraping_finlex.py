import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

### Fetches data from Soup. Assigns data to dictionary, where each key is a type of data and the value is the contents as text
def parse_html(soup):
    doc = {}
        
    doc_id = soup.find('title').text # document id, for example 'KKO:2025:17 - Korkeimman oikeuden ennakkopäätökset - FINLEX ®'
    doc_id = doc_id.split(' -', 1)[0] # Cleans text to just 'KKO:2025:17'
    doc['Doc_id'] = doc_id
    
    subject_matter = soup.find('h3', class_="asiasanat").text # subject matter of the case/title. For example, Lapsen huolto ja tapaamisoikeus.
    doc['Subject'] = subject_matter
    
    metadata = soup.find('table', class_="metadata").text # Case metadata
    doc['Metadata'] = metadata
    
    document = soup.find('div', id="document").text # All of the text of the document here in text format. All the text of the document is stored within this tags.
    return doc

def paragraphs(soup):
    
    headings = soup.find_all(['h4', 'h5'])
    
    data = {}
    current_heading = None
    higher_heading = None
    first_go = True
    higher_heading_last = False #Previous tag was 'h4'
    paragraph_last = False
    
    for tag in soup.find_all(['h4', 'h5', 'p']):
        tag_name = tag.name
        if tag_name in ['h4', 'h5']:
            if tag_name == 'h4':
                higher_heading = tag.get_text(strip=True)
                data[higher_heading] = {}  # Initialize an empty list for subheadings
                higher_heading_last = True
            elif not first_go:
                # New heading found, update current heading
                current_heading = tag.get_text(strip=True)
                data[higher_heading][current_heading] = []   # Initialize an empty list for paragraphs
                higher_heading_last = False
            else:
                data['Description'] = []
                current_heading = 'Description'
                first_go = False
            paragraph_last = False
            
        elif tag_name == 'p' and current_heading:
            if higher_heading_last:
                if not paragraph_last:
                    data[higher_heading]['Contents'] = []
                    data[higher_heading]['Contents'].append(tag.get_text(strip=True))
                else:
                    data[higher_heading]['Contents'].append(tag.get_text(strip=True))
            elif current_heading == 'Description':
                data[current_heading].append(tag.get_text(strip=True))    
            else:         
                # Add paragraph text to the last found heading
                data[higher_heading][current_heading].append(tag.get_text(strip=True))
            
            paragraph_last = True
    
    #data['Description'] = data['Dokumentin versiot'] 
    #del data['Dokumentin versiot']
    
    return data

if __name__ == "__main__":
    url = "https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250017"
    soup = fetch_content(url)
    #print(soup.prettify())
    #print(parse_html(soup))
    p = paragraphs(soup)
    print(p.keys())
    print(p['Description'])
    print(p['Muutoksenhaku Korkeimmassa oikeudessa'])
    print(p['Korkeimman oikeuden ratkaisu'])
    #print(p['Asian käsittely alemmissa oikeuksissa'])
    #print(p['Päätöslauselma'])
    #print(p['Dokumentin versiot'])
    print()
    
    
    url = "https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250002"
    soup = fetch_content(url)
    #print(soup.prettify())
    #print(parse_html(soup))
    p = paragraphs(soup)
    print(p.keys())
    #print(p['Dokumentin versiot'])
    #print(p['Description'])
    print(p['Description'])
    print(p['Muutoksenhaku Korkeimmassa oikeudessa'])
    print(p['Korkeimman oikeuden ratkaisu'])