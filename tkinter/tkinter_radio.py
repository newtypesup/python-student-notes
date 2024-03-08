import tkinter
win = tkinter.Tk()
win.geometry("200x230")



def check():
    label.config(text = " Radio_Var_1 = " + str(Radio_Var_1.get()) + "\n" +
                        " Radio_Var_2 = " + str(Radio_Var_2.get()) + "\n\n" +
                        " Tatal = " + str(Radio_Var_1.get() + Radio_Var_2.get())
                 
                 
                 
                 )
Radio_Var_1 = tkinter.IntVar()
Radio_Var_2 = tkinter.IntVar()


radio1 = tkinter.Radiobutton(win,text="1번",variable=Radio_Var_1,value=3,command=check)
radio1.pack()
radio2 = tkinter.Radiobutton(win,text="2번(1번)",variable=Radio_Var_1,value=3,command=check)
radio2.pack()
radio3 = tkinter.Radiobutton(win,text="3번",variable=Radio_Var_1,value=9,command=check)
radio3.pack()
label = tkinter.Label(win,text="wait",height=5)
label.pack()

radio4 = tkinter.Radiobutton(win,text="4번",variable=Radio_Var_2,value=13,command=check)
radio4.pack()
radio5 = tkinter.Radiobutton(win,text="5번",variable=Radio_Var_2,value=17,command=check)
radio5.pack()

win.mainloop()