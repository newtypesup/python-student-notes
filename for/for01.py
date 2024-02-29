for x in range(10):
    print(x,end=' ')
print('')

for x in range(1,10):
    print(x,end=' ')
print('')

for x in range(0,10,2):
    print(x,end=' ')
    
print('')   #배열
ar=[0,1,2,3,4,5,6]
for x in ar:
    print(x,end=' ')
    
print('')   #역순 배열
ar.sort(reverse=True)
for x in ar:
    print(x,end=' ')
    