import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

### CRAWLING: The Following functions crawl through the site and find all links on all pages: The links for all year, links for all pages for year, and links for all judgements on each page.
# Fetch all year pages. Returns dicionary, with year as key and dictionary as value. This inner dict contains the link to each year page as value. This is so that all years are their own dictionary and all metainfo about that year can be stored in a single dict, e.g. links, how many judgements, possible format info, etc. 
def fetch_links_years():
    url = "https://www.finlex.fi/fi/oikeus/kko/kko/"
    soup = fetch_content(url)
    links_html = soup.find('div', class_="year-toc-container")
    
    links = {}
    for link in links_html.find_all('a'):
        links[link.text] = {}
        links[link.text]["link_year_page"] = "https://www.finlex.fi" + link.get("href")
    return links

def fetch_page_links_for_year(url : str):
    soup = fetch_content(url)
    links_html = soup.find('div', class_="result-pages")
    
    links = []
    if links_html is None:
        links.append(url)
        return links
    
    links.append(url+"?_offset=0")
    
    links_raw = links_html.find_all('a')
        
    for link in links_raw:
        links.append("https://www.finlex.fi" + link.get("href"))
        
    return links

def fetch_links_on_page(url : str):
    soup = fetch_content(url)
    links_html = soup.find('dl', class_="docList")
    links_raw = links_html.find_all('a')
    
    links = []
    for link in links_raw:
        links.append("https://www.finlex.fi" + link.get("href"))
    return list(set(links))

# give start year and end year as arguments, defaults to maximum range
def crawl_finlex(start_yr=1926, end_yr=2025, append_year=False):
    year_links = fetch_links_years()
    
    for year in year_links:
        if int(year) in range(start_yr, end_yr + 1): 
            #print(year, year_links[year]['link_year_page'])
            year_links[year]['links_pages_for_year'] = fetch_page_links_for_year(year_links[year]['link_year_page'])
            jdgmnt_links_for_year = []
            
            for page_url in year_links[year]['links_pages_for_year']:
                
                links_on_page = fetch_links_on_page(page_url)
                for link in links_on_page: jdgmnt_links_for_year.append(link)
                
            jdgmnt_links_for_year = sorted(jdgmnt_links_for_year, reverse=True)
            year_links[year]['links_to_judgements'] = jdgmnt_links_for_year
            
            if append_year: #If store every year, the code rewrites the dict to json file after every loop. This is incase you want to scrape a lot of links, and are worried about the programme failing without finishing, off by default
                store_as_json(year_links)      
                
    return year_links
        
def store_as_json(file_d : dict, url : str):
    with open(url, "w", encoding="utf-8") as outfile: 
        json.dump(file_d, outfile, indent = 4, ensure_ascii=False)
        
### END OF CRAWLING

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
    
    title = soup.find('h2', id='skip').text
    data['Title'] = title
    
    metadata = soup.find('table', class_='metadata')
    metadata_d = {}
    
    #data['Metadata'] = metadata.get_text(strip=True)
    
    for field in metadata.find_all('tr'):
    #    
        field_head = field.find('th').text
        field_data = field.find('td').text
        
        metadata_d[field_head] = field_data
        
    data['Metadata'] = metadata_d
 
    
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

def scrape_links(start_yr, end_yr):
    with open("data/lex_links.json") as json_file:
        data = json.load(json_file)
    res = {}
    for year in range(start_yr, end_yr+1):
        links = data[str(year)]["links_to_judgements"]
        res[str(year)] = {}
        for link in links:
            soup = fetch_content(link)
            doc = paragraphs(soup)
            doc['link'] = link
            res[str(year)][doc['Title']] = doc
            time.sleep(2)
    path = "data/sample_database.json"
    store_as_json(res, path)    
    
            

if __name__ == "__main__":
    #links = crawl_finlex(append_year=True)
    #add_year_to_links()
    #store_as_json(links)
    #print(scrape_links(2023, 2025))
    
    #url = "https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250014"
    #soup = fetch_content(url)
    #doc = paragraphs(soup)
    #path = "data/sample_data.json"
    #store_as_json(doc, path)
    
    scrape_links(2025, 2025)