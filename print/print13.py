from random import *
Range = 100
i = 1
while Range > 0:
    dice = randint(1,6) #1~6이하
    Range -= dice
    print("주사위 :",dice)
    # print(f"{i}칸 진행 남은거리 {Range}")
    print(i,Range,sep="칸 진행 남은거리 : ")
    i+=1