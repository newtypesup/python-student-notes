#Entry = js(inputbox),입력창

import tkinter as tk

win =  tk.Tk()
win.geometry("640x480")

def calc(event):
    label.config(text="결과 = " + str(eval(ipbox.get())))

def zero(event):
    label.config(text="식을 입력하세요.")
    ipbox.delete("0","end")

ipbox = tk.Entry(win,insertwidth=5,insertbackground="red",font=("맑은고딕",30))
ipbox.insert("0","계산식을 입력하세요")
ipbox.bind("<Button-1>",zero)
ipbox.bind("<Return>",calc)
ipbox.bind("<Escape>",zero)
ipbox.pack()
label = tk.Label(win,text="결과 = ",font=("맑은고딕",30))
label.pack()
win.mainloop()

#계산기