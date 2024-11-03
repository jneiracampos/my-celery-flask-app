# Start Minikube with Docker Driver
minikube start --driver=docker
minikube start --driver=docker --cpus=4 --memory=8192

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
# In Grafana, go to Configuration > Data Sources > Add data source
# Choose Prometheus and set the URL:
# http://10.101.43.24:80
# Save & Test to verify the connection

# Import Pre-built Dashboard in Grafana
# Go to Dashboard > Import
# Enter the Dashboard ID (e.g., 6417 for Kubernetes Cluster Monitoring)
# Select Prometheus as the data source and click Import

# Additional Commands for Troubleshooting and Management
# View Deployment Details
kubectl get deployment celery-flask-deployment -o yaml

# Describe Horizontal Pod Autoscaler (HPA)
kubectl describe hpa celery-flask-hpa
