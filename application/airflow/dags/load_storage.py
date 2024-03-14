from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

with DAG('download_and_save_to_s3', default_args=default_args, schedule_interval=None) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    download_and_save_legislaturas = HttpToS3Operator(
        task_id='download_and_save_legislaturas',
        http_conn_id='http_conn',
        path='https://dadosabertos.camara.leg.br/arquivos/legislaturas/csv/legislaturas.csv',
        s3_bucket='your-bucket',
        s3_key='path/to/save/file/legislaturas.csv',
        aws_conn_id='aws_s3_conn'
    )

    download_and_save_deputados = HttpToS3Operator(
        task_id='download_and_save_deputados',
        http_conn_id='http_conn',
        path='https://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv',
        s3_bucket='your-bucket',
        s3_key='path/to/save/file/deputados.csv',
        aws_conn_id='aws_s3_conn'
    )

    start >> download_and_save_legislaturas
    start >> download_and_save_deputados
    download_and_save_legislaturas >> end
    download_and_save_deputados >> end