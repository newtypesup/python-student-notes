import tkinter as tk
from tkinter import messagebox
import pandas as pd
import math
import folium
import webbrowser
from folium.plugins import AntPath
from PIL import Image, ImageTk
import datetime

def load_subway_lines(filename):
    df = pd.read_excel(filename)
    
    line_ranges = {
        '1호선': (0, 39),
        '2호선': (40, 82),
        '3호선': (83, 99),
        '4호선': (100, 113),
        '동해선': (114, 136),
        '김해선': (137, 157)
    }
    
    subway_lines = {}
    
    for line, (start, end) in line_ranges.items():
        line_df = df.iloc[start:end+1]
        stations = []
        for index, row in line_df.iterrows():
            station = row.iloc[1]
            latitude = row.iloc[3]
            longitude = row.iloc[4]
            stations.append({"역": station, "위도": latitude, "경도": longitude})
        subway_lines[line] = stations
    
    return subway_lines

subway_lines = load_subway_lines('C:\\Users\\2class_17\\Desktop\\busan_0.xlsx')

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구의 반지름 (단위: km).

    lat1 = math.radians(lat1)   #위도1
    lon1 = math.radians(lon1)   #경도1
    lat2 = math.radians(lat2)   #위도2
    lon2 = math.radians(lon2)   #경도2

    dlat = lat2 - lat1    # 위도 차이 계산.
    dlon = lon2 - lon1    # 경도 차이 계산.

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2    # 하버사인 공식을 사용하여 거리 계산.
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c    # 거리 계산 및 반환.
    return distance

def show_route(start_station, end_station):
    route = []
    start_line = None
    end_line = None

    for line, stations in subway_lines.items():
        station_names = [station['역'] for station in stations]
        if start_station in station_names:
            start_line = line
        if end_station in station_names:
            end_line = line

    if start_line is None or end_line is None:
        return ["경로를 찾을 수 없습니다."]

    if start_line == end_line:
        stations = subway_lines[start_line]
        start_index = [station['역'] for station in stations].index(start_station)
        end_index = [station['역'] for station in stations].index(end_station)
        if start_index < end_index:  # 정방향.
            route = stations[start_index:end_index + 1]
        else:  # 역방향.
            route = stations[end_index:start_index + 1][::-1]
        
        for station in route:        # 노선 정보 추가.
            station['노선'] = start_line

    else:
        start_stations = subway_lines[start_line]
        end_stations = subway_lines[end_line]

        for start_station_data in start_stations:
            if start_station_data['역'] in [end_station_data['역'] for end_station_data in end_stations]:
                transfer_station = start_station_data['역']
                break

        start_index = [station['역'] for station in start_stations].index(start_station)
        end_index = [station['역'] for station in end_stations].index(end_station)
        transfer_index_start = [station['역'] for station in start_stations].index(transfer_station)
        transfer_index_end = [station['역'] for station in end_stations].index(transfer_station)

        if start_index < transfer_index_start:  # 출발역 -> 환승역 방향.
            route.extend(start_stations[start_index:transfer_index_start + 1])
        else:  # 출발역 <- 환승역 방향.
            route.extend(start_stations[transfer_index_start:start_index + 1][::-1])
        if transfer_index_end < end_index:  # 환승역 -> 도착역 방향.
            route.extend(end_stations[transfer_index_end:end_index + 1])
        else:  # 환승역 <- 도착역 방향.
            route.extend(end_stations[end_index:transfer_index_end + 1][::-1])
        
        for station in route:        # 노선 정보 추가.
            if station in start_stations:
                station['노선'] = start_line
            elif station in end_stations:
                station['노선'] = end_line
    
    unique_route = []    # 중복 제거 및 반환.
    for station in route:
        if station not in unique_route:
            unique_route.append(station)

    return [station['역'] + " (" + station['노선'] + ")" for station in unique_route]

def adjacent_stations(station_name, line):
    stations = subway_lines[line]
    index = [station['역'] for station in stations].index(station_name)
    if index == 0:
        adjacent = [stations[index + 1]['역']]
    elif index == len(stations) - 1:
        adjacent = [stations[index - 1]['역']]
    else:
        adjacent = [stations[index - 1]['역'], stations[index + 1]['역']]
    return adjacent

def show_adjacent_stations(station_name):
    adjacent_stations_list = []
    for line, stations in subway_lines.items():
        if station_name in [station['역'] for station in stations]:
            adjacent_stations_list.extend(adjacent_stations(station_name, line))
    return adjacent_stations_list

def show_adjacent_stations_with_lines(station_name):
    adjacent_stations_dict = {}
    for line, stations in subway_lines.items():
        if station_name in [station['역'] for station in stations]:
            adjacent_stations_dict[line] = adjacent_stations(station_name, line)
    return adjacent_stations_dict

def show_route_handler():
    start_station = start_station_entry.get()
    end_station = end_station_entry.get()
    
    # 입력된 역 이름에 '역'이 포함되어 있지 않으면 '역'을 추가합니다.
    if '역' not in start_station:
        start_station += '역'
    if '역' not in end_station:
        end_station += '역'
    
    route = show_route(start_station, end_station)
    route_str = " -> ".join(route)
    
    # 출발역과 도착역의 좌표찾기.
    start_lat, start_lon = None, None
    end_lat, end_lon = None, None
    for line, stations in subway_lines.items():
        for station in stations:
            if station['역'] == start_station:
                start_lat = station['위도']
                start_lon = station['경도']
            elif station['역'] == end_station:
                end_lat = station['위도']
                end_lon = station['경도']
    
    if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
        straight_line_distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)
        # print("출발역과 도착역의 직선 거리:", straight_line_distance, "km")
    else:
        print("출발역 또는 도착역의 위치를 찾을 수 없습니다.")
    
    # print("경로:", route_str)
    
    pre_transfer_route = []  # 환승 전의 경로를 저장할 리스트.
    transfer_count = 0  # 환승 횟수를 저장할 변수.
    f_route = []
    
    for i in range(len(route)-1):
        current_station = route[i].split(" (")[0]  # 역 이름만 추출.
        current_line = route[i].split(" (")[1].split(")")[0]  # 노선 이름만 추출.
        if current_station == end_station:
            # print(f"도착역 {end_station} 마지막 경로 출력으로, 탐색을 종료합니다.")
            break
        
        adjacent_stations_list = show_adjacent_stations(current_station)
        # print(f"{current_station}({current_line})의 인접한 역들: {', '.join(adjacent_stations_list)}")  # 역 이름과 노선 이름 모두 출력.
        min_distance = float('inf')  # 가장 작은 거리를 저장할 변수.
        closest_station = None  # 가장 가까운 역을 저장할 변수.
        for adjacent_station in adjacent_stations_list:
            adjacent_lat, adjacent_lon = None, None
            # 인접한 역의 위도,경도 찾기.
            for line, stations in subway_lines.items():
                for station in stations:
                    if station['역'] == adjacent_station:
                        adjacent_lat = station['위도']
                        adjacent_lon = station['경도']
            if adjacent_lat is not None and adjacent_lon is not None:
                adjacent_distance = calculate_distance(end_lat, end_lon, adjacent_lat, adjacent_lon)
                # print(f"    - {adjacent_station}({line}): {adjacent_distance:.2f} km")  # 역 이름과 노선 이름 모두 출력.
                # 현재까지의 최소 거리보다 작은 경우, 역과 거리를 갱신.
                if adjacent_distance < min_distance:
                    min_distance = adjacent_distance
                    closest_station = adjacent_station
            else:
                print(f"    - {adjacent_station}({line}): 역의 위치를 찾을 수 없음")  # 역 이름과 노선 이름 함께 출력.
        # 가장 가까운 역을 다음 역으로 지정.
        if closest_station is not None:
            # print(f"가장 가까운 역: {closest_station}({line})")  # 역 이름과 노선 이름 모두 출력.
            pre_transfer_route.append(current_station + " (" + current_line + ")")  # 환승 전의 경로에 현재 역과 노선 추가.
            # 인접한 역이 2개 이하일 때는 기존 경로대로 이동.
            if len(adjacent_stations_list) <= 2:
                # print("인접한 역이 2개 이하이므로 기존 경로대로 이동합니다.")
                next_station = route[i + 1].split(" (")[0]  # 다음 역.
            else:
                # print("인접한 역이 3개 이상이므로 가장 가까운 역으로 이동합니다.")
                # 이후에 사용할 수 있도록 변수로 저장.
                next_station = closest_station
                transfer_count += 1  # 환승 횟수.
                
                # 가장 가까운 역을 새로운 출발역으로 설정하고 도착역까지의 경로를 재갱신.
                route = show_route(next_station, end_station)
                # route_str = " -> ".join(route)
                # print("경로:", route_str)
                # 출발역과 도착역 사이의 거리를 계산합니다.
                start_lat, start_lon = None, None
                for line, stations in subway_lines.items():
                    for station in stations:
                        if station['역'] == next_station:
                            start_lat = station['위도']
                            start_lon = station['경도']
                if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
                    straight_line_distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)
                    # print("출발역과 도착역의 직선 거리:", straight_line_distance, "km")
                # else:
                #     print("출발역 또는 도착역의 위치를 찾을 수 없습니다.")
                # print(f"도착역 {end_station}을 경로의 마지막으로 인식하여 출력을 종료합니다.")
                break
        
        else:
            print("가장 가까운 역을 찾을 수 없음")
        
        # 다음 역 출력.
        if next_station is not None:
            # print(f"다음 역: {next_station}({line})")  # 역 이름과 노선 이름 모두 출력.
            next_station = closest_station
        else:
            print("다음 역을 찾을 수 없음")
    
    # 이전 경로 + 새로운 경로 모두 출력.
    # pre_transfer_route_str = " -> ".join(pre_transfer_route)
    # print("최종 경로:", pre_transfer_route_str + " -> " + route_str)
    
    show_route_on_map(transfer_count, route, pre_transfer_route, f_route)   # show_route_on_map 함수 호출 시 정의하기
    
def add_arrow_line(map_obj, points, popup=None, color='black', weight=6):

    AntPath(points, color=color, weight=weight).add_to(map_obj)
      
    for point in points:
        folium.CircleMarker(location=point, radius=3, color='red').add_to(map_obj)

def add_marker_with_label(map_obj, location, label, color=None):
    if color:
        folium.Marker(location=location, popup=label, icon=folium.Icon(color=color)).add_to(map_obj)
    else:
        folium.Marker(location=location, popup=label).add_to(map_obj)

def show_route_on_map(transfer_count, route, pre_transfer_route, f_route):
    map_center = [35.1796, 129.0756]  # 부산의 위도, 경도.
    map = folium.Map(location=map_center, zoom_start=12)
    route_coordinates = [] 
    total_distance = 0.0  # 총 이동 거리.

    color_dict = {'1호선': 'orange', '2호선': 'green', '3호선': 'beige', '4호선': 'blue', '동해선': 'lightblue', '김해선': 'purple'}

    if transfer_count == 0:
        if route:
            pre_transfer_route.append(route[-1])
            f_route = pre_transfer_route
            print(f_route)

    elif transfer_count >= 1:
        if route:
            f_route = pre_transfer_route + route
            print(f_route)

    for i, station_info in enumerate(f_route):
        station_name, line_name = station_info.split(" (")
        line_name = line_name[:-1]  # 노선 이름에서 ')' 문자 제거.
        for line, stations in subway_lines.items():
            if line == line_name:
                for s in stations:
                    if s["역"] == station_name:
                        route_coordinates.append([s["위도"], s["경도"]])
                        if i == 0:
                            add_marker_with_label(map, [s["위도"], s["경도"]], station_name, color='lightgreen')  # 첫 번째 역.
                        elif i == len(f_route) - 1:
                            add_marker_with_label(map, [s["위도"], s["경도"]], station_name, color='lightred')  # 마지막 역.
                        elif len(f_route) == 2:
                            add_marker_with_label(map, [s["위도"], s["경도"]], station_name, color='lightred')  # 마지막 역(총 경로가 2개 인경우).
                        else:
                            add_marker_with_label(map, [s["위도"], s["경도"]], station_name, color=color_dict.get(line, 'gray'))  # 경로에 있는 역.
                        break
                else:
                    continue
                break

    add_arrow_line(map, route_coordinates, popup=f_route)
        
    for i in range(len(f_route)-1):     # 각 역들 간의 거리를 계산해서 총 이동 거리를 누적.
        current_station = f_route[i].split(" (")[0]  # 역 이름만 추출.
        next_station = f_route[i+1].split(" (")[0]  # 다음 역 이름만 추출.
        current_lat, current_lon = None, None
        next_lat, next_lon = None, None
        for line, stations in subway_lines.items():
            for station in stations:
                if station['역'] == current_station:
                    current_lat = station['위도']
                    current_lon = station['경도']
                elif station['역'] == next_station:
                    next_lat = station['위도']
                    next_lon = station['경도']
        if current_lat is not None and current_lon is not None and next_lat is not None and next_lon is not None:
            distance = calculate_distance(current_lat, current_lon, next_lat, next_lon)
            total_distance += distance
            
    print("총 이동 거리:", total_distance, "km") 
    travel_time = math.ceil(((total_distance*1000)/741.5)+(len(f_route)*0.75)+(transfer_count*3))
    print("소요 시간:",travel_time, "분")
    travel_time_2 = datetime.timedelta(minutes=travel_time)

    current_time = datetime.datetime.now()    # 현재 시각 계산
    
    total_time = current_time + travel_time_2    # 도착 예정 시간 계산.
    print("도착 예정 시간:", total_time)
    messagebox.showinfo("경로: ",f_route)
   
    # HTML 요소를 추가하여 현재 시각과 예상 도착 시각을 표시할 공간을 마련합니다.
    current_time_html = """
    <div style="position: fixed; top: 100px; left: 100px; background-color: white; padding: 10px; border: 5px solid black; border-radius: 5px; z-index: 9999; display: flex; flex-direction: column; align-items: center;">
        <p id="current-time" style="margin: 0; color: green; font-weight: bold;"></p>
        <p id="arrival-time" style="margin: 0; color: red; font-weight: bold;"></p>
        <p id="travel-time" style="margin: 0; color: black; font-weight: bold;"></p>
    </div>
    """
    map.get_root().html.add_child(folium.Element(current_time_html))

    # JavaScript를 사용하여 해당 공간에 현재 시각과 예상 도착 시각을 업데이트합니다.
    update_current_time_js = """
    setInterval(function() {{
        var currentTimeElement = document.getElementById('current-time');
        var arrivalTimeElement = document.getElementById('arrival-time');
        var travelTimeElement = document.getElementById('travel-time');
        var currentTime = new Date().toLocaleString();
        var arrivalTime = new Date({year}, {month} - 1, {day}, {hour}, {minute}, {second}).toLocaleString();
        currentTimeElement.innerHTML = '현재 시각: ' + currentTime;
        arrivalTimeElement.innerHTML = '도착 예정 시각: ' + arrivalTime;
        travelTimeElement.innerHTML = '(이동 소요 시간: {travel_time}분)';
    }}, 1000);
    """.format(year=total_time.year, month=total_time.month, day=total_time.day, 
            hour=total_time.hour, minute=total_time.minute, second=total_time.second,
            travel_time=travel_time)

    map.get_root().script.add_child(folium.Element(update_current_time_js))
    
    map_html = "hyungsubway_route.html"
    map.save(map_html)
    webbrowser.open(map_html, new=2)
    
def switch_places():
    current_start = start_station_entry.get()
    current_dest = end_station_entry.get()
    start_station_entry.delete(0, tk.END)
    end_station_entry.delete(0, tk.END)
    start_station_entry.insert(0, current_dest)
    end_station_entry.insert(0, current_start)
    
def reset_entries():
    start_station_entry.delete(0, tk.END)
    end_station_entry.delete(0, tk.END)

app = tk.Tk()
app.title("지하철 노선도[좌표]")
app.geometry("975x800")

image_path = "C:\\Users\\2class_17\\Desktop\\노선.png"
image_pil = Image.open(image_path)
image_resized = image_pil.resize((925, 600), Image.BICUBIC)
image = ImageTk.PhotoImage(image_resized)

image_label = tk.Label(app, image=image)
image_label.place(relx=0.5, rely=0.4, anchor="center")

start_label = tk.Label(app, text="출발역:")
start_label.place(relx=0.4, rely=0.85, anchor="center")
start_station_entry = tk.Entry(app)
start_station_entry.place(relx=0.5, rely=0.85, anchor="center")
start_station_entry.bind("<Return>", lambda event: show_route_handler())

end_label = tk.Label(app, text="도착역:")
end_label.place(relx=0.4, rely=0.9, anchor="center")
end_station_entry = tk.Entry(app)
end_station_entry.place(relx=0.5, rely=0.9, anchor="center")
end_station_entry.bind("<Return>", lambda event: show_route_handler())

switch_button = tk.Button(app, text="↑↓", command=switch_places)
switch_button.place(relx=0.6, rely=0.85, anchor="center")

reset_button = tk.Button(app, text="리셋", command=reset_entries)
reset_button.place(relx=0.65, rely=0.85, anchor="center")

search_button = tk.Button(app, text="검색", command=show_route_handler)
search_button.place(relx=0.6, rely=0.9, anchor="center")

app.mainloop()