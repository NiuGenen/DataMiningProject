# return dict() file_count
# key : filename
# value : [line_nr, column_nr, total_nr, unknown_nr, unknown_percentage]
def process_unknown_count(datacsv, filename, file_count, verbose):
    data_size=datacsv.shape
    data_value=datacsv.values
    line_nr=data_size[0]
    column_nr=data_size[1]
    l = 0
    unknown_nr = 0
    total_nr = 0
    while l < line_nr:
        total_nr += 1
        if data_value[l][10]=="UNKNOWN_CONGESTION_LEVEL":
            unknown_nr += 1
        l += 1
    percentage=100*unknown_nr/total_nr
    if verbose is 1:
        print("--" + filename + " --" + " Line nr = " + str(line_nr) + "; column nr = " + str(column_nr) + "; Total nr   = " + str(total_nr) + "; Unknown nr = " + str(unknown_nr) +  ";Unknown%  = " + str(percentage) + "%" )
    file_count[filename] = [line_nr, column_nr, total_nr, unknown_nr, percentage]

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

# return dict() sc
# key : linkid
# value : the number of unknown items of this linkid
def process_unknown_sc(datacsv, sc):
    data_size=datacsv.shape
    data_value=datacsv.values
    line_nr=data_size[0]
    l = 0
    while l < line_nr:
        if data_value[l][10]=="UNKNOWN_CONGESTION_LEVEL":
            linkid = data_value[l][4]
            if sc.__contains__(linkid):
                sc[linkid] = sc[linkid] + 1
            else:
                sc[linkid] = 1
        l += 1

def process_file_count(file_count, verbose):
    total_pr = 0
    cnt = 0
    for (k,v) in file_count.items():
        pr = v[v.__len__()-1]
        total_pr += pr
        cnt += 1
    avg_p = total_pr / cnt
    if verbose is 1:
        print("Avgerage Unknown Percentage = " + str(avg_p) + "%" )

# Return dict() sc_cnt and dict() sc_per
# sc_cnt key   :  unknown percentage
# sc_cnt value : the number of linkid whose unknown percentage is the key
# sc_per key   : unknown percentage range of one linkid
# sc_per value : the number of linkid whose unknown percentage is in that range
def process_sc(sc, verbose, sc_pr_cnt, sc_rng_cnt):
    for (k,v) in sc.items():
        sc[k] = v / (72 * 4 * 4)
    sortsc=sorted(sc.values())
    for i in sortsc:
        if sc_pr_cnt.__contains__(i):
            sc_pr_cnt[i] += 1
        else:
            sc_pr_cnt[i] = 1
    per=[10,20,30,40,50,60,70,80,90,100]
    for p in per:
        for (k,v) in sc_pr_cnt.items():
            if k <= p/100 and k > p/100 - 0.1:
                if sc_rng_cnt.__contains__(p):
                    sc_rng_cnt[p] += v
                else:
                    sc_rng_cnt[p] = v
    if verbose is 1:
        print("Unknown Total nr      : " + str(sortsc.__len__()))
        print("Unknown Less Than 10% : " + str(sc_rng_cnt[10])  )
        print("Unknown More Than 90% : " + str(sc_rng_cnt[100])  )
        for (k,v) in sc_rng_cnt.items():
            print("Unknown Percentage = " + str(k-10) + "% - " + str(k) +"% ; Count = " + str(v) )

def add_into_dict(_dict, _k, _v, op, init_value):
    if op is "+":
        if _dict.__contains__(_k):
            _dict[_k] += _v
        else:
            _dict[_k] = init_value

def process_column_count(col_6_cnt, col_7_cnt, col_8_cnt, col_9_cnt, datacsv):
    for item in datacsv.values:
        col6 = item[6] # travel time
        add_into_dict(col_6_cnt, col6, 1, "+", 1)
        col7 = item[7] # volumn
        add_into_dict(col_7_cnt, col7, 1, "+", 1)
        col8 = item[8] # speed
        add_into_dict(col_8_cnt, col8, 1, "+", 1)
        col9 = item[9] # occurpancy
        add_into_dict(col_9_cnt, col9, 1, "+", 1)

def process_column_range_percentage(col_cnt, v_rng, col_pr):
    v_rng_nr = v_rng.__len__()
    i = 0
    while i < v_rng_nr - 1:
        lo = v_rng[i]
        hi = v_rng[i+1]
        for (k,v) in col_cnt.items():
            if lo <= k and k < hi:
                add_into_dict(col_pr, hi, v, "+", v)
        i += 1

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
