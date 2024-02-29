str_a = "son is best soccer player"
print(str_a.upper())    #대문자로 변경
print(str_a.lower())    #소문자로 변경

str_b = str_a.replace("soccer","football")  #1번알 2번으로 몽땅 바꿔준다.
print(str_b)

print(str_b.index("football"))  #해당 단어 몇 번째에 있는 지 검색
print(str_b.find("football"))
print(str_b.find("FOOTBALL"))   #검색되지 않을 때 -1이 나옴.

print(str_a.count("o")) #등장 횟수