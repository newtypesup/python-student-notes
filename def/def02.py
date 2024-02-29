def coffee_order(menu,price,type):
    price = int(price)
    if type == 'ice':
        price += 500
    print(f"메뉴 : {menu}\t가격 : {price}\t 유형 : {type}")

coffee_order("아메리카노",1500,"ice")