import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

training_data = "./training_data/team_stats.csv"
prediction_file = "./prediction_test/team_stats.csv"
output_file = "./prediction_test/2023-teams-predictions.csv"

# Load data
df = pd.read_csv(training_data)

# Select features and target
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

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set for accuracy
y_test_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_test_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")


# Load new data (2023-teams.csv) for prediction
new_data = pd.read_csv(prediction_file)

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

# Make predictions on the new data
new_data["FTR_Prediction"] = model.predict(X_new)

# Save the results with predictions to a new CSV file
new_data.to_csv(output_file, index=False)
