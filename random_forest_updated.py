import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import click


def main(training_data, prediction_file, output_file):
    # Load data
    df = pd.read_csv(training_data)

    # Load new data for prediction (ensure this is loaded before referencing it)
    new_data = pd.read_csv(prediction_file)

    # Initialize LabelEncoder
    le = LabelEncoder()

    # Combine both the training and new data for encoding
    combined_teams = pd.concat(
        [df["HomeTeam"], df["AwayTeam"], new_data["HomeTeam"], new_data["AwayTeam"]]
    )

    # Fit the LabelEncoder on combined data to handle unseen labels
    le.fit(combined_teams)

    # Encode the team columns using the trained encoder
    df["HomeTeam_Encoded"] = le.transform(df["HomeTeam"])
    df["AwayTeam_Encoded"] = le.transform(df["AwayTeam"])

    # Define features and target
    X = df.drop(
        columns=[
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
    )
    y = df["FTR"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize the RandomForestClassifier
    model = RandomForestClassifier(random_state=42)

    # Define the parameter grid for hyperparameter tuning
    param_grid = {
        "n_estimators": [100, 200, 300],  # Number of trees
        "max_depth": [None, 10, 20, 30],  # Depth of trees
        "min_samples_split": [2, 5, 10],  # Minimum samples to split an internal node
        "min_samples_leaf": [1, 2, 4],  # Minimum samples in a leaf node
        "max_features": [
            "auto",
            "sqrt",
            "log2",
        ],  # Number of features to consider at each split
    }

    # Initialize GridSearchCV with RandomForestClassifier and the parameter grid
    grid_search = GridSearchCV(
        estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2
    )

    # Fit GridSearchCV on training data
    grid_search.fit(X_train, y_train)

    # Print the best parameters from GridSearchCV
    print("Best parameters found: ", grid_search.best_params_)

    # Get the best model from grid search
    best_model = grid_search.best_estimator_

    # Make predictions on the test set for accuracy
    y_test_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Prepare the new data (drop identifiers if they exist)
    X_new = new_data.drop(
        columns=[
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
        ],
        errors="ignore",
    )

    # Encode the HomeTeam and AwayTeam columns in the new data using the same encoder
    X_new["HomeTeam_Encoded"] = le.transform(new_data["HomeTeam"])
    X_new["AwayTeam_Encoded"] = le.transform(new_data["AwayTeam"])

    # Make predictions on the new data using the best model from grid search
    new_data["FTR_Prediction"] = best_model.predict(X_new)

    # Save the results with predictions to a new CSV file
    new_data.to_csv(output_file, index=False)

    print("Random forest finished")


@click.command()
@click.option("--trainingdata", required=True)
@click.option("--predictionfile", required=True)
@click.option("--outputfile", required=True)
def commands_processing(trainingdata, predictionfile, outputfile):
    main(trainingdata, predictionfile, outputfile)


if __name__ == "__main__":
    commands_processing()
