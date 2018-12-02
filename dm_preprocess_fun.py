import functools
import pandas as pd

def cvt_targ( targ ):
    if targ == "UNKNOWN_CONGESTION_LEVEL":
        return -1.0
    if targ == "NON_CONGESTION":
        return 0.0
    if targ == "LIGHT_CONGESTION":
        return 1.0
    if targ == "MEDIUM_CONGESTION":
        return 2.0
    if targ == "HEAVY_CONGESTION":
        return 3.0

def process_source_file(csv, train_data, filename, data_cols, label_col, verbose ):
    if verbose >= 1:
        print("=== " + filename + " ===")
    for item in csv.values:
        train_item = []
        # get data
        for idx in data_cols:
            train_item.append( item[idx] )
        # get label
        label = item[ label_col ]
        train_item.append( cvt_targ(label) )
        # store in train_data
        train_data.append( train_item )
        if verbose >= 3:
            print( train_item )
    if verbose >= 2:
        print( train_data )
    return train_data

def pp_correlation_analysis_categorical( list2, colids, colnames):
    nr = colids.__len__()
    cols = []
    cols_dict = []
    cols_cnt = []
    for i in range(0,nr):
        cols.append( [] )
        cols_dict.append( dict() )
        cols_cnt.append( 0 )
    for item in list2:
        i = 0
        for id in colids:
            dct = cols_dict[i]
            if not dct.__contains__( item[id] ):
                dct[ item[id] ] = cols_cnt[i]
                cols_cnt[i] += 1
            cols[i].append( dct[item[id]] )
            i += 1
    pds0 = pd.Series(data=cols[0], name=colnames[0])
    for i in range(1,nr):
        pdsi = pd.Series(data=cols[i], name=colnames[i])
        pds0 = pd.concat([pds0, pdsi], axis=1)
    return pds0.corr()

def pp_correlation_analysis( list2, colids, colnames):
    nr = colids.__len__()
    cols = []
    for i in range(0,nr):
        cols.append( [] )
    for item in list2:
        i = 0
        for id in colids:
            cols[i].append( item[id] )
    pds0 = pd.Series(data=cols[0], name=colnames[0])
    for i in range(1,nr):
        pdsi = pd.Series(data=cols[i], name=colnames[i])
        pds0 = pd.concat([pds0, pdsi], axis=1)
    return pds0.corr()

def pp2_taging(csv, colname, value, tag):
    i = 0
    for d in csv[ colname ]:
        if not value.__contains__(d):
            value.append(d)
            tag.append(i)
            i += 1
    return i

def pp2_read_dict_csv(csv):
    dct = dict()
    for item in csv.values:
        dct[ item[0]] = item[1]
    return dct

def pp2_read_tcid_csv(csv):
    tcd = dict()
    for item in csv.values:
        tcd [ item[1]] = item[0]
    return tcd

def pp2_generating_dict(key, value, n):
    i = 0
    d = dict()
    while i < n:
        d[ key[i] ] = value[i]
        i += 1

def train_item_cmp( item1, item2 ):
    if item1[0] != item2[0]:
        return item1[0] > item2[0]
    else:
        return item1[1] > item2[1]

def pp3_cpy_list(s,t,cols):
    for col in cols:
        t[col] = s[col]

def pp3_process_linkid_unknown(linkid_data):
    linkid_data = sorted(linkid_data, key=functools.cmp_to_key( train_item_cmp ) )
    i = 0
    while i < linkid_data.__len__():
        if linkid_data[i].__getitem__(8) == -1:
            pp3_cpy_list( linkid_data[i-1], linkid_data[i], [4,5,6,7,8])
        i += 1

def pp4_format(csv, data_cols, data_nr, label_col, label_nr):
    format_data     = []
    format_item_in  = []
    format_item_out = []
    format_item     = []
    csv_values = csv.values
    csv_len    = csv.values.__len__()
    data_i_s  = 0
    data_i_e  = data_nr - 1
    label_i_s = data_i_e  + 1
    label_i_e = label_i_s + label_nr - 1
    while label_i_e < csv_len:
        # get the input data
        for i in range(data_i_s, data_i_e + 1):
            item = csv_values[i]
            for data_col in data_cols:
                format_item_in.append( item[data_col] )
        # get the output(label) data
        for i in range(label_i_s, label_i_e + 1):
            item = csv_values[i]
            format_item_out.append( item[label_col] )
        # construct input and output into one item
        for item_in in format_item_in:
            format_item.append( item_in )
        for item_out in format_item_out:
            format_item.append( item_out )
        # append format item in data
        format_data.append( format_item )
        # clear temp store
        format_item_in.clear()
        format_item_out.clear()
        format_item = []
        # update index
        data_i_s  += 1
        data_i_e  += 1
        label_i_s += 1
        label_i_e += 1
    return format_data

def pp4_clear_format_data(data, check_func, para):
    new_data = []
    for item in data:
        if check_func(item, para):
            continue
        new_data.append( item )
    return new_data

def pp4_format_col_name( origin_col_name, data_cols, data_nr, label_col, label_nr):
    col_name = []
    for i in range(0, data_nr):
        for col in data_cols:
            col_name.append( origin_col_name[col] + str(i) )
    for i in range(data_nr, data_nr + label_nr):
        col_name.append( origin_col_name[label_col] + str(i))
    return col_name
