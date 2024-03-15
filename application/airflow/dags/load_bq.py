from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

def load_gcs_to_bigquery(bucket_name, source_object, dataset_id, table_id):
    gcs_hook = GCSHook(gcp_conn_id='gcp_conn_id')
    bigquery_hook = BigQueryHook(
        gcp_conn_id='gcp_conn_id',
    )

    # Download the file from GCS to a local file
    with open('/tmp/temp_file.csv', 'wb') as file:
        file.write(gcs_hook.download(bucket_name, source_object))

    # Load the local file to BigQuery
    bigquery_hook.run_load(
        '/tmp/temp_file.csv',
        destination_project_dataset_table=f'{dataset_id}.{table_id}',
        source_format='CSV',
        autodetect=True,
        write_disposition='WRITE_TRUNCATE',
        schema_update_options=['ALLOW_FIELD_ADDITION'],
    )

with DAG('load_file_to_bigquery', default_args=default_args, schedule_interval=None) as dag:
    load_to_bigquery = PythonOperator(
        task_id='load_to_bigquery',
        python_callable=load_gcs_to_bigquery,
        op_kwargs={
            'bucket_name': 'st-landing-bucket',
            'source_object': 'legislaturas.csv',
            'dataset_id': 'data',
            'table_id': 'legislaturas',
        }
    )

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> load_to_bigquery >> end