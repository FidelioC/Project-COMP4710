import pandas as pd

# Load the CSV file
data = pd.read_csv("./results/random_forest_stats_stats20_h2h10_top5.csv")

# Find rows where FTR does not match FTR_Prediction
matches = data[(data["FTR"] == data["FTR_Prediction"]) & (data["FTR"] != "D")]

# Filter the rows where FTR is not 'D' (draw)
non_draw_rows = data[data["FTR"] != "D"]

# Get the count of rows where FTR is not 'D'
total_rows_non_draw = len(non_draw_rows)

# Calculate the accuracy percentage
total_rows = len(data)
match_count = len(matches)
print(f"Match count: {match_count}. Total rows: {total_rows_non_draw}")
accuracy_percentage = (match_count / total_rows_non_draw) * 100

# Print the results
if total_rows > 0:
    print(f"Accuracy percentage: {accuracy_percentage:.2f}%")
else:
    print("No data to calculate accuracy.")
