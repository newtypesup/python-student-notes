poketmon = {'a':["지우","피카츄"],'b':["웅이","롱스톤"],'c':["이슬이","고라파덕"]}
print(poketmon)
print(poketmon.get('a'))
print(poketmon.get('b')[1])

print(poketmon.keys())
print(poketmon.values())
print(poketmon.items())

del poketmon["b"]
print(poketmon)
poketmon["a"]+=["리자몽"]
print(poketmon)
poketmon["d"] = ["로켓단","냐옹"]
print(poketmon)