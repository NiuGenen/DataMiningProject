import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import tjfilepath as tjf
import os

a=[[1,2],[1,2]]
a[0][0]=1
a[0][1]=2
a[1][0]=3
a[1][1]=4
print(a)
print(a[::-1])

def get_floder_csv_file(dir):
    if not os.path.exists( dir ):
        return []
    csvs = []
    files = os.listdir( dir )
    for f in files:
        if f.endswith(".csv"):
            csvs.append( os.path.join(dir, f) )
    return csvs

floder = tjf.training_data[0]
csv_train = get_floder_csv_file( floder )

floder = tjf.test_data[0]
csv_test = get_floder_csv_file( floder )

# training

