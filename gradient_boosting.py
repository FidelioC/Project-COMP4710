import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# import click
import itertools
import check_predictions

# """
# "HomeTeamShotTargetLast20",
# "AwayTeamShotTargetLast20",
# "HomeTeamGoalScoredLast20",
# "AwayTeamGoalScoredLast20",
# "HomeTeamPointLast20",
# "AwayTeamPointLast20",
# "HomeTeamPointH2HLast10",
# "AwayTeamPointH2HLast10",
# "HomeTeamWin%H2HLast10",
# "AwayTeamWin%H2HLast10",
# "HomeTeamGoalScoredH2HLast10",
# "AwayTeamGoalScoredH2HLast10",
# "HomeTeamShotTargetH2HLast10",
# "AwayTeamShotTargetH2HLast10",
# "HomeTeamRedH2HLast10",
# "AwayTeamRedH2HLast10",
# "HomeTeamRedLast20",
# "AwayTeamRedLast20",
# "HomeTeamGoalConcededLast20",
# "AwayTeamGoalConcededLast20",
# "HomeTeamGoalConcededH2HLast10",
# "AwayTeamGoalConcededH2HLast10",
# """


def calculate_all_possible_attributes(training_data, prediction_file, output_file, attributes):
    all_possible_dict = {}
    # List of attributes
    # attributes = [
    #     "ShotTargetLast20",
    #     "GoalScoredLast20",
    #     "PointLast20",
    #     "PointH2HLast10",
    #     "GoalScoredH2HLast10",
    #     "ShotTargetH2HLast10",
    #     "RedH2HLast10",
    #     "RedLast20",
    #     "GoalConcededLast20",
    #     "GoalConcededH2HLast10",
    # ]

    # Generate all non-empty combinations of attributes

    for r in range(1, len(attributes) + 1):  # r is the size of the subset
        for combo in itertools.combinations(attributes, r):
            # Add HomeTeam and AwayTeam prefixes
            modified_combo = [f"{item}" for item in combo] + [
                f"{item}" for item in combo
            ]
            gradient_boosting(training_data, prediction_file, output_file, modified_combo)
            all_possible_dict[combo] = check_predictions.calculate_prediction(
                output_file
            )
            print(
                f"combo: {combo}, accuracy: {check_predictions.calculate_prediction(output_file)}"
            )

    return all_possible_dict


def gradient_boosting(training_data, prediction_file, output_file, feature_columns):
    # Load data
    df = pd.read_csv(training_data)

    # Drop rows where FTR is 'D'
    df = df[df["FTR"] != "D"]

    # # Define the feature columns
    # feature_columns = [
    #     "HomeTeamShotTargetLast20",
    #     "AwayTeamShotTargetLast20",
    #     "HomeTeamGoalScoredLast20",
    #     "AwayTeamGoalScoredLast20",
    #     "HomeTeamPointLast20",
    #     "AwayTeamPointLast20",
    #     "HomeTeamPointH2HLast10",
    #     "AwayTeamPointH2HLast10",
    # ]

    # Select features and target
    X = df[feature_columns]
    y = df["FTR"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the Random Forest Classifier
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set for accuracy
    # y_test_pred = model.predict(X_test)
    # accuracy = accuracy_score(y_test, y_test_pred)
    # print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Load new data (2023-teams.csv) for prediction
    new_data = pd.read_csv(prediction_file)

    # Select features in the new data
    X_new = new_data[feature_columns]

    # Make predictions on the new data
    new_data["FTR_Prediction"] = model.predict(X_new)

    # Save the results with predictions to a new CSV file
    new_data.to_csv(output_file, index=False)

    # print("Predictions saved successfully.")


# @click.command()
# @click.option("--trainingdata", required=True)
# @click.option("--predictionfile", required=True)
# @click.option("--outputfile", required=True)
# def commands_processing(trainingdata, predictionfile, outputfile):
#     # gradient_boosting
#(trainingdata, predictionfile, outputfile)
#     all_possible_dict = calculate_all_possible_attributes(
#         trainingdata, predictionfile, outputfile
#     )

#     # Convert the dictionary to a Pandas DataFrame

#     df = pd.DataFrame(list(all_possible_dict.items()), columns=["Combo", "Accuracy"])

#     # Sort the DataFrame by the "Accuracy" column
#     df_sorted = df.sort_values(by="Accuracy", ascending=True)

#     # Save the sorted DataFrame to a CSV file
#     df_sorted.to_csv("./results/random_forest_all_possible_combo.csv", index=False)


if __name__ == "__main__":
    # commands_processing()
    normal_size = [10, 15, 20, 25, 30]
    h2h_size = [5, 10]
    for num_game_stats in normal_size:
        for num_game_h2h in h2h_size:
            training_data = f"./training_data/team_stats_normal{num_game_stats}_h2h{num_game_h2h}.csv"
            prediction_file = f"./prediction_test/team_stats_normal{num_game_stats}_h2h{num_game_h2h}.csv"
            output_file = f"./results/gradient_boosting_normal{num_game_stats}_h2h{num_game_h2h}.csv"
            feature_columns = [
                f"HomeTeamShotTargetLast{num_game_stats}",
                f"AwayTeamShotTargetLast{num_game_stats}",
                f"HomeTeamGoalScoredLast{num_game_stats}",
                f"AwayTeamGoalScoredLast{num_game_stats}",
                f"HomeTeamPointLast{num_game_stats}",
                f"AwayTeamPointLast{num_game_stats}",
                f"HomeTeamPointH2HLast{num_game_h2h}",
                f"AwayTeamPointH2HLast{num_game_h2h}",
            ]
            print(f'Start calculating all possible attributes for: Normal = {num_game_stats}, H2H = {num_game_h2h}')
            calculate_all_possible_attributes(
                training_data, prediction_file, output_file, feature_columns
            )
            print("=" * 50)