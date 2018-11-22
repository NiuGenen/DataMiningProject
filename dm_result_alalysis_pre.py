import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import dm_prediction_func as funs

dmc.check_file_and_pause( dmfp.pp4_format_test_path )

verbose = 1

testcsv = pd.read_csv( dmfp.pp4_format_test_path, sep=',')

all_start_times = funs.time_enumrate()
for start_time in all_start_times:
    csv_name = "test_data." + str(start_time) + ".csv"
    csv_path = os.path.join(dmfp.result_real_label_floder_path, csv_name )
    if os.path.exists( csv_path ):
        continue

    item_all = []
    for item in testcsv.values:
        if abs(item[1] - start_time ) < 2:
            item_all.append( item )
    if item_all.__len__() == 0:
        print("No data when start time is " + str(start_time) )
        continue

    dmcsv.write_list2_into_csv( item_all, testcsv.columns.values, csv_path, verbose )
