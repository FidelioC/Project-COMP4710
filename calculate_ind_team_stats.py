import pandas as pd
from collections import defaultdict
from dateutil import parser
# import click
import calculate_stats_points
import calculate_h2h

# input_file = "./prediction_test/combined_file.csv"  # "./training_data/combined_file.csv" "./prediction_test/combined_file.csv"
# output_file = "./prediction_test/team_stats_noh2h.csv"  # "./training_data/team_stats.csv" "./prediction_test/team_stats.csv"
# date_end = "22/05/2022"  # date/month/year "24/05/15" "22/05/2022"
# start_date = "2022-08-05"  # year - month - date "2015-08-08" "2022-08-05"


def parse_date(date_str):
    try:
        # Parse the date using dateutil.parser, which automatically handles multiple formats
        return parser.parse(date_str, dayfirst=True)
    except (ValueError, TypeError):
        # Return NaT (Not a Time) if the date parsing fails
        return pd.NaT


def main(input_file, output_file, num_game_stats, num_game_h2h, date_end, start_date):
    # ======== add new columns ========== "
    df_read = pd.read_csv(input_file)

    calculate_stats_points.stats_new_columns(df_read, num_game_stats)
    calculate_h2h.h2h_new_columns(df_read, num_game_h2h)

    df_read.to_csv(output_file, index=False)

    df_write = pd.read_csv(output_file)

    calculate_stats_points.update_all_stats_last20(df_write, date_end, num_game_stats)
    calculate_h2h.update_h2h_stats_last10(df_write, date_end, num_game_h2h)

    df_write["Date"] = df_write["Date"].apply(parse_date)

    # Filter rows with dates from 08/08/15 to the end
    start_date = pd.to_datetime(start_date)
    df_filtered = df_write[df_write["Date"] >= start_date].copy()
    
    df_filtered = df_filtered.drop(columns=[f"HomeTeamRatingLast{num_game_stats}",
                                            f"AwayTeamRatingLast{num_game_stats}",
                                            f"HomeTeamWin%H2HLast{num_game_h2h}",
                                            f"AwayTeamWin%H2HLast{num_game_h2h}"], errors="ignore")

    df_filtered.to_csv(output_file, index=False)


# @click.command()
# @click.option("--inputfile", required=True)
# @click.option("--outputfile", required=True)
# @click.option("--num_game_stats", required=True)
# @click.option("--num_game_h2h", required=True)
# @click.option("--date_end", required=True)
# @click.option("--start_date", required=True)
# def commands_processing(
#     inputfile, outputfile, num_game_stats, num_game_h2h, date_end, start_date
# ):
#     main(inputfile, outputfile, num_game_stats, num_game_h2h, date_end, start_date)


if __name__ == "__main__":
    # commands_processing()
    input_file = "./prediction_test/combined_file.csv"  # "./training_data/combined_file.csv" "./prediction_test/combined_file.csv"
    normal_size = [10, 15, 20, 25, 30]
    h2h_size = [5, 10]
    test_date_end = "22/05/2022"  # date/month/year "24/05/15" "22/05/2022"
    test_date_start = "2022-08-05"  # year - month - date "2015-08-08" "2022-08-05"
    print("Start processing test data...")
    for num_game_stats in normal_size:
        for num_game_h2h in h2h_size:
            output_file = f"./prediction_test/team_stats_normal{num_game_stats}_h2h{num_game_h2h}.csv"
            main(
                input_file,
                output_file,
                num_game_stats,
                num_game_h2h,
                test_date_end,
                test_date_start,
            )
    print("Test data processed successfully!")
    print("Start processing training data...")
    input_file = "./training_data/combined_file.csv"  # "./training_data/combined_file.csv" "./prediction_test/combined_file.csv"
    train_date_end = "24/05/15"  # date/month/year "24/05/15" "22/05/2022"
    train_date_start = "2015-08-08"  # year - month - date "2015-08-08" "2022-08-05"
    for num_game_stats in normal_size:
        for num_game_h2h in h2h_size:
            output_file = f"./training_data/team_stats_normal{num_game_stats}_h2h{num_game_h2h}.csv"
            main(
                input_file,
                output_file,
                num_game_stats,
                num_game_h2h,
                train_date_end,
                train_date_start,
            )
    print("Training data processed successfully!")