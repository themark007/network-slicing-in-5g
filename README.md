# 📡 Intelligent Network Slicing in 5G

> **"Bringing intelligence to 5G – enabling smarter, faster, and more efficient network slicing."**

---

## 📖 Overview

This project implements **intelligent network slicing in 5G networks** using **both physical testbed** and **simulation environments**.  
It enables **dynamic resource allocation** for three key 5G service categories:

- 📶 **eMBB** – Enhanced Mobile Broadband  
- ⚡ **URLLC** – Ultra-Reliable Low Latency Communications  
- 📡 **mMTC** – massive Machine-Type Communications  

The system uses **Machine Learning** (Random Forest Classifier) for **slice prediction** and allocation based on **real-time traffic characteristics**.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🚀 Dual Implementation | Physical testbed + simulation |
| 🤖 AI Slice Prediction | Random Forest Classifier (93% accuracy) |
| 📶 Multi-Slice Support | eMBB, URLLC, mMTC |
| 📊 Real-Time Monitoring | Prometheus + Grafana dashboards |
| 🔧 Dynamic Resource Allocation | Intelligent load management |
| 📡 End-to-End 5G Core | Full Open5GS deployment |

---

## 🏗️ System Architecture

![System Architecture](https://github.com/user-attachments/assets/1cd62d7b-a40c-4270-a51c-4589c1e1160c)

---

## 🛠️ Technology Stack

### **Core Components**
| Component | Purpose |
|-----------|---------|
| **Open5GS** | 5G Core Network |
| **srsRAN** | Radio Access Network (Testbed) |
| **UERANSIM** | UE & gNB Simulation |
| **USRP B210** | Software-Defined Radio |

### **AI & Monitoring Tools**
| Tool | Purpose |
|------|---------|
| **Random Forest Classifier** | Slice prediction |
| **Wireshark** | Traffic analysis |
| **Prometheus + Grafana** | Performance monitoring |
| **iperf3** | Traffic generation |

---

## 📈 Results

### **Performance Improvements**
| Metric                | Improvement               |
|-----------------------|---------------------------|
| **Throughput**        | Up to **180% increase**    |
| **Latency**           | Up to **63.6% reduction** |
| **Bandwidth Utilization** | Excellent for eMBB       |

### **Slice Prediction Accuracy**
| Slice Type | Precision | Recall | F1-Score |
|------------|-----------|--------|----------|
| **eMBB**   | 0.98      | 0.96   | 0.97     |
| **URLLC**  | 0.90      | 0.90   | 0.90     |
| **mMTC**   | 0.92      | 0.94   | 0.93     |


## 📦 Installation Guide

### **Prerequisites**
- Ubuntu **20.04 LTS**
- Docker
- Python **3.8+**
- USRP B210 (for testbed use)

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/yourusername/network-slicing-in-5g.git
cd 5g-network-slicing

# Install dependencies
sudo apt update
sudo apt install -y docker.io python3-pip wireshark

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build Docker containers
docker-compose up -d

# Install UERANSIM
# (Download from official repository: https://github.com/aligungr/UERANSIM)


# amf.yaml
slices:
  - sst: 1  # eMBB
    sd: 0x010101
  - sst: 2  # URLLC
    sd: 0x020202
  - sst: 3  # mMTC
    sd: 0x030303


# ue.yaml
ues:
  - imsi: '001010123456789'
    slice:
      sst: 1
      sd: 0x010101
    dnn: internet1
# Start 5G core
docker-compose up -d

# Start gNB (Testbed)
sudo srsenb --config=gnb.conf

# Start UERANSIM simulator
./nr-gnb -c gnb.yaml
./nr-ue -c ue.yaml


# Start iperf server
iperf3 -s -p 5201

# Start UE clients
iperf3 -c server_ip -p 5201 -u -b 4M        # eMBB
iperf3 -c server_ip -p 5201 -u -b 1M -t 0.001 # URLLC


from slicing_ai import predict_slice

# Sample traffic metrics
metrics = {
    'latency': 25,
    'throughput': 85,
    'jitter': 5,
    'packet_loss': 0.1
}

slice_type = predict_slice(metrics)
print(f"Recommended slice: {slice_type}")
```
