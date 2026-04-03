import pandas as pd
from glob import glob
from pathlib import Path


def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        participant = Path(f).name.split("-")[0]
        label = Path(f).name.split("-")[1]
        category = Path(f).name.split("-")[2].rstrip("2").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)

        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df])

        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df])

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del gyr_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del gyr_df["time (01:00)"]
    del acc_df["elapsed (s)"]
    del gyr_df["elapsed (s)"]

    return acc_df, gyr_df


files = glob("../../data/raw/MetaMotion/*.csv")
acc_df, gyr_df = read_data_from_files(files)

data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)
data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "label",
    "category",
    "participant",
    "set",
]


sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "label": "last",
    "category": "last",
    "participant": "last",
    "set": "last",
}
data_merged[:1000].resample("200ms").apply(sampling)
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
data_resambled = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)
data_resambled["set"] = data_resambled["set"].astype("int")
data_resambled.info()


data_resambled.to_pickle("../../data/interim/01_data_processed.pkl")
# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
# single_file_acc = pd.read_csv(
#     "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
# )

# single_file_gyt = pd.read_csv(
#     "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"
# )


# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

# len(files)

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
# data_path = "../../data/raw/MetaMotion/"
# participant = Path(files[0]).name.split("-")[0]
# label = Path(files[0]).name.split("-")[1]
# category = Path(files[0]).name.split("-")[2].rstrip("2")

# df = pd.read_csv(files[0])
# df["participant"] = participant
# df["label"] = label
# df["category"] = category
# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
