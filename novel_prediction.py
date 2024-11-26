import pandas as pd

df = pd.read_csv("./prediction_test/team_stats_stats20_h2h10.csv")

max_shot_target = max(
    df["HomeTeamShotTargetLast20"].max(), df["AwayTeamShotTargetLast20"].max()
)

max_H2H_pct = max(df["HomeTeamWin%H2HLast10"].max(), df["AwayTeamWin%H2HLast10"].max())

max_rating = max(df["HomeTeamRatingLast20"].max(), df["AwayTeamRatingLast20"].max())

# print(max_shot_target, max_H2H_pct, max_rating)
ftr_predictions = []  # Temporary list to store predictions

for index, row in df.iterrows():
    HomeShotsTarget = row["HomeTeamShotTargetLast20"] / max_shot_target
    AwayShotsTarget = row["AwayTeamShotTargetLast20"] / max_shot_target
    HomeTeamH2HPct = row["HomeTeamWin%H2HLast10"] / max_H2H_pct
    AwayTeamH2HPct = row["AwayTeamWin%H2HLast10"] / max_H2H_pct
    HomeTeamRating = row["HomeTeamRatingLast20"] / max_rating
    AwayTeamRating = row["AwayTeamRatingLast20"] / max_rating

    total_home_value = HomeShotsTarget + HomeTeamH2HPct + HomeTeamRating

    total_away_value = AwayShotsTarget + AwayTeamH2HPct + AwayTeamRating

    print(
        f"Hometeam: {row["HomeTeam"]}, AwayTeam: {row["AwayTeam"]}, totalHomeValue: {total_home_value}, totalAwayValue: {total_away_value}"
    )
    # Determine prediction and store it in the list
    if total_home_value > total_away_value:
        ftr_predictions.append("H")
    elif total_home_value < total_away_value:
        ftr_predictions.append("A")

df["FTR_Prediction"] = ftr_predictions

df.to_csv("./results/novel_alg_stats20_h2h10.csv", index=False)
