import statistics_data as sd
import pandas as pd
import tjfilepath as tjf

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
# key   : file_name
# value : dict() by linkid
for file in tjf.datafileset1:
    data_csv = pd.read_csv( file, header=None , sep=',', usecols=[0,1,2,3,4,5,6,7,8,9,10])
    sd.unknown_count( data_csv, file ,file_count, 1)
    sd.process_unknown_sc( data_csv , sc)
    sd.process_column_count(col_6_cnt,col_7_cnt,col_8_cnt,col_9_cnt,data_csv)
for file in tjf.datafileset2:
    data_csv = pd.read_csv( file, header=None, sep="\t")
    sd.unknown_count( data_csv, file ,file_count, 1)
    sd.process_unknown_sc( data_csv , sc)
    sd.process_column_count(col_6_cnt,col_7_cnt,col_8_cnt,col_9_cnt,data_csv)
print("=========================")

sd.process_file_count(file_count, 1)
print("=========================")

sc_pr_cnt  = dict()
sc_rng_cnt = dict()
sd.process_sc(sc, 1, sc_pr_cnt, sc_rng_cnt)

print("=========================")
# [6] travel time
all_nr = 24 * 12 * 4 * 855
col_6_pr = dict()
sd.process_column_range_percentage(col_6_cnt, [0,10,20,30,40], col_6_pr)
print("------- travel time -------")
print(col_6_pr)
if col_6_cnt.__contains__(0):
    print("[0]_nr is " + str(col_6_cnt[0]) + ", % = " + str(col_6_cnt[0] / all_nr) + "%" )
# [7] volumn
col_7_pr = dict()
sd.process_column_range_percentage(col_7_cnt, [0,500,10000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000], col_7_pr)
print("------- volumn -------")
print(col_7_pr)
if col_7_cnt.__contains__(0):
    print("[0]_nr is " + str(col_7_cnt[0])  + ", % = " + str(col_7_cnt[0] / all_nr) + "%" )
# [8] speed
col_8_pr = dict()
sd.process_column_range_percentage(col_8_cnt, [0,10,20,30,40,50,60,70,80,90,100], col_8_pr)
print("------- speed -------")
print(col_8_pr)
if col_8_cnt.__contains__(0):
    print("[0]_nr is " + str(col_8_cnt[0])  + ", % = " + str(col_8_cnt[0] / all_nr) + "%" )
# [9] occupancy
col_9_pr = dict()
sd.process_column_range_percentage(col_9_cnt, [0,10,20,30,40,50,60,70,80,90,100], col_9_pr)
print("------- occupancy -------")
print(col_9_pr)
if col_9_cnt.__contains__(0):
    print("[0]_nr is " + str(col_9_cnt[0])  + ", % = " + str(col_9_cnt[0] / all_nr) + "%" )
print("=========================")