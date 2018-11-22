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

dmc.check_file_and_pause( dmfp.pp4_format_test_without_label_path )

verbose = 1

files = os.listdir( sd.source_data_dir )
module_name = None
module_path = None
module_time = 0
flag_found_one = 0
for file in files:
    if not file.__contains__("module"):
        continue
    if flag_found_one == 0:
        flag_found_one = 1
        module_name = file
        module_path = os.path.join(sd.source_data_dir, file)
        module_time = os.path.getmtime( module_path )
    else:
        new_module_path = os.path.join(sd.source_data_dir, file)
        new_module_time = os.path.getmtime( new_module_path )
        if new_module_time > module_time:
            module_name = file
            module_time = new_module_time
            module_path = new_module_path

if flag_found_one == 0:
    dmc.pause_msg("Cannot file module file")
else:
    print("Find Module : " + module_path)

# load module
clf_file = os.path.join( module_path )
fd = open( clf_file, "rb")
clf = pickle.load( fd )
fd.close()

# read prediction data
testcsv = pd.read_csv( dmfp.pp4_format_test_without_label_path, sep=',' )
pred_label = clf.predict( testcsv.values )
col_nr = pred_label.shape[1]
col_name = []
for i in range(0,col_nr):
    col_name.append("predict" + str(i) )

res_path = os.path.join(sd.source_data_dir, module_name + ".res")
dmcsv.write_list2_into_csv( pred_label, col_name, res_path, verbose)