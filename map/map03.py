def add(one,two):   #4번과 같음
    return one + two

numbers_1 = [1,2,3,4,5]
numbers_2 = [10,20,30,40,50]

add_numbers = list(map(add,numbers_1,numbers_2))
print(add_numbers)

