import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import pickle
import dm_prediction_func as funs

dmc.check_file_and_pause( dmfp.prediction_result_floder_path )

res_files = os.listdir( dmfp.prediction_result_floder_path )
res_files = sorted(res_files)

for file in res_files:
    if file[0] == '.':
        continue
    start_time = int( file.split('.')[2] )

    csv = pd.read_csv( os.path.join(dmfp.prediction_result_floder_path ,file), sep=",")
    # [0] linkid
    # [1] linkid's tag
    # [2] predicted value 1
    # [3] predicted value 2
    # [4] predicted value 3
    # [5] predicted value 4
    # [6] predicted value 5
    # [7] predicted value 6

    new_file_name = file + ".final.txt"
    new_file_path = os.path.join( dmfp.final_result_floder_path, new_file_name)
    nfd = open( new_file_path, "w")
    for item in csv.values:
        item_str = item[0] + ":"
        for i in range(2,7):
            item_str = item_str + str(int(item[i])) + ","
        item_str = item_str + str(int(item[7])) + "\r\n"
        nfd.write( item_str )
    nfd.close()

    print(new_file_path)
