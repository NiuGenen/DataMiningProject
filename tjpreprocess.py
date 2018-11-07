import pandas as pd
import preprocessing

dir_data="E:\\tj"
datafileset1 = (
    dir_data + "\\0707_seg_1.txt",
    dir_data + "\\0707_seg_2.txt",
    dir_data + "\\0707_seg_3.txt",
    dir_data + "\\0707_seg_4.txt",
    dir_data + "\\0720_seg_1.txt",
    dir_data + "\\0720_seg_2.txt",
    dir_data + "\\0720_seg_3.txt",
    dir_data + "\\0720_seg_4.txt",
    dir_data + "\\0721_seg_1.txt",
    dir_data + "\\0721_seg_2.txt",
    dir_data + "\\0721_seg_3.txt",
    dir_data + "\\0721_seg_4.txt")
datafileset2 = (
    dir_data + "\\0715_seg_1_sort.txt",
    dir_data + "\\0715_seg_2_sort.txt",
    dir_data + "\\0715_seg_3_sort.txt",
    dir_data + "\\0715_seg_4_sort.txt")

file_count=dict()
sc=dict()
# column value
# [0] data  [1] time  [2] direction [3] road type [4] linkid [5] length
# [6] travel time [7] volumn [8] speed [9] occupancy
# [10] congestion level
col_6_cnt = dict() # [6] travel time
col_7_cnt = dict() # [7] volumn
col_8_cnt = dict() # [8] speed
col_9_cnt = dict() # [9] occupancy
file_data=dict()
# key : file_name
# value : dict() by linkid
#         key = linkid
#         value = [
#                     [[6] [7] [8] [9] [10]],
#                     [[6] [7] [8] [9] [10]],
#                     ......
#                 ]
for file in datafileset1:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    preprocessing.process_unknown_count( data_csv, file ,file_count, 1)
    preprocessing.process_unknown_sc( data_csv , sc)
    preprocessing.process_column_count(col_6_cnt,col_7_cnt,col_8_cnt,col_9_cnt,data_csv)
    preprocessing.process_file_data(data_csv,file_data,file,4,0)
for file in datafileset2:
    data_csv = pd.read_csv( file, header=None, sep="\t")
    preprocessing.process_unknown_count( data_csv, file ,file_count, 1)
    preprocessing.process_unknown_sc( data_csv , sc)
    preprocessing.process_column_count(col_6_cnt,col_7_cnt,col_8_cnt,col_9_cnt,data_csv)
    preprocessing.process_file_data(data_csv,file_data,file,4,0)
print("=========================")

preprocessing.process_file_count(file_count, 1)
print("=========================")

a=dict()
file_10_data = file_data[ datafileset1[0]]
for key in file_10_data.keys():
    res=[]
    preprocessing.transfor_format( file_10_data[key], [6,7,8,9], 6, [10], 6, res)
    for item in res:
        print("Data = " + item[0].__str__() )
        print("Target = " + item[1].__str__() )
    print("0000000000000000000000000000000000000000000000000000000000000000000000")
print("=========================")

sc_pr_cnt  = dict()
sc_rng_cnt = dict()
preprocessing.process_sc(sc, 1, sc_pr_cnt, sc_rng_cnt)

print("=========================")
# [6] travel time
all_nr = 24 * 12 * 4 * 855
col_6_pr = dict()
preprocessing.process_column_range_percentage(col_6_cnt, [0,10,20,30,40], col_6_pr)
print("------- travel time -------")
print(col_6_pr)
if col_6_cnt.__contains__(0):
    print("[0]_nr is " + str(col_6_cnt[0]) + ", % = " + str(col_6_cnt[0] / all_nr) + "%" )
# [7] volumn
col_7_pr = dict()
preprocessing.process_column_range_percentage(col_7_cnt, [0,500,10000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000], col_7_pr)
print("------- volumn -------")
print(col_7_pr)
if col_7_cnt.__contains__(0):
    print("[0]_nr is " + str(col_7_cnt[0])  + ", % = " + str(col_7_cnt[0] / all_nr) + "%" )
# [8] speed
col_8_pr = dict()
preprocessing.process_column_range_percentage(col_8_cnt, [0,10,20,30,40,50,60,70,80,90,100], col_8_pr)
print("------- speed -------")
print(col_8_pr)
if col_8_cnt.__contains__(0):
    print("[0]_nr is " + str(col_8_cnt[0])  + ", % = " + str(col_8_cnt[0] / all_nr) + "%" )
# [9] occupancy
col_9_pr = dict()
preprocessing.process_column_range_percentage(col_9_cnt, [0,10,20,30,40,50,60,70,80,90,100], col_9_pr)
print("------- occupancy -------")
print(col_9_pr)
if col_9_cnt.__contains__(0):
    print("[0]_nr is " + str(col_9_cnt[0])  + ", % = " + str(col_9_cnt[0] / all_nr) + "%" )
print("=========================")
