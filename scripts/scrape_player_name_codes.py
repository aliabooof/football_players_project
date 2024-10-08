import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

def scrape_player_name_codes(url):
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
        df = pd.DataFrame(players_codes )
        df.to_csv('/opt/airflow/data/raw/player_name_codes.csv', index=False)
        return df
        
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []
