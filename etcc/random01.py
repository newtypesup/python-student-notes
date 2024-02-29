from random import *

ar_list = []

for i in range(6):
    rd =  randint(1,46)
    
    while rd in ar_list:
        rd = randint(1,46)
        
    ar_list.append(rd)

print(ar_list)
    



# import random

# def generate_lotto_numbers():
#     lotto_numbers = random.sample(range(1, 46), 6)
#     return sorted(lotto_numbers)

# if __name__ == "__main__":
#     lotto_numbers = generate_lotto_numbers()
#     print("로또 번호:", lotto_numbers)
