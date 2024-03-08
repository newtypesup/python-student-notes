import tkinter

window = tkinter.Tk()
window.geometry("600x400")

#line,arc,polygon,oval
canvas = tkinter.Canvas(window,relief="solid",bd=2)
#체킹 표시
line = canvas.create_line(10,10,50,50,100,30,fill="red",width=10)

#반달
arc = canvas.create_arc(100,100,300,300,start=0,extent=150,fill="yellow")

#다각형
polygon = canvas.create_polygon(50,50,300,50,150,150,fill="blue")

#원형
oval = canvas.create_oval(10,200,150,250,fill="pink")

canvas.pack()

window.mainloop()