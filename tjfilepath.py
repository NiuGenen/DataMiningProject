#dir_data="E:\\tj"
dir_data="./data"
# training data, sep=','
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
    dir_data + "/0721_seg_4.txt"
)
# training data, sep=' '
datafileset2 = (
    dir_data + "/0715_seg_1_sort.txt",
    dir_data + "/0715_seg_2_sort.txt",
    dir_data + "/0715_seg_3_sort.txt",
    dir_data + "/0715_seg_4_sort.txt"
)
# test data, sep=','
datafileset3 = (
    dir_data + "/0722_seg_1.txt",
    dir_data + "/0722_seg_2.txt",
    dir_data + "/0722_seg_3.txt",
    dir_data + "/0722_seg_4.txt"
)
# all formated training data floder
training_data = []
for file in datafileset1:
    training_data.append( file[0:file.__len__()-4] + "_csv")
for file in datafileset2:
    training_data.append( file[0:file.__len__()-4] + "_csv")
# all formated test data floder
test_data = []
for file in datafileset3:
    test_data.append( file[0:file.__len__()-4] + "_csv")