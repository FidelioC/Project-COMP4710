import pandas as pd
from datetime import datetime, timedelta
import os

# Load the combined dataset
combined_data = pd.read_csv("combined_file.csv")

# Initialize an empty dictionary to hold H2H stats
h2h_stats = {}

# Iterate over each row in the data to accumulate stats
for _, row in combined_data.iterrows():
    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    # Create a unique key for each home and away team pair
    matchup_key = (home_team, away_team)

    # Initialize the matchup data if this pair hasn't been seen before
    if matchup_key not in h2h_stats:
        h2h_stats[matchup_key] = {
            "Home team Points H2H": 0,
            "Home team Goal scored H2H": 0,
            "Home Team Red Cards H2H": 0,
            "Home Team Shot on Target H2H": 0,
            "Away team Points H2H": 0,
            "Away team Goal scored H2H": 0,
            "Away Team Red Cards H2H": 0,
            "Away Team Shot on Target H2H": 0,
        }

    # Calculate points based on FTR
    if row["FTR"] == "H":  # Home team wins
        h2h_stats[matchup_key]["Home team Points H2H"] += 3
    elif row["FTR"] == "A":  # Away team wins
        h2h_stats[matchup_key]["Away team Points H2H"] += 3
    elif row["FTR"] == "D":  # Draw
        h2h_stats[matchup_key]["Home team Points H2H"] += 1
        h2h_stats[matchup_key]["Away team Points H2H"] += 1

    # Accumulate goals, red cards, and shots for home and away teams
    h2h_stats[matchup_key]["Home team Goal scored H2H"] += row["FTHG"]
    h2h_stats[matchup_key]["Home Team Red Cards H2H"] += row["HR"]
    h2h_stats[matchup_key]["Home Team Shot on Target H2H"] += row["HST"]

    h2h_stats[matchup_key]["Away team Goal scored H2H"] += row["FTAG"]
    h2h_stats[matchup_key]["Away Team Red Cards H2H"] += row["AR"]
    h2h_stats[matchup_key]["Away Team Shot on Target H2H"] += row["AST"]

# Convert the dictionary to a DataFrame for easier handling and export
h2h_stats_df = pd.DataFrame(
    [
        {"Home team": home_team, "Away team": away_team, **stats}
        for (home_team, away_team), stats in h2h_stats.items()
    ]
)

# Save the H2H stats to a new CSV file
h2h_stats_df.to_csv("h2h_stats_all_seasons.csv", index=False)

# Display the first few rows of the result
print(h2h_stats_df.head())
