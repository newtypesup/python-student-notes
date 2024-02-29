import random   #sample

numbers = list(range(1,46))
print(numbers)
print(len(numbers))

print(random.sample(numbers,6))

num_list = random.sample(range(46),6)
print(num_list)

data = ["사과","바나나","파인애플","자두","포도","수박"]
data_list = random.sample(data,2)
print(data_list)