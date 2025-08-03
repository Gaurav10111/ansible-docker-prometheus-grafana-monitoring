# Dockerized Microservice Monitoring with Prometheus, Grafana, and Node Exporter via Ansible

## 📌 Project Overview
This project provisions a complete **Docker-based monitoring stack** for microservices using:
- **Prometheus** for metrics collection
- **Grafana** for visualization
- **Node Exporter** for system-level metrics
- **Custom-built microservices** exposing `/metrics`
- **Persistent storage** to retain data across restarts

The entire setup is automated using **Ansible** from a **Control Node EC2** to a **Monitoring Node EC2**.  
All images are built **manually from official tarballs** (no DockerHub images).

---

## 🏗 Architecture

[ Ansible EC2 (Control Node) ]  
│  
│ SSH (Ansible)  
▼  
[ Monitoring EC2 (Docker Host) ]  
├── Prometheus container  
├── Grafana container  
├── Node Exporter container  
├── Microservice 1 container (/metrics)  
└── Microservice 2 container (/metrics)  


---

## 📂 Folder Structure

monitoring-project/  
├── ansible/  
│ ├── inventory.ini  
│ ├── playbook.yml  
│ └── roles/  
│ ├── docker-install/  
│ │ └── tasks/main.yml  
│ ├── microservice/  
│ │ └── tasks/main.yml  
│ ├── prometheus/  
│ │ └── tasks/main.yml  
│ ├── grafana/  
│ │ └── tasks/main.yml  
│ └── node_exporter/  
│ └── tasks/main.yml  
├── dockerfiles/  
│ ├── microservice-app/  
│ │ ├── Dockerfile  
│ │ └── app/  
│ │ ├── main.py  
│ │ └── requirements.txt  
│ ├── prometheus/  
│ │ ├── Dockerfile  
│ │ └── prometheus.yml  
│ ├── grafana/  
│ │ └── Dockerfile  
│ └── node_exporter/  
│ └── Dockerfile  
└── persistent/ # Created on Monitoring Node (host machine)  
├── prometheus/  
└── grafana/  


---

## ⚙ Workflow

### 1️⃣ Provision EC2 Instances
- **Control Node EC2** → Runs Ansible
- **Monitoring Node EC2** → Runs Docker & containers

### 2️⃣ Ansible Inventory Configuration
- File: `ansible/inventory.ini`
- Define Monitoring Node's **private IP** for Ansible SSH connection.

### 3️⃣ Install Docker on Monitoring Node
- Role: `ansible/roles/docker-install/tasks/main.yml`
- Configures Docker with metrics endpoint (`/etc/docker/daemon.json`).

### 4️⃣ Deploy Microservices
- Role: `ansible/roles/microservice/tasks/main.yml`
- Builds and runs **two microservice instances**:
  - Microservice 1: App → `http://<private-ip>:8000`, Metrics → `http://<private-ip>:8001/metrics`
  - Microservice 2: App → `http://<private-ip>:8002`, Metrics → `http://<private-ip>:8003/metrics`

### 5️⃣ Deploy Prometheus
- Role: `ansible/roles/prometheus/tasks/main.yml`
- Configuration file: `dockerfiles/prometheus/prometheus.yml`
- **Prometheus targets**:
  ```yaml
  scrape_configs:
    - job_name: 'node_exporter'
      static_configs:
        - targets: ['<private-ip>:9100']

    - job_name: 'docker_engine'
      static_configs:
        - targets: ['<private-ip>:9323']

    - job_name: 'microservices'
      static_configs:
        - targets: ['<private-ip>:8001', '<private-ip>:8003']
  
### 6️⃣ Deploy Grafana
- Role: `ansible/roles/grafana/tasks/main.yml`

- Access Grafana UI: `http://<private-ip>:3000 (Default credentials: admin/admin)`

### 7️⃣ Deploy Node Exporter
- Role: `ansible/roles/node_exporter/tasks/main.yml`

- `Collects host-level metrics on port 9100.`

### 8️⃣ Persistent Storage
- **Host directories created on Monitoring Node:**

`/persistent/prometheus`  # Mounted to Prometheus container  

`/persistent/grafana`     # Mounted to Grafana container  

- **Volume mounts in roles:**  

**Prometheus:** `-v /persistent/prometheus:/opt/prometheus/data`  

**Grafana:** `-v /persistent/grafana:/opt/grafana/data`  

---

## 🔍 Endpoints

**Component	Endpoint (Replace <private-ip> with Monitoring Node's private IP)**  

- Microservice 1 App	`http://<private-ip>:8000`
  
- Microservice 1 Metrics	`http://<private-ip>:8001/metrics`  

- Microservice 2 App	`http://<private-ip>:8002`  

- Microservice 2 Metrics	`http://<private-ip>:8003/metrics`  

- Prometheus UI	`http://<private-ip>:9090`  

- Grafana UI	`http://<private-ip>:3000`  

- Node Exporter Metrics	`http://<private-ip>:9100/metrics`  

- Docker Engine Metrics	`http://<private-ip>:9323/metrics`  

## 📊 Grafana Dashboard  
- Add Prometheus as a data source: `http://<private-ip>:9090`  

- Import Dashboard ID: 1860 (Node Exporter Full)  

## 🏁 Summary
**This project demonstrates:**

- Fully automated monitoring stack provisioning via Ansible

- No dependency on DockerHub images (built from official tarballs)

- Persistent data storage for Prometheus & Grafana

- Multi-instance microservice monitoring with /metrics endpoints

- Unified dashboards in Grafana
