import tkinter

windows = tkinter.Tk()
windows.geometry("200x180")
windows.resizable(False,False)

var_1 = tkinter.IntVar()
var_2 = tkinter.IntVar()
var_3 = tkinter.IntVar()

def flash():
    
    Chk_bt_1.flash()



Chk_bt_1 = tkinter.Checkbutton(windows,text = "O",variable=var_1)
Chk_bt_2 = tkinter.Checkbutton(windows,text = "X",variable=var_2)
Chk_bt_3 = tkinter.Checkbutton(windows,text = "△",variable=var_3,command=flash)


Chk_bt_1.pack()
Chk_bt_2.pack()
Chk_bt_3.pack()

windows.mainloop()

