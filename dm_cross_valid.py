import dm_source_data as sd
import pandas as pd
import dm_preprocess_fun as ppf
import dm_csv as dmcsv
import os
import dm_filepath as dmfp
import dm_common as dmc
import pickle
import time
from sklearn import tree
from sklearn.model_selection import cross_val_score

dmc.check_file_and_pause( dmfp.pp4_format_train_path )

print("Reading Training data " + dmfp.pp4_format_train_path )
traincsv = pd.read_csv( dmfp.pp4_format_train_path, sep=',' )

print("Extract data and label")
item_nr = traincsv.values.__len__()
data  = traincsv.iloc[0:item_nr, 0:48]
label = traincsv.iloc[0:item_nr, 48:54]

#clf = tree.DecisionTreeClassifier()
#clf = tree.DecisionTreeClassifier(criterion="entropy")
#clf = tree.DecisionTreeClassifier(min_samples_split=10)
#clf = tree.DecisionTreeClassifier(min_samples_split=20)
#clf = tree.DecisionTreeClassifier(max_depth=30)
#clf = tree.DecisionTreeClassifier(min_samples_split=20, max_depth=30)
#clf = tree.DecisionTreeClassifier(min_samples_leaf=10)

# cross validation
print("--- criterion = gini ---")
for i in range(0,6):
    test_score = cross_val_score(tree.DecisionTreeClassifier(criterion="gini"), data.values, label.values[0:item_nr,i], cv=4)
    print(test_score)

print("--- criterion = entropy ---")
for i in range(0,6):
    test_score = cross_val_score(tree.DecisionTreeClassifier(criterion="entropy"), data.values, label.values[0:item_nr,i], cv=4)
    print(test_score)

dmc.pause_msg("END corss validation ...........")

print("--- min samples split = 50; max depth = 20; min samples lead = 30 ---")
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,0], cv=4)
print(test_score)

data = traincsv.iloc[0:item_nr, 0:49]
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,1], cv=4)
print(test_score)

data = traincsv.iloc[0:item_nr, 0:50]
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,2], cv=4)
print(test_score)

data = traincsv.iloc[0:item_nr, 0:51]
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,3], cv=4)
print(test_score)

data = traincsv.iloc[0:item_nr, 0:52]
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,4], cv=4)
print(test_score)

data = traincsv.iloc[0:item_nr, 0:53]
test_score = cross_val_score(tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30), data.values, label.values[0:item_nr,5], cv=4)
print(test_score)

