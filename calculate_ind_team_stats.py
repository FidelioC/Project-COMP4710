import pandas as pd
from collections import defaultdict
from dateutil import parser
import click
import calculate_stats_points
import calculate_h2h
import calculate_weighted

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
    # calculate_h2h.h2h_new_columns(df_read, num_game_h2h)
    calculate_weighted.weighted_new_columns(df_read, num_game_stats)

    df_read.to_csv(output_file, index=False)

    df_write = pd.read_csv(output_file)

    calculate_stats_points.update_all_stats_last20(df_write, date_end, num_game_stats)
    # calculate_h2h.update_h2h_stats_last10(df_write, date_end, num_game_h2h)
    calculate_weighted.update_all_weight_last20(df_write, date_end, num_game_stats)

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
