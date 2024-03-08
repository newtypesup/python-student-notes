import tkinter

win = tkinter.Tk()
win.geometry("350x200")

a1 = tkinter.Button(win,text="a1")
# b1 = tkinter.Button(win,text="b1")
img = tkinter.PhotoImage(file="111.png")
label = tkinter.Label(win,image=img)


# b1.grid(row=1,column=1)
a1.place(x=250,y=250)   #그림판으로 좌표 확인할 수 있다.
label.place(x=0,y=0)

a1.lift()

win.mainloop()