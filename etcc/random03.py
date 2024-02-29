ar_1 = set(map(int,input('숫자를 입력해주세요(, 로 구분) : ').split(',')))

from random import *
ar_com = []
for i in range(6):
    rd = randint(1,46)
    while rd in ar_com:
        rd = randint(1,46)
    ar_com.append(rd)
    
print(ar_com)
ar_2 = set(ar_com)

ar = ar_1 & ar_2

print(ar)
print('맞은 개수 : ',len(ar))

if len(ar) == 4:
    print("3등")
elif len(ar) == 5:
    print("2등")
elif len(ar) == 6:
    print("1등")
else:
    print("꽝")
