from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow import settings
from airflow.decorators import task
from airflow.models.baseoperator import chain
from airflow.models.connection import Connection

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

@task
def create_connection(conn_id_name: str):
    conn = Connection(
        conn_id=conn_id_name,
        conn_type="http",
        host="http://dadosabertos.camara.leg.br",
        port=80,
    )
    session = settings.Session()
    session.add(conn)
    session.commit()

with DAG('download_and_save_to_s3', default_args=default_args, schedule_interval=None) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    conn_id_name = 'http_conn_new'
    set_up_connection = create_connection(conn_id_name)

    download_and_save_legislaturas = HttpToS3Operator(
        task_id='download_and_save_legislaturas',
        http_conn_id=conn_id_name,
        method='GET',
        endpoint='arquivos/legislaturas/csv/legislaturas.csv',
        s3_key='s3://landing/legislaturas.csv',
        aws_conn_id='aws_s3_conn'
    )

    download_and_save_deputados = HttpToS3Operator(
        task_id='download_and_save_deputados',
        http_conn_id=conn_id_name,
        method='GET',
        endpoint='arquivos/deputados/csv/deputados.csv',
        s3_key='s3://landing/deputados.csv',
        aws_conn_id='aws_s3_conn'
    )

    start >> download_and_save_legislaturas
    start >> download_and_save_deputados
    download_and_save_legislaturas >> end
    download_and_save_deputados >> end