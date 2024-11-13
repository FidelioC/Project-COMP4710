import pandas as pd

# Load the CSV file
data = pd.read_csv("./prediction_test/gboost-2023-teams-predictions.csv")

# Find rows where FTR does not match FTR_Prediction
mismatches = data[data["FTR"] != data["FTR_Prediction"]]

# Check if there are any mismatches and print them
if not mismatches.empty:
    print("Mismatched rows:\n", mismatches)
else:
    print("All predictions match the actual results.")
