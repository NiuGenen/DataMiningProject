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
    'data',             # 0
    'time',             # 1
    'direction',        # 2
    'linkid',           # 3
    'travel_time',      # 4
    'volumn',           # 5
    'speed',            # 6
    'occupancy',        # 7
    'congestion_level'  # 8
]

def not_in_same_day(item, day_cols):
    day = item[ day_cols[0] ]
    for col in day_cols:
        if day != item[col]:
            return True
    return False

train_files = os.listdir( dmfp.pp3_train_data_folder )
format_data_cols = [0,1,2,3,4,5,6,7]
format_data_nr   = 6
format_label_col = 8
format_label_nr  = 6
for file in train_files:
    path = os.path.join( dmfp.pp3_train_data_folder, file)
    print("Formating " + path)
    # read one linkid's csv
    csv = pd.read_csv( path, sep=',')
    # format data
    linkid_format_data = ppf.pp4_format( csv, format_data_cols, format_data_nr, format_label_col,format_label_nr )
    linkid_format_data = ppf.pp4_clear_format_data( linkid_format_data, not_in_same_day, [0,8,16,24,32,40])
    # store into csv
    linkid = file[0:file.__len__() - 4]
    format_file_name = linkid + "_format.csv"
    format_file_path = os.path.join( dmfp.pp3_train_data_folder, format_file_name)
    col_name = ppf.pp4_format_col_name( train_col_name,format_data_cols, format_data_nr, format_label_col,format_label_nr )
    dmcsv.write_list2_into_csv( linkid_format_data, col_name, format_file_path, 1)
