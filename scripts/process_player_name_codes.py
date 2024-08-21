import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def process_player_name_codes():
    df = pd.read_csv('/opt/airflow/data/raw/player_name_codes.csv')
    try:
        # Perform data cleaning and transformation
        df.rename(columns={'0':'name_code'}, inplace=True)
        df['id'] = range(1, len(df) + 1)
        df = df[['id', 'name_code']]
        df['name_code']=df['name_code'].str.lower()
        print (df.head())
        df.to_csv('/opt/airflow/data/processed/player_name_codes.csv', index=False)
        return df
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return pd.DataFrame()
