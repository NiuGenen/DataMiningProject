import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn import tree
import tjfilepath as tjf
import os
import pickle
import time

#data = pd.read_csv( tjf.all_train_data_file, sep=',', header=0 )
#targ = pd.read_csv( tjf.all_train_targ_file, sep=',', header=0 )
data = pd.read_csv( tjf.all_train_data_file_without_unknown, sep=',', header=0 )
targ = pd.read_csv( tjf.all_train_targ_file_without_unknown, sep=',', header=0 )

clf = tree.DecisionTreeClassifier()
print("Training Start...   " + str(time.clock()) )
clf = clf.fit(data.values, targ.values)
print("Training Finish...   " + str(time.clock()) )

#clffile = os.path.join( tjf.dir_data, "decision_tree.module")
clffile = os.path.join( tjf.dir_data, "decision_tree_without_unknown.module")
print("Dumping into" + clffile )
fd = open( clffile, "wb")
clfstr = pickle.dump(clf, fd )
fd.close()
