import pandas as pd
import os

directory = "./prediction_test/Datasets"
output = "./prediction_test/combined_file.csv"
data_frames = []

for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)

        print(file_path)

        current_file = pd.read_csv(
            file_path,
            usecols=[
                "Date",
                "HomeTeam",
                "AwayTeam",
                "FTHG",
                "FTAG",
                "HST",
                "AST",
                "HR",
                "AR",
                "FTR",
            ],
        )

        data_frames.append(current_file)

# Concatenate the data from both files
combined_data = pd.concat(
    data_frames,
    ignore_index=True,
)

# Save the combined data to a new CSV file
combined_data.to_csv(output, index=False)
