import pandas as pd

# Load the CSV file
data = pd.read_csv("./results/random_forest_stats20_h2h10.csv")

# Find rows where FTR does not match FTR_Prediction
matches = data[data["FTR"] == data["FTR_Prediction"]]

# Calculate the accuracy percentage
total_rows = len(data)
match_count = len(matches)
accuracy_percentage = (match_count / total_rows) * 100

# Print the results
if total_rows > 0:
    print(f"Accuracy percentage: {accuracy_percentage:.2f}%")
else:
    print("No data to calculate accuracy.")
