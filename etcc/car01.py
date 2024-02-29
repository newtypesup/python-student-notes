intime = input('임차시간 > ').split(":")
outtime = input('출차시간 > ').split(':')

intime = int(intime[0])*60 + int(intime[1])
outtime = int(outtime[0])*60 + int(intime[1])

money = (outtime-intime)//10*500
print(f'{money:,}원')
