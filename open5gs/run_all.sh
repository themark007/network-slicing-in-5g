#!/bin/bash

echo "=== Starting Traffic Generation and Monitoring ==="

# Define UE interfaces and IPs
BROWSE_IF="uesimtun0"
VIDEO_IF="uesimtun2"
IOT_IF="uesimtun1"

BROWSE_IP="10.45.0.9"
IOT_IP="10.45.0.10"
VIDEO_IP="10.45.0.11"

# -----------------------
# Browsing traffic (simulated by periodic curl)
# -----------------------
echo "[INFO] Starting Browsing Traffic on $BROWSE_IF ($BROWSE_IP)..."
for i in {1..5}; do
    curl --interface $BROWSE_IF http://speedtest.tele2.net/100KB.zip --output /dev/null --silent &
    echo "[DEBUG] curl download triggered on $BROWSE_IF (Iteration $i)"
    sleep 2
done

# -----------------------
# Start iperf3 server (in background)
# -----------------------
echo "[INFO] Starting iperf3 Server in background..."
iperf3 -s -p 5201 > /dev/null 2>&1 &
sleep 2  # Wait for server to start

# -----------------------
# Video traffic (iperf3 client from VIDEO_IF)
# -----------------------
echo "[INFO] Starting Video Traffic on $VIDEO_IF ($VIDEO_IP)..."
iperf3 -c 127.0.0.1 -B $VIDEO_IP -t 15 -p 5201 > /dev/null 2>&1 &
echo "[DEBUG] iperf3 launched on $VIDEO_IF with bind IP $VIDEO_IP"

# -----------------------
# IoT traffic (ping loop from IOT_IF)
# -----------------------
echo "[INFO] Starting IoT ping loop on $IOT_IF ($IOT_IP)..."
for i in {1..10}; do
    ping -I $IOT_IF -c 1 8.8.8.8 > /dev/null 2>&1
    echo "[DEBUG] Ping sent from $IOT_IF (Iteration $i)"
    sleep 1
done

# -----------------------
# Launch traffic monitor script
# -----------------------
echo "[INFO] Launching traffic monitor (traffic.py)..."
python3 traffic.py &

# -----------------------
# Wait for monitor or kill manually
# -----------------------
echo "[INFO] Monitoring running in background. Press Ctrl+C to stop manually."
wait

