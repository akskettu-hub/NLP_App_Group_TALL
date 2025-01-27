# opens a wikipedia text file and puts it in a list each article is a single string
import re

def extract_articles(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    articles = text.split("</article>")
    cleaned = []
    for article in articles:
        
        cleaned.append(re.sub(r"<.*>", "", article))
        
    return cleaned

small = "wiki_files/enwiki-20181001-corpus.100-articles.txt"
large = "wiki_files/enwiki-20181001-corpus.1000-articles.txt"