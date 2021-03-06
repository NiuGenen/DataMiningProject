import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import pickle
import dm_prediction_func as funs

dmc.check_file_and_pause( dmfp.pp4_format_test_without_label_path )
dmc.check_file_and_pause( dmfp.pp2_linkid_map_path )

linkid_map_csv = pd.read_csv( dmfp.pp2_linkid_map_path, sep=',')
linkid_tcid = ppf.pp2_read_tcid_csv( linkid_map_csv )

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
    dmc.pause_msg("Cannot find module file")
else:
    print("Find Module : " + module_path)

# load module
clf_file = os.path.join( module_path )
fd = open( clf_file, "rb")
clf = pickle.load( fd )
fd.close()

# read prediction data
testcsv = pd.read_csv( dmfp.pp4_format_test_without_label_path, sep=',' )

all_start_times = funs.time_enumrate()


for start_time in all_start_times:
    print("Start Time " + str(start_time) )

    res_name = module_name[0:module_name.__len__()-".module".__len__()] + "." + str(start_time) + ".res"
    res_path = os.path.join(dmfp.prediction_result_floder_path, res_name )
    if os.path.exists( res_path ):
        continue

    test_data = []
    test_data_linkid = []
    test_data_linkid_tag = []
    for item in testcsv.values:
        if abs( item[1] - start_time) < 2:
            test_data.append( item )
            test_data_linkid.append( linkid_tcid[item[3]] )
            test_data_linkid_tag.append( item[3] )
    if test_data.__len__() == 0:
        print("No Data when start_time is " + str(start_time) )
        continue

    pred_label = clf.predict( test_data )
    col_nr = pred_label.shape[1]

    col_name = []
    col_name.append("linkid")
    col_name.append("linkid_tag")
    for i in range(0,col_nr):
        col_name.append("predict" + str(i) )

    csv_data = []
    i = 0
    while i < test_data_linkid.__len__():
        csv_item = []
        csv_item.append( test_data_linkid[i] )
        csv_item.append( test_data_linkid_tag[i] )
        for elem in pred_label[i]:
            csv_item.append( elem )
        csv_data.append( csv_item )
        i += 1

    #dmcsv.write_list2_into_csv( pred_label, col_name, res_path, verbose)
    dmcsv.write_list2_into_csv( csv_data, col_name, res_path, verbose)
