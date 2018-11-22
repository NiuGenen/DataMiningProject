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
dmc.check_file_and_pause( dmfp.pp2_direction_map_path )
dmc.check_file_and_pause( dmfp.pp2_linkid_map_path )

train_col_name=[
    'day',             # 0
    'time',             # 1
    'direction',        # 2
    'linkid',           # 3
    'travel_time',      # 4
    'volumn',           # 5
    'speed',            # 6
    'occupancy',        # 7
    'congestion_level'  # 8
]

direction_col = 2
linkid_col = 3

direction_map_csv = pd.read_csv( dmfp.pp2_direction_map_path, sep=',')
direction_dict = ppf.pp2_read_dict_csv( direction_map_csv )

linkid_map_csv = pd.read_csv( dmfp.pp2_linkid_map_path, sep=',')
linkid_dict = ppf.pp2_read_dict_csv( linkid_map_csv )

uprcsv = pd.read_csv( dmfp.sta_unknown_percentage_path, sep=',')
# cloumn[0] : linkid
# column[1] : unknown percentage
linkid_upr = ppf.pp2_read_dict_csv( uprcsv )

# processing unknown data in training data
traincsv = pd.read_csv( dmfp.pp2_train_data_path, sep=',')
print("Processing training data : " + dmfp.pp2_train_data_path )
for linkid in linkid_upr.keys():
    # remove linkid with too much unknown data
    upr = linkid_upr[ linkid ]
    if upr > 0.5:
        print("Abandon [" + linkid + "]")
        continue
    # get linkid's tag
    linkid_tag = linkid_dict[ linkid ]
    # get all this linkid's data
    linkid_data = []
    for item in traincsv.values:
        if item[ linkid_col ] == linkid_tag:
            linkid_data.append(item)
    # process unknown data on this linkid
    if upr > 0:
        print("Clean [" + linkid + "]")
        ppf.pp3_process_linkid_unknown( linkid_data )
    # store data
    print("Store [" + linkid + "]")
    dmcsv.write_list2_into_csv(linkid_data, train_col_name, os.path.join(dmfp.pp3_train_data_folder, linkid+".csv"), 1)

# processing unknown data in training data
testcsv = pd.read_csv( dmfp.pp2_test_data_path, sep=',')
print("Processing test data : " + dmfp.pp2_test_data_path )
for linkid in linkid_upr.keys():
    # get linkid's tag
    linkid_tag = linkid_dict[ linkid ]
    # get all this linkid's data
    linkid_data = []
    for item in testcsv.values:
        if item[ linkid_col ] == linkid_tag:
            linkid_data.append(item)
    # store into new train data
    print("Store [" + linkid + "]")
    dmcsv.write_list2_into_csv(linkid_data, train_col_name, os.path.join(dmfp.pp3_test_data_folder, linkid+".csv"), 1)
