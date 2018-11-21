import pandas as pd
import os
import dm_source_data as sd

def write_list2_into_csv(list2, colname, filepath, verbose):
    # init
    cols = []
    col_nr = list2[0].__len__()
    i = 0
    while i < col_nr:
        cols.append([])
        i += 1
    # construct column
    for item in list2:
        i = 0
        while i < col_nr:
            cols[i].append( item[i] )
            i += 1
    # construct pandas
    data_csv = pd.Series(cols[0], name=colname[0])
    i = 1
    while i < col_nr:
        a = pd.Series(cols[i], name=colname[i] )
        data_csv = pd.concat([data_csv,a], axis=1)
        i += 1
    # write into csv
    data_csv.to_csv( filepath, index=False, sep=',')
    if verbose >= 1:
        print("write csv : " + filepath)

# test begin
#
# d=[]
# d.append([1,2,3])
# d.append([4,5,6])
# print(d[0].__len__())
# write_list2_into_csv(d,['asd','qwe','zxc'],'asd.csv',1)
#
# test end

# k : key
# v : []
def store_dict_list_into_csv(_d, vl, filename):
    cols = [[]]
    i = 0
    while i <= vl:
        cols.append([])
        i += 1
    for (k,v) in _d.items():
        cols[0].append(k)
        i = 1
        while i <= vl:
            cols[i].append(v[i-1])
            i += 1
    data_csv = pd.Series(cols[0], name=str(0)) # construct as pandas.Series
    i = 1
    while i <= vl:
        a = pd.Series(cols[i], name=str(i))
        data_csv = pd.concat([data_csv,a], axis=1)
        i += 1
    data_csv.to_csv(filename, index=False, sep=',')

def store_dict_into_csv(_d, filename):
    cols = [[]]
    cols.append([])
    for (k,v) in _d.items():
        cols[0].append(k)
        cols[1].append(v)
    data_csv = pd.Series(cols[0], name=str(0)) # construct as pandas.Series
    a = pd.Series(cols[1], name=str(1))
    data_csv = pd.concat([data_csv,a], axis=1)
    data_csv.to_csv(filename, index=False, sep=',')