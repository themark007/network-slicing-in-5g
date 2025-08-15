import time
import psutil
import csv
from datetime import datetime

# Define interfaces and slice labels
interfaces = {
    "uesimtun0": "Browsing",
    "uesimtun1": "IoT",
    "uesimtun2": "Video"
}

output_file = "traffic_log.csv"

# Initialize counters
prev_bytes = {}

print("[DEBUG] Starting traffic monitor...")

# Header for CSV
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Interface", "Slice", "RX_Bytes", "TX_Bytes"])

try:
    for _ in range(30):  # Run only for 30 seconds
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        counters = psutil.net_io_counters(pernic=True)

        for iface, slice_type in interfaces.items():
            rx = counters[iface].bytes_recv
            tx = counters[iface].bytes_sent

            # Calculate deltas (for debugging)
            prev_rx, prev_tx = prev_bytes.get(iface, (rx, tx))
            delta_rx = rx - prev_rx
            delta_tx = tx - prev_tx
            prev_bytes[iface] = (rx, tx)

            print(f"[DEBUG] {iface} ({slice_type}): RX={delta_rx}, TX={delta_tx}")

            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, iface, slice_type, delta_rx, delta_tx])

        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Traffic monitor stopped by user.")

print("[INFO] Traffic logging complete.")

