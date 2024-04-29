import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import hashlib
import json
from time import time

class Block:
    def __init__(self, index, previous_hash, moves, player_stone_color, computer_stone_color, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.moves = moves
        self.player_stone_color = player_stone_color
        self.computer_stone_color = computer_stone_color 
        self.timestamp = timestamp or time()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], "", "")
        self.chain.append(genesis_block)

    def add_block(self, moves, player_stone_color, computer_stone_color):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.compute_hash(), moves, player_stone_color, computer_stone_color)
        self.chain.append(new_block)
        print(f"Block added: {new_block.__dict__}")

class OmokGame(tk.Canvas):
    WINNING_CONDITION = 5
    COMPUTER_TRUN_CNT = 0
    game_mode = 1
    
    def __init__(self, master=None, rows=15, columns=15, cell_size=60, board_color='#c29436', player_color='black', computer_color='white', **kwargs):
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
        self.computer_dropped_stones = 0
        
        self.image_dir = "C:\\PY_study\\stone_images"
        self.stone_images = [filename for filename in os.listdir(self.image_dir) if filename.endswith(".png")]
        self.player_stone_imgs = [ImageTk.PhotoImage(Image.open(os.path.join(self.image_dir, img))) for img in self.stone_images if img.startswith('black')]
        self.computer_stone_imgs = [ImageTk.PhotoImage(Image.open(os.path.join(self.image_dir, img))) for img in self.stone_images if img.startswith('white')]
        
        self.blockchain = Blockchain()
        
        super().__init__(master, width=self.width, height=self.height, **kwargs)
        self.draw_board()
        self.bind('<Button-1>', self.click_handler)
        self.setup_menu()
        
    def setup_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        menu_bar.add_command(label="새로 고침",command=self.reset_game)
        menu_bar.add_command(label="기본 게임", command=self.p_game)
        menu_bar.add_command(label="랜덤 게임", command=self.p_game)
        menu_bar.add_command(label="게임 종료", command=self.master.quit)
        
    def p_game(self):
        if self.game_mode == 1:
            self.game_mode = 2
            self.reset_game()
            
        elif self.game_mode == 2:
            self.game_mode = 1
            self.reset_game()
        
    def draw_board(self):
        self.create_rectangle(0,0,900,900, outline='', fill=self.board_color)
        for i in range(13):
                    self.create_line(30 + (i+1) * 60, 30, 30 + (i+1) * 60, 870, fill='black', width=2)
                    self.create_line(30, 30 + (i+1) * 60, 870, 30 + (i+1) * 60, fill='black', width=2)
        self.create_line(30, 29, 30, 871, fill='black', width=4)
        self.create_line(450, 30, 450, 870, fill='black', width=3)
        self.create_line(870, 29, 870, 871, fill='black', width=4)
        self.create_line(29, 30, 871, 30, fill='black', width=4)
        self.create_line(30, 450, 870, 450, fill='black', width=3)
        self.create_line(29, 870, 871, 870, fill='black', width=4)

    def click_handler(self, event):
        if self.turn == 'O':
            col = event.x // self.cell_size
            row = event.y // self.cell_size

            if self.board[row][col] == '':
                self.draw_piece(row, col, self.player_color)
                self.board[row][col] = 'O'

                if self.check_win(row, col, 'O', self.WINNING_CONDITION):
                    print("플레이어 승리!")
                    self.end_game_message("O")
                    return
                
                self.computer_move()
                
    def computer_move(self):
        self.COMPUTER_TRUN_CNT += 1
        self.computer_DefendAndAttack()
        moves = self.get_moves()
        self.blockchain.add_block(moves, self.player_color, self.computer_color)
        
    def computer_DefendAndAttack(self):
        self.COMPUTER_TRUN_CNT += 1
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        print("컴퓨터 승리!")
                        self.end_game_message("X")
                        return
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-1):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''        
            
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    if self.check_win(i, j, 'O', self.WINNING_CONDITION - 1):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
                    
        for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] == '':
                        if self.check_win(i, j, 'X', self.WINNING_CONDITION-2):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
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
                        self.board[i][j] = 'O'
                        if self.check_win(i, j, 'O', 2):
                            self.board[i][j] = 'X'
                            self.draw_piece(i, j, self.computer_color)
                            return True
                        self.board[i][j] = ''
                        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '':
                    self.board[i][j] = 'X'
                    if self.check_win(i, j, 'X', self.WINNING_CONDITION-3):
                        self.board[i][j] = 'X'
                        self.draw_piece(i, j, self.computer_color)
                        return True
                    self.board[i][j] = ''
            
    def draw_piece(self, row, col, color):
        if self.game_mode == 1:
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            radius = self.cell_size // 2 - 2
            self.create_oval(x - radius, y - radius, x + radius, y + radius, outline='black', fill=color)
        elif self.game_mode == 2:
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            
            if color == 'black':
                    stone_img = random.choice(self.player_stone_imgs)
            elif color == 'white':
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
    
    def get_moves(self):
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != '':
                    moves.append((i, j))
        return moves

    def reset_game(self):
        self.delete('all')
        self.board = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.draw_board()
        self.turn = 'O'
        self.COMPUTER_TRUN_CNT = 0
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
    root.title("Omok Game")
    root.geometry("950x950")

    omok_game = OmokGame(root)
    omok_game.pack()
    omok_game.place(relx=0.5, rely=0.5, anchor="center")
    
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 4 - window_width / 4)
    position_down = int(root.winfo_screenheight() / 12 - window_height / 4)
    root.geometry(f"+{position_right}+{position_down}")

    root.mainloop()