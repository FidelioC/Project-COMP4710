import pandas as pd

# Load CSV into pandas DataFrame
df = pd.read_csv("./training_data/combined_file.csv")


def is_team_home_win(df, team_name):
    return is_home_team(df, team_name) and is_home_win(df)


def is_team_away_win(df, team_name):
    return is_away_team(df, team_name) and is_away_win(df)


def is_home_win(df):
    return df["FTR"] == "H"


def is_away_win(df):
    return df["FTR"] == "A"


def is_home_team(df, team_name):
    return df["HomeTeam"] == team_name


def is_away_team(df, team_name):
    return df["AwayTeam"] == team_name


def calculate_specific_home_pct(df, team_name):
    total_home_win = 0
    total_home_game = 0
    for index, row in df.iterrows():
        if is_team_home_win(row, team_name):
            total_home_win += 1
            total_home_game += 1
        elif is_home_team(row, team_name):
            total_home_game += 1

    return (total_home_win / total_home_game) * 100


def calculate_all_home_pct(df):
    total_home_win = 0
    total_home_game = 0
    for index, row in df.iterrows():
        if is_home_win(row):
            total_home_win += 1
        total_home_game += 1

    return (total_home_win / total_home_game) * 100


def all_team_home_pct(df):
    all_team_dict = {}
    curr_team_home = ""
    for index, row in df.iterrows():
        curr_team_home = row["HomeTeam"]
        if curr_team_home not in all_team_dict:  # curr team hasn't appeared previously
            if is_team_home_win(row, curr_team_home):
                # home team win
                all_team_dict[curr_team_home] = [1, 1]
            else:
                # home team lose, just add to the total games
                all_team_dict[curr_team_home] = [0, 1]
        else:  # curr team has appeared previously
            if is_team_home_win(row, curr_team_home):
                # home team win
                all_team_dict[curr_team_home][0] += 1  # add to total win

            # either home team win/ lose, add the total games
            all_team_dict[curr_team_home][1] += 1

    return all_team_dict


def print_all_pct(dict):
    for item, key in dict.items():
        print(f"Team: {item}, Home Win %: {(key[0]/key[1]) * 100}")


def main():
    print(calculate_specific_home_pct(df, "QPR"))
    print(f"All Home Percentage: {calculate_all_home_pct(df)}")

    dict = all_team_home_pct(df)
    print(print_all_pct(dict))


if __name__ == "__main__":
    main()
