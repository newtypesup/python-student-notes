import tkinter

w = 400
h = 280
p_x = 200
p_y = 200
win = tkinter.Tk()
win.geometry("{}x{}+{}+{}".format(w,h,p_x,p_y))

def close():
    win.quit()


menubar = tkinter.Menu(win)



menu1 = tkinter.Menu(menubar,tearoff=False)
menu1.add_cascade(label="하위 메뉴 1-1")
menu1.add_cascade(label="하위 메뉴 1-2")
menu1.add_separator()
menu1.add_command(label="종 료",command=close)
menubar.add_cascade(label="상위 메뉴1",menu=menu1)

menu2 = tkinter.Menu(menubar,tearoff=False)
menu2.add_command(label="하위 메뉴 2-1")
menu2.add_command(label="하위 메뉴 2-2", state="disabled")
menubar.add_cascade(label="상위 메뉴 2",menu = menu2)



win.config(menu=menubar)
win.mainloop()