import tkinter as tk
import random
from tkinter import messagebox

class Omok:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omok")
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.draw_board()
        self.turn = 0 # 흑돌: 0, 백돌: 1
        self.board = [[-1] * 15 for _ in range(15)] # -1: 빈 칸, 0: 흑돌, 1: 백돌
        self.canvas.bind("<Button-1>", self.click)
        self.root.mainloop()
        
    def draw_board(self):
        for i in range(14):
            self.canvas.create_line(50 + i * 40, 50, 50 + i * 40, 570)
            self.canvas.create_line(50, 50 + i * 40, 570, 50 + i * 40)
                
    def click(self, event):
        x, y = event.x, event.y
        if x < 30 or y < 30 or x > 570 or y > 570: # 오목판 안을 클릭하지 않은 경우
            return
        col = (x - 38) // 40
        row = (y - 38) // 40
        if self.board[row][col] != -1: # 이미 돌이 놓인 자리를 클릭한 경우
            return
        if self.turn == 0: # 흑돌 차례인 경우
            self.canvas.create_oval(50 + col * 40 - 18, 50 + row * 40 - 18,
                                    50 + col * 40 + 18, 50 + row * 40 + 18, fill="black")
            self.board[row][col] = 0
            if self.check_win(0):
                print("Black wins!")
                self.root.quit()
            self.turn = 1
            self.draw_white() # 하얀돌 자동으로 그리기
        else: # 백돌 차례인 경우
            return # 백돌 차례에서는 아무것도 하지 않음




    def draw_white(self):
        empty_cells = [(i, j) for i in range(14) for j in range(14) if self.board[i][j] == -1]
        if not empty_cells:
            return
        best_move = self.find_best_move(1, 5)
        if not best_move:
            best_move = self.find_best_move(0, 4)  # 전략 2: 상대방이 4개를 연속으로 만드는 위치 방어
        if not best_move:
            best_move = self.find_best_move(0, 3) # 전략 3: 상대방이 3개를 연속으로 만드는 위치 방어          
        if not best_move:
            best_move = self.find_best_move(1, 4)
        if not best_move:
            best_move = self.find_best_move(1, 3)
        if not best_move:
            black_cells = []
            for i, j in empty_cells:
                for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    ni, nj = i + di, j + dj
                    if ni < 0 or ni >= 14 or nj < 0 or nj >= 14:
                        continue
                    if self.board[ni][nj] == 0:
                        black_cells.append((i, j))
                        break
            if not black_cells:
                row, col = random.choice(empty_cells)
            else:
                row, col = random.choice(black_cells)
        else:
            row, col = best_move
        self.canvas.after(300, lambda: self.canvas.create_oval(50 + col * 40 - 18, 50 + row * 40 - 18,
                                    50 + col * 40 + 18, 50 + row * 40 + 18, fill="white"))
        self.board[row][col] = 1
        if self.check_win(1):
            print("White wins!")
            self.root.quit()
        self.turn = 0

    def find_best_move(self, color, num_to_win):
        for i in range(14):
            for j in range(14):
                if self.board[i][j] == -1:
                    for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        for offset in range(num_to_win):
                            cnt = 0
                            for k in range(num_to_win):
                                ni, nj = i + di * (k - offset), j + dj * (k - offset)
                                if ni < 0 or ni >= 14 or nj < 0 or nj >= 14:
                                    break
                                if self.board[ni][nj] == color:
                                    cnt += 1
                                elif self.board[ni][nj] != -1:
                                    cnt = 0
                                    break
                            if cnt == num_to_win - 1:
                                if color == 0 and (num_to_win == 4 or num_to_win == 3):
                                    #양쪽을 모두 방어
                                    ni_prev, nj_prev = i - di, j - dj
                                    ni_next, nj_next = i + di * num_to_win, j + dj * num_to_win
                                    if (ni_prev < 0 or ni_prev >= 14 or nj_prev < 0 or nj_prev >= 14 or self.board[ni_prev][nj_prev] == -1) and \
                                       (ni_next < 0 or ni_next >= 14 or nj_next < 0 or nj_next >= 14 or self.board[ni_next][nj_next] == -1):
                                        continue
                                    return i, j
        return None
                                         
    def check_win(self, color):
        for i in range(14):
            for j in range(14):
                if self.board[i][j] == color:
                    # 가로로 승리하는 경우
                    if j + 4 < 14 and self.board[i][j+1] == color and self.board[i][j+2] == color and self.board[i][j+3] == color and self.board[i][j+4] == color:
                        if color == 0:
                            tk.messagebox.showinfo("게임 종료", "Black wins!")
                        else:
                            tk.messagebox.showinfo("게임 종료", "White wins!")
                        return True
                    # 세로로 승리하는 경우
                    if i + 4 < 14 and self.board[i+1][j] == color and self.board[i+2][j] == color and self.board[i+3][j] == color and self.board[i+4][j] == color:
                        if color == 0:
                            tk.messagebox.showinfo("게임 종료", "Black wins!")
                        else:
                            tk.messagebox.showinfo("게임 종료", "White wins!")
                        return True
                    # 대각선으로 승리하는 경우 (왼쪽 상단에서 오른쪽 하단으로)
                    if i + 4 < 14 and j + 4 < 14 and self.board[i+1][j+1] == color and self.board[i+2][j+2] == color and self.board[i+3][j+3] == color and self.board[i+4][j+4] == color:
                        if color == 0:
                            tk.messagebox.showinfo("게임 종료", "Black wins!")
                        else:
                            tk.messagebox.showinfo("게임 종료", "White wins!")
                        return True
                    # 대각선으로 승리하는 경우 (오른쪽 상단에서 왼쪽 하단으로)
                    if i + 4 < 14 and j - 4 >= 0 and self.board[i+1][j-1] == color and self.board[i+2][j-2] == color and self.board[i+3][j-3] == color and self.board[i+4][j-4] == color:
                        if color == 0:
                            tk.messagebox.showinfo("게임 종료", "Black wins!")
                        else:
                            tk.messagebox.showinfo("게임 종료", "White wins!")
                        return True
        return False
        


if __name__ == '__main__':
    omok = Omok()