import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os

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
        
def append_json(data : dict, file_path : str): 
    if os.path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, dict):
                    existing_data = {}  
            except json.JSONDecodeError:
                existing_data = {}  
    else:
        existing_data = {}
        
    existing_data.update(data)
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
### END OF CRAWLING

def paragraphs(soup):    
    data = {}
    
    title = soup.find('h2', id='skip').text
    data['Title'] = title
    
     ### Metadata 
    metadata = soup.find('table', class_='metadata')
    
    metadata_d = {}
    for field in metadata.find_all('tr'):
        
        field_head = field.find('th').text
        field_data = field.find('td').text
        
        metadata_d[field_head] = field_data
        
    data['Metadata'] = metadata_d
    data['Metadata']['Keywords'] = [keyword.text for keyword in soup.find('h3', class_='asiasanat').find_all('strong')] #finds keywords and adds them to metadata
    
    ### Text contents
    current_heading = None
    higher_heading = None
    first_go = True
    higher_heading_last = False #Previous tag was 'h4'
    paragraph_last = False
    
    for tag in soup.find_all(['h4', 'h5', 'p']):
        #print(soup.find_all(['h4', 'h5', 'p']))
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
    
    return data

def tidy_document(doc : dict, link : str):
    print("processing:", doc['Title'])
    doc['Metadata']['Link'] = link
    
    #doc['Proceedings in lower courts'] = {}
    #if "Asian käsittely lunastustoimituksessa ja maaoikeudessa"  in doc.keys():
    #    for section in doc["Asian käsittely lunastustoimituksessa ja maaoikeudessa"]:
    #            if section is not "Contents":
    #                doc['Proceedings in lower courts'][section] = doc["Asian käsittely lunastustoimituksessa ja maaoikeudessa"][section]
    #    del doc["Asian käsittely lunastustoimituksessa ja maaoikeudessa"]
    
    #elif "Asian käsittely alemmassa oikeudessa" in doc.keys():
    #    doc['Proceedings in lower courts']["Contents"] = doc["Asian käsittely alemmassa oikeudessa"]["Contents"]
    #    
    #    del doc["Asian käsittely alemmassa oikeudessa"]
    #    
    #else:
    #    if len(doc['Asian käsittely alemmissa oikeuksissa'].keys()) == 1:
    #        doc['Proceedings in lower courts']["Contents"] = doc["Asian käsittely alemmissa oikeuksissa"]["Contents"]
    #    else:
    #        for section in doc["Asian käsittely alemmissa oikeuksissa"]:
    #            if section is not "Contents":
    #                doc['Proceedings in lower courts'][section] = doc["Asian käsittely alemmissa oikeuksissa"][section]
    #    del doc["Asian käsittely alemmissa oikeuksissa"]
    
    #doc['Appeal to the Supreme Court'] = []
    #for text in doc["Muutoksenhaku Korkeimmassa oikeudessa"]["Contents"]:
    #    doc['Appeal to the Supreme Court'].append(text)
        
    #doc['Decision of the Supreme Court'] = {}
    #for section in doc["Korkeimman oikeuden ratkaisu"]:
    #    if section == "Contents":
    #        doc['Decision of the Supreme Court']["Contents"] = doc["Korkeimman oikeuden ratkaisu"][section]
    #    if section == "Perustelut":
    #        doc['Decision of the Supreme Court']["Reasoning"] = doc["Korkeimman oikeuden ratkaisu"][section]
    #    if section == "Tuomiolauselma":
    #        doc['Decision of the Supreme Court']["Resolution"] = doc["Korkeimman oikeuden ratkaisu"][section]
    #    if section == "Eri mieltä olevan jäsenen lausunto":
    #        doc['Decision of the Supreme Court']["Statements of Dissenting Members"] = doc["Korkeimman oikeuden ratkaisu"][section]            
            
    
    #del doc["Muutoksenhaku Korkeimmassa oikeudessa"]
    #del doc["Korkeimman oikeuden ratkaisu"]
    #del doc["Sisällysluettelo"]
    
    return doc

def scrape_links(start_yr, end_yr, file_path):
    with open("data/lex_links.json") as json_file:
        data = json.load(json_file)
        
    res = {}
    for year in range(start_yr, end_yr+1):
        links = data[str(year)]["links_to_judgements"]
        res[str(year)] = {}
        for link in links:
            soup = fetch_content(link)
            doc = paragraphs(soup)
            doc = tidy_document(doc, link)
            res[str(year)][doc['Title']] = doc
            time.sleep(2)
    
    store_as_json(res, file_path)    
          

if __name__ == "__main__":
    #links = crawl_finlex(append_year=True)
    #add_year_to_links()
    #store_as_json(links)
    #print(scrape_links(2023, 2025))
    
    #url = "https://www.finlex.fi/fi/oikeus/kko/kko/2025/20250017"
    #soup = fetch_content(url)
    #doc = paragraphs(soup)
    #doc = tidy_document(doc, url)
    #path = "data/sample_data.json"
    #store_as_json(doc, path)
    
    scrape_links(2023, 2025, "data/en_sample_database.json")