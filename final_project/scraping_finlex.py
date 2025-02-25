import requests
from bs4 import BeautifulSoup
import json
import time
import datetime 
import os

def store_as_json(file_d : dict, filepath : str):
    with open(filepath, "w", encoding="utf-8") as outfile: 
        json.dump(file_d, outfile, indent = 4, ensure_ascii=False)

def fetch_content(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

### Link scraping: The Following functions crawl through the site and find all links on all pages: The links for all year, links for all pages for year, and links for all judgements on each page.
def fetch_links_years(): # Fetch all year pages. Returns dicionary, with year as key and dictionary as value. This inner dict contains the link to each year page as value. This is so that all years are their own dictionary and all metainfo about that year can be stored in a single dict, e.g. links, how many judgements, possible format info, etc. 
    url = "https://www.finlex.fi/fi/oikeus/kko/kko/"
    soup = fetch_content(url)
    links_html = soup.find('div', class_="year-toc-container")
    
    links = {}
    for link in links_html.find_all('a'):
        links[link.text] = {}
        links[link.text]["link_year_page"] = "https://www.finlex.fi" + link.get("href")
    return links

def fetch_page_links_for_year(url : str): # Fetch all pages for a given year
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

def fetch_links_on_page(url : str): # Fetch all links on a given page for a given year.
    soup = fetch_content(url)
    links_html = soup.find('dl', class_="docList")
    links_raw = links_html.find_all('a')
    
    links = []
    for link in links_raw:
        links.append("https://www.finlex.fi" + link.get("href"))
    return list(set(links))

def fetch_all_links():
    end_yr = datetime.datetime.now().year # End year is current year
    
    year_links = fetch_links_years()
    
    for year in year_links:
        print("Getting links for ", year)
        if int(year) in range(1926, end_yr + 1): 
            year_links[year]['links_pages_for_year'] = fetch_page_links_for_year(year_links[year]['link_year_page'])
            jdgmnt_links_for_year = []
            
            for page_url in year_links[year]['links_pages_for_year']:
                
                links_on_page = fetch_links_on_page(page_url)
                for link in links_on_page: jdgmnt_links_for_year.append(link)
                
            jdgmnt_links_for_year = sorted(jdgmnt_links_for_year, reverse=True)
            year_links[year]['links_to_judgements'] = jdgmnt_links_for_year
                
    return year_links

### This function checks if links database exists. If not, it creates it from scratch. If it does, it will check if years are missing from the database. If yes, it adds them to database. If not, it checks that  the links for the current year are up to date. Update_existing parameter determines whether link database is updated. 
def links(file_path : str, update_existing=True):
    if not os.path.isfile(file_path): # If link file does not already exist, find all links to all judgements and save them as .json.
        links = fetch_all_links()
        store_as_json(links, file_path)
        
    else: # If file does already exist, find all links for current year and add them to current years links. This ensures that the latest links are added to the link database.
        if not update_existing: 
            print("Link database found. Not updating.")
        else:
            print("File found. Checking for updates to database...")
            
            with open(file_path, 'r') as file:
                data = json.load(file)

            current_year = datetime.datetime.now().year # Current year
            
            years_in_database = [int(year) for year in data.keys()]
            missing_years = [year for year in range(1926, current_year + 1) if year not in years_in_database]
            
            if len(missing_years) > 0: # if a year or more is missing, add years to data
            
                for year in missing_years:
                    
                    url = "https://www.finlex.fi/fi/oikeus/kko/kko/" + str(year) + "/"
                    pages = fetch_page_links_for_year(url)
                    
                    links = []
                    for page in pages:
                        links_on_page = fetch_links_on_page(page)
                        for link in links_on_page:
                            links.append(link)
                    links = sorted(links, reverse=True)
                    
                    data[str(year)] = {}
                    data[str(year)]["link_year_page"] = url 
                    data[str(year)]["links_pages_for_year"] = pages
                    data[str(year)]["links_to_judgements"] = links
                    
                    print("Links database updated. Entry for the year", year, "added.", len(links), "links added.")
                
                store_as_json(data, file_path)  
            
            else: 
                url = "https://www.finlex.fi/fi/oikeus/kko/kko/" + str(current_year) + "/"
                pages = fetch_page_links_for_year(url)
                        
                links = []
                for page in pages:
                    links_on_page = fetch_links_on_page(page)
                    for link in links_on_page:
                        links.append(link)
                links = sorted(links, reverse=True)
                    
                if len(data[str(current_year)]["links_to_judgements"]) < len(links): # links are missing, update link list and page link list.
                    links_added = len(links) - len(data[str(current_year)]["links_to_judgements"])
                    data[str(current_year)]["links_pages_for_year"] = pages
                    data[str(current_year)]["links_to_judgements"] = links
                    store_as_json(data, file_path)
                    print("Links database updated.", links_added, "links added.")
                else: print("Links database already up to date.")        
### End of link scraping

### Judgement scraping

def scrape_document(soup):    
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
        
        if tag.name in ['h4', 'h5']:
            if tag.name == 'h4':
                if current_heading == 'Description':
                    higher_heading = "Lower Courts"
                    current_heading = "Lower Courts"
                    data[higher_heading] = {}  # Initialize an empty list for subheadings
                elif higher_heading == "Lower Courts":
                    higher_heading = "Appeal to the Supreme Court"
                    data[higher_heading] = {}
                    
                elif higher_heading == "Appeal to the Supreme Court":
                    higher_heading = "Decision of the Supreme Court"
                    current_heading = "Decision of the Supreme Court"
                    data[higher_heading] = {}
                higher_heading_last = True
            elif not first_go:
                current_heading = tag.get_text(strip=True)
                data[higher_heading][current_heading] = []   # Initialize an empty list for scrape_document
                higher_heading_last = False
            else: 
                data['Description'] = []
                current_heading = 'Description'
                first_go = False
            paragraph_last = False
            
        elif tag.name == 'p' and current_heading:
            if higher_heading_last:
                if not paragraph_last:
                    data[higher_heading]['Contents'] = []
                    data[higher_heading]['Contents'].append(tag.get_text(strip=True))
                else:
                    data[higher_heading]['Contents'].append(tag.get_text(strip=True))
            elif current_heading == 'Description':
                data[current_heading].append(tag.get_text(strip=True))
            elif higher_heading == 'Decision of the Supreme Court' and current_heading == "Decision of the Supreme Court":
                current_heading = "Start of DSC" 
                
            else:
                data[higher_heading][current_heading].append(tag.get_text(strip=True))
            paragraph_last = True
    
    return data

def tidy_document(doc : dict, link : str):
    print("Processing:", doc['Title'])
    doc['Metadata']['Link'] = link
    
    delete_l = ["Lainsäädäntö",
                "Oikeuskäytäntö",
                "Viranomaiset",
                "Valtiosopimukset",
                "Hallituksen esitykset",
                "Julkaisut",
                "Finlex®"
                ]
    try:
        if "Decision of the Supreme Court" in doc:
            for item in delete_l:
                if item in doc["Decision of the Supreme Court"]:
                    del doc["Decision of the Supreme Court"][item]
                
            if 'Contents' in doc["Decision of the Supreme Court"]:
                del doc["Decision of the Supreme Court"]['Contents']
                            
        if len(doc["Lower Courts"].keys()) > 1:
            del doc["Lower Courts"]['Contents']
    except:
        print(doc['Title'], "failed to process. Link:", doc['Metadata']['Link'])
    return doc

def tidy_swedish(path):
    with open(path) as json_file:
        data = json.load(json_file)
    headings = ["Description",
               "Lower Courts",
               "Appeal to the Supreme Court",
               "Decision of the Supreme Court"
               ]
    swe = {}    
    for year in data.keys():
        for doc in data[year].keys():
            for heading in headings:
                if heading not in data[year][doc].keys():
                    if data[year][doc]['Title'] not in swe.keys():
                        swe[data[year][doc]['Title']] = data[year][doc]
            
                
    store_as_json(swe, "data/swe_debug.json")
    
def build_new_database(start_yr, end_yr, file_path, sleep_int : int): #sleep_int determines how long the programme sleeps after each individual page is scraped. 
    with open("data/links.json") as json_file:
        data = json.load(json_file)
        
    res = {}
    for year in range(start_yr, end_yr+1):
        links = data[str(year)]["links_to_judgements"]
        res[str(year)] = {}
        for link in links:
            soup = fetch_content(link)
            doc = scrape_document(soup)
            
            tidy_document(doc, link)
            res[str(year)][doc['Title']] = doc
            time.sleep(sleep_int)
    
        store_as_json(res, file_path) # Stores res after yeach year has been scraped, so that if proccess is interrupted at least something is saved to disc.
        
### END OF Judgement scraping
          
def check_database(path): #for debugging.
    with open(path) as json_file:
        data = json.load(json_file)
    headings = {}    
    for year in data.keys():
        for doc in data[year].keys():
            for key in data[year][doc].keys():
                if key not in headings.keys():
                    headings[key] = 1
                else:
                    headings[key] += 1
                
    print(headings)
        
if __name__ == "__main__":
    #path = "data/links.json"
    #links(path)
    
    build_new_database(2015, 2025, "data/test_database1.json", 0)
    
    #check_database("data/test_database.json")
    #tidy_swedish("data/test_database.json")
    #url = "https://www.finlex.fi/fi/oikeus/kko/kko/2021/20210017"
    #soup = fetch_content(url)
    #doc = scrape_document(soup)
    #store_as_json(doc, "debug.json")