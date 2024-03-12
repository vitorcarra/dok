# Argocd

Documentation for the ArgoCD Helm chart can be found [here](https://argo-cd.readthedocs.io/en/stable/getting_started/)

## Configuration

### Install

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f argo_install.yaml
```

### Expose a service

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get services --namespace argocd argocd-server --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### Access the UI

```bash
minikube service list | grep argocd-server
# copy the IP:PORT
sudo vim /etc/nginx/nginx.conf
# add the following location block
server {
    listen 192.168.10.17:8888;
    proxy_pass 192.168.49.2:10232;
}

sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow from 192.168.10.0/24 to any port 8888
```

### Login

```bash
brew install argocd
argocd admin initial-password -n argocd
argocd login <ARGOCD_SERVER>
# use admin as user and above password

# change the password
argocd account update-password
```
