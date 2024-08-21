from google.cloud import bigquery
import pandas as pd




def create_dataset(project_id, dataset_id, location='US'):
    """
    Creates a dataset in BigQuery if it does not already exist.

    Args:
    - project_id (str): The ID of the Google Cloud project.
    - dataset_id (str): The ID of the dataset to be created.
    - location (str): The geographic location where the dataset will be stored.
    """
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id, project=project_id)

    try:
        # Check if dataset already exists
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists.")
    except Exception:
        # If not, create the dataset
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        dataset = client.create_dataset(dataset)
        print(f"Created dataset {dataset.project}.{dataset.dataset_id} in location {dataset.location}.")

def create_table(project_id, dataset_id, table_id):
    """
    Creates a table in the specified dataset if it does not already exist.

    Args:
    - project_id (str): The ID of the Google Cloud project.
    - dataset_id (str): The ID of the dataset where the table will be created.
    - table_id (str): The ID of the table to be created.
    """
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)

    try:
        # Check if table already exists
        client.get_table(table_ref)
        print(f"Table {table_id} already exists in dataset {dataset_id}.")
    except Exception:
        # Define schema for the new table
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name_code", "STRING", mode="REQUIRED"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}.")

def load_data_to_bigquery(project_id, table_id, dataset_id):
    """
    Loads data from a DataFrame into a BigQuery table.

    Args:
    - project_id (str): The ID of the Google Cloud project.
    - df (pd.DataFrame): The DataFrame to be loaded.
    - table_id (str): The ID of the table to load data into.
    - dataset_id (str): The ID of the dataset where the table is located.
    """
    df = pd.read_csv('/opt/airflow/data/processed/player_name_codes.csv')
    
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    
    job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("name_code", "STRING", mode="REQUIRED")
    ],
    write_disposition=bigquery.WriteDisposition.WRITE_EMPTY
)
    # Load data into the table
    try:
        job = client.load_table_from_dataframe(df, table_ref,job_config = job_config)
        print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")

        job.result()  # Wait for the job to complete
        print(f"Loaded {job.output_rows} rows into {table_id}.")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")

