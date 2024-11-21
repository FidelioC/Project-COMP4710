import pandas as pd

# Load the dataset
file_path = (
    "./english_premier/2022:2023-betting.csv"  # Update with the path to your file
)
df = pd.read_csv(file_path)

betting_site = "WH"


# Add the 'FTR_Prediction' column based on the highest B365H, B365D, and B365A values
def predict_ftr(row):
    # Find the highest of the three columns: B365H, B365D, B365A
    min_value = min(
        row[f"{betting_site}H"], row[f"{betting_site}D"], row[f"{betting_site}A"]
    )

    if min_value == row[f"{betting_site}H"]:
        return "H"  # Home team prediction
    elif min_value == row[f"{betting_site}D"]:
        return "D"  # Draw prediction
    else:
        return "A"  # Away team prediction


# Apply the prediction function to each row
df["FTR_Prediction"] = df.apply(predict_ftr, axis=1)

# Save the updated dataframe with the new column
output_file_path = f"./results/{betting_site}_betting_results.csv"  # Update with the desired output path
df.to_csv(output_file_path, index=False)

print(f"Updated file saved to: {output_file_path}")
