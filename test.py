import sklearn
from sklearn import datasets
from sklearn import neighbors
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier # KNN


#iris = datasets.load_iris()
#X,y = iris.data, iris.target
#print(X)
#print(y)
#knn = neighbors.KNeighborsClassifier(n_neighbors=5)
#knn.fit(X,y)
#result = knn.predict([[6.5,3.0,5.2,2.0],])
#print(result)
#print(iris.target_names[result])
#print("-----------------------")

tmp_csv = "E:\\tmp\\dm\\tmp.csv"
train_csv = "E:\\tmp\\dm\\train\\train.csv"
test_csv  = "E:\\tmp\\dm\\test\\test.csv"

mcsv = pd.read_csv( tmp_csv )
#csv_file = open( tmp_csv, 'r')
#mcsv = csv.reader( csv_file )
#for item in mcsv:
#    print( item )

# DataFrame.shape()
# Return a tuple representing the dimensionality of the DataFrame
shape = mcsv.shape
print( shape )

# DataFrame.values
# 	Return a Numpy representation of the DataFrame.
mvalue = mcsv.values
#print( mvalue )
#print("------列--------")

i = 0
mdata = np.empty( [10,4], dtype=np.int )
mtype = np.empty( [shape[0]], dtype=np.int )
while i < shape[0]:
    j = 0
    while j < shape[1] - 1:
        try:
            mdata[i][j] = mvalue[i][j]
        except ValueError:
            mdata[i][j] = 0
        j += 1
    mtype[i] = mvalue[i][j]
    i += 1
print( mdata )
print( mtype )

knn = neighbors.KNeighborsClassifier(n_neighbors=5)
knn.fit( mdata, mtype )
mtest = [
    [3,6,5,4],
    [0,0,0,0],
    [8,7,6,5]
]
mtest_id = [
    "qwe",
    "asd",
    "zxc"
]
print( mtest_id )

#res = knn.predict( [[3,6,7,4],] )
#print( res )

res = knn.predict( mtest )
res_csv_data = np.empty( (3,2) , dtype=str )
i = 0
while i < 3:
    res_csv_data[i][0] = mtest_id.__getitem__(i)
    res_csv_data[i][1] = str(res[i])
    i += 1
print( res_csv_data )

a = mtest_id
b = res
english_column = pd.Series(a, name='user_id')
number_column = pd.Series(b, name='type_predicted')
predictions = pd.concat([english_column, number_column], axis=1)
#another way to handle
save = pd.DataFrame({'english':a,'number':b})
save.to_csv('test.csv',index=False,sep=',')
