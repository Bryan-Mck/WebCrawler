import requests
from bs4 import BeautifulSoup
from queue import Queue
import re
import json

unwanted_tags = ["script", "style", "header", "footer", "nav", "noscript", "aside", "svg", "form"]
SEED_SET = ["https://www.instagram.com/?hl=en", "https://www.facebook.com/", "https://www.twitter.com/"]

# SET UP QUEUE ---------------------------------------------
queue = Queue()

for url in SEED_SET:
    queue.put(url)
# ---------------------------------------------------------

def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        link = anchor['href']
        if link.startswith('http'):
            queue.put(link)

def add_text(text):
    data = { "text": text }

    with open("text.jsonl", "a") as f:
        json.dump(data, f)
        f.write("\n")

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in soup(unwanted_tags):
        tag.decompose()

    raw_text = soup.get_text(separator=" || ", strip=True)

    clean_text = re.sub(r' +', ' ', raw_text) 
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text) 

    text_array = raw_text.split(" || ")

    for text in text_array:
        if (text == ""): continue
        add_text(text.strip())



while not queue.empty():
    url = queue.get()
    try:
        response = requests.get(url)
        print(f"URL: {url} | Status Code: {response.status_code}")

        extract_links(response.text)

        text_content = extract_text(response.text)

        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        continue



