for i in range(1,6):
    for j in range(0,i):
        print("☆",end=' ')
    print("")
        
for i in range(5):
    print('{} '.format('  '*(i)),end="")
    print('{} '.format('☆ '*(5-i)))
    
    
    
for i in range(1,6):
    print("☆ "*i + "  "*(5-i) + "☆ "*(6-i))

for i in range(1,6):
    print("  "*(5-i),end='')
    print("☆ "*(i) +"  "*(i-1) +"☆ "*(6-i))