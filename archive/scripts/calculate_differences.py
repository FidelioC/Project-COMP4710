import pandas as pd

# Load the dataset
file_name = "./prediction_test/team_stats_stats20_h2h10.csv"
df = pd.read_csv(file_name)

# Calculate differences for aggregated stats
df["Point_Difference"] = df["HomeTeamPointLast20"] - df["AwayTeamPointLast20"]
df["Goal_Scored_Difference"] = (
    df["HomeTeamGoalScoredLast20"] - df["AwayTeamGoalScoredLast20"]
)
df["Goal_Conceded_Difference"] = (
    df["AwayTeamGoalConcededLast20"] - df["HomeTeamGoalConcededLast20"]
)
df["Shot_Target_Difference"] = (
    df["HomeTeamShotTargetLast20"] - df["AwayTeamShotTargetLast20"]
)
df["Red_Card_Difference"] = df["AwayTeamRedLast20"] - df["HomeTeamRedLast20"]

# Calculate differences for H2H stats
df["H2H_Point_Difference"] = df["HomeTeamPointH2HLast10"] - df["AwayTeamPointH2HLast10"]
df["H2H_Goal_Scored_Difference"] = (
    df["HomeTeamGoalScoredH2HLast10"] - df["AwayTeamGoalScoredH2HLast10"]
)
df["H2H_Goal_Conceded_Difference"] = (
    df["AwayTeamGoalConcededH2HLast10"] - df["HomeTeamGoalConcededH2HLast10"]
)
df["H2H_Shot_Target_Difference"] = (
    df["HomeTeamShotTargetH2HLast10"] - df["AwayTeamShotTargetH2HLast10"]
)
df["H2H_Red_Card_Difference"] = df["AwayTeamRedH2HLast10"] - df["HomeTeamRedH2HLast10"]

# Save the result to a new file
output_file = "./prediction_test/team_stats_stats20_h2h10_differences.csv"
df.to_csv(output_file, index=False)

print(f"Differences calculated and saved to {output_file}")
