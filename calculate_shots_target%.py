import pandas as pd
from collections import defaultdict

# Load CSV into pandas DataFrame
df = pd.read_csv("./training_data/team_stats_stats20_h2h10.csv")


def is_home_bigger(df):
    return df["HomeTeamShotTargetLast20"] > df["AwayTeamShotTargetLast20"]


def is_away_bigger(df):
    return df["HomeTeamShotTargetLast20"] < df["AwayTeamShotTargetLast20"]


def calculate_shots_target_all_pct(df):
    total_shots_bigger_win = 0
    total_match_better_shots = 0
    for index, row in df.iterrows():
        if (is_home_bigger(row) and row["FTR"] == "H") or (
            is_away_bigger(row) and row["FTR"] == "A"
        ):
            # bigger shots on target and win
            total_shots_bigger_win += 1
            total_match_better_shots += 1
        elif (is_home_bigger(row) and (row["FTR"] == "A" or row["FTR"] == "D")) or (
            is_away_bigger(row) and (row["FTR"] == "H" or row["FTR"] == "D")
        ):  # bigger shots on target but lose or draw
            total_match_better_shots += 1

    # print(total_shots_bigger_win, total_match_better_shots)
    return (total_shots_bigger_win / total_match_better_shots) * 100


def all_team_shots_target_win_pct(df):
    # [0] = shots target bigger and win
    # [1] = total shots target bigger (doesn't matter if winning or losing)
    shots_target_dict = defaultdict(lambda: [0, 0])
    for index, row in df.iterrows():
        if is_home_bigger(row):
            if row["FTR"] == "H":
                shots_target_dict[row["HomeTeam"]][0] += 1
            shots_target_dict[row["HomeTeam"]][1] += 1
        elif is_away_bigger(row):
            if row["FTR"] == "A":
                shots_target_dict[row["AwayTeam"]][0] += 1
            shots_target_dict[row["AwayTeam"]][1] += 1

    return shots_target_dict


def print_all_pct(dict):
    for item, key in dict.items():
        print(f"Team: {item}, Win%ShotsTargetBetter: {(key[0]/key[1]) * 100}")


def main():
    print(f"All Shots Target Percentage: {calculate_shots_target_all_pct(df)}")

    dict = all_team_shots_target_win_pct(df)
    # print(dict)
    print(print_all_pct(dict))


if __name__ == "__main__":
    main()
