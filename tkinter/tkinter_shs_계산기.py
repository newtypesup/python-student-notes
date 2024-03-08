import tkinter as tk


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter 계산기")

        # 배경 이미지 설정
        self.bg_image = tk.PhotoImage(file="rPtksrl.png")
        self.canvas = tk.Canvas(master, width=400, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # 입력 필드 설정
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.entry_var, justify='center', width=20, font=('Arial', 23),
                              relief="solid", bd=4, background="lightgreen")
        self.entry_window = self.canvas.create_window(50, 50, anchor="nw", window=self.entry)

        # 버튼 이미지 설정
        self.button_images = {
            '7': tk.PhotoImage(file="button_7.png",width=50,height=50),
            '8': tk.PhotoImage(file="button_8.png",width=50,height=50),
            '9': tk.PhotoImage(file="button_9.png",width=50,height=50),
            '/': tk.PhotoImage(file="button_divide.png",width=50,height=50),
            '4': tk.PhotoImage(file="button_4.png",width=50,height=50),
            '5': tk.PhotoImage(file="button_5.png",width=50,height=50),
            '6': tk.PhotoImage(file="button_6.png",width=50,height=50),
            '*': tk.PhotoImage(file="button_multiply.png",width=50,height=50),
            '1': tk.PhotoImage(file="button_1.png",width=50,height=50),
            '2': tk.PhotoImage(file="button_2.png",width=50,height=50),
            '3': tk.PhotoImage(file="button_3.png",width=50,height=50),
            '-': tk.PhotoImage(file="button_minus.png",width=50,height=50),
            'C': tk.PhotoImage(file="button_clear.png",width=50,height=50),
            '0': tk.PhotoImage(file="button_0.png",width=50,height=50),
            '=': tk.PhotoImage(file="button_equal.png",width=50,height=50),
            '+': tk.PhotoImage(file="button_plus.png",width=50,height=50),
        }

        # 버튼 설정
        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
        ]

        self.create_buttons()

    def create_buttons(self):
        row = 1
        col = 0
        for button in self.buttons:
            if button in self.button_images:
                img = self.button_images[button]
                btn = tk.Button(self.master, image=img, command=lambda button=button: self.on_click(button),
                                borderwidth=5, background="pink")
            else:
                btn = tk.Button(self.master, text=button, font=('Arial', 20),
                                command=lambda button=button: self.on_click(button))

            btn_window = self.canvas.create_window(50 + col * 100, 150 + row * 100, anchor="nw", window=btn)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_click(self, button):
        # 버튼에서 호출되는 함수로, 버튼의 텍스트를 가져와 입력 필드에 추가한다.
        if button == "C":
            self.entry_var.set("")
        elif button == "=":
            try:
                self.entry_var.set(eval(self.entry_var.get()))
            except Exception as e:
                self.entry_var.set("Error")
        else:
            self.entry_var.set(self.entry_var.get() + button)


root = tk.Tk()
root.geometry("450x700")
app = CalculatorApp(root)
root.mainloop()
