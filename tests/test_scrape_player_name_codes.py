import unittest
from scripts.scrape_player_name_codes import scrape_player_name_codes

class TestScrapePlayerNameCodes(unittest.TestCase):

    def test_scrape(self):
        # Add tests for scraping function
        scrape_player_name_codes("https://fbref.com/en/players/")
        # Check if the file exists and is not empty
        self.assertTrue(os.path.exists('/opt/airflow/data/raw/player_name_codes.csv'))

if __name__ == '__main__':
    unittest.main()