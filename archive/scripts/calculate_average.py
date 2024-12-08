import pandas as pd

input_file = "./prediction_test/team_stats.csv"
output_file = "./prediction_test/team_stats_avg.csv"

# Load your dataset
data = pd.read_csv(input_file)

# Columns related to last 20 games
home_team_last_20 = [
    "HomeTeamPointLast20",
    "HomeTeamGoalScoredLast20",
    "HomeTeamGoalConcededLast20",
    "HomeTeamShotTargetLast20",
    "HomeTeamRedLast20",
]

away_team_last_20 = [
    "AwayTeamPointLast20",
    "AwayTeamGoalScoredLast20",
    "AwayTeamGoalConcededLast20",
    "AwayTeamShotTargetLast20",
    "AwayTeamRedLast20",
]

# Columns related to H2H (Head to Head) data for the last 10 games
home_team_h2h_last_10 = [
    "HomeTeamPointH2HLast10",
    "HomeTeamGoalScoredH2HLast10",
    "HomeTeamGoalConcededH2HLast10",
    "HomeTeamShotTargetH2HLast10",
    "HomeTeamRedH2HLast10",
]

away_team_h2h_last_10 = [
    "AwayTeamPointH2HLast10",
    "AwayTeamGoalScoredH2HLast10",
    "AwayTeamGoalConcededH2HLast10",
    "AwayTeamShotTargetH2HLast10",
    "AwayTeamRedH2HLast10",
]

# Calculate the averages for the columns related to the last 20 games
for column in home_team_last_20 + away_team_last_20:
    data[column + "Avg"] = data[column] / 20

# Calculate the averages for the columns related to the H2H last 10 games
for column in home_team_h2h_last_10 + away_team_h2h_last_10:
    data[column + "Avg"] = data[column] / 10

# Save the updated dataset to the same CSV file, overwriting the original
data.to_csv(output_file, index=False)
