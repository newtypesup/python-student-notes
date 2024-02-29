sports1 = ["축구","야구","배구","농구","복싱","축구","야구"]   #list
print(sports1)
sports2 = {"축구","야구","배구","농구","복싱","축구","야구"}   #list, set 중복 X, 무순서
print(sports2)

su = {4,5,6,7,8,9,1,2,3,10,100,1000}
print(su)
number = (1,2,3,4,5)    #tuple
str_1 = "가나다라마바사","123"
ar = [123,"문자",False]

print(sports1[2])
print(number[2])

print(sports1)
sports1.pop()
print(sports1)
sports1.append("다이빙")
print(sports1)
sports1.insert(2,"격투기")
print(sports1)
sports1.insert(4,"")
print(sports1)
sports1.extend("수영")
print(sports1)
