from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dotenv import load_dotenv
from scraper.scraper import scrape_data
import os 
from processor.processor import process_data
from bigquery.bigquery_loader import create_dataset , create_table , load_data_to_bigquery

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = "bigquery-python-433113"
DATASET_ID = "players" 
TABLE_ID = "names-codes"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 20),
    'retries': 1,
}

dag = DAG('data_pipeline',
            default_args=default_args,
             schedule_interval=None)

def scrape_task_func(**kwargs):
    url = "https://fbref.com/en/players/"
    data = scrape_data(url)
    print (data)
    return data

def process_task_func(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(task_ids='scrape_data')
    df = process_data(raw_data)
    return df

def create_dataset_task_func(**kwargs):
    create_dataset(PROJECT_ID, DATASET_ID, location='US')

def create_table_task_func(**kwargs):
    create_table(PROJECT_ID, DATASET_ID, TABLE_ID)



def load_task_func(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='process_data')
    print(df)
    load_data_to_bigquery(PROJECT_ID, df, TABLE_ID, DATASET_ID)

scrape_task = PythonOperator(
    task_id='scrape_data',
    python_callable=scrape_task_func,
    op_kwargs={'url': os.getenv('SCRAPE_URL')},  # Use environment variable for URL
    provide_context=True,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_task_func,
    provide_context=True,
    dag=dag,
)



create_dataset_task = PythonOperator(
    task_id='create_dataset',
    python_callable=create_dataset_task_func,
    provide_context=True,
    dag=dag,
)

create_table_task = PythonOperator(
    task_id= 'create_table',
    python_callable = create_table_task_func,
    provide_context = True, 
    dag = dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_task_func,
    provide_context=True,
    dag=dag,
)
scrape_task >> process_task >> create_dataset_task >> create_table_task >> load_task
# >> process_task >> load_task
