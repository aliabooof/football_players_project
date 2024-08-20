import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def process_data(raw_data):
    try:
        # Perform data cleaning and transformation
        
        lowercase_list = list(map(str.lower, raw_data))
        print(lowercase_list)
        df = pd.DataFrame({
                'id': range(1, len(lowercase_list) + 1),  # Primary key column
                'name': lowercase_list                    # Names column
                        })
    
        print(df)
        # Rename columns

        return df
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return pd.DataFrame()
