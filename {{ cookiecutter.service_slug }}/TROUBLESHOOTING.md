# {{ cookiecutter.service_name }} - Troubleshooting Guide

This guide provides solutions for common issues encountered when deploying, running, and managing `{{ cookiecutter.service_slug }}` on Kubernetes. It covers debugging techniques, common failure modes, and optimization strategies.

## Table of Contents

1. [Common Deployment Issues](#common-deployment-issues)
2. [Debugging Failed Pod Starts](#debugging-failed-pod-starts)
3. [Networking Issues](#networking-issues)
4. [Storage and Volume Troubleshooting](#storage-and-volume-troubleshooting)
5. [Performance Optimization](#performance-optimization)
6. [Log Analysis and Debugging](#log-analysis-and-debugging)
7. [Resource Constraint Issues](#resource-constraint-issues)
8. [Health Check Failures](#health-check-failures)
9. [Testing and Validation](#testing-and-validation)

## Common Deployment Issues

### Issue: Helm Chart Installation Fails with "Chart not Found"

**Symptoms**: 
- Error: `Error: chart not found`
- Helm install command fails immediately

**Causes**:
- Chart path is incorrect
- Chart.yaml is missing or malformed
- Helm repository not added (for external charts)

**Solutions**:

```bash
# Verify chart exists
ls -la helm/Chart.yaml

# Validate Chart.yaml syntax
helm lint helm/

# Check for YAML errors
cat helm/Chart.yaml | yamllint -

# If using external chart, ensure repo is added
helm repo add myrepo https://charts.example.com
helm repo update

# List available charts
helm search repo myrepo
```

### Issue: Pods Stay in Pending State

**Symptoms**:
- `kubectl get pods` shows Pending status
- Pod doesn't transition to Running
- No error messages in describe output

**Causes**:
- Insufficient cluster resources
- Node selector mismatch
- PVC not bound
- Resource quota exceeded

**Diagnostic Steps**:

```bash
# Describe the pending pod
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Check available nodes
kubectl get nodes
kubectl describe nodes

# Check resource availability
kubectl top nodes

# Check if PVC is bound
kubectl get pvc -n {{ cookiecutter.service_slug }}

# Check resource quota
kubectl describe resourcequota -n {{ cookiecutter.service_slug }}
```

**Solutions**:

```bash
# Remove node selector constraint if not needed
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set nodeSelector=null \
  -n {{ cookiecutter.service_slug }}

# Increase cluster size
# For AWS EKS
eksctl scale nodegroup --cluster=my-cluster --name=my-nodegroup --nodes=5

# Check PVC status and ensure storage class exists
kubectl get storageclass
kubectl get pvc -n {{ cookiecutter.service_slug }}

# Increase resource quota if needed
kubectl edit resourcequota -n {{ cookiecutter.service_slug }}
```

### Issue: ImagePullBackOff Error

**Symptoms**:
- Pod status: `ImagePullBackOff`
- Event: `Failed to pull image`

**Causes**:
- Image doesn't exist in registry
- Incorrect image tag
- Registry credentials not configured
- Image pull rate limit exceeded

**Solutions**:

```bash
# Verify image exists in registry
docker pull your-registry/{{ cookiecutter.service_slug }}:v1.0.0

# Check image pull error details
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Create image pull secret if needed
kubectl create secret docker-registry regcred \
  --docker-server=your-registry \
  --docker-username=username \
  --docker-password=password \
  -n {{ cookiecutter.service_slug }}

# Update deployment to use pull secret
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set imagePullSecrets[0].name=regcred \
  -n {{ cookiecutter.service_slug }}

# Check registry rate limits
# Try pulling after some time or use a different image tag
```

### Issue: CrashLoopBackOff State

**Symptoms**:
- Pod repeatedly crashes and restarts
- Status: `CrashLoopBackOff`
- Container exit code: non-zero

**Causes**:
- Application crash on startup
- Configuration errors
- Missing dependencies
- Insufficient permissions

**Solutions**:

```bash
# Check application logs
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Check previous logs (from crash)
kubectl logs {{ cookiecutter.service_slug }}-0 --previous -n {{ cookiecutter.service_slug }}

# Increase startup timeout
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set startupProbe.failureThreshold=60 \
  --set startupProbe.periodSeconds=10 \
  -n {{ cookiecutter.service_slug }}

# Disable health checks temporarily to debug
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set livenessProbe.enabled=false \
  --set readinessProbe.enabled=false \
  -n {{ cookiecutter.service_slug }}

# Get detailed event information
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}
```

## Debugging Failed Pod Starts

### Enable Debug Mode

```bash
# Deploy a debug container in the pod
kubectl debug pod/{{ cookiecutter.service_slug }}-0 -it -n {{ cookiecutter.service_slug }}

# Or create a standalone debug pod
kubectl run debug-pod --image=debian -it --rm -n {{ cookiecutter.service_slug }} -- bash

# Inside debug container, run diagnostic commands
ps aux
netstat -tlnp
env | grep -E 'ENV|CONFIG'
```

### Check Environment Variables

```bash
# List all env vars in a pod
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- env | sort

# Check specific env var
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  printenv DATABASE_URL
```

### Verify Mount Points

```bash
# Check mounted volumes
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- mount

# List mounted volumes
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- ls -la /data

# Check permissions on mounted volumes
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  stat /data
```

### Application Initialization Debugging

```bash
# Run application with verbose logging
kubectl set env deployment/{{ cookiecutter.service_slug }} \
  LOG_LEVEL=DEBUG \
  -n {{ cookiecutter.service_slug }}

# Check initialization files
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  find /app -name "init*" -o -name "startup*"

# Verify database migrations ran
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  /app/bin/check-migrations.sh
```

## Networking Issues

### Service Discovery Not Working

**Symptoms**:
- Pods can't connect to other services
- DNS resolution fails
- Connection timeout errors

**Diagnostic Steps**:

```bash
# Test DNS resolution
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  nslookup {{ cookiecutter.service_slug }}.{{ cookiecutter.service_slug }}.svc.cluster.local

# Test connectivity to service
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  curl -v http://{{ cookiecutter.service_slug }}:8080/health

# Check CoreDNS logs (if using CoreDNS)
kubectl logs -n kube-system -l k8s-app=kube-dns -f

# Check service endpoints
kubectl get endpoints {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Verify service selector
kubectl describe service {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

**Solutions**:

```bash
# Restart CoreDNS if DNS issues
kubectl rollout restart deployment/coredns -n kube-system

# Verify service labels match selector
kubectl get pods --show-labels -n {{ cookiecutter.service_slug }}
kubectl get service {{ cookiecutter.service_slug }} -o yaml -n {{ cookiecutter.service_slug }}

# Recreate service if misconfigured
kubectl delete service {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
kubectl apply -f helm/templates/service.yaml -n {{ cookiecutter.service_slug }}
```

### External Traffic Not Reaching Service

**Symptoms**:
- LoadBalancer service shows `<pending>` for EXTERNAL-IP
- External connections fail
- Ingress shows no endpoints

**Diagnostic Steps**:

```bash
# Check service status
kubectl get service -n {{ cookiecutter.service_slug }}

# Check service endpoints
kubectl get endpoints {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Check cloud provider status (AWS)
aws elbv2 describe-load-balancers

# Check ingress status
kubectl get ingress -n {{ cookiecutter.service_slug }}
kubectl describe ingress {{ cookiecutter.service_slug }}-ingress -n {{ cookiecutter.service_slug }}

# Test service from within cluster
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/health
```

**Solutions**:

```bash
# Wait for external IP assignment (can take 5 minutes)
kubectl get svc -n {{ cookiecutter.service_slug }} -w

# Check cloud provider quotas and limits
# AWS: Check VPC limits
aws ec2 describe-account-attributes --attribute-names vpc-max-security-groups-per-interface

# Manually assign external IP if needed
kubectl patch service {{ cookiecutter.service_slug }} -p '{"spec":{"externalIP":["203.0.113.0"]}}'

# Check security groups and firewall rules
aws ec2 describe-security-groups
```

### DNS Resolution Issues

**Symptoms**:
- "Name or service not known" errors
- Services can't resolve internal DNS names

**Solutions**:

```bash
# Test DNS resolution directly
kubectl run -it --rm debug --image=ubuntu -n {{ cookiecutter.service_slug }} -- bash
apt-get update && apt-get install -y dnsutils
nslookup {{ cookiecutter.service_slug }}.{{ cookiecutter.service_slug }}.svc.cluster.local
dig {{ cookiecutter.service_slug }}.{{ cookiecutter.service_slug }}.svc.cluster.local

# Check CoreDNS configuration
kubectl get configmap coredns -n kube-system -o yaml

# Check /etc/resolv.conf in pod
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  cat /etc/resolv.conf

# Restart DNS pods
kubectl rollout restart deployment/coredns -n kube-system
```

## Storage and Volume Troubleshooting

### PersistentVolumeClaim Stuck in Pending

**Symptoms**:
- PVC status: `Pending`
- Pod can't start due to PVC not bound
- "no persistent volumes available" errors

**Solutions**:

```bash
# Check PVC status
kubectl describe pvc -n {{ cookiecutter.service_slug }}

# Verify storage class exists
kubectl get storageclass

# Check available PVs
kubectl get pv

# If using dynamic provisioning, check provisioner
kubectl get storageclass -o yaml

# Create PV manually if needed
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {{ cookiecutter.service_slug }}-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/{{ cookiecutter.service_slug }}
EOF

# Check if storage provisioner is running
kubectl get pods -n kube-system | grep provision
```

### Volume Mount Failures

**Symptoms**:
- Pod fails to mount volume
- "Unable to mount volumes" errors
- Data not persisted

**Solutions**:

```bash
# Check volume mount status
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Verify volume source exists
kubectl get pvc -n {{ cookiecutter.service_slug }}

# Check mount permissions
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  ls -la /data

# Verify volume path in StatefulSet
kubectl get statefulset {{ cookiecutter.service_slug }} -o yaml -n {{ cookiecutter.service_slug }} | \
  grep -A 20 "volumeMounts"

# Test volume access
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  touch /data/test.txt

# Check storage node affinity
kubectl get pvc -n {{ cookiecutter.service_slug }} -o yaml | grep -A 5 "nodeAffinity"
```

### Data Loss or Corruption

**Solutions**:

```bash
# Check filesystem integrity
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  fsck -n /dev/pvc-xxx  # (if accessible)

# Verify backup exists
ls -la backup-{{ cookiecutter.service_slug }}.tar.gz

# Restore from backup
tar xzf backup-{{ cookiecutter.service_slug }}.tar.gz -C /

# Create backup before recovery attempts
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  tar czf - /data | gzip > backup-$(date +%Y%m%d-%H%M%S).tar.gz
```

## Performance Optimization

### High CPU Usage

**Symptoms**:
- CPU usage consistently above 80%
- kubectl top shows high CPU values
- Response times degrading

**Investigation**:

```bash
# Check CPU metrics
kubectl top pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Profile CPU usage (requires profiling tool)
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  curl http://localhost:8080/debug/pprof/profile

# Check for goroutine leaks (Go services)
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  curl http://localhost:8080/debug/pprof/goroutine
```

**Solutions**:

```bash
# Increase CPU requests/limits
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set resources.requests.cpu=1000m \
  --set resources.limits.cpu=2000m \
  -n {{ cookiecutter.service_slug }}

# Enable CPU throttling/cgroup limits
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set resources.limits.cpu=2000m \
  -n {{ cookiecutter.service_slug }}

# Scale out to more replicas
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set replicaCount=5 \
  -n {{ cookiecutter.service_slug }}

# Enable HPA for automatic scaling
kubectl apply -f hpa.yaml -n {{ cookiecutter.service_slug }}
```

### High Memory Usage

**Symptoms**:
- Memory usage increasing over time
- OOMKilled pod status
- "Cannot allocate memory" errors

**Investigation**:

```bash
# Check memory metrics
kubectl top pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Check for memory leaks
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  cat /proc/meminfo

# Profile heap (Java/Python services)
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  jmap -heap <pid>
```

**Solutions**:

```bash
# Increase memory limits
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set resources.requests.memory=1024Mi \
  --set resources.limits.memory=2048Mi \
  -n {{ cookiecutter.service_slug }}

# Configure JVM heap (if Java)
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set jvm.heapMin=512m \
  --set jvm.heapMax=1024m \
  -n {{ cookiecutter.service_slug }}

# Check for connection leaks
# Restart affected pod
kubectl delete pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Enable memory profiling
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set env[0].name=DEBUG_MEMORY \
  --set env[0].value=true \
  -n {{ cookiecutter.service_slug }}
```

### Slow Response Times

**Symptoms**:
- API response times > 500ms
- Timeouts in logs
- Increased error rates

**Investigation**:

```bash
# Check latency metrics
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
# Run load test
ab -n 100 -c 10 http://localhost:8080/health

# Check database query performance
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  psql -c "SELECT * FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Check network latency
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  ping -c 5 database.default.svc.cluster.local

# Check service endpoints
kubectl get endpoints {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

**Solutions**:

```bash
# Add caching layer
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set cache.enabled=true \
  --set cache.ttl=300 \
  -n {{ cookiecutter.service_slug }}

# Increase database connection pool
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set database.poolSize=50 \
  -n {{ cookiecutter.service_slug }}

# Enable request compression
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set config.compression=true \
  -n {{ cookiecutter.service_slug }}

# Scale database if needed
# Connect to database and optimize slow queries

# Add rate limiting
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set rateLimit.enabled=true \
  --set rateLimit.requestsPerSecond=1000 \
  -n {{ cookiecutter.service_slug }}
```

## Log Analysis and Debugging

### Viewing Application Logs

```bash
# View logs from single pod
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# View logs from all pods
kubectl logs -l app={{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Follow logs in real-time
kubectl logs -f {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# View logs with timestamps
kubectl logs {{ cookiecutter.service_slug }}-0 --timestamps=true -n {{ cookiecutter.service_slug }}

# View logs from specific time range
kubectl logs {{ cookiecutter.service_slug }}-0 --since=1h -n {{ cookiecutter.service_slug }}

# View last N lines
kubectl logs {{ cookiecutter.service_slug }}-0 --tail=100 -n {{ cookiecutter.service_slug }}

# View previous pod logs (after crash)
kubectl logs {{ cookiecutter.service_slug }}-0 --previous -n {{ cookiecutter.service_slug }}
```

### Log Filtering and Searching

```bash
# Filter by log level
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} | \
  grep -i "ERROR\|FATAL"

# Search for specific error pattern
kubectl logs -l app={{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }} | \
  grep "DatabaseConnection"

# Count log lines by level
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} | \
  grep -oE "^\[ERROR\]|\[WARN\]|\[INFO\]" | sort | uniq -c

# Export logs to file
kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} > app.log
```

### Centralized Log Analysis with ELK

```bash
# Query Elasticsearch for errors
curl -X GET "localhost:9200/logs-*/_search?q=level:ERROR"

# Kibana queries
# Create index pattern: logs-*
# Build dashboard filtering by service: {{ cookiecutter.service_slug }}
# Create alerts for error rates > threshold
```

## Resource Constraint Issues

### Out of Memory (OOMKilled)

**Symptoms**:
- Pod status: `OOMKilled`
- Exit code: 137
- "Killed" message in logs

**Solutions**:

```bash
# Check memory usage
kubectl top pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Increase memory limits
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set resources.limits.memory=2048Mi \
  -n {{ cookiecutter.service_slug }}

# Check for memory leaks in code
# Review application logs for leak patterns

# Enable memory monitoring
kubectl top pod -n {{ cookiecutter.service_slug }} --containers
```

### CPU Throttling

**Symptoms**:
- Pods experiencing performance degradation
- CPU cgroup throttling in metrics
- Response time variability

**Solutions**:

```bash
# Check current CPU limits
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Increase CPU limits
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set resources.limits.cpu=2000m \
  --set resources.requests.cpu=1000m \
  -n {{ cookiecutter.service_slug }}

# Monitor CPU throttling
kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/{{ cookiecutter.service_slug }}/pods
```

### Disk Space Issues

**Symptoms**:
- "No space left on device" errors
- Pod eviction due to disk pressure
- Persistent volume full

**Solutions**:

```bash
# Check disk usage
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- df -h

# Identify large files
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  find /data -type f -size +100M

# Clean up old logs
kubectl exec {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -- \
  find /var/log -mtime +7 -delete

# Expand persistent volume
kubectl patch pvc {{ cookiecutter.service_slug }}-pvc \
  -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}' \
  -n {{ cookiecutter.service_slug }}

# Monitor disk space usage
kubectl top pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}
```

## Health Check Failures

### Liveness Probe Failing

**Symptoms**:
- Pod being killed and restarted
- "Liveness probe failed" in events
- High restart count

**Solutions**:

```bash
# Check endpoint availability
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/health/live

# Increase probe timeout
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set healthChecks.liveness.timeoutSeconds=10 \
  -n {{ cookiecutter.service_slug }}

# Check probe dependencies
# Ensure database, cache, etc. are available

# Disable liveness probe temporarily
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set livenessProbe.enabled=false \
  -n {{ cookiecutter.service_slug }}
```

### Readiness Probe Failing

**Symptoms**:
- Pod marked not ready
- Service has no endpoints
- Traffic not reaching pod

**Solutions**:

```bash
# Test readiness endpoint
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/health/ready

# Check initialization status
kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}

# Increase initial delay
helm upgrade {{ cookiecutter.service_slug }} helm/ \
  --set healthChecks.readiness.initialDelaySeconds=30 \
  -n {{ cookiecutter.service_slug }}

# Check dependencies (database, cache)
# Ensure all required services are running
```

## Testing and Validation

### Smoke Testing

Run basic smoke tests after deployment:

```bash
# Test service availability
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}

# Test health endpoints
curl http://localhost:8080/health
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready

# Test API basic functionality
curl -X GET http://localhost:8080/api/v1/status
curl -X POST http://localhost:8080/api/v1/data -d '{"test":"data"}'

# Test metrics endpoint
curl http://localhost:8080/metrics
```

### Integration Testing

```bash
# Run integration tests in cluster
kubectl apply -f tests/integration-tests-job.yaml -n {{ cookiecutter.service_slug }}

# Monitor test progress
kubectl logs -f job/integration-tests -n {{ cookiecutter.service_slug }}

# Check test results
kubectl describe job integration-tests -n {{ cookiecutter.service_slug }}
```

### Load Testing

```bash
# Deploy load testing tool
kubectl run load-test --image=grafana/k6 -it -n {{ cookiecutter.service_slug }} -- \
  k6 run /scripts/load-test.js

# Monitor under load
kubectl top pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} -w

# Check response times
# Review metrics in Prometheus
```

### Health Check Validation

```bash
# Verify all health checks pass
for check in health health/live health/ready; do
  status=$(curl -s http://localhost:8080/$check | jq -r '.status')
  echo "$check: $status"
done

# Check pod readiness
kubectl get pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }} \
  -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
```

## Troubleshooting Checklist

Before reaching out for support, verify:

- [ ] Pod status is Running
- [ ] All containers are ready
- [ ] Health probes are passing
- [ ] Service has endpoints
- [ ] Network connectivity between services works
- [ ] Resource limits are not exceeded
- [ ] PersistentVolumes are mounted and accessible
- [ ] Logs show no critical errors
- [ ] ConfigMaps and Secrets are properly mounted
- [ ] Database and external dependencies are accessible

## Getting Help

If issues persist after following this guide:

1. Collect diagnostic information:
   ```bash
   kubectl describe pod {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}
   kubectl logs {{ cookiecutter.service_slug }}-0 -n {{ cookiecutter.service_slug }}
   kubectl get events -n {{ cookiecutter.service_slug }} --sort-by='.lastTimestamp'
   helm get values {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
   ```

2. Review related documentation:
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment procedures
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
   - [API.md](./API.md) - API documentation

3. Check cloud provider documentation for region-specific issues

4. Consult Kubernetes documentation for cluster-level issues
