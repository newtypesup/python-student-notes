import tkinter
win = tkinter.Tk()
win.geometry("350x200")

#sticky(anchor) = e,w,s,n,ns,se,sw,nw = 위치

a1 = tkinter.Button(win,text="(0,0)",width=10)
a2 = tkinter.Button(win,text="(1,1)",height=5)
a3 = tkinter.Button(win,text="(0,1)",width=10)
a4 = tkinter.Button(win,text="(1,4)")
a5 = tkinter.Button(win,text="(2,3)")


a1.grid(row=0,column=0)
a2.grid(row=1,column=1,sticky="w")
a3.grid(row=0,column=1)
a4.grid(row=1,column=4)
a5.grid(row=2,column=3)

win.mainloop()