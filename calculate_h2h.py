# ======= H2H Codes =========== #
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
