num_1 = {1,2,3,4,5}
num_2 = set([4,5,6,7,8])

#합집합(union, &)
print(num_1.union(num_2))
print(num_1|num_2)

#교집합(interection, &)
print(num_1.intersection(num_2))
print(num_1 & num_2)

#차집합
print(num_1.difference(num_2))
print(num_2.difference(num_1))
print(num_1-num_2)