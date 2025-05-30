# Project-COMP4710

## Overview

![alt text](4710-project.png)

This repo is used to prepare the dataset of the english premier league, that will be used to calculate contribution of attributes and also used to train the random forest and gradient boosting algorithm, will use those model to predict an outcome of a match.

1. combined_file.py: used to combined all csv files from the english premier datasets.
2. calculate_ind_team_stats.py: used to calculate each team stats and H2H values of each team using a sliding window model.
3. random_forest.py: used to train the random forest algorithm and predict the Full Time Result given a csv file with the appropiate columns.
4. gradient_boosting.py: used to train the gradient boosting algorithm and predict the Full Time Result given a csv file with the appropiate columns.
5. check_predictions.py: to calculate the accuracy of the prediction. Given a csv file, it must have two columns, (1) FTR, (2) FTR_Prediction

## How to run calculate_ind_team_stats.py

### Getting Training Datasets

#### Different Stats Window Size

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

#### Different H2H Window Size

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 15, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats15_h2h10.csv" --num_game_stats 15 --num_game_h2h 10 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 20, H2H window size = 7**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats20_h2h7.csv" --num_game_stats 20 --num_game_h2h 7 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 20, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats20_h2h10.csv" --num_game_stats 20 --num_game_h2h 10 --date_end "24/05/15" --start_date "2015-08-08"`

**Stats window size = 30, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./training_data/combined_file.csv" --outputfile "./training_data/team_stats_stats30_h2h10.csv" --num_game_stats 30 --num_game_h2h 10 --date_end "24/05/15" --start_date "2015-08-08"`

### Getting Prediction Datasets

#### Different Stats Window Size

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

#### Different H2H Window Size

**Stats window size = 15, H2H window size = 5**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats15_h2h5.csv" --num_game_stats 15 --num_game_h2h 5 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 15, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats15_h2h10.csv" --num_game_stats 15 --num_game_h2h 10 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 20, H2H window size = 7**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats20_h2h7.csv" --num_game_stats 20 --num_game_h2h 7 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 20, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats20_h2h10.csv" --num_game_stats 20 --num_game_h2h 10 --date_end "22/05/2022" --start_date "2022-08-05"`

**Stats window size = 30, H2H window size = 10**
`python .\calculate_ind_team_stats.py --inputfile "./prediction_test/combined_file.csv" --outputfile "./prediction_test/team_stats_stats30_h2h10.csv" --num_game_stats 30 --num_game_h2h 10 --date_end "22/05/2022" --start_date "2022-08-05"`

## Random forest/ Gradient Boosting

`python ./random_forest.py --trainingdata ./training_data/team_stats_stats20_h2h10.csv --predictionfile ./prediction_test/team_stats_stats20_h2h10.csv --outputfile ./results/random_forest_stats_stats20_h2h10.csv`
