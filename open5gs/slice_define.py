import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import yaml

# Load dataset
df = pd.read_csv("train_dataset.csv")

# Mapping integer slice types to readable names
slice_name_map = {
    0: "eMBB",
    1: "URLLC",
    2: "mMTC",
    3: "Custom"
}

# Split features and label
X = df.drop(columns=["slice Type"])
y = df["slice Type"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = model.predict(X_test_scaled)
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# Save model & scaler
joblib.dump(model, "slice_classifier.pkl")
joblib.dump(scaler, "scaler.pkl")

# Build `network_slices` block
network_slices = []
for slice_id, slice_name in slice_name_map.items():
    if slice_id not in df["slice Type"].values:
        print(f"⚠️ No data for slice {slice_name}, skipping.")
        continue
    network_slices.append({
        "slice_id": str(slice_id + 1),
        "slice_name": slice_name,
        "slice_type": slice_name,
        "relative_capacity": 100 - (slice_id * 25)  # Example logic
    })

# Build AMF config dict in Open5GS format
amf_config = {
    "logger": {
        "file": {
            "path": "/var/log/open5gs/amf.log"
        }
    },
    "global": {
        "max": {
            "ue": 1024
        }
    },
    "amf": {
        "sbi": {
            "server": [{"address": "192.168.40.102", "port": 7777}],
            "client": {
                "scp": [{"uri": "http://127.0.0.200:7777"}]
            }
        },
        "ngap": {
            "server": [{"address": "192.168.40.102"}]
        },
        "metrics": {
            "server": [{"address": "192.168.40.102", "port": 9090}]
        },
        "guami": [{
            "plmn_id": {"mcc": "999", "mnc": "70"},
            "amf_id": {"region": 2, "set": 1}
        }],
        "tai": [{
            "plmn_id": {"mcc": "999", "mnc": "70"},
            "tac": 1
        }],
        "plmn_support": [{
            "plmn_id": {"mcc": "999", "mnc": "70"},
            "s_nssai": [
                {"sst": 1, "sd": "000001"},
                {"sst": 2, "sd": "000002"},
                {"sst": 3, "sd": "000003"},
                {"sst": 4, "sd": "000004"}
            ]
        }],
        "security": {
            "integrity_order": ["NIA2", "NIA1", "NIA0"],
            "ciphering_order": ["NEA0", "NEA1", "NEA2"]
        },
        "network_name": {
            "full": "Open5GS",
            "short": "Next"
        },
        "amf_name": "open5gs-amf0",
        "time": {
            "t3512": {
                "value": 540
            }
        },
        "network_slices": network_slices
    }
}

# Save to YAML
with open("amf.yaml", "w") as f:
    yaml.dump(amf_config, f, sort_keys=False)

print("✅ amf.yaml saved with slices:", ", ".join([ns["slice_name"] for ns in network_slices]))

