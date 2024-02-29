#매개체가 없는 함수형
def pp():
    print('hi~')
    
pp()

#매개체가 있는 함수 return O
def add(a,b):
    return a**b

print(add(5,5))

#매개체가 있는 함수 return X 
def add_2(a,b):
    print(a**b)

add_2(4,4)