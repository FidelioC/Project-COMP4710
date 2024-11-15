import pandas as pd

# Load the CSV file
data = pd.read_csv("./prediction_test/gboost_stats40_h2h5.csv")

# Find rows where FTR does not match FTR_Prediction
mismatches = data[data["FTR"] != data["FTR_Prediction"]]
matches = data[data["FTR"] == data["FTR_Prediction"]]

accuracy = 1 - (len(mismatches) / len(data))

# Check if there are any mismatches and print them
if not mismatches.empty:
    print("Mismatched rows:\n", mismatches[["Date", "HomeTeam", "AwayTeam", "FTR", "FTR_Prediction"]])
    print("\nMatched rows:\n", matches[["Date", "HomeTeam", "AwayTeam", "FTR", "FTR_Prediction"]])
    print(f"\nAccuracy: {accuracy*100:.2f}%\n")
else:
    print("All predictions match the actual results.")
