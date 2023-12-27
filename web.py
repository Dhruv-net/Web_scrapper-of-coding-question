import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        
        soup = BeautifulSoup(response.text, 'html.parser')

        
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Title not found"

        all_paragraphs = soup.find_all('p')
        question = " ".join(paragraph.text.strip() for paragraph in all_paragraphs)

        
        print(f"Title: {title}")
        print(f"Question: {question}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
url_to_scrape = 'https://www.w3resource.com/python-exercises/oop/python-oop-exercise-9.php'
scrape_website(url_to_scrape)