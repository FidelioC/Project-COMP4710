import pandas as pd
from collections import defaultdict

df = pd.read_csv("./training_data/combined_file.csv")


def calculate_total_HAD(df):
    # calculate each percentage of Home, Draw and Away percentages
    HAD_dict = defaultdict(int)
    total_games = 0
    for index, row in df.iterrows():
        HAD_dict[row["FTR"]] += 1
        total_games += 1

    return HAD_dict, total_games


def print_all_pct(dict, total_games):
    for item, key in dict.items():
        print(f"FTR: {item}, {item}%: {(key/total_games) * 100}")


def main():
    dict, total_games = calculate_total_HAD(df)
    print(print_all_pct(dict, total_games))


if __name__ == "__main__":
    main()
