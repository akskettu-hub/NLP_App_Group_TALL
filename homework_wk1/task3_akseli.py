# This is and empty python file for initial commit purposes
#what happens if I add a line
import requests
from bs4 import BeautifulSoup

#Fetch webcontent and parse to variable. print variable

url = "https://www.ilmatieteenlaitos.fi/saa/espoo"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)