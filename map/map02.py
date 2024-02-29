ar = [9,8,7,6,5,4,3,2,1]
start,end = map(int,input('시작위치 끝위치 띄어쓰기로 입력 ').split())
sum_ar = []
if start < end:
    for x in range(start-1,end):
        sum_ar.append(ar[x])
    print(sum_ar)
    print(start,'부터 ',end,'까지의 합계는 :',sum(sum_ar))
else:
    for x in range(end-1,start):
        sum_ar.append(ar[x])
    print(sum_ar)
    print(end,'부터 ',start,'까지의 합계는 :',sum(sum_ar))