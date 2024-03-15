from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

def download_file(url, filename):
    response = requests.get(url)
    print(response)
    with open(filename, 'wb') as f:
        f.write(response.content)

with DAG('download_file', default_args=default_args, schedule_interval=None) as dag:
    download_legislaturas = PythonOperator(
        task_id='download_legislaturas',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://dadosabertos.camara.leg.br/arquivos/legislaturas/csv/legislaturas.csv',
            'filename': 'legislaturas.csv',
        }
    )

    download_deputados = PythonOperator(
        task_id='download_deputados',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv',
            'filename': 'deputados.csv',
        }
    )


    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> download_legislaturas >> download_deputados >> end