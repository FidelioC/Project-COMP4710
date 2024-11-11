import pandas as pd

# Load datasets
h2h_data = pd.read_csv("h2h_stats_all_seasons.csv")  # Contains H2H stats data
match_data = pd.read_csv("combined_schedule_stats.csv")  # Contains the main match data

# Merge the datasets on HomeTeam and AwayTeam to get the H2H stats into the match_data
merged_data = pd.merge(
    match_data,
    h2h_data,
    how="left",
    left_on=["HomeTeam", "AwayTeam"],
    right_on=["Home team", "Away team"],
)

# Drop the redundant columns after merging
merged_data = merged_data.drop(columns=["Home team", "Away team"])

# Reorder the columns to match the required format
ordered_columns = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "Home team Points",
    "Home team Goal scored",
    "Home team Goal conceded",
    "Home team Shot on target",
    "Home team Red Cards",
    "Away team Points",
    "Away team Goal scored",
    "Away team Goal conceded",
    "Away team Shot on target",
    "Away team Red Cards",
    "Home team Points H2H",
    "Home team Goal scored H2H",
    "Home Team Red Cards H2H",
    "Home Team Shot on Target H2H",
    "Away team Points H2H",
    "Away team Goal scored H2H",
    "Away Team Red Cards H2H",
    "Away Team Shot on Target H2H",
]

# Select and reorder columns
merged_data = merged_data[ordered_columns]

# Save the merged data to a new CSV file
merged_data.to_csv("merged_final_data.csv", index=False)

# Display the first few rows of the result
print(merged_data.head())
