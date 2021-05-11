# Kubeflow Bandit
https://github.com/wielrenner/kubeflow-bandit

## Building the container
docker login
docker build . -t wroosmalen/kubeflow-bandit:tagname
docker push wroosmalen/kubeflow-bandit:tagname

## Deploying the app
kubectl apply -f kubeflow-bandit.yaml -n log-replayer

## Getting IP of the app
kubectl get pods -n log-replayer -o wide

## Interacting with the app
kubectl logs kubeflow-bandit-wouter -n log-replayer kubeflow-bandit
kubectl logs kubeflow-bandit-wouter -n log-replayer kubeflow-bandit-redis
pip install httpie
http http://192.168.3.167:8080