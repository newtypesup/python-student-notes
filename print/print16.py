a_num = 12
b_num = 150
c_num = 1234567
print("{:>5}".format(a_num))
print(f"{b_num:>5}")
print(c_num)

for x in range(8,12):
    print("{0:*<5}".format(x))
for x in range(8,12):
    print("{0:*>5}".format(x))