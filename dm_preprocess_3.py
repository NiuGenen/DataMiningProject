import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc

dmc.check_file_and_pause( dmfp.sta_unknown_percentage_path )
dmc.check_file_and_pause( dmfp.pp2_train_data_path )
dmc.check_file_and_pause( dmfp.pp2_test_data_path )

uprcsv = pd.read_csv( dmfp.sta_unknown_percentage_path, sep=',')
# cloumn[0] : linkid
# column[1] : unknown percentage
linkid_upr = dict()
for item in uprcsv.values:
    linkid_upr[ item[0] ] = item[1]


