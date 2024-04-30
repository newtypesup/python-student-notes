import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import heapq

# 엑셀 파일에서 역 이름과 좌표 정보를 불러오기
DB_coordinate = pd.read_excel("C:\\Users\\2class_17\\Desktop\\지하철좌표.xlsx", 
                              engine="openpyxl", sheet_name="Sheet1", header=0)
DB_coordinate_frame = DB_coordinate.set_index('name').T.to_dict('list')

start_selected = False  # 출발지 선택 여부 플래그
end_selected = False  # 도착지 선택 여부 플래그

def find_nearest_station(x, y):
    nearest_station = None
    min_distance = float('inf')
    for station, coordinates in DB_coordinate_frame.items():
        station_x, station_y = coordinates
        distance = ((x - station_x) ** 2 + (y - station_y) ** 2) ** 0.5
        if distance < min_distance:
            nearest_station = station
            min_distance = distance
    return nearest_station

def on_click(event):
    global start_selected, end_selected
    x, y = event.x, event.y
    nearest_station = find_nearest_station(x, y)
    
    # 출발지를 선택하지 않았다면
    if not start_selected:
        start_entry.delete(0, tk.END)  # 출발지 텍스트 상자 내용 초기화
        start_entry.insert(tk.END, nearest_station)  # 가장 가까운 역을 출발지 텍스트 상자에 출력
        start_selected = True  # 출발지 선택 상태를 True로 변경
    # 출발지를 이미 선택했고, 도착지를 선택하지 않았다면
    elif not end_selected:
        # 출발지와 도착지가 같은 경우, 도착지를 선택하지 않은 것으로 간주하여 무시
        if nearest_station != start_entry.get():
            end_entry.delete(0, tk.END)  # 도착지 텍스트 상자 내용 초기화
            end_entry.insert(tk.END, nearest_station)  # 가장 가까운 역을 도착지 텍스트 상자에 출력
            end_selected = True  # 도착지 선택 상태를 True로 변경

def clear_entries():     # 초기화 함수
    global start_selected, end_selected
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    start_selected = False
    end_selected = False

def find_shortest_path(start_station, end_station):
    # 역 이름과 인덱스 번호 매핑 딕셔너리 생성
    station_index = {station: i for i, station in enumerate(DB_coordinate_frame.keys())}

    # 역 사이의 거리 정보를 읽어옴
    distances = pd.read_excel("C:\\Users\\2class_17\\Desktop\\전철소요시간.xlsx", 
                              engine="openpyxl", sheet_name="Sheet1", header=0, index_col=0)

    # 다익스트라 알고리즘을 사용하여 최단 경로 계산
    def dijkstra(graph, start):
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances

    # 출발지와 도착지 설정
    start_index = station_index[start_station]
    end_index = station_index[end_station]

    # 최단 경로 계산
    shortest_path = dijkstra(distances, start_index)
    
    # 각 역마다 걸리는 시간 계산
    def calculate_travel_time(graph, shortest_path):
        travel_times = {}
        for station_index, distance in shortest_path.items():
            station_name = list(station_index.keys())[0]
            travel_times[station_name] = distance
        return travel_times

    return shortest_path, calculate_travel_time(graph, shortest_path)

def on_click(event):
    global start_selected, end_selected
    x, y = event.x, event.y
    nearest_station = find_nearest_station(x, y)
    
    # 출발지를 선택하지 않았다면
    if not start_selected:
        start_entry.delete(0, tk.END)  # 출발지 텍스트 상자 내용 초기화
        start_entry.insert(tk.END, nearest_station)  # 가장 가까운 역을 출발지 텍스트 상자에 출력
        start_selected = True  # 출발지 선택 상태를 True로 변경
    # 출발지를 이미 선택했고, 도착지를 선택하지 않았다면
    elif not end_selected:
        # 출발지와 도착지가 같은 경우, 도착지를 선택하지 않은 것으로 간주하여 무시
        if nearest_station != start_entry.get():
            end_entry.delete(0, tk.END)  # 도착지 텍스트 상자 내용 초기화
            end_entry.insert(tk.END, nearest_station)  # 가장 가까운 역을 도착지 텍스트 상자에 출력
            end_selected = True  # 도착지 선택 상태를 True로 변경

# 메인 코드 시작
win = tk.Tk()
win.title("Subway Map")
win.geometry("1600x1000")

frame = tk.Frame(win, relief="solid", bd=2)
frame.pack(side="left", expand=True, fill="both")

# 레이블 추가
label = tk.Label(frame, text="수도권 지하철 노선도",)
label.grid(row=0, column=0)

# 출발역 레이블 추가
start_label = tk.Label(frame, text="출발역 : ")
start_label.grid(row=4, column=0, pady=8)

# 출발역 텍스트 상자 추가
start_entry = tk.Entry(frame)
start_entry.grid(row=4, column=1, pady=5)

# 도착역 레이블 추가
end_label = tk.Label(frame, text="도착역 : ")
end_label.grid(row=5, column=0, pady=10)

# 도착역 텍스트 상자 추가
end_entry = tk.Entry(frame)
end_entry.grid(row=5, column=1, pady=10)

# 초기화 버튼 추가
clear_button = tk.Button(frame, text="초기화", command=clear_entries)
clear_button.grid(row=6, column=1, pady=10)

# 마우스 이벤트 바인딩
canvas = tk.Canvas(win, width=1300, height=1000, background='white')
canvas.pack()

def show_coordinates(event):
    x = event.x
    y = event.y
    canvas.coords(cursor_text, x, y+20)
    canvas.itemconfigure(cursor_text, text=f"({x}, {y})")

# 이미지 그리기
img = tk.PhotoImage(file="C:\\Users\\2class_17\\Desktop\\subway_map.png")
canvas.create_image(5, 5, anchor=tk.NW, image=img)
canvas.bind("<Motion>", show_coordinates)
cursor_text = canvas.create_text(50, 30, text='', fill='black', font=('Arial', 20))

# 마우스 클릭 이벤트 바인딩
canvas.bind("<Button-1>", on_click)

# 최단 경로와 소요 시간 출력 함수
def print_shortest_path():
    start_station = start_entry.get()
    end_station = end_entry.get()
    if start_station and end_station:
        shortest_path, travel_times = find_shortest_path(start_station, end_station)
        print("최단 경로:", shortest_path)
        print("소요 시간:", travel_times)

# 최단 경로 출력 버튼 추가
print_button = tk.Button(frame, text="최단 경로 출력", command=print_shortest_path)
print_button.grid(row=7, column=1, pady=10)

win.mainloop()