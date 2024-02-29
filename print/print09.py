str = "가나다라마바사"
print(str)
print(str[2])
str2 = ["네이버","카카오","라인"]
print(str2[1])
print(str2[2][1])
str3 = "'asdf','zxcv'"
print(str3[1])
birthday = "20240219"
print("현재년도 "+birthday[0:4]+"년 입니다.")
cnt = len(birthday)
print("글자수",cnt)
print("현재월",birthday[4:cnt-2])
print("현재일",birthday[6:],"일 입니다.")
print("년도",birthday[-6:-4],"년도")
print(birthday[2:6:2])
