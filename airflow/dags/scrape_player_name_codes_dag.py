from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dotenv import load_dotenv
from scripts.scrape_player_name_codes import scrape_player_name_codes
from scripts.process_player_name_codes import process_player_name_codes
from scripts.save_player_name_codes import create_dataset , create_table ,load_data_to_bigquery

import os 

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = "bigquery-python-433113"
DATASET_ID = "players" 
TABLE_ID = "names-codes"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 21),
    'retries': 1,
}

dag = DAG('player_name_codes_dag',
            default_args=default_args,
             schedule_interval=None)

def scrape_task(**kwargs):
    url = "https://fbref.com/en/players/"
    data = scrape_player_name_codes(url)
    print (data)
    return data

def process_task(**kwargs):
    df = process_player_name_codes()
    return df

def create_dataset_task(**kwargs):
    create_dataset(PROJECT_ID, DATASET_ID, location='US')

def create_table_task(**kwargs):
    create_table(PROJECT_ID, DATASET_ID, TABLE_ID)



def load_task(**kwargs):
    #if the i want to load the data from xcom
    #  df = kwargs['ti'].xcom_pull(task_ids='process_data')
    load_data_to_bigquery(PROJECT_ID , TABLE_ID, DATASET_ID)

scrape_task = PythonOperator(
    task_id='scrape_data',
    python_callable=scrape_task,
    # op_kwargs={'url': os.getenv('SCRAPE_URL')},  # Use environment variable for URL
    provide_context=True,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_task,
    provide_context=True,
    dag=dag,
)



create_dataset_task = PythonOperator(
    task_id='create_dataset',
    python_callable=create_dataset_task,
    provide_context=True,
    dag=dag,
)

create_table_task = PythonOperator(
    task_id= 'create_table',
    python_callable = create_table_task,
    provide_context = True, 
    dag = dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_task,
    provide_context=True,
    dag=dag,
)



scrape_task >> process_task >> create_dataset_task >> create_table_task >> load_task

