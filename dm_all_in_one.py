import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import pickle
import dm_prediction_func as funs

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

all_test_data=[]
verbose = 1
for file in sd.test_0722:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    for item in data_csv.values:
        item_new=[]
        for itm in item:
            item_new.append( itm )
        all_test_data.append( item_new )

# dmc.check_file_and_pause( dmfp.pp1_test_data_path )
# print("read origin test all data " + dmfp.pp1_test_data_path)
# origin_test_data_csv=pd.read_csv( dmfp.pp1_test_data_path, sep=",")

print("get half hour data from 0 to 25 ...")
#half_hour=[0,5,10,15,20,25]
half_hour=[1200,1205,1210,1215,1220,1225]
half_hour_data=[]
#for item in origin_test_data_csv.values:
for item in all_test_data:
    item_new=[]
    append_flag=0
    for t in half_hour:
        if abs( item[1] - t ) < 2:
            append_flag = 1
    if append_flag == 1:
        for itm in item:
            item_new.append( itm)
        half_hour_data.append( item_new )
dmcsv.write_list2_into_csv(half_hour_data, txt_col_name, dmfp.all_in_one_file_path_old, 1)





train_col_name=[
    'day',              # 0 <- 0
    'time',             # 1 <- 1
    'direction',        # 2 <- 2
    'linkid',           # 3 <- 4
    'travel_time',      # 4 <- 6
    'volumn',           # 5 <- 7
    'speed',            # 6 <- 8
    'occupancy',        # 7 <- 9
    'congestion_level'  # 8 <- 10
]

col_idx=[0,1,2,4,6,7,8,9,10]

dmc.check_file_and_pause( dmfp.pp2_linkid_map_path )
dmc.check_file_and_pause( dmfp.pp2_direction_map_path )

print("reading linkid map" + dmfp.pp2_linkid_map_path )
linkid_map_csv = pd.read_csv( dmfp.pp2_linkid_map_path, sep=',')
linkid_tcid = ppf.pp2_read_tcid_csv( linkid_map_csv )
linkid_dict = ppf.pp2_read_dict_csv( linkid_map_csv )

print("reading dirction map" + dmfp.pp2_direction_map_path )
direction_map_csv = pd.read_csv( dmfp.pp2_direction_map_path, sep=',')
direction_tcid = ppf.pp2_read_tcid_csv( direction_map_csv )
direction_dict = ppf.pp2_read_dict_csv( direction_map_csv )

dmc.check_file_and_pause( dmfp.all_in_one_file_path_old )

half_hour_data_old_csv=pd.read_csv(dmfp.all_in_one_file_path_old, sep=",")
half_hour_data_new = []
for item in half_hour_data_old_csv.values:
    item_new=[]
    item_new.append(item[0]) # day
    item_new.append(item[1]) # time
    item_new.append(direction_dict[item[2]]) # direction
    item_new.append(linkid_dict[item[4]]) # linkid
    item_new.append(item[6]) # travel_time
    item_new.append(item[7]) # volumn
    item_new.append(item[8]) # speed
    item_new.append(item[9]) # occupancy
    item_new.append(ppf.cvt_targ(item[10])) # congestion_level
    half_hour_data_new.append( item_new )
dmcsv.write_list2_into_csv(half_hour_data_new, train_col_name, dmfp.all_in_one_file_path_new, 1)






data_cols = [0,1,2,3,4,5,6,7]
data_nr   = 6
label_col = 8
label_nr  = 6

format_col_name  = ppf.pp4_format_col_name( train_col_name, data_cols, data_nr, label_col, label_nr )
format_data = []

print("formating data into " + dmfp.all_in_one_file_name_format)
new_csv=pd.read_csv( dmfp.all_in_one_file_path_new, sep=",")
for linkid_num in linkid_tcid.keys():
    linkid_data=[]
    for item in new_csv.values:
        item_linkid=[]
        if item[3] == linkid_num:
            for itm in item:
                item_linkid.append( itm )
            linkid_data.append(item_linkid)
    sorted(linkid_data)
    format_data_item=[]
    for t in half_hour:
        item=None
        for itm in linkid_data:
            if abs(itm[1] - t) < 2:
                item=itm
                break
        for idx in data_cols:
            format_data_item.append(item[idx])
    format_data.append( format_data_item )
dmcsv.write_list2_into_csv(format_data, format_col_name, dmfp.all_in_one_file_path_format, 1)




training_module_config="best3"
module_path = os.path.join(sd.source_data_dir, dmfp.training_module_name + "." + training_module_config + dmfp.training_module_suffix)
dmc.check_file_and_pause(module_path)

print("reading module " + module_path)
clf_file = os.path.join( module_path )
fd = open( clf_file, "rb")
clf = pickle.load( fd )
fd.close()

print("reading formated data " + dmfp.all_in_one_file_path_format)
format_data_csv = pd.read_csv( dmfp.all_in_one_file_path_format, sep=",")
format_data = format_data_csv.values
format_labels = clf.predict( format_data )
i=0
while i < 855:
    item = format_data[i]
    labels=format_labels[i]
    linkid = linkid_tcid[ item[3] ]
    i += 1
    print( linkid + ":" + str(int(labels[0])) + ","+ str(int(labels[1])) + ","+ str(int(labels[2])) + ","+ str(int(labels[3])) + ","+ str(int(labels[4])) + ","+ str(int(labels[5])) + ",")