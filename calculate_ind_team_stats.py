import pandas as pd
from collections import defaultdict
from dateutil import parser

input_file = "./prediction_test/combined_file.csv"  # "./training_data/combined_file.csv" "./prediction_test/combined_file.csv"
output_file = "./prediction_test/team_stats_noh2h.csv"  # "./training_data/team_stats.csv" "./prediction_test/team_stats.csv"
date_end = "22/05/2022"  # date/month/year "24/05/15" "22/05/2022"
start_date = "2022-08-05"  # year - month - date "2015-08-08" "2022-08-05"


# ======= Team Stats Codes =========== #
def get_stats_last_20(df_write, start_index, team_name):
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


def get_row_last_20(df_write, start_index):
    """get row last 20 games stats"""
    team_home = df_write.loc[start_index]["HomeTeam"]
    team_away = df_write.loc[start_index]["AwayTeam"]

    # ===== updating the home team =======
    (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    ) = get_stats_last_20(df_write, start_index, team_home)

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
    ) = get_stats_last_20(df_write, start_index, team_away)

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
    df_write.at[index, "HomeTeamPointLast20"] = total_team_points
    df_write.at[index, "HomeTeamShotTargetLast20"] = total_team_shot_target
    df_write.at[index, "HomeTeamRedLast20"] = total_team_red
    df_write.at[index, "HomeTeamGoalScoredLast20"] = total_team_goal_scored
    df_write.at[index, "HomeTeamGoalConcededLast20"] = total_team_goal_conceded


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
    df_write.at[index, "AwayTeamPointLast20"] = total_team_points
    df_write.at[index, "AwayTeamShotTargetLast20"] = total_team_shot_target
    df_write.at[index, "AwayTeamRedLast20"] = total_team_red
    df_write.at[index, "AwayTeamGoalScoredLast20"] = total_team_goal_scored
    df_write.at[index, "AwayTeamGoalConcededLast20"] = total_team_goal_conceded


def update_all_stats_last20(df_write, date_end):
    for index, _ in df_write[::-1].iterrows():
        print(df_write.loc[index]["Date"])
        if df_write.loc[index]["Date"] == date_end:
            return
        # print(index)
        get_row_last_20(df_write, index)


# ======= H2H Codes =========== #
def get_h2h_stats_last_10(df_write, start_index, team_name1, team_name2):
    """
    get h2h of two teams for the last 10 games.
    The reason why we're using the last 10 games is because there might be not enough
    past data if we use 20 games.
    """
    total_count = 0
    index = start_index - 1

    total_team1_points = 0
    total_team1_goal_scored = 0
    total_team1_goal_conceded = 0
    total_team1_shot_target = 0
    total_team1_red = 0

    total_team2_points = 0
    total_team2_goal_scored = 0
    total_team2_goal_conceded = 0
    total_team2_shot_target = 0
    total_team2_red = 0

    row = df_write.loc[index]
    print(f"{df_write.loc[index]["Date"]}, team1: {team_name1}, team2: {team_name2}")

    while total_count < 10 and index > 0:
        row = df_write.loc[index]
        if row["HomeTeam"] == team_name1 and row["AwayTeam"] == team_name2:
            total_count += 1
            # print(f"{row["Date"]}, Home: {row["HomeTeam"]}, Away: {row["AwayTeam"]}")

            # if team 1 is the home team
            total_team1_points += (
                3 if row["FTR"] == "H" else 1 if row["FTR"] == "D" else 0
            )
            total_team1_shot_target += int(row["HST"])
            total_team1_red += int(row["HR"])
            total_team1_goal_scored += int(row["FTHG"])
            total_team1_goal_conceded += int(row["FTAG"])

            # and team 2 is the away team
            total_team2_points += (
                3 if row["FTR"] == "A" else 1 if row["FTR"] == "D" else 0
            )
            total_team2_shot_target += int(row["AST"])
            total_team2_red += int(row["AR"])
            total_team2_goal_scored += int(row["FTAG"])
            total_team2_goal_conceded += int(row["FTHG"])

        elif row["HomeTeam"] == team_name2 and row["AwayTeam"] == team_name1:
            total_count += 1
            # print(f"{row["Date"]}, Home: {row["HomeTeam"]}, Away: {row["AwayTeam"]}")

            # if team 2 is the home team
            total_team2_points += (
                3 if row["FTR"] == "H" else 1 if row["FTR"] == "D" else 0
            )
            total_team2_shot_target += int(row["HST"])
            total_team2_red += int(row["HR"])
            total_team2_goal_scored += int(row["FTHG"])
            total_team2_goal_conceded += int(row["FTAG"])

            # and team 1 is the home team
            total_team1_points += (
                3 if row["FTR"] == "A" else 1 if row["FTR"] == "D" else 0
            )
            total_team1_shot_target += int(row["AST"])
            total_team1_red += int(row["AR"])
            total_team1_goal_scored += int(row["FTAG"])
            total_team1_goal_conceded += int(row["FTHG"])

        index -= 1

    return (
        total_team1_points,
        total_team1_goal_scored,
        total_team1_goal_conceded,
        total_team1_shot_target,
        total_team1_red,
        total_team2_points,
        total_team2_goal_scored,
        total_team2_goal_conceded,
        total_team2_shot_target,
        total_team2_red,
    )


def get_h2h_last_10(df_write, start_index):
    team1 = df_write.loc[start_index]["HomeTeam"]
    team2 = df_write.loc[start_index]["AwayTeam"]
    (
        total_team1_points,
        total_team1_goal_scored,
        total_team1_goal_conceded,
        total_team1_shot_target,
        total_team1_red,
        total_team2_points,
        total_team2_goal_scored,
        total_team2_goal_conceded,
        total_team2_shot_target,
        total_team2_red,
    ) = get_h2h_stats_last_10(df_write, start_index, team1, team2)

    update_h2h_home_columns(
        df_write,
        start_index,
        total_team1_points,
        total_team1_goal_scored,
        total_team1_goal_conceded,
        total_team1_shot_target,
        total_team1_red,
    )

    update_h2h_away_columns(
        df_write,
        start_index,
        total_team2_points,
        total_team2_goal_scored,
        total_team2_goal_conceded,
        total_team2_shot_target,
        total_team2_red,
    )


def update_h2h_home_columns(
    df_write,
    index,
    total_team1_points,
    total_team1_goal_scored,
    total_team1_goal_conceded,
    total_team1_shot_target,
    total_team1_red,
):
    df_write.at[index, "HomeTeamPointH2HLast10"] = total_team1_points
    df_write.at[index, "HomeTeamGoalScoredH2HLast10"] = total_team1_goal_scored
    df_write.at[index, "HomeTeamGoalConcededH2HLast10"] = total_team1_goal_conceded
    df_write.at[index, "HomeTeamShotTargetH2HLast10"] = total_team1_shot_target
    df_write.at[index, "HomeTeamRedH2HLast10"] = total_team1_red


def update_h2h_away_columns(
    df_write,
    index,
    total_team2_points,
    total_team2_goal_scored,
    total_team2_goal_conceded,
    total_team2_shot_target,
    total_team2_red,
):
    df_write.at[index, "AwayTeamPointH2HLast10"] = total_team2_points
    df_write.at[index, "AwayTeamGoalScoredH2HLast10"] = total_team2_goal_scored
    df_write.at[index, "AwayTeamGoalConcededH2HLast10"] = total_team2_goal_conceded
    df_write.at[index, "AwayTeamShotTargetH2HLast10"] = total_team2_shot_target
    df_write.at[index, "AwayTeamRedH2HLast10"] = total_team2_red


def update_h2h_stats_last10(df_write, date_end):
    for index, _ in df_write[::-1].iterrows():
        if df_write.loc[index]["Date"] == date_end:
            return
        get_h2h_last_10(df_write, index)


def parse_date(date_str):
    try:
        # Parse the date using dateutil.parser, which automatically handles multiple formats
        return parser.parse(date_str, dayfirst=True)
    except (ValueError, TypeError):
        # Return NaT (Not a Time) if the date parsing fails
        return pd.NaT


def h2h_new_columns(df_read):
    df_read["HomeTeamPointH2HLast10"] = 0
    df_read["HomeTeamGoalScoredH2HLast10"] = 0
    df_read["HomeTeamGoalConcededH2HLast10"] = 0
    df_read["HomeTeamShotTargetH2HLast10"] = 0
    df_read["HomeTeamRedH2HLast10"] = 0

    df_read["AwayTeamPointH2HLast10"] = 0
    df_read["AwayTeamGoalScoredH2HLast10"] = 0
    df_read["AwayTeamGoalConcededH2HLast10"] = 0
    df_read["AwayTeamShotTargetH2HLast10"] = 0
    df_read["AwayTeamRedH2HLast10"] = 0


def stats_new_columns(df_read):
    df_read["HomeTeamPointLast20"] = 0
    df_read["HomeTeamGoalScoredLast20"] = 0
    df_read["HomeTeamGoalConcededLast20"] = 0
    df_read["HomeTeamShotTargetLast20"] = 0
    df_read["HomeTeamRedLast20"] = 0

    df_read["AwayTeamPointLast20"] = 0
    df_read["AwayTeamGoalScoredLast20"] = 0
    df_read["AwayTeamGoalConcededLast20"] = 0
    df_read["AwayTeamShotTargetLast20"] = 0
    df_read["AwayTeamRedLast20"] = 0


def main(start_date):
    # ======== add new columns ========== "
    df_read = pd.read_csv(input_file)

    stats_new_columns(df_read)
    # h2h_new_columns(df_read)

    df_read.to_csv(output_file, index=False)

    df_write = pd.read_csv(output_file)

    update_all_stats_last20(df_write, date_end)
    # update_h2h_stats_last10(df_write, date_end)

    df_write["Date"] = df_write["Date"].apply(parse_date)

    # Filter rows with dates from 08/08/15 to the end
    start_date = pd.to_datetime(start_date)
    df_filtered = df_write[df_write["Date"] >= start_date].copy()

    df_filtered.to_csv(output_file, index=False)


if __name__ == "__main__":
    main(start_date)
