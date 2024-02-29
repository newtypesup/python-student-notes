import sys
ar = []
print('커플 계산기')
cnt = int(input('몇번 계산하시겠습니까? '))
for x in range(cnt):
    one, two = map(int, sys.stdin.readline().split())
    ar.append(one+two)
print(ar)
print(sum(ar))