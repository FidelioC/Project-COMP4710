# ======= Team Stats Codes =========== #
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
