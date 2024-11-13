import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

training_data = "./training_data/team_stats.csv"
prediction_file = "./prediction_test/team_stats.csv"
output_file = "./prediction_test/gboost-2023-teams-predictions.csv"


# Load the dataset
data = pd.read_csv(training_data)

# Split data into features and target
X = data.drop(columns=[
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTR",
        "FTHG",
        "FTAG",
        "HR",
        "AR",
        "HST",
        "AST",],
        errors="ignore"
)
Y = data["FTR"]

# Split data into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train the Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, Y_train)

# Evaluate the model
# Make prediction
Y_pred = gb_model.predict(X_test)

# Calculate accuracy and classification report
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Fetch new data (2022-2023)
new_data = pd.read_csv(prediction_file)

X_new = new_data.drop(columns=[
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTR",
        "FTHG",
        "FTAG",
        "HR",
        "AR",
        "HST",
        "AST",], 
        errors="ignore"
)

# Make predictions on the new data
new_data["FTR_Prediction"] = gb_model.predict(X_new)

# Save the results with predictions to a new CSV file
new_data.to_csv(output_file, index=False)