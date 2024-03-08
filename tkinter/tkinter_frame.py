import tkinter

win=tkinter.Tk()
win.geometry("650x480")

area1 = tkinter.Frame(win,relief="solid",bd=2)
area1.pack(side="left",expand=True,fill="both")
area2 = tkinter.Frame(win,relief="solid",bd=2)
area2.pack(side="right",expand=True,fill="both")

bt1 = tkinter.Button(area1,text="버튼1")
bt1.pack(anchor="e")
bt2 = tkinter.Button(area2,text="버튼2")
bt2.pack(side="left")


win.mainloop()