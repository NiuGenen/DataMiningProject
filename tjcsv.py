import pandas as pd
import tjfilepath as tjf

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
