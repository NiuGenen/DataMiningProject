import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc

dmc.check_file_and_pause( dmfp.pp4_format_test_path )

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

res_files = os.listdir( dmfp.prediction_result_floder_path)
res_files = sorted(res_files)
res_all = []
for file in res_files:
    print("Result File : " + file )

    res_path = os.path.join( dmfp.prediction_result_floder_path, file)

    rescsv = pd.read_csv(res_path , sep=',')
    labelcsv = pd.read_csv( dmfp.pp4_format_test_path , sep=',')

    start_time = int( file.split('.')[2] )

    item_nr = 0
    elem_nr = 0

    item_right = 0
    elem_right = 0

    item_right_without_unknown = 0
    elem_right_without_unknown = 0

    res_item = []

    i = 0
    l = 0
    while i < rescsv.values.__len__():
        label = None
        while l < labelcsv.values.__len__():
            label = labelcsv.values[l]
            if abs( label[1] - start_time) > 2:
                l += 1
                continue
            else:
                l += 1
                break

        res   = rescsv.values[i]
        label_len = label.__len__()
        label = label[ label_len - 6 : label_len ]

        item_nr += 1
        elem_nr += res.__len__()

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