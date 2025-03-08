# NLP_App_Group_TALL - final_project

## About our project
Hi! We are **Team TALL (Tzang, Aleksi, Liisa, Lisa) **! Our project is a **search engine** designed to search within the **Supreme Court precedence rulings of Finland**. The goal of our application is to make these court rulings more open and accessible to the public, including those who may not be familiar with legal terminology or legislative language.

The search engine supports multiple search modes:
- **Boolean Search**: Allows searching using logical operators (AND, OR, NOT) for precise results.
- **TF-IDF Search**: Uses term frequency-inverse document frequency to rank relevant documents.
- **Neural Search**: Supports **English queries** and finds relevant matches within **Finnish legal texts** using machine learning techniques.

## How to run the search engine
Our search engine is not a public website; it must be run locally. To do this, follow these steps:

### Installation
Ensure you have Python installed, then install all required dependencies using:
```
pip install -r requirements.txt
```

### Running the project
After installing dependencies, navigate to the project directory and start the application:

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

Once the application is running, open your browser and go to **http://127.0.0.1:5000** to start using the search engine.



