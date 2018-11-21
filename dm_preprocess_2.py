import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp

if not os.path.exists( dmfp.pp1_train_data_path ):
    print("Not Found File : " + dmfp.pp1_train_data_path )
    while 1:
        continue

if not os.path.exists( dmfp.pp1_test_data_path ):
    print("Not Found File : " + dmfp.pp1_test_data_path )
    while 1:
        continue

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

direction_col = 2
linkid_col = 3

print("Reading csv file......")
traincsv = pd.read_csv( dmfp.pp1_train_data_path, sep=',')
testcsv = pd.read_csv( dmfp.pp1_test_data_path, sep=',')

print("Taging direction...")
direction_value = []
direction_tag = []
i = 0
for d in traincsv['direction']:
    if not direction_value.__contains__(d):
        direction_value.append(d)
        direction_tag.append(i)
        i += 1

print("Taging linkid...")
linkid_value = []
linkid_tag = []
j = 0
for l in traincsv['linkid']:
    if not linkid_value.__contains__(l):
        linkid_value.append(l)
        linkid_tag.append(j)
        j += 1

print("Total Type of Direction = " + str(i))
print("Total Type of LinkId    = " + str(j))

if not os.path.exists( dmfp.pp2_direction_map_path):
    print("Generating " + dmfp.pp2_direction_map_path)
    direction_map = []
    k = 0
    while k < i:
        direction_map.append( [direction_value[k], direction_tag[k]] )
        k += 1
    dmcsv.write_list2_into_csv(direction_map, ['direction', 'tag'], dmfp.pp2_direction_map_path, 1)

if not os.path.exists( dmfp.pp2_linkid_map_path):
    print("Generating " + dmfp.pp2_linkid_map_path)
    linkid_map = []
    k = 0
    while k < j:
        linkid_map.append( [linkid_value[k], linkid_tag[k]] )
        k += 1
    dmcsv.write_list2_into_csv(linkid_map, ['linkid','tag'], dmfp.pp2_linkid_map_path, 1)

direction_dict = dict()
k = 0
while k < i:
    direction_dict[ direction_value[k] ] = direction_tag[k]
    k += 1

linkid_dict = dict()
k = 0
while k < j:
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

