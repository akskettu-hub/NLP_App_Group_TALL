
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website we want to scrape
url = "https://valtioneuvosto.fi/en/prime-ministers-office/press-releases"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

releases = []
for release in soup.find_all("div", class_="feed-item simple"):    
    title = release.a['title']
    link = url + release.a['href']
    date = release.find("span", class_="date").string
    type = release.find("span", class_="label").string
    
    releases.append({
        "title": title,
        "link": link,
        "date": date,
        "type": type
    })

releases_df = pd.DataFrame(releases)
releases_df.to_csv("pm_office_press_releases.csv", index="True", sep=";")


