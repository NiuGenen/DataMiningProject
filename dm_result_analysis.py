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

dmc.check_file_and_pause( dmfp.pp4_format_test_path )

verbose = 1

files = os.listdir( sd.source_data_dir )
res_name = None
res_path = None
res_time = 0
flag_found_one = 0
for file in files:
    if not file.__contains__(".res"):
        continue
    if flag_found_one == 0:
        flag_found_one = 1
        res_name = file
        res_path = os.path.join(sd.source_data_dir, file)
        res_time = os.path.getmtime( res_path )
    else:
        new_res_path = os.path.join(sd.source_data_dir, file)
        new_res_time = os.path.getmtime( new_res_path )
        if new_res_time > res_time:
            res_name = file
            res_time = new_res_time
            res_path = new_res_path

rescsv = pd.read_csv(res_path , sep=',')
lavelcsv = pd.read_csv( dmfp.pp4_format_test_path , sep=',')

item_nr = rescsv.values.__len__()
elem_nr = rescsv.size

item_right = 0
elem_right = 0

item_right_without_unknown = 0
elem_right_without_unknown = 0

i = 0
while i < item_nr:
    res   = rescsv.values[i]
    label = lavelcsv.values[i]
    label_len = label.__len__()
    label = label[ label_len - 6 : label_len ]
    flag_item = 1
    flag_item_without_unknown = 1
    k = 0
    while k < res.__len__():
        # considering unknown
        if res[k] == label[k]:
            elem_right += 1
        else:
            flag_item = 0
        # ignoring unknown
        if res[k] == label[k] or label[k] == -1:
            elem_right_without_unknown += 1
        else:
            flag_item_without_unknown = 0
        k += 1
    item_right += flag_item
    item_right_without_unknown += flag_item_without_unknown
    i += 1

print("Item Nr : " + str(item_nr))
print("Elem Nr : " + str(elem_nr))

print("Item Right : " + str(item_right) + " ; % = " + str(item_right / item_nr))
print("Elem Right : " + str(elem_right) + " ; % = " + str(elem_right / elem_nr))

print("Item Right Wirhout Unknown : " + str(item_right_without_unknown) + " ; % = " + str(item_right_without_unknown / item_nr))
print("Elem Right Wirhout Unknown : " + str(elem_right_without_unknown) + " ; % = " + str(elem_right_without_unknown / elem_nr))
