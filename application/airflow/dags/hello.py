from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from datetime import datetime
import requests

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

with DAG('download_file_and_upload_to_s3', default_args=default_args, schedule_interval=None) as dag:
    download_deputados = PythonOperator(
        task_id='download_deputados',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv',
            'filename': '/tmp/deputados.csv',
        },
        do_xcom_push=True
    )

    upload_to_s3 = S3CreateObjectOperator(
        task_id='upload_to_s3',
        s3_bucket='landing',
        s3_key='deputados.csv',
        data="testando",
        aws_conn_id='aws_s3_conn'
    )

    download_deputados >> upload_to_s3