from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

def download_file(url, filename):
    response = requests.get(url)
    print(response.content)
    with open(filename, 'wb') as f:
        f.write(response.content)

with DAG('download_file', default_args=default_args, schedule_interval=None) as dag:
    download_legislaturas = PythonOperator(
        task_id='download_legislaturas',
        python_callable=download_file,
        op_kwargs={
            'url': 'http://dadosabertos.camara.leg.br/arquivos/legislaturas/csv/legislaturas.csv',
            'filename': 'legislaturas.csv',
        }
    )

    download_deputados = PythonOperator(
        task_id='download_deputados',
        python_callable=download_file,
        op_kwargs={
            'url': 'http://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv',
            'filename': 'deputados.csv',
        }
    )

    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file",
        gcp_conn_id="gcp_conn_id",
        src='legislaturas.csv',
        dst='legislaturas.csv',
        bucket='landing',
    )


    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> download_legislaturas >> upload_file >> end
    start >> download_deputados >> end