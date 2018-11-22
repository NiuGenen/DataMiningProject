import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc

dmc.check_file_and_pause( dmfp.pp1_train_data_path )
dmc.check_file_and_pause( dmfp.pp1_test_data_path )

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

print("Reading csv file......")
traincsv = pd.read_csv( dmfp.pp1_train_data_path, sep=',')
testcsv = pd.read_csv( dmfp.pp1_test_data_path, sep=',')

print("Taging direction...")
direction_value = []
direction_tag = []
direction_type_nr = ppf.pp2_taging(traincsv, train_col_name[ direction_col], direction_value, direction_tag)

print("Taging linkid...")
linkid_value = []
linkid_tag = []
linkid_type_nr = ppf.pp2_taging(traincsv, train_col_name[ linkid_col], linkid_value, linkid_tag)

print("Total Type of Direction = " + str(direction_type_nr))
print("Total Type of LinkId    = " + str(linkid_type_nr))

if not os.path.exists( dmfp.pp2_direction_map_path):
    print("Generating " + dmfp.pp2_direction_map_path)
    direction_map = []
    k = 0
    while k < direction_type_nr:
        direction_map.append( [direction_value[k], direction_tag[k]] )
        k += 1
    dmcsv.write_list2_into_csv(direction_map, ['direction', 'tag'], dmfp.pp2_direction_map_path, 1)

if not os.path.exists( dmfp.pp2_linkid_map_path):
    print("Generating " + dmfp.pp2_linkid_map_path)
    linkid_map = []
    k = 0
    while k < linkid_type_nr:
        linkid_map.append( [linkid_value[k], linkid_tag[k]] )
        k += 1
    dmcsv.write_list2_into_csv(linkid_map, ['linkid','tag'], dmfp.pp2_linkid_map_path, 1)

direction_dict = dict()
k = 0
while k < direction_type_nr:
    direction_dict[ direction_value[k] ] = direction_tag[k]
    k += 1

linkid_dict = dict()
k = 0
while k < linkid_type_nr:
    linkid_dict[ linkid_value[k] ] = linkid_tag[k]
    k += 1

if not os.path.exists( dmfp.pp2_train_data_path):
    print("Generating " + dmfp.pp2_train_data_path)
    new_train_data = []
    for item in traincsv.values:
        item[ direction_col ] = direction_dict[ item[ direction_col ] ]
        item[ linkid_col ] = linkid_dict[ item[ linkid_col ] ]
        new_train_data.append( item )
    dmcsv.write_list2_into_csv(new_train_data, train_col_name, dmfp.pp2_train_data_path , 1)

if not os.path.exists( dmfp.pp2_test_data_path):
    print("Generating " + dmfp.pp2_test_data_path)
    new_test_data = []
    for item in testcsv.values:
        item[ direction_col ] = direction_dict[ item[ direction_col ] ]
        item[ linkid_col ] = linkid_dict[ item[ linkid_col ] ]
        new_test_data.append( item )
    dmcsv.write_list2_into_csv(new_test_data, train_col_name, dmfp.pp2_test_data_path, 1)

