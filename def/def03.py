def football(name,team,*position):
    print(f"이름 : {name}\t소속팀 : {team}\t" ,end="포지션 : ")
    for i in position:
        print(i, end=" ")


football("손흥민","토트넘","공격수","윙어","미드필더","득점왕","슈퍼스타","연예인")