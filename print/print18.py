from random import *
ar_dict = {}        #dict
ar_list = []        #list
ar_tuple = str()       #tuple
str_char = "name"   #string

for i in range(10):
    rd = randint(1,10)
    ar_dict[i] = rd     #[i] <- key -rd <- value
    ar_list.append(rd)
    ar_tuple += str(rd)
    str_char += str(rd)
    
print(ar_dict)
print(ar_list)
print(ar_tuple)
print(str_char)