# Start Minikube with Docker Driver
minikube start --driver=docker
minikube start --driver=docker --cpus=4 --memory=8192

# To enable all features please run:
minikube addons enable metrics-server

# Configure Docker Environment to Use Minikube
# In CMD:
@FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env --shell cmd') DO @%i
# In Ubuntu:
eval $(minikube -p minikube docker-env)

# Build Docker Image
docker build -t my-celery-flask-app .
docker images

# Apply Kubernetes Configuration Files
# Persistent Volume Claim (PVC)
kubectl apply -f k8s/pvc.yaml
kubectl get pvc

# Deployment
kubectl apply -f k8s/deployment.yaml

# Service
kubectl apply -f k8s/service.yaml

# Horizontal Pod Autoscaler (HPA)
kubectl apply -f k8s/hpa.yaml
kubectl get hpa
kubectl delete hpa celery-flask-hpa

# Verify Pods
kubectl get pods

# Access Service URL
minikube service celery-flask-service --url

# Configure Prometheus and Grafana for Monitoring
# Install Helm (if not already installed)
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
helm version

# Add Prometheus and Grafana Repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Create Monitoring Namespace
kubectl create namespace monitoring

# Install Prometheus
helm install prometheus prometheus-community/prometheus --namespace monitoring

# Install Grafana
helm install grafana grafana/grafana --namespace monitoring

# Access Grafana Dashboard
kubectl port-forward -n monitoring service/grafana 3000:80

# Retrieve Grafana Default Password
kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode

# Set Up Prometheus Data Source in Grafana
In Grafana, go to Configuration > Data Sources > Add data source
Choose Prometheus and set the URL: http://<CLUSTER-IP>:80 

To find the CLUSTER-IP:
    1. Run kubectl get svc -n monitoring
    2. Search for CLUSTER-IP in prometheus-server

Save & Test to verify the connection

# Import a Dashboard from `Dashboard.json`
The `Dashboard.json` file references a specific data source by UID, update the UID in the JSON file to match the UID of your Prometheus data source in Grafana:

To find the UID of the Prometheus data source:
    1. Go to **Configuration > Data Sources** in Grafana.
    2. Click on **Prometheus**. The UID is shown in the URL as `/datasources/edit/<UID>`.

Open `Dashboard.json` in a text editor and replace any existing data source UID with the Prometheus UID from your Grafana setup.
Save the modified `Dashboard.json` file.
Choose **Upload JSON file** and select your `Dashboard.json` file.

# Additional Commands for Troubleshooting and Management

# View Deployment Details
kubectl get deployment celery-flask-deployment -o yaml

# Describe Horizontal Pod Autoscaler (HPA)
kubectl describe hpa celery-flask-hpa
