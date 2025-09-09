import pandas as pd
import os

# directory = "./training_data/Datasets"
output = "./prediction_test/combined_file_from_url.csv"
data_frames = []

season_codes = ["0001","0102","0203","0304","0405","0506","0607","0708"
                ,"0809","0910","1011","1112","1213","1314","1415"
                ,"1516","1617","1718","1819","1920","2021","2122","2223"] # Training data
# season_codes = ["2223"] # Prediction data 
for code in season_codes:
    url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
    try:
        current_file = pd.read_csv(
            url,
            usecols=[
                "Date",
                "HomeTeam",
                "AwayTeam",
                "FTHG",
                "FTAG",
                "HST",
                "AST",
                "HR",
                "AR",
                "FTR",
            ],
            encoding="utf-8"
        )
        data_frames.append(current_file)
    except UnicodeDecodeError as ude:
        current_file = pd.read_csv(
            url,
            usecols=[
                "Date",
                "HomeTeam",
                "AwayTeam",
                "FTHG",
                "FTAG",
                "HST",
                "AST",
                "HR",
                "AR",
                "FTR",
            ],
            encoding="latin1"
        )
    except Exception as e:
        print(f"Could not fetch season {code}: {e}")
        continue
    
    #Concatenate the data from both files
    combined_data = pd.concat(
        data_frames,
        ignore_index=True,
    )
    
#Save the combined data to a new CSV file
combined_data.to_csv(output, index=False)
    
# for filename in os.listdir(directory):
#     # Check if the file is a CSV
#     if filename.endswith(".csv"):
#         file_path = os.path.join(directory, filename)

#         print(file_path)

#         current_file = pd.read_csv(
#             file_path,
#             usecols=[
#                 "Date",
#                 "HomeTeam",
#                 "AwayTeam",
#                 "FTHG",
#                 "FTAG",
#                 "HST",
#                 "AST",
#                 "HR",
#                 "AR",
#                 "FTR",
#             ],
#         )

#         data_frames.append(current_file)

# # Concatenate the data from both files
# combined_data = pd.concat(
#     data_frames,
#     ignore_index=True,
# )

# # Save the combined data to a new CSV file
# combined_data.to_csv(output, index=False)
