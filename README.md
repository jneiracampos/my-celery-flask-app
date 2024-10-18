minikube start --driver=docker
minikube start --driver=docker --cpus=4 --memory=8192

minikube docker-env

@FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env --shell cmd') DO @%i

docker build -t my-celery-flask-app .

docker images

kubectl apply -f k8s/pvc.yaml
kubectl get pvc

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

kubectl apply -f k8s/hpa.yaml
kubectl get hpa

kubectl get pods

minikube service celery-flask-service --url

-----------------------------------------------------------

kubectl get deployment celery-flask-deployment -o yaml

kubectl describe hpa celery-flask-hpa
