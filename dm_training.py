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

dmc.check_file_and_pause( dmfp.pp4_format_train_path )

print("Reading Training data " + dmfp.pp4_format_train_path )
traincsv = pd.read_csv( dmfp.pp4_format_train_path, sep=',' )

print("Extract data and label")
item_nr = traincsv.values.__len__()
data  = traincsv.iloc[0:item_nr, 0:48]
label = traincsv.iloc[0:item_nr, 48:54]

# using decision tree
print("Using Decision Tree Module")
#clf = tree.DecisionTreeClassifier()
clf = tree.DecisionTreeClassifier(criterion="entropy")
#clf = tree.DecisionTreeClassifier(min_samples_split=10)

# training
print("Training Start...   " + str(time.clock()) )
clf = clf.fit(data.values, label.values)
print("Training Finish...   " + str(time.clock()) )

# saving the training module
save_path = os.path.join(sd.source_data_dir, dmfp.training_module_name + "." + dmfp.training_module_config + dmfp.training_module_suffix)
clf_file = os.path.join( save_path )
print("Dumping Result into" + clf_file )
fd = open( clf_file, "wb")
clfstr = pickle.dump(clf, fd )
fd.close()
