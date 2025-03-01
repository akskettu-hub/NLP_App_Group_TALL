# NLP_App_Group_TALL
A repository for the group project for the course "Building NLP Applications", Group TALL.

[The following is a description of the data and can be copy and pasted to wherever it makes sense in the read me]: #
## Data

The data for this project consists of the rulings of the Finnish Supreme Court from 2015-2025, totaling 953 rulings, scraped from [Finlex](https://www.finlex.fi/en), a public database for Finnish law and legal documents maintaied by the Finnish Ministry of Justice. The data is stored in json format at the location `data/database.json`.

Due to an **[unexpected overhaul to the Finlex website](https://www.finlex.fi/en/information-about-the-upgrade)**, the initial intention of using all rulings from the years 1980-2025 was abandoned as the code that was used to scrape the previous version of the website did not work anymore. As this update happened in the final stretch of the project, it was decided that attemting to scrape the new version of the website was not feasible or sensible. Instead, the data that had already been scraped was used for this project, which happened to be for the years 2015-2025. Even with this smaller dataset, the core functionality of this project can still be demonstrated. 

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
```
### Scraping
These data were scraped from [Finlex](https://www.finlex.fi/en), a public database for Finnish law and legal documents mainatied by the Finnish Ministry of Justice. The code used for scraping is available at the location `final_project/
t/scraping_finlex.py`. The main tool use for scraping was {BeautifulSoup](https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)).

The code first scraped the website to find all the links to all the rulings. This entaield finding all the pages where links to rulings are found. The initial landing page was scraped for links to all years pages, all year pages were scraped to find all offset pages for that year, and all the offset pages were scraped for links to individual rulings. In `final_project/t/scraping_finlex.py` these were handled by the functions `fetch_links_years()`,  `fetch_page_links_for_year()`, and `fetch_links_on_page()`, which pulled all these links together with the function `fetch_all_links()`. The function `links()` automated the process of finding all links and storing them as a json file (the latest example of this is available in `data/links.json`). This function also automatically updated any links not already in `data/links.json` to possibly enable the app to keep up to date with the latest rulings. The change to the website on 27th of February made this function redundant, as scraping for links or indeed their content no longer works with the current website.

The scraping of the individual rulings was handled with the function `scrape_document()`, which scraped through a ruling, using the structure of the HTML to find the different sections found in each ruling. This was not a straightforward proccess because the structure of the HTML was not particularly clear and consistent across rulings, and the logic of `scrape_document()` is therefore quite complicated. Some rulings varied quite significantly from most other rulings and the function `tidy_document()` was implemented as a result. Even with this, some inconsistencies emerged in the data due to variability in the documents. It was decided that perfecting the database was too laboursome for the scope of this project, and documents that varied sigificantly enough to cause problems in the app were deleted with the functions `check_database()` and `final_database()`. 

Finally, the actual database was built with the function `build_new_database()` which stored the data in json format in `data/`.
