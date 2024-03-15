from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.operators.gcs import GCSToBigQueryOperator

default_args = {
    'start_date': datetime(2024, 3, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'load_file_to_bigquery',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:
    load_to_bigquery = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket='st-landing-bucket',
        source_objects=['legislatura.csv'],
        schema_update_options=['ALLOW_FIELD_ADDITION'],
        destination_project_dataset_table='study-341002.data.legislatura',
        write_disposition='WRITE_TRUNCATE',
        autodetect=True,
    )

    load_to_bigquery