# return dict() file_count
# key : filename
# value : [line_nr, column_nr, total_nr, unknown_nr, unknown_percentage]
def unknown_count(datacsv, filename, file_count, verbose):
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

# return dict() sc
# key : linkid
# value : the number of unknown items of this linkid
def process_unknown_sc(datacsv, sc):
    data_size=datacsv.shape
    data_value=datacsv.values
    line_nr=data_size[0]
    l = 0
    while l < line_nr:
        linkid = data_value[l][4]
        if data_value[l][10]=="UNKNOWN_CONGESTION_LEVEL":
            if sc.__contains__(linkid):
                sc[linkid] = sc[linkid] + 1
            else:
                sc[linkid] = 1
        else:
            if not sc.__contains__(linkid):
                sc[linkid] = 0
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

# input dict() sc
# key : linkid
# value : the number of unknown items of this linkid
#
# Return dict() sc_cnt and dict() sc_per
# sc_cnt key   :  unknown percentage
# sc_cnt value : the number of linkid whose unknown percentage is the key
# sc_per key   : unknown percentage range of one linkid
# sc_per value : the number of linkid whose unknown percentage is in that range
def process_sc(sc, verbose, sc_pr_cnt, sc_rng_cnt):
    # record the linkid
    sc_pr_linked = dict()
    sc_rng_linkid = dict()
    # number to percentage
    #
    # k : linkid
    # v : number of unknown data
    #
    for (k,v) in sc.items():
        # transform into percentage
        # sc[k] = v / (72 * 4 * 4)
        v = v / ( 72 * 4 * 4 )
        sc[k] = v
        # count the number of a specific percentage
        if sc_pr_cnt.__contains__(v):
            sc_pr_cnt[v] += 1
        else:
            sc_pr_cnt[v] = 1
        # store its linkid
        if sc_pr_linked.__contains__(v):
            sc_pr_linked[v].append(k)
        else:
            sc_pr_linked[v]=[]
            sc_pr_linked[v].append(k)
    # sort percentage
    sortsc=sorted(sc.values())
    # count the percentage range
    per=[10,20,30,40,50,60,70,80,90,100]
    for p in per:
        # k : percentage
        # v : the number of this percentage
        for (k,v) in sc_pr_cnt.items():
            if k <= p/100 and k > p/100 - 0.1:
                # count the range
                if sc_rng_cnt.__contains__(p):
                    sc_rng_cnt[p] += v
                else:
                    sc_rng_cnt[p] = v
                # store its linkid
                if sc_rng_linkid.__contains__(p):
                    for linkid in sc_pr_linked[k]:
                        sc_rng_linkid[p].append(linkid)
                else:
                    sc_rng_linkid[p]=[]
                    for linkid in sc_pr_linked[k]:
                        sc_rng_linkid[p].append(linkid)
    if verbose is 1:
        print("Unknown Total nr      : " + str(sortsc.__len__()))
        print("Unknown Less Than 10% : " + str(sc_rng_cnt[10])  )
        print("Unknown More Than 90% : " + str(sc_rng_cnt[100])  )
        for (k,v) in sc_rng_cnt.items():
            print("Unknown Percentage = " + str(k-10) + "% - " + str(k) +"% ; Count = " + str(v) )
            for linkid in sc_rng_linkid[k]:
                print(linkid)
            print("----------------------------")

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
