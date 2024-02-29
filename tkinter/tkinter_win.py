import tkinter

window = tkinter.Tk()

window.geometry("300x500+200+500")  #너비 x 높이 + 가로 좌표 +세로 좌표
window.resizable(False,False)   #크기 조정(너비,높이) 고정

lb = tkinter.Label(window,text="Hello~\n Tkinter")
lb.pack()
lb2 = tkinter.Label(window,text="곧 쉬는시간입니다")
lb2.pack()


window.mainloop()
