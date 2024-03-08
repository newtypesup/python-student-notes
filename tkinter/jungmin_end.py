import tkinter as tk
from tkinter import messagebox



class OmokGame(tk.Canvas):
    WINNING_CONDITION = 5
    COMPUTER_TRUN_CNT = 0
    
    def __init__(self, master=None, rows=19, columns=19, cell_size=40, board_color='#8B4513', player_color='black', computer_color='white', **kwargs):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.board_color = board_color
        self.player_color = player_color
        self.computer_color = computer_color
        self.width = columns * cell_size
        self.height = rows * cell_size
        self.board = []
        for _ in range(rows):
            row = ['' for _ in range(columns)]
            self.board.append(row)
        self.turn = 'O'

        super().__init__(master, width=self.width, height=self.height, **kwargs)
        self.draw_board()
        self.bind('<Button-1>', self.click_handler)
        self.setup_menu()
        
    def setup_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)
        
    #보드 판 생성 
    def draw_board(self):
        self.create_rectangle(0,0,760,760, outline='', fill=self.board_color)
        self.create_line(20, 20, 20, 740, fill='black', width=3)
        self.create_line(60, 20, 60, 740, fill='black', width=2)
        self.create_line(100, 20, 100, 740, fill='black', width=2)
        self.create_line(140, 20, 140, 740, fill='black', width=2)
        self.create_line(180, 20, 180, 740, fill='black', width=2)
        self.create_line(220, 20, 220, 740, fill='black', width=2)
        self.create_line(260, 20, 260, 740, fill='black', width=2)
        self.create_line(300, 20, 300, 740, fill='black', width=2)
        self.create_line(340, 20, 340, 740, fill='black', width=2)
        self.create_line(380, 20, 380, 740, fill='black', width=2)
        self.create_line(420, 20, 420, 740, fill='black', width=2)
        self.create_line(460, 20, 460, 740, fill='black', width=2)
        self.create_line(500, 20, 500, 740, fill='black', width=2)
        self.create_line(540, 20, 540, 740, fill='black', width=2)
        self.create_line(580, 20, 580, 740, fill='black', width=2)
        self.create_line(620, 20, 620, 740, fill='black', width=2)
        self.create_line(660, 20, 660, 740, fill='black', width=2)
        self.create_line(700, 20, 700, 740, fill='black', width=2)
        self.create_line(740, 20, 740, 740, fill='black', width=3)
        self.create_line(20, 20, 740, 20, fill='black', width=3)
        self.create_line(20, 60, 740, 60, fill='black', width=2)
        self.create_line(20, 100, 740, 100, fill='black', width=2)
        self.create_line(20, 140, 740, 140, fill='black', width=2)
        self.create_line(20, 180, 740, 180, fill='black', width=2)
        self.create_line(20, 220, 740, 220, fill='black', width=2)
        self.create_line(20, 260, 740, 260, fill='black', width=2)
        self.create_line(20, 300, 740, 300, fill='black', width=2)
        self.create_line(20, 340, 740, 340, fill='black', width=2)
        self.create_line(20, 380, 740, 380, fill='black', width=2)
        self.create_line(20, 420, 740, 420, fill='black', width=2)
        self.create_line(20, 460, 740, 460, fill='black', width=2)
        self.create_line(20, 500, 740, 500, fill='black', width=2)
        self.create_line(20, 540, 740, 540, fill='black', width=2)
        self.create_line(20, 580, 740, 580, fill='black', width=2)
        self.create_line(20, 620, 740, 620, fill='black', width=2)
        self.create_line(20, 660, 740, 660, fill='black', width=2)
        self.create_line(20, 700, 740, 700, fill='black', width=2)
        self.create_line(20, 740, 740, 740, fill='black', width=3)
                

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
        # 컴퓨터의 방어 동작과 공격 동작
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
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 공격 : (다음 턴에 컴퓨터가 4개가 완성된다면 공격)
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-1):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''        
            
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 방어: 다음 턴에 사용자가 4개 일때 방어)
                        self.board[i][j] = 'O'
                        if self.check_win(i, j, 'O', self.WINNING_CONDITION - 1):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''
                    
        for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] == '':
                        # 공격 : (다음 턴에 컴퓨터가 3개가 완성된다면 공격)
                        if self.check_win(i, j, 'X', self.WINNING_CONDITION-2):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''


        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    # 방어: 다음 턴에 사용자가 3개 일때 방어)
                    self.board[i][j] = 'O'
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION - 2):
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
        self.create_oval(x - radius, y - radius, x + radius, y + radius, outline='black', fill=color)

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


    def reset_game(self):
        self.delete('all')
        self.board = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.draw_board()
        self.turn = 'O'
        self.COMPUTER_TRUN_CNT = 0
        
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
    root.title("Omok Game")
    root.geometry("800x800")

    omok_game = OmokGame(root)
    omok_game.pack()
    omok_game.place(relx=0.5, rely=0.5, anchor="center")
    
        # 화면 중앙에 창 배치
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 3 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 5 - window_height / 4)
    root.geometry(f"+{position_right}+{position_down}")

    root.mainloop()