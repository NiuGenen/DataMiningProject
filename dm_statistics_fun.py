import dm_common as dmcn

# return dict() file_count
# key : filename
# value : [line_nr, column_nr, total_nr, unknown_nr, unknown_percentage]
def unknown_count_by_file(datacsv, filename, uc_file, verbose):
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
    if verbose >= 1:
        print("[" + filename + " ]" + " Line nr = " + str(line_nr) + "; column nr = " + str(column_nr) + "; Total nr   = " + str(total_nr) + "; Unknown nr = " + str(unknown_nr) +  ";Unknown%  = " + str(percentage) + "%" )
    uc_file[filename] = [line_nr, column_nr, total_nr, unknown_nr, percentage]

# return dict()
# key : linkid
# value : the number of unknown items of this linkid
def unknown_count_by_linkid(datacsv, uc_linkid):
    data_size=datacsv.shape
    data_value=datacsv.values
    line_nr=data_size[0]
    l = 0
    while l < line_nr:
        linkid = data_value[l][4]
        if data_value[l][10]=="UNKNOWN_CONGESTION_LEVEL":
            if uc_linkid.__contains__(linkid):
                uc_linkid[linkid] = uc_linkid[linkid] + 1
            else:
                uc_linkid[linkid] = 1
        else:
            if not uc_linkid.__contains__(linkid):
                uc_linkid[linkid] = 0
        l += 1

# input dict() uc_linkid
# key   :  linkid
# value :  the number of unknown items of this linkid
#
# Return dict() sc_cnt and dict() sc_per
# sc_cnt key   : unknown percentage
# sc_cnt value : the number of linkid whose unknown percentage is the key
# sc_per key   : unknown percentage range of one linkid
# sc_per value : the number of linkid whose unknown percentage is in that range
def unknown_count_percentage(uc_linkid, verbose, upc, uprc):
    # record the linkid
    upc_s_linkid = dict()
    uprc_s_linkid = dict()
    # number to percentage
    #
    # linkid : linkid
    # count : number of unknown data
    #
    for (linkid,count) in uc_linkid.items():
        # transform into percentage
        count = count / ( 72 * 4 * 4 )
        uc_linkid[linkid] = count
        # count the number of a specific percentage
        if upc.__contains__(count):
            upc[count] += 1
        else:
            upc[count] = 1
        # store its linkid
        if upc_s_linkid.__contains__(count):
            upc_s_linkid[count].append(linkid)
        else:
            upc_s_linkid[count]=[]
            upc_s_linkid[count].append(linkid)
    # count the percentage range
    per=[10,20,30,40,50,60,70,80,90,100]
    for p in per:
        # linkid : percentage
        # count : the number of this percentage
        for (linkid,count) in upc.items():
            if linkid <= p/100 and linkid > p/100 - 0.1:
                # count the range
                if uprc.__contains__(p):
                    uprc[p] += count
                else:
                    uprc[p] = count
                # store its linkid
                if uprc_s_linkid.__contains__(p):
                    for linkid in upc_s_linkid[linkid]:
                        uprc_s_linkid[p].append(linkid)
                else:
                    uprc_s_linkid[p]=[]
                    for linkid in upc_s_linkid[linkid]:
                        uprc_s_linkid[p].append(linkid)
    if verbose >= 1:
        print("Unknown Linkid Total nr      : " + str(uc_linkid.__len__()))
        for (linkid,count) in uprc.items():
            print("Unknown Percentage = " + str(linkid-10) + "% - " + str(linkid) +"% ; Count = " + str(count) )
            dmcn.print_list( uprc_s_linkid[linkid] , 3)
            print("----------------------------")

#
# return dict()
#    key   : col_value
#    value : count
def column_count(col_6_cnt, col_7_cnt, col_8_cnt, col_9_cnt, datacsv):
    for item in datacsv.values:
        dmcn.add_into_dict(col_6_cnt, item[6], 1, "+", 1) # travel time
        dmcn.add_into_dict(col_7_cnt, item[7], 1, "+", 1) # volumn
        dmcn.add_into_dict(col_8_cnt, item[8], 1, "+", 1) # speed
        dmcn.add_into_dict(col_9_cnt, item[9], 1, "+", 1) # occurpancy

def column_range_percentage(col_cnt, v_rng, col_pr):
    v_rng_nr = v_rng.__len__()
    i = 0
    while i < v_rng_nr - 1:
        lo = v_rng[i]
        hi = v_rng[i+1]
        for (k,v) in col_cnt.items():
            if lo <= k and k < hi:
                dmcn.add_into_dict(col_pr, hi, v, "+", v)
        i += 1