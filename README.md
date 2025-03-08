# NLP_App_Group_TALL - final_project

## About our project
Hi! We are **Team TALL (Tzang, Aleksi, Liisa, Lisa)**! This repository is for the group project for the course **"Building NLP Applications"**.

This project is a search engine for the Supreme Court of Finland's rulings. The aim is to make these rulings more accessible to the public, especially those unfamiliar with legal language. The app allows users to search using **Boolean search**, **TF-IDF search**, and **Neural search**, with support for English queries that retrieve results from Finnish texts.

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

## Running the project
The relevant code is stored in the folder **final_project**. 

### Prerequisites
Make sure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package manager)
- A virtual environment (optional but recommended)

### Installation

#### 1. Clone the Repository
```sh
$ git clone <repository-url>
$ cd final_project
```

#### 2. Create and Activate a Virtual Environment (Optional but Recommended)

##### On Windows (Command Prompt):
```sh
$ python -m venv venv
$ venv\Scripts\activate
```

##### On macOS/Linux:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

#### 3. Install Required Dependencies
```sh
$ pip install -r requirements.txt
```

### Running the Application

1. Ensure you are in the `final_project` directory.
2. Run the Flask application with the following command:

```sh
$ python run.py
```

By default, the application will be available at:

```
http://127.0.0.1:5000/
```





