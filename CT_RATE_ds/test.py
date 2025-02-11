import pandas as pd

df = pd.read_csv(
    "/home/dhxmo/Builds/builds/Autonosis/01_MVP/open_clip/CT_RATE_ds/valid_reports.csv",
    sep=",",
)
images = df["filepath"].tolist()
print("images", images)
