from sklearn import neighbors
import pandas as pd
import numpy as np

#file_tmp_csv = "E:\\tmp\\dm\\tmp.csv"
#file_train_csv = "E:\\tmp\\dm\\train\\train.csv"
#file_test_csv  = "E:\\tmp\\dm\\test\\test.csv"
file_train_csv = "E:\\tmp\\ndm\\train_all\\train_all.csv"
file_test_csv  = "E:\\tmp\\ndm\\republish_test\\republish_test.csv"

data_train_csv = pd.read_csv( file_train_csv )
shape_train = data_train_csv.shape
value_train = data_train_csv.values
i = 0
data_train = np.empty( [ shape_train[0], shape_train[1] - 2 ], dtype=np.double )
type_train = np.empty( [ shape_train[0]], dtype=np.int )
while i < shape_train[0]:
    j = 0
    while j < shape_train[1] - 2:
        try:
            data_train[i][j] = value_train[i][j]
        except ValueError:
            data_train[i][j] = 0
        j += 1
    type_train[i] = value_train[i][j]
    i += 1
knn = neighbors.KNeighborsClassifier( n_neighbors=7 )
knn.fit( data_train, type_train )

data_test_csv = pd.read_csv( file_test_csv )
shape_test = data_test_csv.shape
value_test = data_test_csv.values
i = 0
data_test = np.empty( [ shape_test[0], shape_test[1] - 1 ], dtype=np.double )
while i < shape_test[0]:
    j  = 0
    while j < shape_test[1] - 1:
        try:
            data_test[i][j] = value_test[i][j]
        except ValueError:
            data_test[i][j] = 0
        j += 1
    i += 1
type_test = knn.predict( data_test )
#type_test = np.empty( [shape_test[0]] )

#value_test_usrid_idx = shape_test[1] - 1
#i = 0
#while i < shape_test[0]:
#    usrid = value_test[i][value_test_usrid_idx]
#    res = type_test[i]
#    print( usrid )
#    print( res )
#    i += 1

a = data_test_csv['user_id']
b = type_test
english_column = pd.Series(a, name='user_id')
number_column = pd.Series(b, name='current_service')
predictions = pd.concat([english_column, number_column], axis=1)
#another way to handle
save = pd.DataFrame({'user_id':a,'current_service':b})
save.to_csv('E:\\tmp\\ndm\\result_7.csv',index=False,sep=',')

knn = neighbors.KNeighborsClassifier( n_neighbors=11 )
knn.fit( data_train, type_train )
type_test = knn.predict( data_test )
b = type_test
save = pd.DataFrame({'user_id':a,'current_service':b})
save.to_csv('E:\\tmp\\ndm\\result_11.csv',index=False,sep=',')

knn = neighbors.KNeighborsClassifier( n_neighbors=31 )
knn.fit( data_train, type_train )
type_test = knn.predict( data_test )
b = type_test
save = pd.DataFrame({'user_id':a,'current_service':b})
save.to_csv('E:\\tmp\\ndm\\result_31.csv',index=False,sep=',')
