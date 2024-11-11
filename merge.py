import pandas as pd
from datetime import datetime, timedelta

file1516 = pd.read_csv("1516.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file1617 = pd.read_csv("1617.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file1718 = pd.read_csv("1718.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file1819 = pd.read_csv("1819.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file1920 = pd.read_csv("1920.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file2021 = pd.read_csv("2021.csv", usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
file2122 = pd.read_csv("2122.csv", usecols=["Date","HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])

# Concatenate the data from both files
combined_data = pd.concat([file1516, file1617, file1718, file1819, file1920,  file2021, file2122], ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv("combined_file.csv", index=False)

##########################
# Load the combined dataset
combined_data = pd.read_csv("combined_file.csv")

# Define the teams you want to analyze for head-to-head data
team_a = "Man United"  # Replace with the actual team name you're interested in
team_b = "Man City"  # Replace with the actual team name you're interested in

# Filter for head-to-head matches between team_a and team_b
head_to_head_data = combined_data[
    ((combined_data['HomeTeam'] == team_a) & (combined_data['AwayTeam'] == team_b)) |
    ((combined_data['HomeTeam'] == team_b) & (combined_data['AwayTeam'] == team_a))
]

# Save the filtered data into a new CSV file
head_to_head_data.to_csv("head_to_head_data.csv", index=False)