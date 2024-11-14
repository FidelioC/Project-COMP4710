import pandas as pd
from collections import defaultdict
from dateutil import parser

input_file = "./training_data/combined_file.csv"
output_file = "./training_data/team_stats.csv"
date_end = "24/05/2015"  # date/month/year "24/05/2015" "13/08/2021"
start_date = "2015-08-08"  # year - month - date "2015-08-08" "2022-08-05"


def get_stats_last_10(df_write, start_index, team_name):
    total_count = 0
    index = start_index - 1
    total_team_points = 0
    total_team_goal_scored = 0
    total_team_goal_conceded = 0
    total_team_shot_target = 0
    total_team_red = 0

    while total_count < 20 and index > 0:
        row = df_write.loc[index]
        if row["HomeTeam"] == team_name:
            total_team_points += (
                3 if row["FTR"] == "H" else 1 if row["FTR"] == "D" else 0
            )
            total_team_shot_target += int(row["HST"])
            total_team_red += int(row["HR"])
            total_team_goal_scored += int(row["FTHG"])
            total_team_goal_conceded += int(row["FTAG"])
            total_count += 1
        elif row["AwayTeam"] == team_name:
            total_team_points += (
                3 if row["FTR"] == "A" else 1 if row["FTR"] == "D" else 0
            )
            total_team_shot_target += int(row["AST"])
            total_team_red += int(row["AR"])
            total_team_goal_scored += int(row["FTAG"])
            total_team_goal_conceded += int(row["FTHG"])
            total_count += 1

        index -= 1
    return (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    )


def get_row_last_10(df_write, start_index):
    """get row last 10 games stats"""
    team_home = df_write.loc[start_index]["HomeTeam"]
    team_away = df_write.loc[start_index]["AwayTeam"]

    # ===== updating the home team =======
    (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    ) = get_stats_last_10(df_write, start_index, team_home)

    update_home_columns(
        df_write,
        start_index,
        total_team_points,
        total_team_shot_target,
        total_team_red,
        total_team_goal_scored,
        total_team_goal_conceded,
    )

    # ===== updating the away team =======
    (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    ) = get_stats_last_10(df_write, start_index, team_away)

    update_away_columns(
        df_write,
        start_index,
        total_team_points,
        total_team_shot_target,
        total_team_red,
        total_team_goal_scored,
        total_team_goal_conceded,
    )


def update_home_columns(
    df_write,
    index,
    total_team_points,
    total_team_shot_target,
    total_team_red,
    total_team_goal_scored,
    total_team_goal_conceded,
):
    """updating home stat columns"""
    df_write.at[index, "HomeTeamPointLast10"] = total_team_points
    df_write.at[index, "HomeTeamShotTargetLast10"] = total_team_shot_target
    df_write.at[index, "HomeTeamRedLast10"] = total_team_red
    df_write.at[index, "HomeTeamGoalScoredLast10"] = total_team_goal_scored
    df_write.at[index, "HomeTeamGoalConcededLast10"] = total_team_goal_conceded


def update_away_columns(
    df_write,
    index,
    total_team_points,
    total_team_shot_target,
    total_team_red,
    total_team_goal_scored,
    total_team_goal_conceded,
):
    """updating away stat columns"""
    df_write.at[index, "AwayTeamPointLast10"] = total_team_points
    df_write.at[index, "AwayTeamShotTargetLast10"] = total_team_shot_target
    df_write.at[index, "AwayTeamRedLast10"] = total_team_red
    df_write.at[index, "AwayTeamGoalScoredLast10"] = total_team_goal_scored
    df_write.at[index, "AwayTeamGoalConcededLast10"] = total_team_goal_conceded


def update_all_stats_last10(df_write, date_end):
    for index, _ in df_write[::-1].iterrows():
        if df_write.loc[index]["Date"] == date_end:
            return
        # print(index)
        get_row_last_10(df_write, index)


def parse_date(date_str):
    try:
        # Parse the date using dateutil.parser, which automatically handles multiple formats
        return parser.parse(date_str, dayfirst=True)
    except (ValueError, TypeError):
        # Return NaT (Not a Time) if the date parsing fails
        return pd.NaT


def main(start_date):
    # ======== add new columns ========== "
    df_read = pd.read_csv(input_file)

    df_read["HomeTeamPointLast10"] = 0
    df_read["HomeTeamGoalScoredLast10"] = 0
    df_read["HomeTeamGoalConcededLast10"] = 0
    df_read["HomeTeamShotTargetLast10"] = 0
    df_read["HomeTeamRedLast10"] = 0

    df_read["AwayTeamPointLast10"] = 0
    df_read["AwayTeamGoalScoredLast10"] = 0
    df_read["AwayTeamGoalConcededLast10"] = 0
    df_read["AwayTeamShotTargetLast10"] = 0
    df_read["AwayTeamRedLast10"] = 0

    df_read.to_csv(output_file, index=False)

    df_write = pd.read_csv(output_file)

    update_all_stats_last10(df_write, date_end)

    df_write["Date"] = df_write["Date"].apply(parse_date)

    # Filter rows with dates from 08/08/15 to the end
    start_date = pd.to_datetime(start_date)
    df_filtered = df_write[df_write["Date"] >= start_date].copy()

    df_filtered.to_csv(output_file, index=False)


if __name__ == "__main__":
    main(start_date)
