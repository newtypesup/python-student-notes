def add(one,two):   #3번과 같음
    return one + two

numbers_1 = [1,2,3,4,5]
numbers_2 = [10,20,30,40,50]
add_numbers = []
for x in range(5):
    add_numbers.append(numbers_1[x]+numbers_2[x])
print(add_numbers)