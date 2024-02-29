etc = 'tuple'
tp = ('☆','1234')
ar = (123,"가나다라",etc,tp)

print(ar)
print(ar[3])
print(ar[3][0]) #배열

(name,age,hobby) = ("형섭신",20,('game','language'))
print(name)
print(age)
print(hobby)

a = 4
b = 7
print(a,b)
a,b = b,a
print(a,b)