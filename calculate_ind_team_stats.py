import pandas as pd
from collections import defaultdict

# Load the CSV data
df = pd.read_csv(
    "combined_file.csv",
    usecols=["HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HR", "AR", "HST", "AST"],
)

# Initialize dictionaries to store points, goals scored, goals conceded, red cards, and shots for each team
team_points = defaultdict(int)
team_goals_scored = defaultdict(int)
team_goals_conceded = defaultdict(int)
team_red_cards = defaultdict(int)
team_shots = defaultdict(int)

# Iterate over each row to calculate points, goals, red cards, and shots
for _, row in df.iterrows():
    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]
    home_goals = row["FTHG"]
    away_goals = row["FTAG"]
    home_red_cards = row["HR"]
    away_red_cards = row["AR"]
    home_shots = row["HST"]
    away_shots = row["AST"]
    result = row["FTR"]

    # Points calculation
    if result == "H":  # Home team wins
        team_points[home_team] += 3
    elif result == "A":  # Away team wins
        team_points[away_team] += 3
    elif result == "D":  # Draw
        team_points[home_team] += 1
        team_points[away_team] += 1

    # Goals scored and conceded calculation
    team_goals_scored[home_team] += home_goals
    team_goals_scored[away_team] += away_goals
    team_goals_conceded[home_team] += away_goals
    team_goals_conceded[away_team] += home_goals

    # Red cards calculation
    team_red_cards[home_team] += home_red_cards
    team_red_cards[away_team] += away_red_cards

    # Shots calculation
    team_shots[home_team] += home_shots
    team_shots[away_team] += away_shots

# Combine all data into a single DataFrame
result_df = pd.DataFrame(
    {
        "Team": team_points.keys(),
        "Points": team_points.values(),
        "Total Goals Scored": [team_goals_scored[team] for team in team_points.keys()],
        "Total Goals Conceded": [
            team_goals_conceded[team] for team in team_points.keys()
        ],
        "Total Red Cards": [team_red_cards[team] for team in team_points.keys()],
        "Total Shots": [team_shots[team] for team in team_points.keys()],
    }
)

# Save to CSV
result_df.to_csv("team_stats.csv", index=False)

# Display the first few rows of the result
print(result_df.head())
