import pandas as pd
import preprocessing
import os

#dir_data="E:\\tj"
dir_data="./data"
datafileset1 = (
    dir_data + "/0707_seg_1.txt",
    dir_data + "/0707_seg_2.txt",
    dir_data + "/0707_seg_3.txt",
    dir_data + "/0707_seg_4.txt",
    dir_data + "/0720_seg_1.txt",
    dir_data + "/0720_seg_2.txt",
    dir_data + "/0720_seg_3.txt",
    dir_data + "/0720_seg_4.txt",
    dir_data + "/0721_seg_1.txt",
    dir_data + "/0721_seg_2.txt",
    dir_data + "/0721_seg_3.txt",
    dir_data + "/0721_seg_4.txt")
datafileset2 = (
    dir_data + "/0715_seg_1_sort.txt",
    dir_data + "/0715_seg_2_sort.txt",
    dir_data + "/0715_seg_3_sort.txt",
    dir_data + "/0715_seg_4_sort.txt")
datafileset3 = (
    dir_data + "/0722_seg_1.txt",
    dir_data + "/0722_seg_2.txt",
    dir_data + "/0722_seg_3.txt",
    dir_data + "/0722_seg_4.txt")

file_data=dict()
# key   : file_name
# value : dict() by linkid
#for file in datafileset1:
#    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
#    preprocessing.process_file_data(data_csv,file_data,file,4,0)
#for file in datafileset2:
#    data_csv = pd.read_csv( file, header=None, sep="\t")
#    preprocessing.process_file_data(data_csv,file_data,file,4,0)
for file in datafileset3:
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
#for file in datafileset1:
#    all_data_file_name.append( file )
#for file in datafileset2:
#    all_data_file_name.append( file )
for file in datafileset3:
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
        # construct [input][output] data into 'linkid,input0,...,inputn,output1,...,outputm'
        # and count the column number, which is needed by pandas to form csv file
        linkid_value=[]
        col_nr = 0
        for item in res:
            value = []
            col_nr = 1
            value.append( linkid )
            for item0 in item[0]: # item[0] is a list contains input data
                value.append(item0)
                col_nr += 1
            for item1 in item[1]: # item[1] is a list contains output data
                value.append(item1)
                col_nr += 1
            linkid_value.append( value ) # construct one data for this linkid, append!
        # construct with pandas and write into csv file
        # first column is the linkid
        col_i = 0
        col=[]
        for item in linkid_value: # get all columa 0 data
            col.append( item[col_i] )
        linkid_csv = pd.Series(col, name=str(col_i)) # construct as pandas.Series
        col_i += 1
        while col_i < col_nr: # for other column
            col=[]
            for item in linkid_value:
                col.append( item[col_i] )
            a = pd.Series(col, name=str(col_i))
            linkid_csv = pd.concat([linkid_csv,a], axis=1)
            col_i += 1
        # create file floder for each original data file .txt
        if not os.path.exists( filecsv ):
            os.mkdir( filecsv )
        # create one csv file for each linkid
        csv_data_file = filecsv + "/" + linkid + ".csv"
        linkid_csv.to_csv(csv_data_file, index=False, sep=',')
        print( csv_data_file )
