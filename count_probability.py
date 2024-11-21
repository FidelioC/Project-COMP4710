import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load training data
train_file_path = "./training_data/team_stats_stats20_h2h10.csv"
df_train = pd.read_csv(train_file_path)

# Map FTR (Full-Time Result) to numerical values for training
# We will not store this in the final file
df_train["FTR_Encoded"] = df_train["FTR"].map({"H": 2, "D": 1, "A": 0})

# Define features and target for training
features = [
    "HomeTeamPointLast20",
    "AwayTeamPointLast20",
    "HomeTeamGoalScoredLast20",
    "AwayTeamGoalScoredLast20",
    "HomeTeamGoalConcededLast20",
    "AwayTeamGoalConcededLast20",
    "HomeTeamShotTargetLast20",
    "AwayTeamShotTargetLast20",
    "HomeTeamRedLast20",
    "AwayTeamRedLast20",
    "HomeTeamPointH2HLast10",
    "AwayTeamPointH2HLast10",
]
X_train = df_train[features]
y_train = df_train["FTR_Encoded"]

# Train the model
model = Pipeline(
    [
        ("scaler", StandardScaler()),
        (
            "log_reg",
            LogisticRegression(
                multi_class="multinomial", solver="lbfgs", max_iter=1000
            ),
        ),
    ]
)
model.fit(X_train, y_train)

# Make predictions on the entire training data (not just the split)
train_probabilities = model.predict_proba(X_train)

# Load prediction test data
test_file_path = "./prediction_test/team_stats_stats20_h2h10.csv"
df_test = pd.read_csv(test_file_path)

# Define features for test data prediction
X_test_data = df_test[features]

# Predict probabilities for the test dataset
test_probabilities = model.predict_proba(X_test_data)

# Add probabilities to the training dataset without FTR_Encoded
df_train["Home_Win_Prob"] = train_probabilities[:, 2]
df_train["Draw_Prob"] = train_probabilities[:, 1]
df_train["Away_Win_Prob"] = train_probabilities[:, 0]

# Add probabilities to the test dataset
df_test["Home_Win_Prob"] = test_probabilities[:, 2]
df_test["Draw_Prob"] = test_probabilities[:, 1]
df_test["Away_Win_Prob"] = test_probabilities[:, 0]

# Output the updated training and test datasets with probabilities to CSV files
train_output_file = "./training_data/team_stats_stats20_h2h10_probability.csv"
test_output_file = "./prediction_test/team_stats_stats20_h2h10_probability.csv"

# Save only the relevant columns (no FTR_Encoded in the final output)
df_train.drop(columns=["FTR_Encoded"], inplace=True)

# No need to drop anything from df_test, since FTR_Encoded doesn't exist there
df_train.to_csv(train_output_file, index=False)
df_test.to_csv(test_output_file, index=False)

print(
    f"Predicted probabilities for training data have been saved to {train_output_file}"
)
print(f"Predicted probabilities for test data have been saved to {test_output_file}")
