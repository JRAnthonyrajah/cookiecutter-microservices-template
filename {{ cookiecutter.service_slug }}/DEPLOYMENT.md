# {{ cookiecutter.service_name }} - Deployment Guide

This guide provides comprehensive instructions for deploying `{{ cookiecutter.service_slug }}` to Kubernetes clusters using Helm charts. It covers prerequisites, cluster setup, deployment procedures, configuration management, monitoring, scaling, and recovery strategies.

## Table of Contents

1. [Deployment Prerequisites](#deployment-prerequisites)
2. [Kubernetes Cluster Setup](#kubernetes-cluster-setup)
3. [Helm Chart Deployment](#helm-chart-deployment)
4. [Configuration Management](#configuration-management)
5. [Service Exposure](#service-exposure)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Scaling and Resource Management](#scaling-and-resource-management)
8. [Health Checks and Readiness Probes](#health-checks-and-readiness-probes)
9. [Rolling Updates and Rollbacks](#rolling-updates-and-rollbacks)
10. [Disaster Recovery](#disaster-recovery)

## Deployment Prerequisites

Before deploying `{{ cookiecutter.service_slug }}`, ensure your environment meets the following requirements.

### Required Tools

#### 1. kubectl - Kubernetes Command-Line Tool

**Installation**:
```bash
# macOS with Homebrew
brew install kubectl

# Linux with apt
sudo apt-get update && sudo apt-get install -y kubectl

# Windows with Chocolatey
choco install kubernetes-cli

# Verify installation
kubectl version --client
```

**Minimum Version**: 1.19+

#### 2. Helm 3 - Kubernetes Package Manager

**Installation**:
```bash
# macOS with Homebrew
brew install helm

# Linux with curl
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Windows with Chocolatey
choco install kubernetes-helm

# Verify installation
helm version
```

**Minimum Version**: 3.0+

#### 3. Docker - Container Runtime

**Installation**:
```bash
# macOS
brew install --cask docker

# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh

# Verify installation
docker --version
```

**Minimum Version**: 20.10+

### Cloud Provider Access

#### AWS EKS

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Configure AWS credentials
aws configure

# Verify cluster access
aws eks describe-cluster --name your-cluster-name --region us-east-1
```

#### Google Cloud GKE

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Initialize and authenticate
gcloud init
gcloud auth login

# Get cluster credentials
gcloud container clusters get-credentials your-cluster-name --zone us-central1-a
```

#### Azure AKS

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Get cluster credentials
az aks get-credentials --resource-group myResourceGroup --name myCluster
```

### Kubernetes Cluster Requirements

- **Version**: 1.19 or higher
- **Node Count**: Minimum 2 worker nodes (production should have 3+)
- **Node Resources**:
  - CPU: 4 cores per node minimum
  - Memory: 8GB per node minimum
  - Storage: 50GB available storage
- **Network**: Cluster must support LoadBalancer service type or Ingress controller

### Container Registry Access

Configure authentication to your container registry:

```bash
# Docker Hub
docker login

# Private Registry (e.g., Docker private repo)
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  -n {{ cookiecutter.service_slug }}
```

## Kubernetes Cluster Setup

### Creating a Kubernetes Cluster

#### AWS EKS Cluster

```bash
# Create EKS cluster with eksctl
eksctl create cluster \
  --name {{ cookiecutter.service_slug }}-cluster \
  --region us-east-1 \
  --node-type t3.medium \
  --nodes 3 \
  --managed

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

#### Google Cloud GKE Cluster

```bash
# Create GKE cluster
gcloud container clusters create {{ cookiecutter.service_slug }}-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-stackdriver-kubernetes \
  --enable-ip-alias

# Get cluster credentials
gcloud container clusters get-credentials {{ cookiecutter.service_slug }}-cluster --zone us-central1-a
```

#### Azure AKS Cluster

```bash
# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name {{ cookiecutter.service_slug }}-cluster \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard \
  --enable-managed-identity

# Get cluster credentials
az aks get-credentials --resource-group myResourceGroup --name {{ cookiecutter.service_slug }}-cluster
```

### Cluster Verification

Verify your cluster is properly configured:

```bash
# Check cluster version
kubectl version

# Check node status
kubectl get nodes -o wide

# Check system namespaces
kubectl get namespaces

# Verify RBAC is enabled
kubectl auth can-i create deployments --as=system:serviceaccount:default:default
```

### Create Service Namespace

```bash
# Create namespace for the service
kubectl create namespace {{ cookiecutter.service_slug }}

# Set as default namespace for convenience
kubectl config set-context --current --namespace={{ cookiecutter.service_slug }}

# Verify namespace was created
kubectl get namespaces
```

## Helm Chart Deployment

### Helm Chart Structure

The Helm chart is located in `helm/` directory with the following structure:

```
helm/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration values
├── templates/
│   ├── _helpers.tpl        # Template helpers
│   ├── configmap.yaml      # ConfigMap template
│   ├── service.yaml        # Service template
│   ├── pvc.yaml           # PersistentVolumeClaim template
│   └── statefulset.yaml    # StatefulSet template
└── values-*.yaml           # Environment-specific values
```

### Pre-Deployment Configuration

Create an environment-specific values file for your deployment:

**values-staging.yaml**:
```yaml
replicaCount: 2

image:
  repository: your-registry/{{ cookiecutter.service_slug }}
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

config:
  serviceName: "{{ cookiecutter.service_slug }}-staging"
  logLevel: "INFO"
  enableMetrics: "true"
  enableTracing: "false"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

nodeSelector:
  environment: staging
```

**values-production.yaml**:
```yaml
replicaCount: 3

image:
  repository: your-registry/{{ cookiecutter.service_slug }}
  tag: "v1.0.0"
  pullPolicy: Always

service:
  type: LoadBalancer
  port: 8080

config:
  serviceName: "{{ cookiecutter.service_slug }}-prod"
  logLevel: "WARN"
  enableMetrics: "true"
  enableTracing: "true"

resources:
  limits:
    cpu: 1000m
    memory: 1024Mi
  requests:
    cpu: 500m
    memory: 512Mi

persistence:
  enabled: true
  storageClassName: "fast"
  size: 20Gi

nodeSelector:
  environment: production

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - {{ cookiecutter.service_slug }}
      topologyKey: kubernetes.io/hostname
```

### Helm Dependency Management

If the chart has dependencies (in Chart.yaml):

```bash
# Update Helm dependencies
cd helm/
helm dependency update

# Check dependencies
helm dependency list
```

### Initial Helm Deployment

Deploy the service using Helm:

```bash
# Create a release (staging environment)
helm install {{ cookiecutter.service_slug }} helm/ \
  --namespace {{ cookiecutter.service_slug }} \
  --values helm/values-staging.yaml \
  --create-namespace

# Or with direct value overrides
helm install {{ cookiecutter.service_slug }} helm/ \
  --namespace {{ cookiecutter.service_slug }} \
  --set replicaCount=2 \
  --set image.tag=v1.0.0

# Verify deployment
kubectl get all -n {{ cookiecutter.service_slug }}
kubectl describe statefulset {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

### Helm Release Management

```bash
# List all releases
helm list -n {{ cookiecutter.service_slug }}

# Get release values
helm get values {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# View release history
helm history {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Upgrade a release
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --namespace {{ cookiecutter.service_slug }} \
  --values helm/values-production.yaml

# Rollback to previous release
helm rollback {{ cookiecutter.service_slug }} 1 -n {{ cookiecutter.service_slug }}

# Delete a release
helm uninstall {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

## Configuration Management

### ConfigMap Management

ConfigMaps store non-sensitive configuration data:

```bash
# View ConfigMap
kubectl get configmap -n {{ cookiecutter.service_slug }}
kubectl describe configmap {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Edit ConfigMap
kubectl edit configmap {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Create ConfigMap from file
kubectl create configmap app-config \
  --from-file=config.yml \
  -n {{ cookiecutter.service_slug }}

# Create ConfigMap from literal values
kubectl create configmap app-settings \
  --from-literal=log_level=DEBUG \
  --from-literal=db_timeout=30 \
  -n {{ cookiecutter.service_slug }}
```

### Secret Management

Secrets store sensitive data (credentials, API keys, certificates):

```bash
# Create a secret
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secretpassword \
  -n {{ cookiecutter.service_slug }}

# Create a secret from a file
kubectl create secret generic tls-cert \
  --from-file=tls.crt=./tls.crt \
  --from-file=tls.key=./tls.key \
  -n {{ cookiecutter.service_slug }}

# List secrets
kubectl get secrets -n {{ cookiecutter.service_slug }}

# View secret (base64 encoded)
kubectl get secret db-credentials -o yaml -n {{ cookiecutter.service_slug }}

# Update a secret
kubectl patch secret db-credentials \
  -p '{"data":{"password":"'$(echo -n newpassword | base64)'"}}'  \
  -n {{ cookiecutter.service_slug }}
```

### Environment-Specific Configuration

Use different values files for different environments:

```bash
# Staging deployment
helm install {{ cookiecutter.service_slug }}-staging helm/ \
  --values helm/values.yaml \
  --values helm/values-staging.yaml \
  -n staging

# Production deployment
helm install {{ cookiecutter.service_slug }}-prod helm/ \
  --values helm/values.yaml \
  --values helm/values-production.yaml \
  -n production
```

## Service Exposure

### ClusterIP Service (Internal Communication)

For internal service-to-service communication:

```yaml
# helm/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "{{ cookiecutter.service_slug }}.fullname" . }}
  labels:
    {{- include "{{ cookiecutter.service_slug }}.labels" . | nindent 4 }}
spec:
  type: ClusterIP
  selector:
    {{- include "{{ cookiecutter.service_slug }}.selectorLabels" . | nindent 4 }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: {{ .Values.service.targetPort }}
    protocol: TCP
    name: http
```

Deploy and verify:

```bash
# Deploy service
kubectl apply -f helm/templates/service.yaml -n {{ cookiecutter.service_slug }}

# Verify service
kubectl get service -n {{ cookiecutter.service_slug }}
kubectl describe service {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Test internal connectivity
kubectl run test-pod --image=curlimages/curl --rm -it -n {{ cookiecutter.service_slug }} \
  -- curl http://{{ cookiecutter.service_slug }}:8080/health
```

### LoadBalancer Service (External Access)

For direct external access:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ cookiecutter.service_slug }}-lb
spec:
  type: LoadBalancer
  selector:
    app: {{ cookiecutter.service_slug }}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

Deploy and expose:

```bash
# Deploy LoadBalancer service
kubectl apply -f service-lb.yaml -n {{ cookiecutter.service_slug }}

# Get external IP (may take a few minutes)
kubectl get service {{ cookiecutter.service_slug }}-lb -n {{ cookiecutter.service_slug }} -w

# Test external access
curl http://<EXTERNAL-IP>:80/health
```

### Ingress (Recommended for Production)

For advanced routing, TLS, and path-based routing:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ cookiecutter.service_slug }}-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - {{ cookiecutter.service_slug }}.example.com
    secretName: {{ cookiecutter.service_slug }}-tls
  rules:
  - host: {{ cookiecutter.service_slug }}.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {{ cookiecutter.service_slug }}
            port:
              number: 8080
```

Setup Ingress:

```bash
# Install NGINX Ingress Controller (if not already installed)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

# Install cert-manager for SSL certificates
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Deploy Ingress
kubectl apply -f ingress.yaml -n {{ cookiecutter.service_slug }}

# Verify Ingress
kubectl get ingress -n {{ cookiecutter.service_slug }}
kubectl describe ingress {{ cookiecutter.service_slug }}-ingress -n {{ cookiecutter.service_slug }}

# Test DNS resolution (after DNS is configured)
curl https://{{ cookiecutter.service_slug }}.example.com/health
```

## Monitoring and Logging

### Prometheus Metrics Setup

Enable metrics collection:

```bash
# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Create ServiceMonitor for {{ cookiecutter.service_slug }}
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ cookiecutter.service_slug }}
  namespace: {{ cookiecutter.service_slug }}
spec:
  selector:
    matchLabels:
      app: {{ cookiecutter.service_slug }}
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
EOF

# Verify metrics are being collected
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
# Access Prometheus at http://localhost:9090
# Query: up{job="{{ cookiecutter.service_slug }}"}
```

### ELK Stack Setup (Elasticsearch, Logstash, Kibana)

Deploy the ELK stack for log aggregation:

```bash
# Install Elasticsearch
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --create-namespace \
  --values elasticsearch-values.yaml

# Install Logstash for log processing
helm install logstash elastic/logstash \
  --namespace logging \
  --values logstash-values.yaml

# Install Kibana for log visualization
helm install kibana elastic/kibana \
  --namespace logging \
  --values kibana-values.yaml

# Configure Logstash pipeline
kubectl create configmap logstash-pipeline \
  --from-file=logstash.conf \
  -n logging

# Verify ELK stack
kubectl get pods -n logging
kubectl port-forward -n logging svc/kibana-kibana 5601:5601
# Access Kibana at http://localhost:5601
```

### Distributed Tracing with Jaeger

Setup distributed tracing:

```bash
# Install Jaeger
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace tracing \
  --create-namespace

# Configure application to send traces to Jaeger
# Set environment variables in Helm values
env:
  - name: JAEGER_AGENT_HOST
    value: jaeger-agent.tracing.svc.cluster.local
  - name: JAEGER_AGENT_PORT
    value: "6831"
  - name: JAEGER_SERVICE_NAME
    value: {{ cookiecutter.service_slug }}

# Verify Jaeger
kubectl port-forward -n tracing svc/jaeger-query 16686:16686
# Access Jaeger UI at http://localhost:16686
```

### Log Aggregation and Analysis

Query logs from all pods:

```bash
# View logs from a single pod
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# View logs from all pods in deployment
kubectl logs -f -l app={{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }} --all-containers=true

# View logs from a specific container
kubectl logs {{ cookiecutter.service_slug }}-0 -c {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# View logs with timestamps
kubectl logs {{ cookiecutter.service_slug }}-0 --timestamps=true -n {{ cookiecutter.service_slug }}

# Stream logs in real-time
kubectl logs -f {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Get logs from previous pod instance
kubectl logs {{ cookiecutter.service_slug }}-0 --previous -n {{ cookiecutter.service_slug }}
```

## Scaling and Resource Management

### Horizontal Pod Autoscaling (HPA)

Automatically scale replicas based on metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ cookiecutter.service_slug }}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: {{ cookiecutter.service_slug }}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
```

Deploy and monitor HPA:

```bash
# Deploy HPA
kubectl apply -f hpa.yaml -n {{ cookiecutter.service_slug }}

# Monitor HPA status
kubectl get hpa {{ cookiecutter.service_slug }}-hpa -n {{ cookiecutter.service_slug }} -w

# Describe HPA for detailed information
kubectl describe hpa {{ cookiecutter.service_slug }}-hpa -n {{ cookiecutter.service_slug }}

# Get HPA metrics
kubectl get hpa {{ cookiecutter.service_slug }}-hpa -n {{ cookiecutter.service_slug }} --show-metrics
```

### Manual Scaling

Scale deployment manually when needed:

```bash
# Scale StatefulSet
kubectl scale statefulset {{ cookiecutter.service_slug }} --replicas=5 -n {{ cookiecutter.service_slug }}

# Verify scaling
kubectl get statefulset {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Watch scaling in progress
kubectl get statefulset {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }} -w
```

### Resource Management

Ensure pods have appropriate resource limits:

```yaml
# In Helm values
resources:
  limits:
    cpu: 1000m          # 1 CPU core
    memory: 1024Mi      # 1 GB
  requests:
    cpu: 500m           # 500m = 0.5 CPU cores
    memory: 512Mi       # 512 MB
```

Monitor resource usage:

```bash
# View resource usage
kubectl top nodes -n {{ cookiecutter.service_slug }}
kubectl top pods -n {{ cookiecutter.service_slug }}

# Detailed resource metrics
kubectl describe nodes
kubectl describe pods -n {{ cookiecutter.service_slug }}
```

## Health Checks and Readiness Probes

### Liveness Probe

Restarts unhealthy containers:

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Readiness Probe

Removes unhealthy pods from service:

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### Startup Probe (for slow-starting applications)

Allows time for application startup:

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### Configure Health Checks in Helm

Update `helm/values.yaml`:

```yaml
healthChecks:
  liveness:
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  readiness:
    initialDelaySeconds: 10
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
```

Test health endpoints:

```bash
# Port forward to service
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}

# Test health endpoints
curl http://localhost:8080/health
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
```

## Rolling Updates and Rollbacks

### Rolling Update Strategy

Deploy new versions with zero downtime:

```yaml
# helm/templates/statefulset.yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0  # Number of pods to update at once
```

Perform rolling update:

```bash
# Update image tag in values
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set image.tag=v2.0.0 \
  --namespace {{ cookiecutter.service_slug }}

# Monitor rolling update
kubectl rollout status statefulset/{{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Watch pods being updated
kubectl get pods -n {{ cookiecutter.service_slug }} -w
```

### Blue-Green Deployment

Deploy new version alongside old version:

```bash
# Deploy new version as "green"
helm install {{ cookiecutter.service_slug }}-green helm/ \
  --set image.tag=v2.0.0 \
  --namespace {{ cookiecutter.service_slug }}

# Test green deployment
kubectl port-forward svc/{{ cookiecutter.service_slug }}-green 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/health

# Switch traffic to green (update service selector)
kubectl patch service {{ cookiecutter.service_slug }} \
  -p '{"spec":{"selector":{"version":"green"}}}' \
  -n {{ cookiecutter.service_slug }}

# Delete old blue deployment
helm uninstall {{ cookiecutter.service_slug }}-blue -n {{ cookiecutter.service_slug }}

# Rename green to primary
helm install {{ cookiecutter.service_slug }} helm/ \
  --namespace {{ cookiecutter.service_slug }}
```

### Canary Deployments

Gradually roll out new version to subset of traffic:

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: {{ cookiecutter.service_slug }}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: {{ cookiecutter.service_slug }}
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
```

### Rollback to Previous Release

If deployment fails, rollback immediately:

```bash
# View deployment history
kubectl rollout history statefulset/{{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Rollback to previous revision
kubectl rollout undo statefulset/{{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Rollback to specific revision
kubectl rollout undo statefulset/{{ cookiecutter.service_slug }} --to-revision=2 -n {{ cookiecutter.service_slug }}

# Or use Helm to rollback
helm rollback {{ cookiecutter.service_slug }} 1 -n {{ cookiecutter.service_slug }}

# Verify rollback
kubectl rollout status statefulset/{{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

## Disaster Recovery

### Backup Strategy

Regular backups are critical for disaster recovery:

```bash
# Backup Kubernetes manifests
kubectl get all -n {{ cookiecutter.service_slug }} -o yaml > backup-{{ cookiecutter.service_slug }}.yaml

# Backup Helm release values
helm get values {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }} > values-backup.yaml

# Backup persistent data
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- tar czf - /data | \
  gzip > data-backup-$(date +%Y%m%d-%H%M%S).tar.gz

# Automated backups with Velero
helm install velero velero/velero \
  --namespace velero \
  --create-namespace \
  --set credentials.useSecret=true
```

### Disaster Recovery Procedures

Complete recovery from scratch:

```bash
# 1. Create new cluster
eksctl create cluster --name {{ cookiecutter.service_slug }}-recovery --region us-east-1

# 2. Create namespace
kubectl create namespace {{ cookiecutter.service_slug }}

# 3. Restore secrets and configs
kubectl apply -f secrets-backup.yaml -n {{ cookiecutter.service_slug }}
kubectl apply -f configmap-backup.yaml -n {{ cookiecutter.service_slug }}

# 4. Restore using Velero schedule
velero restore create --from-schedule {{ cookiecutter.service_slug }}-daily

# 5. Verify restoration
kubectl get all -n {{ cookiecutter.service_slug }}

# 6. Restore persistent data volumes
kubectl apply -f pvc-backup.yaml -n {{ cookiecutter.service_slug }}

# 7. Redeploy application
helm install {{ cookiecutter.service_slug }} helm/ \
  --namespace {{ cookiecutter.service_slug }} \
  --values values-backup.yaml

# 8. Verify service is running
kubectl get pods -n {{ cookiecutter.service_slug }}
kubectl get service -n {{ cookiecutter.service_slug }}
```

### Multi-Region Setup

High-availability setup across regions:

```bash
# Create clusters in multiple regions
eksctl create cluster --name {{ cookiecutter.service_slug }}-us-east \
  --region us-east-1
eksctl create cluster --name {{ cookiecutter.service_slug }}-us-west \
  --region us-west-2

# Deploy to all regions
for cluster in {{ cookiecutter.service_slug }}-us-east {{ cookiecutter.service_slug }}-us-west; do
  kubectl config use-context $cluster
  helm install {{ cookiecutter.service_slug }} helm/ \
    --namespace {{ cookiecutter.service_slug }}
done

# Setup cross-region replication
# (Implementation depends on your data store)
```

### Post-Disaster Validation

Verify system health after disaster recovery:

```bash
# Check pod status
kubectl get pods -n {{ cookiecutter.service_slug }}

# Verify services are running
kubectl get service -n {{ cookiecutter.service_slug }}

# Test health endpoints
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/health

# Check persistence
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  ls -la /data

# Verify data integrity
# (Run application-specific validation queries)
```

## Summary

This deployment guide covers the complete lifecycle of deploying and managing `{{ cookiecutter.service_slug }}` on Kubernetes. Key takeaways:

1. **Prerequisites**: Ensure all tools are installed and cluster access configured
2. **Setup**: Create cluster and namespaces properly
3. **Deployment**: Use Helm for reproducible deployments
4. **Configuration**: Manage secrets and configs separately from code
5. **Monitoring**: Setup metrics, logs, and traces for visibility
6. **Scaling**: Use HPA for automatic scaling based on metrics
7. **Updates**: Use rolling updates and canary deployments for safe rollouts
8. **Disaster Recovery**: Regular backups and documented recovery procedures

For additional help, refer to:
- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [{{ cookiecutter.service_name }} API Documentation](./API.md)
- [{{ cookiecutter.service_name }} Architecture](./ARCHITECTURE.md)
