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

files = os.listdir( dmfp.training_modules_floder_path )
clfs = [None, None, None, None, None, None]
for file in files:
    if file.__contains__("DS_Store"):
        continue
    words = file.split('.') # [0] modulename [1] predict_id [2] suffix
    # load module
    clf_file = os.path.join( dmfp.training_modules_floder_path, file )
    fd = open( clf_file, "rb")
    clfs[ int(words[1]) ] = pickle.load( fd )
    fd.close()

# read prediction data
testcsv = pd.read_csv( dmfp.pp4_format_test_without_label_path, sep=',' )

all_start_times = funs.time_enumrate()

if_train_with_predict_result = 1

for start_time in all_start_times:
    print("Start Time " + str(start_time) )

    res_name = files[0][0:files[0].__len__()-".0.module".__len__()] + "." + str(start_time) + ".res"
    res_path = os.path.join(dmfp.prediction_result_floder_path, res_name )
    if os.path.exists( res_path ):
        continue

    test_data = []
    test_data_linkid = []
    test_data_linkid_tag = []
    for item in testcsv.values:
        if abs( item[1] - start_time) < 2:
            list_item = []
            for i in range(0,item.__len__()):
                list_item.append( item[i])
            test_data.append( list_item )
            test_data_linkid.append( linkid_tcid[item[3]] )
            test_data_linkid_tag.append( item[3] )
    if test_data.__len__() == 0:
        print("No Data when start_time is " + str(start_time) )
        continue

    #pred_label = clf.predict( test_data )
    #col_nr = pred_label.shape[1]
    pred_label = []
    pred_label_cols = [None, None, None, None, None, None]
    for idx in range(0,6):
        res = clfs[idx].predict(test_data)
        pred_label_cols[idx] = res
        if if_train_with_predict_result is 1:
            for j in range(0,test_data.__len__()):
                test_data.__getitem__(j).append( res[j] )
    for idx in range(0,pred_label_cols[0].__len__()):
        item = []
        for j in range(0,6):
            labels = pred_label_cols[j]
            item.append( labels[idx] )
        pred_label.append( item )

    col_nr = 6
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
