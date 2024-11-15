import pandas as pd
from collections import defaultdict
from dateutil import parser
import click

# input_file = "./prediction_test/combined_file.csv"  # "./training_data/combined_file.csv" "./prediction_test/combined_file.csv"
# output_file = "./prediction_test/team_stats_noh2h.csv"  # "./training_data/team_stats.csv" "./prediction_test/team_stats.csv"
# date_end = "22/05/2022"  # date/month/year "24/05/15" "22/05/2022"
# start_date = "2022-08-05"  # year - month - date "2015-08-08" "2022-08-05"


# ======= Team Stats Codes =========== #
def get_stats_last_20(df_write, start_index, team_name, num_game_stats):
    total_count = 0
    index = start_index - 1
    total_team_points = 0
    total_team_goal_scored = 0
    total_team_goal_conceded = 0
    total_team_shot_target = 0
    total_team_red = 0

    while total_count < int(num_game_stats) and index > 0:
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


def get_row_last_20(df_write, start_index, num_game_stats):
    """get row last X games stats"""
    team_home = df_write.loc[start_index]["HomeTeam"]
    team_away = df_write.loc[start_index]["AwayTeam"]

    # ===== updating the home team =======
    (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    ) = get_stats_last_20(df_write, start_index, team_home, num_game_stats)

    update_home_columns(
        df_write,
        start_index,
        total_team_points,
        total_team_shot_target,
        total_team_red,
        total_team_goal_scored,
        total_team_goal_conceded,
        num_game_stats,
    )

    # ===== updating the away team =======
    (
        total_team_points,
        total_team_goal_scored,
        total_team_goal_conceded,
        total_team_shot_target,
        total_team_red,
    ) = get_stats_last_20(df_write, start_index, team_away, num_game_stats)

    update_away_columns(
        df_write,
        start_index,
        total_team_points,
        total_team_shot_target,
        total_team_red,
        total_team_goal_scored,
        total_team_goal_conceded,
        num_game_stats,
    )


def update_home_columns(
    df_write,
    index,
    total_team_points,
    total_team_shot_target,
    total_team_red,
    total_team_goal_scored,
    total_team_goal_conceded,
    num_game_stats,
):
    """updating home stat columns"""
    df_write.at[index, f"HomeTeamPointLast{num_game_stats}"] = total_team_points
    df_write.at[index, f"HomeTeamShotTargetLast{num_game_stats}"] = (
        total_team_shot_target
    )
    df_write.at[index, f"HomeTeamRedLast{num_game_stats}"] = total_team_red
    df_write.at[index, f"HomeTeamGoalScoredLast{num_game_stats}"] = (
        total_team_goal_scored
    )
    df_write.at[index, f"HomeTeamGoalConcededLast{num_game_stats}"] = (
        total_team_goal_conceded
    )


def update_away_columns(
    df_write,
    index,
    total_team_points,
    total_team_shot_target,
    total_team_red,
    total_team_goal_scored,
    total_team_goal_conceded,
    num_game_stats,
):
    """updating away stat columns"""
    df_write.at[index, f"AwayTeamPointLast{num_game_stats}"] = total_team_points
    df_write.at[index, f"AwayTeamShotTargetLast{num_game_stats}"] = (
        total_team_shot_target
    )
    df_write.at[index, f"AwayTeamRedLast{num_game_stats}"] = total_team_red
    df_write.at[index, f"AwayTeamGoalScoredLast{num_game_stats}"] = (
        total_team_goal_scored
    )
    df_write.at[index, f"AwayTeamGoalConcededLast{num_game_stats}"] = (
        total_team_goal_conceded
    )


def update_all_stats_last20(df_write, date_end, num_game_stats):
    for index, _ in df_write[::-1].iterrows():
        print(df_write.loc[index]["Date"])
        if df_write.loc[index]["Date"] == date_end:
            return
        # print(index)
        get_row_last_20(df_write, index, num_game_stats)


# ======= H2H Codes =========== #
def get_h2h_stats_last_10(df_write, start_index, team_name1, team_name2, num_game_h2h):
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

    while total_count < int(num_game_h2h) and index > 0:
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


def get_h2h_last_10(df_write, start_index, num_game_h2h):
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
    ) = get_h2h_stats_last_10(df_write, start_index, team1, team2, num_game_h2h)

    update_h2h_home_columns(
        df_write,
        start_index,
        total_team1_points,
        total_team1_goal_scored,
        total_team1_goal_conceded,
        total_team1_shot_target,
        total_team1_red,
        num_game_h2h,
    )

    update_h2h_away_columns(
        df_write,
        start_index,
        total_team2_points,
        total_team2_goal_scored,
        total_team2_goal_conceded,
        total_team2_shot_target,
        total_team2_red,
        num_game_h2h,
    )


def update_h2h_home_columns(
    df_write,
    index,
    total_team1_points,
    total_team1_goal_scored,
    total_team1_goal_conceded,
    total_team1_shot_target,
    total_team1_red,
    num_game_h2h,
):
    df_write.at[index, f"HomeTeamPointH2HLast{num_game_h2h}"] = total_team1_points
    df_write.at[index, f"HomeTeamGoalScoredH2HLast{num_game_h2h}"] = (
        total_team1_goal_scored
    )
    df_write.at[index, f"HomeTeamGoalConcededH2HLast{num_game_h2h}"] = (
        total_team1_goal_conceded
    )
    df_write.at[index, f"HomeTeamShotTargetH2HLast{num_game_h2h}"] = (
        total_team1_shot_target
    )
    df_write.at[index, f"HomeTeamRedH2HLast{num_game_h2h}"] = total_team1_red


def update_h2h_away_columns(
    df_write,
    index,
    total_team2_points,
    total_team2_goal_scored,
    total_team2_goal_conceded,
    total_team2_shot_target,
    total_team2_red,
    num_game_h2h,
):
    df_write.at[index, f"AwayTeamPointH2HLast{num_game_h2h}"] = total_team2_points
    df_write.at[index, f"AwayTeamGoalScoredH2HLast{num_game_h2h}"] = (
        total_team2_goal_scored
    )
    df_write.at[index, f"AwayTeamGoalConcededH2HLast{num_game_h2h}"] = (
        total_team2_goal_conceded
    )
    df_write.at[index, f"AwayTeamShotTargetH2HLast{num_game_h2h}"] = (
        total_team2_shot_target
    )
    df_write.at[index, f"AwayTeamRedH2HLast{num_game_h2h}"] = total_team2_red


def update_h2h_stats_last10(df_write, date_end, num_game_h2h):
    for index, _ in df_write[::-1].iterrows():
        if df_write.loc[index]["Date"] == date_end:
            return
        get_h2h_last_10(df_write, index, num_game_h2h)


def parse_date(date_str):
    try:
        # Parse the date using dateutil.parser, which automatically handles multiple formats
        return parser.parse(date_str, dayfirst=True)
    except (ValueError, TypeError):
        # Return NaT (Not a Time) if the date parsing fails
        return pd.NaT


def h2h_new_columns(df_read, num_game_h2h):
    df_read[f"HomeTeamPointH2HLast{num_game_h2h}"] = 0
    df_read[f"HomeTeamGoalScoredH2HLast{num_game_h2h}"] = 0
    df_read[f"HomeTeamGoalConcededH2HLast{num_game_h2h}"] = 0
    df_read[f"HomeTeamShotTargetH2HLast{num_game_h2h}"] = 0
    df_read[f"HomeTeamRedH2HLast{num_game_h2h}"] = 0

    df_read[f"AwayTeamPointH2HLast{num_game_h2h}"] = 0
    df_read[f"AwayTeamGoalScoredH2HLast{num_game_h2h}"] = 0
    df_read[f"AwayTeamGoalConcededH2HLast{num_game_h2h}"] = 0
    df_read[f"AwayTeamShotTargetH2HLast{num_game_h2h}"] = 0
    df_read[f"AwayTeamRedH2HLast{num_game_h2h}"] = 0


def stats_new_columns(df_read, num_game_stats):
    df_read[f"HomeTeamPointLast{num_game_stats}"] = 0
    df_read[f"HomeTeamGoalScoredLast{num_game_stats}"] = 0
    df_read[f"HomeTeamGoalConcededLast{num_game_stats}"] = 0
    df_read[f"HomeTeamShotTargetLast{num_game_stats}"] = 0
    df_read[f"HomeTeamRedLast{num_game_stats}"] = 0

    df_read[f"AwayTeamPointLast{num_game_stats}"] = 0
    df_read[f"AwayTeamGoalScoredLast{num_game_stats}"] = 0
    df_read[f"AwayTeamGoalConcededLast{num_game_stats}"] = 0
    df_read[f"AwayTeamShotTargetLast{num_game_stats}"] = 0
    df_read[f"AwayTeamRedLast{num_game_stats}"] = 0


def main(input_file, output_file, num_game_stats, num_game_h2h, date_end, start_date):
    # ======== add new columns ========== "
    df_read = pd.read_csv(input_file)

    stats_new_columns(df_read, num_game_stats)
    h2h_new_columns(df_read, num_game_h2h)

    df_read.to_csv(output_file, index=False)

    df_write = pd.read_csv(output_file)

    update_all_stats_last20(df_write, date_end, num_game_stats)
    update_h2h_stats_last10(df_write, date_end, num_game_h2h)

    df_write["Date"] = df_write["Date"].apply(parse_date)

    # Filter rows with dates from 08/08/15 to the end
    start_date = pd.to_datetime(start_date)
    df_filtered = df_write[df_write["Date"] >= start_date].copy()

    df_filtered.to_csv(output_file, index=False)


@click.command()
@click.option("--inputfile", required=True)
@click.option("--outputfile", required=True)
@click.option("--num_game_stats", required=True)
@click.option("--num_game_h2h", required=True)
@click.option("--date_end", required=True)
@click.option("--start_date", required=True)
def commands_processing(
    inputfile, outputfile, num_game_stats, num_game_h2h, date_end, start_date
):
    main(inputfile, outputfile, num_game_stats, num_game_h2h, date_end, start_date)


if __name__ == "__main__":
    commands_processing()
