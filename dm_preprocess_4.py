import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc

dmc.check_file_and_pause( dmfp.pp3_train_data_folder )
dmc.check_file_and_pause( dmfp.pp3_test_data_folder )

dmc.check_file_and_pause( dmfp.pp2_linkid_map_path )
linkid_map_csv = pd.read_csv( dmfp.pp2_linkid_map_path, sep=',')
linkid_dict = ppf.pp2_read_dict_csv( linkid_map_csv )

train_col_name=[
    'day',              # 0
    'time',             # 1
    'direction',        # 2
    'linkid',           # 3
    'travel_time',      # 4
    'volumn',           # 5
    'speed',            # 6
    'occupancy',        # 7
    'congestion_level'  # 8
]

format_data_cols = [0,1,2,3,4,5,6,7]
format_data_nr   = 6
format_label_col = 8
format_label_nr  = 6
format_col_name  = ppf.pp4_format_col_name( train_col_name,format_data_cols, format_data_nr, format_label_col,format_label_nr )

if_format_train = 0
if_format_test  = 0
if_format_test_without_label = 0
if_combine_train = 0
if_combine_test  = 0
if_combine_test_without_label  = 0

verbose = 1

def not_in_same_day(item, day_cols):
    day = item[ day_cols[0] ]
    for col in day_cols:
        if day != item[col]:
            return True
    return False

if if_format_train == 1:
    print(" === format train data === ")
    train_files = os.listdir( dmfp.pp3_train_data_folder )
    for file in train_files:
        if file.__contains__("format"):
            continue
        path = os.path.join( dmfp.pp3_train_data_folder, file)
        # read one linkid's csv
        csv = pd.read_csv( path, sep=',')
        # format data
        linkid_format_data = ppf.pp4_format( csv, format_data_cols, format_data_nr, format_label_col,format_label_nr )
        linkid_format_data = ppf.pp4_clear_format_data( linkid_format_data, not_in_same_day, [0,8,16,24,32,40])
        # store into csv
        linkid = file[0:file.__len__() - 4]
        format_file_name = linkid + "_format.csv"
        format_file_path = os.path.join( dmfp.pp3_train_data_folder, format_file_name)
        dmcsv.write_list2_into_csv( linkid_format_data, format_col_name, format_file_path, verbose)

if if_format_test == 1:
    print(" === format test data === ")
    test_files = os.listdir( dmfp.pp3_test_data_folder )
    for file in test_files:
        if file.__contains__("format"):
            continue
        path = os.path.join( dmfp.pp3_test_data_folder, file)
        # 1. read ont link's csv
        csv = pd.read_csv( path, sep=',')
        # 2. format with label
        linkid_format_data = ppf.pp4_format( csv, format_data_cols, format_data_nr, format_label_col,format_label_nr )
        linkid_format_data = ppf.pp4_clear_format_data( linkid_format_data, not_in_same_day, [0,8,16,24,32,40])
        # 3. store into csv
        linkid = file[0:file.__len__() - 4]
        format_file_name = linkid + "_format.csv"
        format_file_path = os.path.join( dmfp.pp3_test_data_folder, format_file_name)
        dmcsv.write_list2_into_csv( linkid_format_data, format_col_name, format_file_path, verbose)

if if_format_test_without_label == 1:
    print(" === format test data without label ===")
    test_files = os.listdir( dmfp.pp3_test_data_folder )
    for file in test_files:
        if not file.__contains__("format"):
            continue
        path = os.path.join( dmfp.pp3_test_data_folder, file)
        # 1. read formated csv
        csv = pd.read_csv( path, sep=',')
        # 2. remove label
        label_i_s = format_data_cols.__len__() * format_data_nr
        label_i_e = label_i_s + format_label_nr - 1
        for i in range(label_i_s, label_i_e + 1):
            label_col_name = format_col_name[i]
            del csv[ label_col_name ]
        # 3. stroe
        linkid = file[0:file.__len__() - 4]
        without_label_file_name = linkid + "_without_label.csv"
        without_label_file_path = os.path.join( dmfp.pp3_test_data_folder, without_label_file_name)
        dmcsv.write_list2_into_csv( csv.values, format_col_name,without_label_file_path ,verbose)

if if_combine_train == 1:
    print(" === combine format train data === ")
    all_train_csv = None
    flag_train = 0
    for file in os.listdir( dmfp.pp3_train_data_folder ):
        # read format train data
        if not file.__contains__("format"):
            continue
        path = os.path.join( dmfp.pp3_train_data_folder, file)
        csv = pd.read_csv( path, sep=',')
        # combint into one csv
        if flag_train == 0:
            all_train_csv = csv
            flag_train = 1
        else:
            all_train_csv = pd.concat([all_train_csv, csv], ignore_index=True)
    # save all csv file
    dmcsv.write_list2_into_csv( all_train_csv.values, format_col_name, dmfp.pp4_format_train_path, verbose)

if if_combine_test == 1 or if_combine_test_without_label == 1:
    print(" === combine format test data === ")
    all_test_csv = None
    all_test_without_label_csv = None
    flag_test = 0
    flag_test_without_label = 0
    for file in os.listdir( dmfp.pp3_test_data_folder ):
        # read format train data
        if not file.__contains__("format"):
            continue
        path = os.path.join( dmfp.pp3_test_data_folder, file)
        csv = pd.read_csv( path, sep=',')
        # combint into one csv
        if file.__contains__("without_label"):
            if if_combine_test_without_label == 0:
                continue
            if flag_test_without_label == 0:
                all_test_without_label_csv = csv
                flag_test_without_label = 1
            else:
                all_test_without_label_csv = pd.concat([all_test_without_label_csv, csv], ignore_index=True)
        else:
            if if_combine_test == 0:
                continue
            if flag_test == 0:
                all_test_csv = csv
                flag_test = 1
            else:
                all_test_csv = pd.concat([all_test_csv, csv], ignore_index=True)
    # save all csv file
    if if_combine_test == 1:
        dmcsv.write_list2_into_csv( all_test_csv.values, format_col_name, dmfp.pp4_format_test_path, verbose)
    if if_combine_test_without_label == 1:
        dmcsv.write_list2_into_csv( all_test_without_label_csv.values, format_col_name, dmfp.pp4_format_test_without_label_path, verbose)
