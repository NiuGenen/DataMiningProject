def process_file_data(csv, file_data, filename, key_col, verbose):
    file_value = dict()
    if file_data.__contains__(filename):
        return
    for item in csv.values:
        key = item[ key_col ]
        if file_value.__contains__(key):
            vs = file_value[key]
            vs.append(item)
            file_value[key] = vs
        else:
            vs = [[]]
            vs[0] = item
            file_value[key] = vs
    file_data[ filename ] = file_value
    if verbose is 1:
        print("-- file data in " + filename + " --")
        for k in file_value.keys():
            print("Key = " + k)
            print("Value = ")
            print(file_value[k])

def transfor_format(data, data_column, data_nr, predict_column, predict_nr, res):
    if data_nr <= 0:
        return
    # data_nr >= 1
    data_len = data.__len__()
    data_col_nr = data_column.__len__()
    pr_col_nr  = predict_column.__len__()
    v = [] # store input data
    p = [] # store output data
    res_item = [] # store v[] and p[]
    i = 0
    i_end = data_len - 1
    while i <= i_end - (data_nr - 1) - predict_nr :
        data_idx = i # suppose i = 0, data_nr = 3, predict_nr = 3, shoule be [0][1][2] -> [3][4][5]
        data_idx_end = i + data_nr - 1 # 0 + 3 - 1 = 2 : [0][1][2]
        pr_idx = i + data_nr # 3
        pr_idx_end = i + data_nr + predict_nr - 1 # 0 + 3 + 3 - 1 = 5 : [3][4][5]
        # get v[] as input data
        # combine with @data_nr items's value indexed by @data_column[]
        while data_idx <= data_idx_end:
            col_idx = 0
            while col_idx < data_col_nr:
                v.append( data[ data_idx ][ data_column[col_idx]] )
                col_idx += 1
            data_idx += 1
        # get p[] as output data
        # combine with @predict_nr item's value indexed by @predict_column[]
        while pr_idx <= pr_idx_end:
            col_idx = 0
            while col_idx < pr_col_nr:
                p.append( data[ pr_idx ][ predict_column[col_idx]] )
                col_idx += 1
            pr_idx += 1
        # we have one v[] and p[]
        res_item.append( v )
        res_item.append( p )
        res.append( res_item )
        # reset them
        res_item = []
        p = []
        v = []
        i += 1
