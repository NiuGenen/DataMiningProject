import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import pickle
import time
from sklearn import tree
from sklearn.model_selection import cross_val_score

txt_col_name=[
    'day',              # 0
    'time',             # 1
    'direction',        # 2
    'road_type',        # 3
    'linkid',           # 4
    'length',           # 5
    'travel_time',      # 6
    'volumn',           # 7
    'speed',            # 8
    'occupancy',        # 9
    'congestion_level'  # 10
]

dmc.check_file_and_pause( dmfp.pp1_train_data_path )
verbose = 1
train_data = []
for file in sd.train_0707:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,3,4,5,6,7,8,9], 10, verbose)
for file in sd.train_0715:
    data_csv = pd.read_csv( file, header=None , sep='\t', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,3,4,5,6,7,8,9], 10, verbose)
for file in sd.train_0720:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,3,4,5,6,7,8,9], 10, verbose)
for file in sd.train_0721:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,3,4,5,6,7,8,9], 10, verbose)

print("correlation analysis [4] and [5]")
dfcorr = ppf.pp_correlation_analysis_categorical( train_data, [2,3], ["linkid","length"] )
print(dfcorr)

print("correlation analysis [6] and [7]")
dfcorr = ppf.pp_correlation_analysis_categorical( train_data, [6,7,8,9], ["travel_time","volumn","speed","occupancy"] )
print(dfcorr)

