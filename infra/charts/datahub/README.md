# Datahub

## Helm Chart Guide

This chart is used to deploy Datahub on a Kubernetes cluster. [[here](https://datahubproject.io/docs/deploy/kubernetes/)]

### Setup

To install the chart with the release name `datahub`:

```bash
kubectl create secret generic mysql-secrets --from-literal=mysql-root-password=datahub
kubectl create secret generic neo4j-secrets --from-literal=neo4j-password=datahub

helm repo add datahub https://helm.datahubproject.io/
```
