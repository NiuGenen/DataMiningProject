import sklearn.tree as tree
import dm_csv as dmcsv
import pandas as pd

asd = pd.read_csv("./asd.csv", sep=',')
zxc = pd.read_csv("./zxc.csv", sep=',')
qwe = pd.concat([asd,zxc])
dmcsv.write_list2_into_csv( qwe.values, ['asd1','asd2','asd3'], "./qwe1.csv", 1)
qwe = pd.concat([asd,zxc], ignore_index=True)
dmcsv.write_list2_into_csv( qwe.values, ['asd1','asd2','asd3'], "./qwe2.csv", 1)
