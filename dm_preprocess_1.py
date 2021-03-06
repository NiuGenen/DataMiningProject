import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp

txt_col_name=[
    'day',             # 0
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

train_col_name=[
    'day',             # 0 - 0
    'time',             # 1 - 1
    'direction',        # 2 - 2
    'linkid',           # 3 - 4
    'travel_time',      # 4 - 6
    'volumn',           # 5 - 7
    'speed',            # 6 - 8
    'occupancy',        # 7 - 9
    'congestion_level'  # 8 - 10
]

if not os.path.exists( dmfp.pp1_train_data_path ):
    train_data=[]
    verbose = 1
    for file in sd.train_0707:
        data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
        train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,4,6,7,8,9], 10, verbose)
    for file in sd.train_0715:
        data_csv = pd.read_csv( file, header=None , sep='\t', usecols=[0,1,2,3,4,5,6,7,8,9,10])
        train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,4,6,7,8,9], 10, verbose)
    for file in sd.train_0720:
        data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
        train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,4,6,7,8,9], 10, verbose)
    for file in sd.train_0721:
        data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
        train_data = ppf.process_source_file(data_csv, train_data, file, [0,1,2,4,6,7,8,9], 10, verbose)
    dmcsv.write_list2_into_csv(train_data, train_col_name, dmfp.pp1_train_data_path, verbose)

if not os.path.exists( dmfp.pp1_test_data_path ):
    test_data=[]
    verbose = 1
    for file in sd.test_0722:
        data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
        test_data = ppf.process_source_file(data_csv, test_data, file, [0,1,2,4,6,7,8,9], 10, verbose)
    dmcsv.write_list2_into_csv(test_data, train_col_name, dmfp.pp1_test_data_path, verbose)
