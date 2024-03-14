from datetime import datetime
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.amazon.aws.operators.s3_file_transform_operator import S3FileTransformOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 12),
}

with DAG('download_and_save_to_s3', default_args=default_args, schedule_interval=None) as dag:
    download_file = SimpleHttpOperator(
        task_id='download_legislaturas',
        method='GET',
        http_conn_id='http_conn',
        endpoint='https://dadosabertos.camara.leg.br/arquivos/legislaturas/csv/legislaturas.csv',
        headers={'Content-Type': 'application/octet-stream'},
        response_check=lambda response: True if response.status_code == 200 else False,
        log_response=True,
        xcom_push=True
    )

    save_to_s3 = S3FileTransformOperator(
        task_id='load_legislaturas_to_s3',
        source_s3_key="{{ task_instance.xcom_pull('download_file') }}",
        dest_s3_key='s3://your-bucket/path/to/save/file',
        transform_script=None,
        replace=False,
        aws_conn_id='aws_s3_conn'
    )


    download_file_2 = SimpleHttpOperator(
        task_id='download_deputados',
        method='GET',
        http_conn_id='http_conn',
        endpoint='https://dadosabertos.camara.leg.br/arquivos/deputados/csv/deputados.csv',
        headers={'Content-Type': 'application/octet-stream'},
        response_check=lambda response: True if response.status_code == 200 else False,
        log_response=True,
        xcom_push=True
    )

    save_to_s3_2 = S3FileTransformOperator(
        task_id='load_legislaturas_to_s3',
        source_s3_key="{{ task_instance.xcom_pull('download_file_2') }}",
        dest_s3_key='s3://your-bucket/path/to/save/file',
        transform_script=None,
        replace=False,
        aws_conn_id='aws_s3_conn'
    )

    download_file >> save_to_s3
    download_file_2 >> save_to_s3_2