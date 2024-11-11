import pandas as pd
import os

directory = "./english_premier/Datasets"
data_frames = []

for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)

    current_file = pd.read_csv(
        file_path,
        usecols=[
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "FTR",
            "HST",
            "AST",
            "HR",
            "AR",
        ],
    )

    data_frames.append(current_file)

# Concatenate the data from both files
combined_data = pd.concat(
    data_frames,
    ignore_index=True,
)

# Save the combined data to a new CSV file
combined_data.to_csv("combined_file.csv", index=False)

##########################
# Load the combined dataset
combined_data = pd.read_csv("combined_file.csv")
