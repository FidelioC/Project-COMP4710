# ======= Team Stats Codes =========== #
def weighted_new_columns(df_read, num_game_stats):
    df_read[f"HomeTeamPointWeightLast{num_game_stats}"] = 0
    df_read[f"HomeTeamGoalScoredWeightLast{num_game_stats}"] = 0
    df_read[f"HomeTeamGoalConcededWeightLast{num_game_stats}"] = 0
    df_read[f"HomeTeamShotTargetWeightLast{num_game_stats}"] = 0
    df_read[f"HomeTeamRedWeightLast{num_game_stats}"] = 0

    df_read[f"AwayTeamPointWeightLast{num_game_stats}"] = 0
    df_read[f"AwayTeamGoalScoredWeightLast{num_game_stats}"] = 0
    df_read[f"AwayTeamGoalConcededWeightLast{num_game_stats}"] = 0
    df_read[f"AwayTeamShotTargetWeightLast{num_game_stats}"] = 0
    df_read[f"AwayTeamRedWeightLast{num_game_stats}"] = 0


def get_weighted_last_20(
    df_write, start_index, team_name, num_game_stats, decay_constant=0.2
):
    total_count = 0
    index = start_index - 1
    total_team_points = 0
    total_team_goal_scored = 0
    total_team_goal_conceded = 0
    total_team_shot_target = 0
    total_team_red = 0
    weight = 0

    while total_count < int(num_game_stats) and index > 0:
        row = df_write.loc[index]
        weight = pow(decay_constant, (int(num_game_stats) - total_count))
        if row["HomeTeam"] == team_name:
            total_team_points += weight * (
                3 if row["FTR"] == "H" else 1 if row["FTR"] == "D" else 0
            )
            total_team_shot_target += weight * int(row["HST"])
            total_team_red += weight * int(row["HR"])
            total_team_goal_scored += weight * int(row["FTHG"])
            total_team_goal_conceded += weight * int(row["FTAG"])
            total_count += 1
        elif row["AwayTeam"] == team_name:
            total_team_points += weight * (
                3 if row["FTR"] == "A" else 1 if row["FTR"] == "D" else 0
            )
            total_team_shot_target += weight * int(row["AST"])
            total_team_red += weight * int(row["AR"])
            total_team_goal_scored += weight * int(row["FTAG"])
            total_team_goal_conceded += weight * int(row["FTHG"])
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
    ) = get_weighted_last_20(df_write, start_index, team_home, num_game_stats)

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
    ) = get_weighted_last_20(df_write, start_index, team_away, num_game_stats)

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
    df_write.at[index, f"HomeTeamPointWeightLast{num_game_stats}"] = total_team_points
    df_write.at[index, f"HomeTeamShotTargetWeightLast{num_game_stats}"] = (
        total_team_shot_target
    )
    df_write.at[index, f"HomeTeamRedWeightLast{num_game_stats}"] = total_team_red
    df_write.at[index, f"HomeTeamGoalScoredWeightLast{num_game_stats}"] = (
        total_team_goal_scored
    )
    df_write.at[index, f"HomeTeamGoalConcededWeightLast{num_game_stats}"] = (
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
    df_write.at[index, f"AwayTeamPointWeightLast{num_game_stats}"] = total_team_points
    df_write.at[index, f"AwayTeamShotTargetWeightLast{num_game_stats}"] = (
        total_team_shot_target
    )
    df_write.at[index, f"AwayTeamRedWeightLast{num_game_stats}"] = total_team_red
    df_write.at[index, f"AwayTeamGoalScoredWeightLast{num_game_stats}"] = (
        total_team_goal_scored
    )
    df_write.at[index, f"AwayTeamGoalConcededWeightLast{num_game_stats}"] = (
        total_team_goal_conceded
    )


def update_all_weight_last20(df_write, date_end, num_game_stats):
    for index, _ in df_write[::-1].iterrows():
        print(df_write.loc[index]["Date"])
        if df_write.loc[index]["Date"] == date_end:
            return
        # print(index)
        get_row_last_20(df_write, index, num_game_stats)
