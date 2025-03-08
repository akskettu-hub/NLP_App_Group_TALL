# NLP_App_Group_TALL - final_project

## About our project
Hi! We are **Team TALL (Tzang, Aleksi, Liisa, Lisa) **! This repository is for the group project for the course **"Building NLP Applications"**.

Our project is a **search engine** designed to search within the **Supreme Court precedence rulings of Finland**. The goal of our application is to make these court rulings more open and accessible to the public and to non-finish speaking. 

The search engine supports multiple search modes:
- **Boolean Search**: Allows searching using logical operators (AND, OR, NOT) for precise results.
- **TF-IDF Search**: Uses term frequency-inverse document frequency to rank relevant documents.
- **Neural Search**: Supports **English queries** and finds relevant matches within **Finnish legal texts** using machine learning techniques.

## Data
The data for this project consists of the rulings of the Finnish Supreme Court from **2015-2025**, totaling **953 rulings**, scraped from **Finlex**, a public database for Finnish law and legal documents maintained by the **Finnish Ministry of Justice**. The data is stored in JSON format at the location `final_project/data/database.json`.

Due to an unexpected overhaul of the Finlex website, the initial intention of using all rulings from **1980-2025** was abandoned. The scraping script for the previous version of the website became non-functional, and given the time constraints, we decided to use the data that had already been collected (2015-2025). Despite this smaller dataset, the core functionality of the project remains intact.

## Structure
The database is structured so that at the highest level, each year is a key, and its value is a dictionary of all the cases for that year. Example:

```json
{"2015": { "case 1": ..., "case 2": ..., ... },
 "2016": { "case 1": ..., "case 2": ..., ... },
 ...
}
```

Each individual case is stored as follows:
```json
{ "2015": {
        "KKO:2015:105": {
            "Title": "KKO:2015:105",
            "Metadata": {
                "Diaarinumero": "S2012/695",
                "Antopäivä": "29.12.2015",
                "Taltio": "2490",
                "Keywords": ["example keyword"],
                "Link": "link to the ruling"
            },
            "Description": "Brief description of the case",
            "Lower Courts": "Background and proceedings in lower courts",
            "Appeal to the Supreme Court": "Details of the appeal",
            "Decision of the Supreme Court": "Final decision and reasoning"
        }
    }
}
```

## Scraping
These data were scraped from Finlex, a public database for Finnish law and legal documents maintained by the Finnish Ministry of Justice. The scraping code is available in `final_project/scraping_finlex.py`, primarily utilizing **BeautifulSoup**.

The scraping process involved multiple steps:
1. **Finding links to rulings**: This was done through a sequence of functions (`fetch_links_years()`, `fetch_page_links_for_year()`, and `fetch_links_on_page()`), which collectively automated the retrieval of ruling links.
2. **Scraping individual rulings**: The function `scrape_document()` extracted relevant legal content, though inconsistencies in the HTML structure required additional handling through `tidy_document()`.
3. **Finalizing the database**: Some documents had inconsistencies, requiring manual filtering via `check_database()` and `final_database()`. About **30 out of 983** rulings were removed.
4. **Storing the data**: The final dataset was structured and stored using `build_new_database()` in `final_project/data/database.json`.

## Data Handling in the App
### Document Loader
The script **document_loader.py** is responsible for handling all data when the app is running. It implements the **LexDatabase** class, which manages the in-app data. The search function scripts interact with **LexDatabase** to ensure modularity.

#### **LexDatabase Attributes**
- `self.data`: Stores the JSON-formatted database.
- `self.doc_dict`: A dictionary of all rulings with the format:
  ```json
  {
      "Title": "...",
      "Link": "...",
      "Diaarinumero": "...",
      "Antopäivä": "...",
      "Description": "...",
      "Lower Courts": "...",
      "Appeal to the Supreme Court": "...",
      "Decision of the Supreme Court": "..."
  }
  ```
- `self.contents`: Stores a list of tuples with **case titles** and **descriptions** for search indexing.
- `self.embeddings`: Stores document embeddings for **neural search**.
- `self.tf_matrix`: (Planned) Will contain the **TF-IDF matrix** for **TF-IDF search**.

## Search Functions
### **1. Boolean Search**
Performs **exact** matches for the given query using logical operators (`AND`, `OR`, `NOT`).

### **2. TF-IDF Search**
Ranks documents based on the statistical significance of words within the entire corpus.

### **3. Neural Search**
Utilizes transformer models for **semantic search**. The current implementation uses **distiluse-base-multilingual-cased-v2** from **Hugging Face**.

## How to run the search engine
The application must be run locally. Follow these steps:

### Installation
Ensure you have Python installed, then install dependencies:
```
pip install -r requirements.txt
```

### Running the project
After installation, navigate to the project directory and start the app:

On Linux/macOS:
```
export FLASK_APP=app.py
export FLASK_DEBUG=True
flask run
```

On Windows (Command Prompt):
```
set FLASK_APP=app.py
set FLASK_DEBUG=True
flask run
```

On Windows (PowerShell):
```
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "True"
flask run
```

Once the app is running, open **http://127.0.0.1:5000** in your browser.





# NLP_App_Group_TALL
A repository for the group project for the course "Building NLP Applications", Group TALL.

[The following is a description of the data and can be copy and pasted to wherever it makes sense in the read me]: #
## Data

The data for this project consists of the rulings of the Finnish Supreme Court from 2015-2025, totaling 953 rulings, scraped from [Finlex](https://www.finlex.fi/en), a public database for Finnish law and legal documents maintained by the Finnish Ministry of Justice. The data is stored in json format at the location `final_project/data/database.json`.

Due to an **[unexpected overhaul to the Finlex website](https://www.finlex.fi/en/information-about-the-upgrade)**, the initial intention of using all rulings from the years 1980-2025 was abandoned as the code that was used to scrape the previous version of the website did not work anymore. As this update happened in the final stretch of the project, it was decided that attemting to scrape the new version of the website was not feasible or sensible. Instead, the data that had already been scraped was used for this project, which happened to be for the years 2015-2025, would be used. Even with this smaller dataset, the core functionality of this project can still be demonstrated. 

### Structure
The database is structured so that at the highest level each year is a key and it's value is a dictionary of all the years in that year. For example:

```
{"2015" : { "case 1",
            "case 2",
            ...
            ...
          },

 "2016" : { "case 1",
            "case 2",
            ...
            ...
          },
 ...,
 ...
}
```

Each individual case is stored as follows, with a brief explainaion of the data typiclly contained in each field. For example:
```
{ "2015": {
        "KKO:2015:105": {
            "Title": " e.g. KKO:2015:105",
            "Metadata": {
                "Diaarinumero:": "e.g. S2012/695",
                "Antopäivä:": "date of ruling e.g. 29.12.2015",
                "Taltio:": "e.g. 2490",
                "Keywords": [keywords],
                "Link": "link to the ruling"
            },
            "Description": [ A brief description of the case ],
            "Lower Courts": { Proceedings of the case through the lower courts. Typically a description of the background of the case is incuded followed by procedings at each individual court. },
            "Appeal to the Supreme Court": { Describes the circumstances of the appeal made to the supreme court },
            "Decision of the Supreme Court": { Contains a description of the decision of the Supreme court. Typically contains the sections reasoning, the final decision, and possible dissenting oppions. }
                        }
        }
}
```
### Scraping
These data were scraped from [Finlex](https://www.finlex.fi/en), a public database for Finnish law and legal documents mainatied by the Finnish Ministry of Justice. The code used for scraping is available at the location `final_project/scraping_finlex.py`. The main tool use for scraping was [BeautifulSoup](https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)).

The code first scraped the website to find all the links to all the rulings. This entaield finding all the pages where links to rulings are found. The initial landing page was scraped for links to all years pages, all year pages were scraped to find all offset pages for that year, and all the offset pages were scraped for links to individual rulings. In `final_project/t/scraping_finlex.py` these were handled by the functions `fetch_links_years()`,  `fetch_page_links_for_year()`, and `fetch_links_on_page()`, which pulled all these links together with the function `fetch_all_links()`. The function `links()` automated the process of finding all links and storing them as a json file (the latest example of this is available in `data/links.json`). This function also automatically updated any links not already in `data/links.json` to possibly enable the app to keep up to date with the latest rulings. The change to the website on 27th of February made this function redundant, as scraping for links or indeed their content no longer works with the current website.

The scraping of the individual rulings was handled with the function `scrape_document()`, which scraped through a ruling, using the structure of the HTML to find the different sections found in each ruling. This was not a straightforward proccess because the structure of the HTML was not particularly clear and consistent across rulings, and the logic of `scrape_document()` is therefore quite complicated. Some rulings varied quite significantly from most other rulings and the function `tidy_document()` was implemented as a result. Even with this, some inconsistencies emerged in the data due to variability in the documents. It was decided that perfecting the database was too laboursome for the scope of this project, and documents that varied sigificantly enough to cause problems in the app were simply deleted with the functions `check_database()` and `final_database()`. This ended up being about 30 documents out of 983.

Finally, the actual database was built with the function `build_new_database()` which stored the data in json format in `final_project/data/database.json`.

### Data handling in app
#### Document Loader
The script `document_loader.py` is responsible of the handling of all data when the app is running. It implements a class called `LexDatabase`, which stores the in-app data in it's attributes, and has class methods that interact with the data. This is so that the search function scripts don't have deal with handling the data, and to make the app more modular. Initialising the class, which takes a file path as its argument, stores the data stored on disk in the attribute `self.data`

##### LexDatabase Attributes

Initialising the class, which takes a file path as its argument, stores the data stored on disk in the attribute `self.data`

`self.doc_dict` contains a list of all the documents in the database, each as a dictionary with the following format:

```
{
    'Title' = ... , 
    'Link' = ... ,
    'Diaarinumero' = ... , 
    'Antopäivä' = ... ,
    'Description' = ... , 
    "Lower Courts" = ...,
    "Appeal to the Supreme Court" = ... ,
    "Decision of the Supreme Court" = ...

}
```
In other words, this class attribute contains all the data available to the programme. The construction of this variable happens automatically when the class is initilised with the function `self.documents_dict()` 

*Note from Akseli: if you need to have a piece of data available that is not currently here , add it here to the function `self.documents_dict()`, it shouldn't mess with any current functionality. This could be, for example, adding a the year to the data, adding additional fields, etc.*

The class attribute `self.contents` contains a list with each item being a list, with the first element being the title of the case, and the second being the description as a string. This attribute is used in setting up documents for neural_search and tfidf. The attribute is construcred at inisialiation with the class method`text_contents()`, which uses the attribute `self.doc_dict` as it's argument. The tittle is present as an id for each text, so that in setting up documents, preforming searches, and fetching results, the correct document is associated with the correct text. 

*Note from Akseli: Currently, this field contains only the description, and that's all that's used for document set up and therefore searches. I will later test if adding the whole text of each case makes the programme too slow because it will increase the text used in the document setup by about threefold. In the future we might have two separate attributes: one with just the description and one with all the text in each doc*

The attribute `self.embeddings` contains the word emeddings for each document, along with its title. This is so that the embeddings are stored for each document individually and can therefore be stored in memory as opposed to being run each time a search is performed. This attribute is constructed by passing the embeddings from `neural_search.embedd_doc()` to the class method `add_document_embeddings()` 

`self.tf_matrix` will contain the tf_matrix variable currently in routes.py. Hasn't been implemented, and will not greatly affect the overall programme. It's just neater to store it here. I will probably also store the tfv here, but those are not critical things.  

## Search functions
### 1. Boolean search: 
Boolean search performs exact matches for the given query and retrieves documents that meet the conditions. It allows users to query the database using logical operators like "and", "or", and "not". 
### 2. Tf-idf search:
TF-IDF (Term Frequency - Inverse Document Frequency) search ranks documents based on the importance of the search terms in relation to the entire corpus. It returns documents with terms ranked by relevance.
### 3. Neural search:
Neural search uses transformer models to understand the semantic meaning of a query. The current search function uses the pretrained open-source model [distiluse-base-multilingual-cased-v2](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2) from Hugging Face library.
