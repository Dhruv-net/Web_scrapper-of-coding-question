import requests
from bs4 import BeautifulSoup

def generic_scraper(url):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text content from the page
        all_text = soup.get_text(separator='\n', strip=True)

        # Extract all links from the page
        all_links = [link.get('href') for link in soup.find_all('a', href=True)]

        # Extract all image sources from the page
        all_images = [img.get('src') for img in soup.find_all('img', src=True)]

        # Print or do something with the extracted information
        print(f"All Text:\n{all_text}\n")
        print(f"All Links:\n{all_links}\n")
        print(f"All Images:\n{all_images}\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")

# Replace 'https://example.com' with the URL of the website you want to scrape
url_to_scrape = 'https://www.w3resource.com/python-exercises/oop/python-oop-exercise-9.php'
generic_scraper(url_to_scrape)
