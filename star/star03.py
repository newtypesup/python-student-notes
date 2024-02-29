for i in range(10):
    for j in range(i+1):
        print("☆ ",end="")
    for j in range(9-i):
        print("  ",end="")
    for j in range(10-i):
        print("☆ ",end="")
    print("")
for i in range(10):
    for j in range(9-i):
        print("  ",end="")
    for j in range(i+1):
        print("☆ ",end="")
    for j in range(i):
        print("  ",end="")
    for j in range(10-i):
        print("☆ ",end="")
    print("")