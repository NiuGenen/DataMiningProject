import pandas as pd
import preprocessing
import os
import tjfilepath as tjf

file_data=dict()
# key   : file_name
# value : dict() by linkid
for file in tjf.datafileset1:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    preprocessing.process_file_data(data_csv,file_data,file,4,0)
for file in tjf.datafileset2:
    data_csv = pd.read_csv( file, header=None, sep="\t")
    preprocessing.process_file_data(data_csv,file_data,file,4,0)
for file in tjf.datafileset3:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    preprocessing.process_file_data(data_csv,file_data,file,4,0)
print("=========================")

# file_data = dict()
# key   : file_name
# value : dict() by linkid
#         key = linkid
#         value = [ [[6] [7] [8] [9] [10]],
#                     ...... ]
all_data_file_name = []
for file in tjf.datafileset1:
    all_data_file_name.append( file )
for file in tjf.datafileset2:
    all_data_file_name.append( file )
for file in tjf.datafileset3:
    all_data_file_name.append( file )
# process all data file
for filename in all_data_file_name:
    file_data_value = file_data[ filename ]
    filecsv = filename[0:filename.__len__()-4] + "_csv"
    print("Processing " + filecsv)
    # process each linkid's data
    for linkid in file_data_value.keys():
        # transformat data into [input][output] format
        res = []
        preprocessing.transfor_format( file_data_value[linkid], [6,7,8,9], 6, [10], 6, res)
        col_data_nr = 4 * 6
        col_targ_nr = 6
        # construct [input][output] data into 'input0,...,inputn,output1,...,outputm'
        # and count the column number, which is needed by pandas to form csv file
        linkid_value=[]
        for item in res:
            value = []
            #value.append( linkid )
            for item0 in item[0]: # item[0] is a list contains input data
                value.append(item0)
            for item1 in item[1]: # item[1] is a list contains output data
                value.append(item1)
            linkid_value.append( value ) # construct one data for this linkid, append!
        # construct with pandas and write into csv file
        #
        # data file
        col_i = 0
        col=[]
        for item in linkid_value: # get all columa 0 data
            col.append( item[col_i] )
        linkid_data_csv = pd.Series(col, name=str(col_i)) # construct as pandas.Series
        col_i += 1
        while col_i < col_data_nr: # for other column
            col=[]
            for item in linkid_value:
                col.append( item[col_i] )
            a = pd.Series(col, name=str(col_i))
            linkid_data_csv = pd.concat([linkid_data_csv,a], axis=1)
            col_i += 1
        # target file
        col=[]
        for item in linkid_value:
            col.append( item[col_i])
        linkid_targ_csv = pd.Series(col, name=str(col_i - col_data_nr))
        col_i += 1
        while col_i < col_data_nr + col_targ_nr:
            col=[]
            for item in linkid_value:
                col.append( item[col_i] )
            a = pd.Series(col, name=str(col_i))
            linkid_targ_csv = pd.concat([linkid_targ_csv,a], axis=1)
            col_i += 1
        # create file floder for each original data file .txt
        if not os.path.exists( filecsv ):
            os.mkdir( filecsv )
        # create one csv file for each linkid
        csv_data_file = filecsv + "/" + linkid + "_data.csv"
        csv_targ_file = filecsv + "/" + linkid + "_targ.csv"
        linkid_data_csv.to_csv(csv_data_file, index=False, sep=',')
        linkid_targ_csv.to_csv(csv_targ_file, index=False, sep=',')
        print( csv_data_file + " ; " + csv_targ_file)
