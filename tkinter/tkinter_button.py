import tkinter

win = tkinter.Tk()
win.geometry("650x400")
win.resizable(False,False)
win.title("Button 연습")

count = 0

def cntup():
    global count
    count += 1
    if(count>100):
        count = 100
    label.config(text=count)

def cntdown():
    global count
    count -= 1
    if(count<0):
        count = 0
    label.config(text=count)

def rt():   
    global count
    count = 0
    label.config(text=count)

label = tkinter.Label(win,text="0",font=("맑은고딕",30),relief="sunken",width=10,height=2)
label.pack()

up = tkinter.Button(win,text="1증가",font=("맑은고딕",20),width=5,height=1,command=cntup)
up.pack()

down = tkinter.Button(win,text="1감소",font=("맑은고딕",20),width=5,height=1,command=cntdown)
down.pack()

rt = tkinter.Button(win,text="초기화",font=("맑은고딕",20),width=5,height=1,command=rt)
rt.pack()

win.mainloop()

#pack은 div랑 비슷함