import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import random
from tkinter import PhotoImage


class OmokGame(tk.Tk):
    # 클래스 변수로 승패 기록을 관리합니다.
    win_count = {"흑돌": 0, "백돌": 0}

    def __init__(self):
        super().__init__()
        self.title("Omok Game")  # 윈도우 제목 설정
        self.geometry("300x200")  # 윈도우 크기 설정
        self.create_widgets()  # 위젯 생성
        

    def create_widgets(self):
        self.image = PhotoImage(file="qkenr.png")
        
        bgbg = tk.Button(self, image=self.image,width=300,height=300,state="disabled")
        bgbg.place(x=0,y=0)
        
        # 오목 게임 시작 버튼
        start_button = tk.Button(self, text="사람 VS 사람", command=self.start_game)
        start_button.pack(pady=20)
        
        # 추가된 버튼: 오목 게임 시작 1
        start_button_1 = tk.Button(self, text="사람 VS COM", command=self.start_game_1)
        start_button_1.pack(pady=10)
        
        

    def start_game(self):
        self.destroy()  # 현재 윈도우 종료
        app = OmokGameWindow()  # 오목 게임 창 열기

    def start_game_1(self):
        self.destroy()  # 현재 윈도우 종료
        app = OmokGameAI()  # 오목 게임 창 열기

class OmokGameWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Omok Game")  # 윈도우 제목 설정
        self.canvas_size = 600
        self.board_size = 20
        self.cell_size = self.canvas_size // (self.board_size - 1)
        self.timer_interval = 1000  # 타이머 갱신 간격 (밀리초)
        self.time_limit = 5  # 시간 제한 (초)
        self.geometry(f"{self.canvas_size+500}x{self.canvas_size+100}")  # 윈도우 크기 설정
        self.create_widgets()  # 위젯 생성
        self.is_timer_running = True  # 타이머 상태를 나타내는 플래그
        self.start_game()  # 게임 시작
        self.timeout_message_shown = False  # 시간 초과 메시지 박스가 표시되었는지 여부를 나타내는 플래그
        self.timeout_count = 0  # 시간 초과가 발생한 횟수를 추적하는 변수

    def create_widgets(self):
        # 오목판 그리기
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="white")  # 캔버스 생성
        self.canvas.pack(side=tk.LEFT)

        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size*i, 0, self.cell_size*i, self.canvas_size, fill="black")  # 수직 선 그리기
            self.canvas.create_line(0, self.cell_size*i, self.canvas_size, self.cell_size*i, fill="black")  # 수평 선 그리기

        self.canvas.bind("<Button-1>", self.place_piece)  # 마우스 클릭 이벤트 바인딩

        # 타이머 표시 네모 박스
        self.timer_frame = tk.Frame(self, width=200, height=self.canvas_size, bg="lightgray")
        self.timer_frame.pack(side=tk.RIGHT)

        # 타이머 라벨
        self.timer_label = tk.Label(self.timer_frame, text=f"Time left: {self.time_limit:02d}", font=("Arial", 12), bg="lightgray")
        self.timer_label.pack(side=tk.TOP, padx=10, pady=10)

        # 승패 기록 라벨
        self.result_label = tk.Label(self.timer_frame, text=f"승점: 흑 - {OmokGame.win_count['흑돌']} | 백 - {OmokGame.win_count['백돌']}",
                                     font=("Arial", 12), bg="lightgray")
        self.result_label.pack(side=tk.TOP, padx=10, pady=10)

        # 무르기 버튼
        self.undo_button = tk.Button(self.timer_frame, text="무르기", command=self.undo_move)
        self.undo_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 새로운 게임 시작 버튼
        self.new_game_button = tk.Button(self.timer_frame, text="새로운 게임 시작", command=self.restart_btn)
        self.new_game_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 홈 버튼
        self.home_button = tk.Button(self.timer_frame, text="홈", command=self.go_to_home)
        self.home_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # 타이머 정지 버튼
        self.stop_timer_button = tk.Button(self.timer_frame, text="타이머 정지", command=self.stop_timer)
        self.stop_timer_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 타이머 시작 버튼
        self.start_timer_button = tk.Button(self.timer_frame, text="타이머 시작", command=self.start_timer)
        self.start_timer_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def start_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]  # 오목판 초기화
        self.moves = []  # 플레이어의 돌을 저장할 리스트
        self.current_player = "흑돌"  # 현재 플레이어 초기화
        self.start_time = datetime.now()  # 게임 시작 시간 기록
        self.update_timer()  # 타이머 업데이트

    def place_piece(self, event):
        col = round(event.x / self.cell_size)  # 클릭 위치를 열로 변환
        row = round(event.y / self.cell_size)  # 클릭 위치를 행으로 변환

        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':  # 클릭한 위치에 돌이 없는 경우
            self.board[row][col] = self.current_player  # 돌을 놓음
            self.moves.append((row, col))  # 플레이어의 돌 위치 저장
            self.draw_piece(row, col)  # 돌 그리기 함수 호출

            if self.check_win(row, col):  # 승리 조건 확인
                messagebox.showinfo("Game Over", f"승자는 {self.current_player} 입니다")  # 메시지 창 표시
                self.update_win_count(self.current_player)  # 승리 횟수 업데이트
                self.restart_game()  # 게임 리셋
                return

            self.start_time = datetime.now()  # 현재 플레이어의 턴이 끝났으므로 시간 재설정
            self.update_timer()  # 타이머 업데이트

            # 플레이어 교체
            if self.current_player == "흑돌":
                self.current_player = "백돌"
            else:
                self.current_player = "흑돌"

    def draw_piece(self, row, col):
        x = col * self.cell_size  # 돌의 x 좌표 계산
        y = row * self.cell_size  # 돌의 y 좌표 계산
        color = "black" if self.current_player == "흑돌" else "white"  # 돌의 색상 결정
        piece_tag = f"piece_{row}_{col}"  # 각 돌에 대한 태그 생성
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags=piece_tag)  # 돌 그리기

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향
        for dr, dc in directions:
            count = 1
            r, c = row, col
            for _ in range(4):
                r, c = r + dr, c + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            r, c = row, col
            for _ in range(4):
                r, c = r - dr, c - dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def update_timer(self):
        if self.is_timer_running:
            elapsed_time = datetime.now() - self.start_time
            remaining_time = timedelta(seconds=self.time_limit) - elapsed_time
            if remaining_time <= timedelta(0) and not self.timeout_message_shown:  # 시간 초과 및 메시지 박스가 표시되지 않은 경우
                self.timer_label.config(text="시간 초과!!")
                self.update_win_count(self.get_opponent_player())  # 시간 초과로 패한 플레이어의 승리 횟수 업데이트
                self.timeout_message_shown = True  # 메시지 박스가 표시되었음을 표시
                messagebox.showinfo("Game Over", f"승자는 {self.get_opponent_player()} 입니다")
                self.restart_game()
                return
            else:
                self.timer_label.config(text=f"초 읽기: {remaining_time.seconds:02d}")
        self.after(self.timer_interval, self.update_timer)

    def undo_move(self):
        if self.moves:
            last_move_row, last_move_col = self.moves.pop()  # 마지막으로 놓은 돌 위치 가져오기
            self.board[last_move_row][last_move_col] = ' '  # 오목판에서 해당 돌 삭제
            piece_tag = f"piece_{last_move_row}_{last_move_col}"  # 삭제할 돌의 태그
            self.canvas.delete(piece_tag)  # 캔버스에서 해당 돌 삭제
            self.start_time = datetime.now()
            self.update_timer()
            # 마지막 플레이어 교체
            if self.current_player == "흑돌":
                self.current_player = "백돌"
            else:
                self.current_player = "흑돌"

    def update_win_count(self, winner):
        # 현재 게임에서 승리한 플레이어의 승리 횟수를 업데이트합니다.
        if not self.timeout_message_shown:  # 시간 초과 메시지가 표시되지 않은 경우에만 점수를 업데이트합니다.
            OmokGame.win_count[winner] += 1

    def restart_game(self):
        self.destroy()  # 현재 윈도우 종료
        app = OmokGameWindow()  # 새로운 게임 시작
        app.mainloop()  # 새로운 게임 창 열기

    def restart_btn(self):
        # 현재 윈도우 종료
        self.destroy()
        # 승점 초기화
        OmokGame.win_count = {"흑돌": 0, "백돌": 0}
        # 새로운 게임 시작
        app = OmokGameWindow()
        app.mainloop()  # 새로운 게임 창 열기

    def go_to_home(self):
        # 현재 윈도우 종료
        # 홈 화면으로 돌아가기
        self.destroy()
        app = OmokGame()
        app.mainloop()

    def get_opponent_player(self):
        # 현재 플레이어의 상대 플레이어를 반환합니다.
        if self.current_player == "흑돌":
            return "백돌"
        else:
            return "흑돌"

    def start_timer(self):
        self.is_timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.is_timer_running = False

class OmokGameAI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Omok Game")  # 윈도우 제목 설정
        self.canvas_size = 600
        self.board_size = 20
        self.cell_size = self.canvas_size // (self.board_size - 1)
        self.timer_interval = 1000  # 타이머 갱신 간격 (밀리초)
        self.time_limit = 20  # 시간 제한 (초)
        self.geometry(f"{self.canvas_size+500}x{self.canvas_size+100}")  # 윈도우 크기 설정
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]  # 보드 초기화
        self.moves = []  # 플레이어의 돌을 저장할 리스트
        self.current_player = ''  # 현재 플레이어 초기화
        self.is_timer_running = True  # 타이머 상태를 나타내는 플래그
        self.create_widgets()  # 위젯 생성
        self.start_game()  # 게임 시작
        self.timeout_message_shown = False  # 시간 초과 메시지 박스가 표시되었는지 여부를 나타내는 플래그
        self.timeout_count = -1  # 시간 초과가 발생한 횟수를 추적하는 변수




    def create_widgets(self):
        # 캔버스 생성
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(side=tk.LEFT)

        # 오목판 그리기
        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size*i, 0, self.cell_size*i, self.canvas_size, fill="black")
            self.canvas.create_line(0, self.cell_size*i, self.canvas_size, self.cell_size*i, fill="black")

        self.canvas.bind("<Button-1>", self.place_piece)#클릭이벤트 바인딩

        # 타이머 표시 네모 박스
        self.timer_frame = tk.Frame(self, width=200, height=self.canvas_size, bg="lightgray")
        self.timer_frame.pack(side=tk.RIGHT)

        # 타이머 라벨
        self.timer_label = tk.Label(self.timer_frame, text=f"Time left: {self.time_limit:02d}", font=("Arial", 12), bg="lightgray")
        self.timer_label.pack(side=tk.TOP, padx=10, pady=10)

        # 승패 기록 라벨
        self.result_label = tk.Label(self.timer_frame, text=f"승점: 흑 - {OmokGame.win_count["흑돌"]} | 백 - {OmokGame.win_count["백돌"]}",
                                     font=("Arial", 12), bg="lightgray")
        self.result_label.pack(side=tk.TOP, padx=10, pady=10)

        # 무르기 버튼
        self.undo_button = tk.Button(self.timer_frame, text="무르기", command=self.undo_move)
        self.undo_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 새로운 게임 시작 버튼
        self.new_game_button = tk.Button(self.timer_frame, text="새로운 게임 시작", command=self.restart_btn)
        self.new_game_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 홈 버튼
        self.home_button = tk.Button(self.timer_frame, text="홈", command=self.go_to_home)
        self.home_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # 타이머 정지 버튼
        self.stop_timer_button = tk.Button(self.timer_frame, text="타이머 정지", command=self.stop_timer)
        self.stop_timer_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 타이머 시작 버튼
        self.start_timer_button = tk.Button(self.timer_frame, text="타이머 시작", command=self.start_timer)
        self.start_timer_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def start_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]  # 오목판 초기화
        self.moves = []  # 플레이어의 돌을 저장할 리스트
        self.current_player = "흑돌"  # 현재 플레이어 초기화
        self.start_time = datetime.now()  # 게임 시작 시간 기록
        self.update_timer()  # 타이머 업데이트

    def place_piece(self, event):
        col = round(event.x / self.cell_size)
        row = round(event.y / self.cell_size)

        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.moves.append((row, col))
            self.draw_piece(row, col)

            if self.check_win(row, col):
                messagebox.showinfo("Game Over", f"승자는 {self.current_player} 입니다")
                self.update_win_count(self.current_player)
                self.restart_game()
                return

            self.start_time = datetime.now()
            self.update_timer()

            if self.current_player == "흑돌":
                self.current_player = "백돌"
                self.computer_play()
                
    def computer_play(self):
        if self.current_player == "백돌":  # 컴퓨터 플레이어일 때만 수행
            empty_cells = [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] == ' ']
            if empty_cells:
                row, col = self.find_best_move()
                self.board[row][col] = self.current_player
                print(f"Computer (O) move: ({row}, {col})")
                self.moves.append((row, col))
                self.draw_piece(row, col)
                if self.check_win(row, col):
                    messagebox.showinfo("Game Over", f"승자는 {self.current_player} 입니다")
                    self.update_win_count(self.current_player)
                    self.restart_game()
                else:
                    self.current_player = "흑돌"  # 플레이어 교체
    
    def find_best_move(self):
        # Check for X pattern (3 in a row), and place O next to it
        for i in range(self.board_size):
            for j in range(self.board_size - 3):
                if self.board[i][j:j+4] == ["흑돌", "흑돌", "흑돌", ' ']:
                    return i, j + 3
                elif self.board[i][j:j+4] == [' ', "흑돌", "흑돌", "흑돌"]:
                    return i, j

        # Check for X pattern (3 in a column), and place O above or below it
        for i in range(self.board_size - 3):
            for j in range(self.board_size):
                if [self.board[i+k][j] for k in range(4)] == ["흑돌", "흑돌", "흑돌", ' ']:
                    return i + 3, j
                elif [self.board[i+k][j] for k in range(4)] == [' ', "흑돌", "흑돌", "흑돌"]:
                    return i, j 

        # Check for X pattern (3 in a diagonal), and place O next to it
        for i in range(self.board_size - 3):
            for j in range(self.board_size - 3):
                if [self.board[i+k][j+k] for k in range(4)] == ["흑돌", "흑돌", "흑돌", ' ']:
                    return i + 3, j + 3
                elif [self.board[i+k][j+k] for k in range(4)] == [' ', "흑돌", "흑돌", "흑돌"]:
                    return i, j 

        # Check for X pattern (3 in an anti-diagonal), and place O next to it
        for i in range(self.board_size - 3):
            for j in range(3, self.board_size):
                if [self.board[i+k][j-k] for k in range(4)] == ["흑돌", "흑돌", "흑돌", ' ']:
                    return i + 3, j - 3
                elif [self.board[i+k][j-k] for k in range(4)] == [' ', "흑돌", "흑돌", "흑돌"]:
                    return i, j 

        # Check for O pattern (2 in a row), and place O next to it
        for i in range(self.board_size):
            for j in range(self.board_size - 1):
                if self.board[i][j:j+2] == ["백돌", ' ']:
                    return i, j + 1
                elif self.board[i][j:j+2] == [' ', "백돌"]:
                    return i, j

        # Check for O pattern (2 in a column), and place O above or below it
        for i in range(self.board_size - 1):
            for j in range(self.board_size):
                if [self.board[i+k][j] for k in range(2)] == ["백돌", ' ']:
                    return i + 1, j
                elif [self.board[i+k][j] for k in range(2)] == [' ', "백돌"]:
                    return i, j 

        # Check for O pattern (2 in a diagonal), and place O next to it
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                if [self.board[i+k][j+k] for k in range(2)] == ["백돌", ' ']:
                    return i + 1, j + 1
                elif [self.board[i+k][j+k] for k in range(2)] == [' ', "백돌"]:
                    return i, j 

        # Check for O pattern (2 in an anti-diagonal), and place O next to it
        for i in range(self.board_size - 1):
            for j in range(1, self.board_size):
                if [self.board[i+k][j-k] for k in range(2)] == ["백돌", ' ']:
                    return i + 1, j - 1
                elif [self.board[i+k][j-k] for k in range(2)] == [' ', "백돌"]:
                    return i, j 

        # If no pattern found, place O randomly
        return random.choice([(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == ' '])





    def draw_piece(self, row, col):
        x = col * self.cell_size  # 돌의 x 좌표 계산
        y = row * self.cell_size  # 돌의 y 좌표 계산
        color = "black" if self.current_player == "흑돌" else "white"  # 돌의 색상 결정
        piece_tag = f"piece_{row}_{col}"  # 각 돌에 대한 태그 생성
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags=piece_tag)  # 돌 그리기

    def check_win(self, row, col):
        # 승리 여부 확인 함수
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            r, c = row, col
            for _ in range(4):
                r, c = r + dr, c + dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            r, c = row, col
            for _ in range(4):
                r, c = r - dr, c - dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        
        if self.current_player == "백돌":
            return False

        # 컴퓨터가 흑돌일 때만 가장 좋은 수 찾기
        if self.current_player == "백돌":
            row, col = self.find_best_move()
            self.board[row][col] = self.current_player
            self.moves.append((row, col))
            self.draw_piece(row, col)
            if self.check_win(row, col):
                messagebox.showinfo("Game Over", f"승자는 {self.current_player} 입니다")
                self.restart_game()
                self.update_win_count()
                return True

        return False
    

    def update_timer(self):
        if self.is_timer_running:
            elapsed_time = datetime.now() - self.start_time
            remaining_time = timedelta(seconds=self.time_limit) - elapsed_time
            if remaining_time <= timedelta(0) and not self.timeout_message_shown:  # 시간 초과 및 메시지 박스가 표시되지 않은 경우
                self.timer_label.config(text="시간 초과!!")
                self.update_win_count(self.get_opponent_player())  # 시간 초과로 패한 플레이어의 승리 횟수 업데이트
                self.timeout_message_shown = True  # 메시지 박스가 표시되었음을 표시
                messagebox.showinfo("Game Over", f"승자는 {self.get_opponent_player()} 입니다")
                self.restart_game()
                return
            else:
                self.timer_label.config(text=f"초 읽기: {remaining_time.seconds:02d}")
        self.after(self.timer_interval, self.update_timer)

    def undo_move(self):
        if self.moves:
            last_move_row, last_move_col = self.moves.pop()  # 마지막으로 놓은 돌 위치 가져오기
            self.board[last_move_row][last_move_col] = ' '  # 오목판에서 해당 돌 삭제
            piece_tag = f"piece_{last_move_row}_{last_move_col}"  # 삭제할 돌의 태그
            self.canvas.delete(piece_tag)  # 캔버스에서 해당 돌 삭제
            # 마지막 플레이어 교체
            if self.current_player == "흑돌":
                self.current_player = "백돌"
            else:
                self.current_player = "흑돌"

    def update_win_count(self, winner):
        # 현재 게임에서 승리한 플레이어의 승리 횟수를 업데이트합니다.
        OmokGame.win_count[winner] += 1

    def restart_game(self):
        self.destroy()  # 현재 윈도우 종료
        app = OmokGameAI()  # 새로운 게임 시작
        app.mainloop()  # 새로운 게임 창 열기

    def restart_btn(self):
        # 현재 윈도우 종료
        self.destroy()
        # 승점 초기화
        OmokGame.win_count = {"흑돌": 0, "백돌": 0}
        # 새로운 게임 시작
        app = OmokGameAI()
        app.mainloop()  # 새로운 게임 창 열기

    def go_to_home(self):
        # 현재 윈도우 종료
        # 홈 화면으로 돌아가기
        self.destroy()
        app = OmokGame()
        app.mainloop()

    def get_opponent_player(self):
        # 현재 플레이어의 상대 플레이어를 반환합니다.
        if self.current_player == "흑돌":
            return "백돌"
        else:
            return "흑돌"

    def start_timer(self):
        self.is_timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.is_timer_running = False



if __name__ == "__main__":
    app = OmokGame()  # 애플리케이션 인스턴스 생성
    app.mainloop()  # 이벤트 루프 실행