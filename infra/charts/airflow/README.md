# Airflow

## Helm Setup

[Official Helm Chart](https://artifacthub.io/packages/helm/apache-airflow/airflow)

## Installation

```bash
helm repo add apache-airflow https://airflow.apache.org/
helm repo update
helm pull apache-airflow/airflow --version 1.13.0
```

## Custom docker image

```bash
docker buildx build --platform linux/amd64 -t vitorcarra/airflow2-custom:2.0.1 .
```
