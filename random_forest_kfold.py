import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import accuracy_score
import click

ignore_columns = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTR",
    "FTHG",
    "FTAG",
    "HR",
    "AR",
    "HST",
    "AST",
]


def main(training_data, prediction_file, output_file):
    # Load data
    df = pd.read_csv(training_data)

    # Select features and target
    X = df.drop(
        columns=ignore_columns,
        errors="ignore",
    )
    # Encode categorical columns using one-hot encoding
    X = pd.get_dummies(X, drop_first=True)

    y = df["FTR"]

    # Initialize KFold cross-validation
    kf = KFold(n_splits=10, shuffle=True, random_state=42)

    # Initialize and train the Random Forest Classifier
    model = RandomForestClassifier(random_state=42)

    # Perform cross-validation and calculate accuracy scores
    accuracy_scores = cross_val_score(model, X, y, cv=kf, scoring="accuracy")
    average_accuracy = accuracy_scores.mean()
    print(f"Average cross-validation accuracy: {average_accuracy * 100:.2f}%")

    # Train the model on the full dataset
    model.fit(X, y)

    # Load new data (2023-teams.csv) for prediction
    new_data = pd.read_csv(prediction_file)

    # Prepare the new data (drop identifiers if they exist)
    X_new = new_data.drop(
        columns=ignore_columns,
        errors="ignore",
    )
    # Encode categorical columns in the new data using the same process as training
    X_new = pd.get_dummies(X_new, drop_first=True)
    X_new = X_new.reindex(columns=X.columns, fill_value=0)

    # Make predictions on the new data
    new_data["FTR_Prediction"] = model.predict(X_new)

    # Save the results with predictions to a new CSV file
    new_data.to_csv(output_file, index=False)

    print("Random forest finished")


# training_data = "./training_data/team_stats_stats.csv"
# prediction_file = "./prediction_test/team_stats_avg.csv"
# output_file = "./prediction_test/2023-teams-predictions-avg-randomforest.csv"


@click.command()
@click.option("--trainingdata", required=True)
@click.option("--predictionfile", required=True)
@click.option("--outputfile", required=True)
def commands_processing(trainingdata, predictionfile, outputfile):
    main(trainingdata, predictionfile, outputfile)


if __name__ == "__main__":
    commands_processing()
