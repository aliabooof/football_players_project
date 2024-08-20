import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def scrape_data(url):
    try:
        
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
       
        players_codes_content=[]
        players_section = soup.find('div', {'class': 'section_content'})
        players_codes_content= players_section.find_all('a')
        players_codes=[]
        for player in players_codes_content :
            players_codes.append(player.text)
        # Extract data from soup
        return players_codes
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []
