import functools

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
