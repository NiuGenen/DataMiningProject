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
