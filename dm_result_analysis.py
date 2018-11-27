import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc

verbose = 1

res_col = [
    'start_time',
    'item_nr',
    'elem_nr',
    'item_right',
    'item_right_percentage',
    'elem_right',
    'elem_right_percentage',
    'item_right_without_unknown',
    'item_right_without_unknown_percentage',
    'elem_right_without_unknown',
    'elem_right_without_knonown_percentage'
]

label_files = os.listdir( dmfp.result_real_label_floder_path )

res_files = os.listdir( dmfp.prediction_result_floder_path)
res_files = sorted(res_files)
res_all = []
for file in res_files:
    if file[0] == '.':
        continue
    start_time = int( file.split('.')[2] )

    res_path = os.path.join( dmfp.prediction_result_floder_path, file)
    print("Result File : " + res_path )
    rescsv = pd.read_csv(res_path , sep=',')

    label_file = ""
    for f in label_files:
        if f.__contains__("." + str(start_time) + "."):
            label_file = f
            break
    label_path = os.path.join( dmfp.result_real_label_floder_path, label_file)
    print("Label File : " + label_path)
    labelcsv = pd.read_csv( label_path, sep=',')
    # [3] is linkid_tag
    label_data = dict()
    for item in labelcsv.values:
        item_label = item[ item.__len__() - 6 : item.__len__() ]
        label_data[ item[3] ] = item_label

    item_nr = 0
    elem_nr = 0

    item_right = 0
    elem_right = 0

    item_right_without_unknown = 0
    elem_right_without_unknown = 0

    res_item = []

    i = 0
    while i < rescsv.values.__len__():
        res   = rescsv.values[i]
        label = label_data[ res[1] ]

        item_nr += 1
        elem_nr += res.__len__() - 2

        flag_item = 1
        flag_item_without_unknown = 1

        k = 2
        while k < res.__len__():
            # considering unknown
            if res[k] == label[k - 2]:
                elem_right += 1
            else:
                flag_item = 0
            # ignoring unknown
            if res[k] == label[k - 2] or label[k - 2] == -1:
                elem_right_without_unknown += 1
            else:
                flag_item_without_unknown = 0
            k += 1
        item_right += flag_item
        item_right_without_unknown += flag_item_without_unknown
        i += 1

    res_item.append( start_time)

    res_item.append( item_nr )
    res_item.append( elem_nr )

    res_item.append( item_right )
    res_item.append( item_right / item_nr )
    res_item.append( elem_right )
    res_item.append( elem_right / elem_nr )

    res_item.append( item_right_without_unknown )
    res_item.append( item_right_without_unknown / item_nr )
    res_item.append( elem_right_without_unknown )
    res_item.append( elem_right_without_unknown / elem_nr )

    print( res_item )

    res_all.append(res_item)

dmcsv.write_list2_into_csv(res_all, res_col, dmfp.result_analysis_path , verbose)