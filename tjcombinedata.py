import pandas as pd
import tjfilepath as tjf
import os

def get_floder_csv_file(dir, prex):
    if not os.path.exists( dir ):
        return []
    csvs = []
    files = os.listdir( dir )
    for f in files:
        if f.endswith(prex + ".csv"):
            csvs.append( os.path.join(dir, f) )
    return csvs

# combine each floder's training data into one csv
for floder in tjf.training_data:
    #floder_data_all_csv = os.path.join( floder, "data_all.csv")
    floder_data_all_csv = os.path.join( floder, "data_all_without_unknown.csv")
    #floder_targ_all_csv = os.path.join( floder, "targ_all.csv")
    floder_targ_all_csv = os.path.join( floder, "targ_all_without_unknown.csv")
    if os.path.exists( floder_data_all_csv) and os.path.exists( floder_targ_all_csv):
        continue
    csv_train_data = get_floder_csv_file( floder , "data")
    csv_train_targ = get_floder_csv_file( floder , "targ")
    # combine all data_csv for each floder
    i = 0
    # process unknown
    has_unknown = tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( csv_train_data[i], "_data") )
    while has_unknown:
        i += 1
        has_unknown = tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( csv_train_data[i], "_data") )
    # end unknown
    train_data = pd.read_csv( csv_train_data[i], header=0, sep=',')
    i += 1
    while i < csv_train_data.__len__():
        file = csv_train_data[i]
        if tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( file, "_data") ):
            i += 1
            continue
        td = pd.read_csv(file, header=0, sep=',')
        train_data = train_data.append( td)
        i += 1
    # combine all targ_csv for each floder
    i = 0
    # process unknown
    has_unknown = tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( csv_train_data[i], "_data") )
    while has_unknown:
        i += 1
        has_unknown = tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( csv_train_data[i], "_data") )
    # end unknown
    train_targ = pd.read_csv( csv_train_targ[i], header=0, sep=',')
    i += 1
    while i < csv_train_targ.__len__():
        file = csv_train_targ[i]
        if tjf.unknown_linkids.__contains__( tjf.get_linkid_from_csvpath( file, "_data") ):
            i += 1
            continue
        tt = pd.read_csv(file, header=0, sep=',')
        train_targ = train_targ.append( tt )
        i += 1
    # write into one data_csv
    train_data.to_csv( floder_data_all_csv ,index=False, sep=',')
    print( floder_data_all_csv )
    # write into one targ_csv
    train_targ.to_csv( floder_targ_all_csv ,index=False, sep=',')
    print( floder_targ_all_csv )

# combine all floder's training data into one csv
i = 0
floder = tjf.training_data[i]
#floder_data_all_csv = os.path.join( floder, "data_all.csv")
floder_data_all_csv = os.path.join( floder, "data_all_without_unknown.csv")
#floder_targ_all_csv = os.path.join( floder, "targ_all.csv")
floder_targ_all_csv = os.path.join( floder, "targ_all_without_unknown.csv")
all_train_data = pd.read_csv(floder_data_all_csv, header=0, sep=',')
all_train_targ = pd.read_csv(floder_targ_all_csv, header=0, sep=',')
i += 1
while i < tjf.training_data.__len__():
    floder = tjf.training_data[i]
    floder_data_all_csv = os.path.join( floder, "data_all_without_unknown.csv")
    floder_targ_all_csv = os.path.join( floder, "targ_all_without_unknown.csv")
    all_train_data = all_train_data.append( pd.read_csv(floder_data_all_csv, header=0, sep=',') )
    all_train_targ = all_train_targ.append( pd.read_csv(floder_targ_all_csv, header=0, sep=',') )
    i += 1
all_train_data.to_csv( os.path.join( tjf.dir_data, "all_train_data_without_unknown.csv"), index=False, sep=',')
all_train_targ.to_csv( os.path.join( tjf.dir_data, "all_train_targ_without_unknown.csv"), index=False, sep=',')

