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

# training
for i in range(0,6):
    data  = traincsv.iloc[0:item_nr, 0:48 + i]
    label = traincsv.iloc[0:item_nr, 48 + i]
    # using decision tree
    print("Using Decision Tree Module with specific parameter")
    clf = tree.DecisionTreeClassifier(min_samples_split=50, max_depth=20, min_samples_leaf=30)
    print("Training " + str(i) + " Start...   " + str(time.clock()) )
    clf = clf.fit(data.values, label.values)
    print("Training " + str(i) + " Finish...   " + str(time.clock()) )
    # saving the training module
    save_path = os.path.join(dmfp.training_modules_floder_path, dmfp.training_module_name + "." + str(i) + dmfp.training_module_suffix)
    clf_file = os.path.join( save_path )
    print("Dumping Result into" + clf_file )
    fd = open( clf_file, "wb")
    clfstr = pickle.dump(clf, fd )
    fd.close()
