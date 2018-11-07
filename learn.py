
def asd(sc,k,v):
    sc[k] = v

k=['a','b','c']
v=[1,2,3]

i=0
sc=dict()
while i < 3:
    asd(sc,k[i],v[i])
    i += 1

print(sc)