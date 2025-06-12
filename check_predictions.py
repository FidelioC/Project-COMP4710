import pandas as pd


def calculate_prediction(file_name):
    data = pd.read_csv(file_name)
    # Find rows where FTR does not match FTR_Prediction
    matches = data[(data["FTR"] == data["FTR_Prediction"]) & (data["FTR"] != "D")]

    # Filter the rows where FTR is not 'D' (draw)
    non_draw_rows = data[data["FTR"] != "D"]

    # Get the count of rows where FTR is not 'D'
    total_rows_non_draw = len(non_draw_rows)

    # Calculate the accuracy percentage
    total_rows = len(data)
    match_count = len(matches)
    # print(f"Match count: {match_count}. Total rows: {total_rows_non_draw}")
    # accuracy_percentage = (match_count / total_rows_non_draw) * 100
    accuracy_percentage = (match_count / total_rows) * 100

    # Print the results
    # if total_rows > 0:
    #     print(f"Accuracy percentage: {accuracy_percentage:.2f}%")
    # else:
    #     print("No data to calculate accuracy.")

    return accuracy_percentage

def calculate_prediction_draw_init(file_name):
    data = pd.read_csv(file_name)

    # Find rows where FTR matches FTR_Prediction (including draws)
    matches = data[data["FTR"] == data["FTR_Prediction"]]

    # Total number of rows
    total_rows = len(data)

    # Number of correct predictions
    match_count = len(matches)

    # Calculate accuracy
    if total_rows > 0:
        accuracy_percentage = (match_count / total_rows) * 100
        print(f"Accuracy percentage: {accuracy_percentage:.2f}%")
    else:
        # print("No data to calculate accuracy.")
        accuracy_percentage = 0.0

    return accuracy_percentage


if __name__ == "__main__":
    # normal_size = [5, 10, 15, 20, 25, 30]
    # h2h_size = [5, 10]
    
    # # Random Forest Stats and H2H
    # for num_game_stats in normal_size:
    #     for num_game_h2h in h2h_size:
    #         file_name = f"./results/random_forest_normal{num_game_stats}_h2h{num_game_h2h}.csv"
    #         accuracy = calculate_prediction_draw_init(file_name)
    #         print(
    #             f"Accuracy for RF normal {num_game_stats} and h2h {num_game_h2h}: {accuracy:.2f}%"
    #         )
    #         file_name = f"./results/gradient_boosting_normal{num_game_stats}_h2h{num_game_h2h}.csv"
    #         accuracy = calculate_prediction_draw_init(file_name)
    #         print(
    #             f"Accuracy for GB normal {num_game_stats} and h2h {num_game_h2h}: {accuracy:.2f}%"
    #         )
    #         print("--" * 20)

            

    ## Testing
    file_name = "./results/random_forest_stats5_h2h5.csv"
    calculate_prediction_draw_init(file_name)
