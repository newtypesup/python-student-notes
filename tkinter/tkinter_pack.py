import tkinter
import PIL  #cmd에서 PIL을 설치해야함.(pip install pillow 입력)
from PIL import ImageTk,Image

windows = tkinter.Tk()
windows.geometry("640x480")

btn1 = tkinter.Button(windows,text="btn1")
btn2 = tkinter.Button(windows,text="btn2")
btn3 = tkinter.Button(windows,text="btn3")
btn4 = tkinter.Button(windows,text="btn4")

img = Image.open("111.png")
img_re = img.resize((400,400))
img_fix = ImageTk.PhotoImage(img_re)
ct = tkinter.Button(windows,image=img_fix)

left_btn = tkinter.Button(windows,text="left")

#side = 바깥쪽(top,bottom,left,right) = 방향
#anchor = center,e,w,s,n,ne,se,sw,ne = 위치
#fill = 채우기(none,x,y,both)
#expand = 사용허지 않은 모든 부분 채우기

btn1.pack()
btn4.pack(side="bottom",fill="both")
btn2.pack(side="left",fill="both")
btn3.pack(side="right",anchor="n")
ct.pack(expand=True,fill="both")
left_btn.pack(side="left")


windows.mainloop()