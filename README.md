# Project-COMP4710

## Getting Training Datasets

### Different Stats Window Size

**Stats window size = 5, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats5_h2h5.csv" --num_game_stats 5 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 10, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats10_h2h5.csv" --num_game_stats 10 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 20, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats20_h2h5.csv" --num_game_stats 20 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 30, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats30_h2h5.csv" --num_game_stats 30 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 40, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats40_h2h5.csv" --num_game_stats 40 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

### Different H2H Window Size

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 15, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats15_h2h10.csv" --num_game_stats 15 --num_game_h2h 10 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 20, H2H window size = 7**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats20_h2h7.csv" --num_game_stats 20 --num_game_h2h 7 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 30, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats30_h2h10.csv" --num_game_stats 30 --num_game_h2h 10 --date_end "24/05/15" --start_date "2015-08-08"`

## Getting Prediction Datasets

### Different Stats Window Size

**Stats window size = 5, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats5_h2h5.csv" --num_game_stats 5 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 10, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats10_h2h5.csv" --num_game_stats 10 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 20, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats20_h2h5.csv" --num_game_stats 20 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 30, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats30_h2h5.csv" --num_game_stats 30 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 40, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats40_h2h5.csv" --num_game_stats 40 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

### Different H2H Window Size

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 15, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats15_h2h10.csv" --num_game_stats 15 --num_game_h2h 10 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 20, H2H window size = 7**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats20_h2h7.csv" --num_game_stats 20 --num_game_h2h 7 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 30, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats30_h2h10.csv" --num_game_stats 30 --num_game_h2h 10 --date_end "22/05/2022" --start_date "2022-08-05"`

## Random forest

`python .\random_forest.py --trainingdata .\training_data\team_stats_stats5_h2h5.csv --predictionfile .\prediction_test\team_stats_stats5_h2h5.csv --outputfile .\results\random_forest_stats5_h2h5.csv`
