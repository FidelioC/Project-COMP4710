import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import click


def main(training_data, prediction_file, output_file):
    # Load data
    df = pd.read_csv(training_data)

    # Drop rows where FTR is 'D'
    df = df[df["FTR"] != "D"]

    # Define the feature columns
    feature_columns = [
        "HomeTeamShotTargetLast20",
        "AwayTeamShotTargetLast20",
        "HomeTeamGoalScoredLast20",
        "AwayTeamGoalScoredLast20",
        "HomeTeamPointLast20",
        "AwayTeamPointLast20",
        "HomeTeamPointH2HLast10",
        "AwayTeamPointH2HLast10",
        "HomeTeamWin%H2HLast10",
        "AwayTeamWin%H2HLast10",
    ]

    # Select features and target
    X = df[feature_columns]
    y = df["FTR"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set for accuracy
    y_test_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Load new data (2023-teams.csv) for prediction
    new_data = pd.read_csv(prediction_file)

    # Select features in the new data
    X_new = new_data[feature_columns]

    # Make predictions on the new data
    new_data["FTR_Prediction"] = model.predict(X_new)

    # Save the results with predictions to a new CSV file
    new_data.to_csv(output_file, index=False)

    print("Predictions saved successfully.")


@click.command()
@click.option("--trainingdata", required=True)
@click.option("--predictionfile", required=True)
@click.option("--outputfile", required=True)
def commands_processing(trainingdata, predictionfile, outputfile):
    main(trainingdata, predictionfile, outputfile)


if __name__ == "__main__":
    commands_processing()
