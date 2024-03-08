import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class OmokGame_2(tk.Canvas):
    WINNING_CONDITION = 5
    COMPUTER_TRUN_CNT = 0
    
    def __init__(self, master=None, rows=15, columns=15, cell_size=60, board_color='#8B4513', player_color='black', computer_color='white', **kwargs):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.board_color = board_color
        self.player_color = player_color
        self.computer_color = computer_color
        self.width = columns * cell_size
        self.height = rows * cell_size
        self.board = [['' for _ in range(columns)] for _ in range(rows)]
        for _ in range(rows):
            row = ['' for _ in range(columns)]
        self.board.append(row)
        self.turn = 'O'
        self.computer_dropped_stones = 0
        
        self.image_dir = "stone_images"
        # 돌 이미지들의 파일명 리스트
        self.stone_images = [filename for filename in os.listdir(self.image_dir) if filename.endswith(".png")]
        # 플레이어와 컴퓨터 돌 이미지
        self.player_stone_imgs = [ImageTk.PhotoImage(Image.open(os.path.join(self.image_dir, img))) for img in self.stone_images if img.startswith('black')]
        self.computer_stone_imgs = [ImageTk.PhotoImage(Image.open(os.path.join(self.image_dir, img))) for img in self.stone_images if img.startswith('white')]

        super().__init__(master, width=self.width, height=self.height, **kwargs)
        self.draw_board()
        self.bind('<Button-1>', self.click_handler)
        
    #보드 판 생성 
    def draw_board(self):
        self.create_rectangle(0,0,900,900, outline='', fill=self.board_color)
        #세로
        self.create_line(30, 30, 30, 870, fill='black', width=4)
        self.create_line(90, 30, 90, 870, fill='black', width=2)
        self.create_line(150, 30, 150, 870, fill='black', width=2)
        self.create_line(210, 30, 210, 870, fill='black', width=2)
        self.create_line(270, 30, 270, 870, fill='black', width=2)
        self.create_line(330, 30, 330, 870, fill='black', width=2)
        self.create_line(390, 30, 390, 870, fill='black', width=2)
        self.create_line(450, 30, 450, 870, fill='black', width=2)
        self.create_line(510, 30, 510, 870, fill='black', width=2)
        self.create_line(570, 30, 570, 870, fill='black', width=2)
        self.create_line(630, 30, 630, 870, fill='black', width=2)
        self.create_line(690, 30, 690, 870, fill='black', width=2)
        self.create_line(750, 30, 750, 870, fill='black', width=2)
        self.create_line(810, 30, 810, 870, fill='black', width=2)
        self.create_line(870, 30, 870, 870, fill='black', width=4)
        #가로
        self.create_line(30, 30, 870, 30, fill='black', width=4)
        self.create_line(30, 90, 870, 90, fill='black', width=2)
        self.create_line(30, 150, 870, 150, fill='black', width=2)
        self.create_line(30, 210, 870, 210, fill='black', width=2)
        self.create_line(30, 270, 870, 270, fill='black', width=2)
        self.create_line(30, 330, 870, 330, fill='black', width=2)
        self.create_line(30, 390, 870, 390, fill='black', width=2)
        self.create_line(30, 450, 870, 450, fill='black', width=2)
        self.create_line(30, 510, 870, 510, fill='black', width=2)
        self.create_line(30, 570, 870, 570, fill='black', width=2)
        self.create_line(30, 630, 870, 630, fill='black', width=2)
        self.create_line(30, 690, 870, 690, fill='black', width=2)
        self.create_line(30, 750, 870, 750, fill='black', width=2)
        self.create_line(30, 810, 870, 810, fill='black', width=2)
        self.create_line(30, 870, 870, 870, fill='black', width=4)
    
    def click_handler(self, event):
        if self.turn == 'O':
            # 클릭한 곳의 가까운 행과 열의 인덱스를 구한다.
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if self.board[row][col] == '':
                self.draw_piece(row, col, self.player_color)
                self.board[row][col] = 'O'
                if self.check_win(row, col, 'O', self.WINNING_CONDITION):
                    print("Player wins!")
                    # 승자 메시지 표시
                    self.end_game_message("O")
                    self.reset_game()
                    return
                self.computer_move()
                
    def computer_move(self):
        # 컴퓨터의 방어 동작과 공격 동작을 분리
        self.computer_DefendAndAttack()
        # for i in self.board:
        #     print(i)
        self.turn = 'O'
        
    def computer_DefendAndAttack(self):
        self.COMPUTER_TRUN_CNT += 1
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 공격 : (다음 턴에 컴퓨터가 5개가 완성된다면 공격)
                    self.board[i][j] == 'X'
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        print("컴퓨터 승리!")
                        # 승자 메시지 표시
                        self.end_game_message("X")
                        self.reset_game()
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 방어 : (다음 턴에 사용자가 5개 일때 방어)
                    self.board[i][j] == 'O'
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 공격 : (다음 턴에 컴퓨터가 4개가 완성된다면 공격)
                    self.board[i][j] == 'X'
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-1):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
            
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 방어: 다음 턴에 사용자가 4개 일때 방어)
                    if not self.check_user_threat(i,j,'O',self.WINNING_CONDITION - 2):
                        self.board[i][j] = 'O'
                        if self.check_win(i, j, 'O', self.WINNING_CONDITION - 1):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''
                    
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 방어: 사용자의 3개를 막기
                    self.board[i][j] = 'O'
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION - 2):
                        if self.check_user_threat(i,j,'O',self.WINNING_CONDITION - 2): #한쪽이 막혀 있다면 공격
                            
                            for x in range(self.rows):
                                for z in range(self.columns):
                                        # 공격 : (다음 턴에 컴퓨터가 3개가 완성된다면 공격)
                                        self.board[x][z] == 'X'
                                        if self.check_win(x, z, 'X', self.WINNING_CONDITION-2):
                                            self.board[x][z] = 'X'
                                            self.draw_piece(x, z, self.computer_color)
                                            return True
                            
                            for x in range(self.rows):
                                for z in range(self.columns):
                                        # 공격 : (다음 턴에 컴퓨터가 2개가 완성된다면 공격)
                                        self.board[x][z] == 'X'
                                        if self.check_win(x, z, 'X', self.WINNING_CONDITION-3):
                                            self.board[x][z] = 'X'
                                            self.draw_piece(x, z, self.computer_color)
                                            return True
                                        
                            else:
                                self.board[i][j] = 'X'
                                self.draw_piece(i, j, self.computer_color)
                                return True
                    self.board[i][j] = ''
                    
        if self.COMPUTER_TRUN_CNT == 1 or self.COMPUTER_TRUN_CNT == 2:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] == '':
                        # 방어: 사용자의 2개를 막기
                        self.board[i][j] = 'O'
                        if self.check_win(i, j, 'O', 2):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 공격 : (다음 턴에 컴퓨터가 3개가 완성된다면 공격)
                    self.board[i][j] == 'X'
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-2):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
                        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 공격 : (다음 턴에 컴퓨터가 2개가 완성된다면 공격)
                    self.board[i][j] == 'X'
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-3):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
            
    # 바둑 돌 생성
    def draw_piece(self, row, col, color):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        if color == 'black':
            stone_img = random.choice(self.player_stone_imgs)
        else:
            stone_img = random.choice(self.computer_stone_imgs)
        self.create_image(x, y, image=stone_img)
        
    def check_win(self, row, col, player, count_needed):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for i in range(1, count_needed):
                r = row + i * dr
                c = col + i * dc
                if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == player:
                    count += 1
                else:
                    break

            for i in range(1, count_needed):
                r = row - i * dr
                c = col - i * dc
                if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == player:
                    count += 1
                else:
                    break
            
            if count >= count_needed:
                return True
            
        return False

    def check_user_threat(self, row, col, player, count_needed):
        # 승리 여부 확인하는 메서드
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            open_ends = 0  # 사용자 돌 사이의 열린 공간 개수
            blocked_ends = 0  # 사용자 돌 사이의 막힌 공간 개수

            for i in range(1, count_needed):
                r = row + i * dr
                c = col + i * dc

                if 0 <= r < self.rows and 0 <= c < self.columns:
                    if self.board[r][c] == player:
                        count += 1
                    elif self.board[r][c] == '':
                        open_ends += 1
                    else:
                        blocked_ends += 1
                else:
                    blocked_ends += 1

            for i in range(1, count_needed):
                r = row - i * dr
                c = col - i * dc

                if 0 <= r < self.rows and 0 <= c < self.columns:
                    if self.board[r][c] == player:
                        count += 1
                    elif self.board[r][c] == '':
                        open_ends += 1
                    else:
                        blocked_ends += 1
                else:
                    blocked_ends += 1

            if count == count_needed - 1 and open_ends == 1 and blocked_ends == 1:
                return True

        return False

    def reset_game(self):
        self.delete('all')
        self.board = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.draw_board()
        self.turn = '0'
        self.computer_dropped_stones = 0
        
    def end_game_message(self, winner):
        if winner == 'O':
            message = "플레이어 승리!"
        elif winner == 'X':
            message = "컴퓨터 승리!"
        else:
            message = "무승부!"

        messagebox.showinfo("Game Over", message)
        self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Omok Game_2")
    root.geometry("950x950")

    omok_game = OmokGame_2(root)
    omok_game.pack()
    omok_game.place(relx=0.5, rely=0.5, anchor="center")
    
    # 화면 중앙에 창 배치
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 4 - window_width / 4)
    position_down = int(root.winfo_screenheight() / 10 - window_height / 10)
    root.geometry(f"+{position_right}+{position_down}")

    root.mainloop()