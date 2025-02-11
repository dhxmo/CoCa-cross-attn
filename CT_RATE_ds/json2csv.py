import json
import os
import pandas as pd

base_path = "/root/data_volumes/dataset/"

# Load JSON file
with open("valid_reports.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract rows
rows = [entry["row"] for entry in data["rows"]]

# Convert to DataFrame
df = pd.DataFrame(rows)


# Function to generate correct file path
def get_full_path(volume_name):
    parts = volume_name.split(
        "_"
    )  # Split "valid_1_a_1.nii.gz" → ['valid', '1', 'a', '1.nii.gz']
    if len(parts) < 4 or "2" in parts[3]:
        return None  # Fallback if format is unexpected

    base = parts[0]
    base_no = f"{base}_{parts[1]}"  # e.g., "valid_1"
    base_no_version = f"{base_no}_{parts[2]}"  # e.g., "valid_1_a"

    return os.path.join(base_path, base, base_no, base_no_version, volume_name)


# Add file path to VolumeName
df["VolumeName"] = df["VolumeName"].apply(get_full_path)

# Remove rows where VolumePath is None (i.e., those that had "_b")
df = df.dropna(subset=["VolumeName"])
df.rename(columns={"VolumeName": "filepath"}, inplace=True)
df.rename(columns={"Impressions_EN": "title"}, inplace=True)
df.drop(columns=["ClinicalInformation_EN", "Technique_EN", "Findings_EN"], inplace=True)

# Convert to CSV
df.to_csv("valid_reports.csv", index=False)
