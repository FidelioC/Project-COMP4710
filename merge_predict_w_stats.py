import pandas as pd

# Load the first file (match schedule) into a DataFrame
schedule_df = pd.read_csv("schedule.csv")

# Load the second file (team statistics) into a DataFrame
stats_df = pd.read_csv("team_stats.csv")

# Rename columns in the stats DataFrame for easier merging
stats_df = stats_df.rename(
    columns={
        "Team": "Team",
        "Points": "Points",
        "Total Goals Scored": "Goal Scored",
        "Total Goals Conceded": "Goal Conceded",
        "Total Red Cards": "Red Cards",
        "Total Shots": "Shots",
    }
)

# Merge the stats with the home team details
schedule_df = schedule_df.merge(
    stats_df.add_prefix("Home team "),
    left_on="HomeTeam",
    right_on="Home team Team",
    how="left",
)

# Merge the stats with the away team details
schedule_df = schedule_df.merge(
    stats_df.add_prefix("Away team "),
    left_on="AwayTeam",
    right_on="Away team Team",
    how="left",
)

# Select and rename columns to match the desired output format
final_df = schedule_df[
    [
        "Date",
        "HomeTeam",
        "AwayTeam",
        "Home team Points",
        "Home team Goal Scored",
        "Home team Goal Conceded",
        "Home team Shots",
        "Home team Red Cards",
        "Away team Points",
        "Away team Goal Scored",
        "Away team Goal Conceded",
        "Away team Shots",
        "Away team Red Cards",
    ]
]

# Rename columns for consistency
final_df = final_df.rename(
    columns={
        "Date": "Date",
        "HomeTeam": "Home team",
        "AwayTeam": "Away team",
        "Home team Points": "Home team Points",
        "Home team Goal Scored": "Home team Goal scored",
        "Home team Goal Conceded": "Home team Goal conceded",
        "Home team Shots": "Home team Shot on target",
        "Home team Red Cards": "Home team Red Cards",
        "Away team Points": "Away team Points",
        "Away team Goal Scored": "Away team Goal scored",
        "Away team Goal Conceded": "Away team Goal conceded",
        "Away team Shots": "Away team Shot on target",
        "Away team Red Cards": "Away team Red Cards",
    }
)

# Save the result to a new CSV file
final_df.to_csv("combined_schedule_stats.csv", index=False)

# Display the first few rows of the result
print(final_df.head())
