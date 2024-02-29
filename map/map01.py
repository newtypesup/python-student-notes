def sq(x):  #1번 리스트 출력
    return x**2

numbers = [1,2,3,4,5]
sp_numbers = map(sq,numbers)
print(list(sp_numbers))


def sq(x):  #2번 리스트 출력 [단일]
    return x**2

numbers = [1,2,3,4,5]
sp_numbers = list(map(sq,numbers))
print(sp_numbers[2])
