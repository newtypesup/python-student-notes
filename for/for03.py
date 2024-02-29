for y in range(2,10):
    for x in range(1,10):
        print(f"{y} x {x} = {y*x}")


for i in range(2,10):
    su = [i*x for x in range(1,10)]
    for j in range(1,10):
        print(f'{i:2d} x {j:2d} = {su[j-1]:2d}',end=' ')
    print('')
    
    