import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn import tree
import tjfilepath as tjf
import os
import pickle
import time


def get_floder_csv_file(dir, prex):
    if not os.path.exists( dir ):
        return []
    csvs = []
    files = os.listdir( dir )
    for f in files:
        if f.endswith(prex + ".csv"):
            csvs.append( os.path.join(dir, f) )
    return csvs


clffile = os.path.join( tjf.dir_data, "decision_tree.module")
fd = open( clffile, "rb")
clf = pickle.load( fd )
fd.close()

test_floder = tjf.test_data[0]

test_data_files = get_floder_csv_file( test_floder, "data")
test_targ_files = get_floder_csv_file( test_floder, "targ")

test_data_files = sorted( test_data_files )
test_targ_files = sorted( test_targ_files )

print(test_data_files)
print(test_targ_files)

fi = 0
while fi < test_data_files.__len__():
    test_data_file = test_data_files[ fi ]
    test_targ_file = test_targ_files[ fi ]
    #if not test_targ_file.__contains__("IL-TESTTSC-134_targ.csv"):
    #    fi += 1
    #    continue
    test_data = pd.read_csv( test_data_file, header=0, sep=',' )
    test_targ = pd.read_csv( test_targ_file, header=0, sep=',' )
    print(test_targ)
    pred_targ = clf.predict( test_data.values )
    i = 0
    while i < test_targ.__len__():
        y = test_targ.values[i]
        z = pred_targ[i]
        print([y,z])
        i += 1
    print("=====================")
    fi += 1
