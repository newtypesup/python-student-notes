for i in range(10):
    for j in range(i):
        print("  ",end="")
    for j in range(19,i*2,-1):
        print("☆ ",end="")
    print("")
for i in range(9):
    for j in range(8-i):
        print("  ",end="")
    for j in range(0,3+i*2):
        print("☆ ",end="")
    print("")
