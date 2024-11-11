import pandas as pd

# Load the first file (match schedule) into a DataFrame
schedule_df = pd.read_csv("./prediction_test/epl_results_2022-23.csv")

# Load the second file (team statistics) into a DataFrame
stats_df = pd.read_csv("team_stats.csv")

# Set the 'Team' column as the index in the stats DataFrame for easier lookup
stats_df.set_index("Team", inplace=True)

# Initialize lists to store the home and away team stats for each match
home_team_points = []
home_team_goals_scored = []
home_team_goals_conceded = []
home_team_shots = []
home_team_red_cards = []

away_team_points = []
away_team_goals_scored = []
away_team_goals_conceded = []
away_team_shots = []
away_team_red_cards = []

# Iterate over each match in the schedule
for _, row in schedule_df.iterrows():
    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    # Retrieve stats for the home team
    if home_team in stats_df.index:
        home_team_points.append(stats_df.at[home_team, "Points"])
        home_team_goals_scored.append(stats_df.at[home_team, "Total Goals Scored"])
        home_team_goals_conceded.append(stats_df.at[home_team, "Total Goals Conceded"])
        home_team_shots.append(stats_df.at[home_team, "Total Shots"])
        home_team_red_cards.append(stats_df.at[home_team, "Total Red Cards"])
    else:
        home_team_points.append(None)
        home_team_goals_scored.append(None)
        home_team_goals_conceded.append(None)
        home_team_shots.append(None)
        home_team_red_cards.append(None)

    # Retrieve stats for the away team
    if away_team in stats_df.index:
        away_team_points.append(stats_df.at[away_team, "Points"])
        away_team_goals_scored.append(stats_df.at[away_team, "Total Goals Scored"])
        away_team_goals_conceded.append(stats_df.at[away_team, "Total Goals Conceded"])
        away_team_shots.append(stats_df.at[away_team, "Total Shots"])
        away_team_red_cards.append(stats_df.at[away_team, "Total Red Cards"])
    else:
        away_team_points.append(None)
        away_team_goals_scored.append(None)
        away_team_goals_conceded.append(None)
        away_team_shots.append(None)
        away_team_red_cards.append(None)

# Add the collected stats to the schedule DataFrame
schedule_df["Home team Points"] = home_team_points
schedule_df["Home team Goal scored"] = home_team_goals_scored
schedule_df["Home team Goal conceded"] = home_team_goals_conceded
schedule_df["Home team Shot on target"] = home_team_shots
schedule_df["Home team Red Cards"] = home_team_red_cards

schedule_df["Away team Points"] = away_team_points
schedule_df["Away team Goal scored"] = away_team_goals_scored
schedule_df["Away team Goal conceded"] = away_team_goals_conceded
schedule_df["Away team Shot on target"] = away_team_shots
schedule_df["Away team Red Cards"] = away_team_red_cards

# Select and reorder columns to match the desired output format
final_df = schedule_df[
    [
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
    ]
]

# Save the result to a new CSV file
final_df.to_csv("combined_schedule_stats.csv", index=False)

# Display the first few rows of the result
print(final_df.head())
