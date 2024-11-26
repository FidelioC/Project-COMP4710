import pandas as pd
from collections import defaultdict

# Load CSV into pandas DataFrame
df = pd.read_csv("./training_data/team_stats_stats20_h2h10.csv")


def is_home_bigger(df, HomeColumnName, AwayColumnName):
    return df[HomeColumnName] > df[AwayColumnName]


def is_away_bigger(df, HomeColumnName, AwayColumnName):
    return df[HomeColumnName] < df[AwayColumnName]


def calculate_all_pct(df, HomeColumnName, AwayColumnName):
    better_win = 0
    total_match_better = 0
    for index, row in df.iterrows():
        if (
            is_home_bigger(row, HomeColumnName, AwayColumnName) and row["FTR"] == "H"
        ) or (
            is_away_bigger(row, HomeColumnName, AwayColumnName) and row["FTR"] == "A"
        ):
            # bigger shots on target and win
            better_win += 1
            total_match_better += 1
        elif (
            is_home_bigger(row, HomeColumnName, AwayColumnName) and (row["FTR"] == "A")
        ) or (
            is_away_bigger(row, HomeColumnName, AwayColumnName) and (row["FTR"] == "H")
        ):  # bigger shots on target but lose or draw
            total_match_better += 1

    # print(better_win, total_match_better)
    return (better_win / total_match_better) * 100


def all_team_shots_target_win_pct(df, HomeColumnName, AwayColumnName):
    # [0] = shots target bigger and win
    # [1] = total shots target bigger (doesn't matter if winning or losing)
    target_dict = defaultdict(lambda: [0, 0])
    for index, row in df.iterrows():
        if is_home_bigger(row, HomeColumnName, AwayColumnName):
            if row["FTR"] == "H":
                target_dict[row["HomeTeam"]][0] += 1
            target_dict[row["HomeTeam"]][1] += 1
        elif is_away_bigger(row, HomeColumnName, AwayColumnName):
            if row["FTR"] == "A":
                target_dict[row["AwayTeam"]][0] += 1
            target_dict[row["AwayTeam"]][1] += 1

    return target_dict


def calculate_pct(df, HomeColumnName, AwayColumnName, feature):
    # for all teams
    result = calculate_all_pct(df, HomeColumnName, AwayColumnName)
    print(f"All {feature} Percentage: {result}")

    # for each team
    # dict = all_team_shots_target_win_pct(df, HomeColumnName, AwayColumnName)
    # print_all_pct(dict, feature)

    print("\n")


def print_all_pct(dict, feature):
    for item, key in dict.items():
        print(f"Team: {item}, Win%{feature}Better: {(key[0]/key[1]) * 100}")


def main():
    # ==== NORMAL STATS LAST 20 ======= #
    # PointLast20
    calculate_pct(df, "HomeTeamPointLast20", "AwayTeamPointLast20", "Point")

    # GoalScoredLast20
    calculate_pct(
        df, "HomeTeamGoalScoredLast20", "AwayTeamGoalScoredLast20", "GoalScored"
    )

    # GoalConcededLast20
    calculate_pct(
        df, "HomeTeamGoalConcededLast20", "AwayTeamGoalConcededLast20", "GoalConceded"
    )

    # ShotsOnTargetLast20
    calculate_pct(
        df, "HomeTeamShotTargetLast20", "AwayTeamShotTargetLast20", "ShotsTarget"
    )

    # RedCardLast20
    calculate_pct(df, "HomeTeamRedLast20", "AwayTeamRedLast20", "Red")

    # ==== H2H STATS LAST 10 ======= #
    # PointH2HLast10
    calculate_pct(
        df, "HomeTeamPointH2HLast10", "AwayTeamPointH2HLast10", "PointH2HLast10"
    )

    # GoalScoredH2HLast10
    calculate_pct(
        df,
        "HomeTeamGoalScoredH2HLast10",
        "AwayTeamGoalScoredH2HLast10",
        "GoalScoredH2HLast10",
    )

    # GoalConcededH2HLast10
    calculate_pct(
        df,
        "HomeTeamGoalConcededH2HLast10",
        "AwayTeamGoalConcededH2HLast10",
        "GoalConcededH2HLast10",
    )

    # ShotTargetH2HLast10
    calculate_pct(
        df,
        "HomeTeamShotTargetH2HLast10",
        "AwayTeamShotTargetH2HLast10",
        "ShotTargetH2HLast10",
    )

    # RedH2HLast10
    calculate_pct(
        df,
        "HomeTeamRedH2HLast10",
        "AwayTeamRedH2HLast10",
        "RedH2HLast10",
    )

    # Win%H2HLast10
    calculate_pct(df, "HomeTeamWin%H2HLast10", "AwayTeamWin%H2HLast10", "Win%H2HLast10")


if __name__ == "__main__":
    main()
