import requests
from bs4 import BeautifulSoup
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

def create_database_connection():
    # import pdb;pdb.set_trace()
    
    return mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        database=os.getenv("db_database")
    )

def create_table(connection):
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS scraped_data (
        title VARCHAR(255),
        question TEXT,
        sample_inputs TEXT,
        sample_outputs TEXT,
        explanations TEXT,
        PRIMARY KEY (title)
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
    connection.commit()

def insert_data(connection, title, question, sample_inputs, sample_outputs, explanations):
    insert_data_query = """
    INSERT INTO scraped_data (title, question, sample_inputs, sample_outputs, explanations)
    VALUES (%s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(insert_data_query, (title, question, sample_inputs, sample_outputs, explanations))
    connection.commit()

def scrape_website_and_store(url):
    try:
        
        response = requests.get(url)
        response.raise_for_status()

        
        soup = BeautifulSoup(response.text, 'html.parser')

        
        title = soup.find('h1').text.strip() if soup.find('h1') else "Title not found"
        question = soup.find('p').text.strip() if soup.find('p') else "Question not found"
        sample_inputs = [code.text.strip() for code in soup.find_all('code')]
        sample_outputs = [pre.text.strip() for pre in soup.find_all('pre')]
        explanations = [div.text.strip() for div in soup.find_all('div', class_='explanation')]

        
        print(f"Title: {title}")
        print(f"Question: {question}")
        print(f"Sample Inputs: {sample_inputs}")
        print(f"Sample Outputs: {sample_outputs}")
        print(f"Explanations: {explanations}")

        
        connection = create_database_connection()

        
        create_table(connection)

        
        insert_data(connection, title, question, str(sample_inputs), str(sample_outputs), str(explanations))

        
        connection.close()

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")

url_to_scrape = 'https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-linked-list-exercise-11.php'
scrape_website_and_store(url_to_scrape)
