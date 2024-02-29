years = {"2021년":2,"22년":5,"2024년":10}
print(years)
for a,b in years.items():
    print(a,b)

print("-------------------")
    
for y,c in years.items():
    print(y.rjust(5),str(c).rjust(2)+"개 취득하였습니다.",sep="자격증을 ")