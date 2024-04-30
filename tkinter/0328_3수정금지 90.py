import pandas as pd
import hashlib
import datetime
import tkinter as tk
from tkinter import messagebox
from geopy.distance import geodesic #테스트

class Block:
    def __init__(self, index, data1, data2, data3, data4, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.next_block = None  # 다음 블록을 가리키는 포인터

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.data1) + str(self.data2) + str(self.data3) + str(self.data4) + str(self.previous_hash)).encode()).hexdigest()

def create_blockchain(df, start_index, end_index, previous_hash):
    blockchain = []
    previous_hash = previous_hash
    index = 1
    
    for i in range(start_index, min(end_index, len(df))):
        data1 = str(df.iloc[i, 1])
        data2 = str(df.iloc[i, 2])
        data3 = float(df.iloc[i, 3])
        data4 = float(df.iloc[i, 4])
        block = Block(index, data1, data2, data3, data4, previous_hash)
        blockchain.append(block)
        previous_hash = block.hash
        index += 1
    
    for i in range(len(blockchain) - 1):
        blockchain[i].next_block = blockchain[i + 1]

    return blockchain, previous_hash

def load_excel():
    try:
        # 첫 번째 엑셀 파일 읽기
        file_path_1 = "C:\\Users\\2class_17\\Desktop\\busan1.xlsx"
        df_1 = pd.read_excel(file_path_1)
        print("첫 번째 Excel 파일을 성공적으로 불러왔습니다.")
        
        blockchains = {}
        blockchain_indices_1 = {
            "blockchain_1호선": (0, 48),
            "blockchain_3호선": (48, 77)
        }
        previous_hashes_1 = [None] * len(blockchain_indices_1)

        # 첫 번째 엑셀 파일의 블록체인 생성
        for i, (blockchain_name, (start, end)) in enumerate(blockchain_indices_1.items()):
            blockchain, prev_hash = create_blockchain(df_1, start, end, previous_hashes_1[i])
            blockchains[blockchain_name] = blockchain
            previous_hashes_1[i] = prev_hash

        # 두 번째 엑셀 파일 읽기2class_17
        file_path_2 = "C:\\Users\\2class_17\\Desktop\\busan2.xlsx"
        df_2 = pd.read_excel(file_path_2)
        print("두 번째 Excel 파일을 성공적으로 불러왔습니다.")

        blockchain_indices_2 = {
            "blockchain_2호선": (0, 53),
            "blockchain_4호선": (53, 72)

        }
        previous_hashes_2 = [None] * len(blockchain_indices_2)

        # 두 번째 엑셀 파일의 블록체인 생성
        for i, (blockchain_name, (start, end)) in enumerate(blockchain_indices_2.items()):
            blockchain, prev_hash = create_blockchain(df_2, start, end, previous_hashes_2[i])
            blockchains[blockchain_name] = blockchain
            previous_hashes_2[i] = prev_hash

        # 세 번째 엑셀 파일 읽기2class_17
        file_path_3 = "C:\\Users\\2class_17\\Desktop\\busan3.xlsx"
        df_3 = pd.read_excel(file_path_3)
        print("세 번째 Excel 파일을 성공적으로 불러왔습니다.")

        blockchain_indices_3 = {
            "blockchain_동해선": (0, 29),
            "blockchain_김해선": (30, 54)
        }
        previous_hashes_3 = [None] * len(blockchain_indices_3)

        # 세 번째 엑셀 파일의 블록체인 생성
        for i, (blockchain_name, (start, end)) in enumerate(blockchain_indices_3.items()):
            blockchain, prev_hash = create_blockchain(df_3, start, end, previous_hashes_3[i])
            blockchains[blockchain_name] = blockchain
            previous_hashes_3[i] = prev_hash
       
        return blockchains, previous_hashes_1 + previous_hashes_2 + previous_hashes_3

    except Exception as e:
        print("Excel 파일을 불러오는 중 오류가 발생했습니다:", e)
                               
        return None
    
def search_blocks(starting_point, destination, blockchains, previous_hashes):
    # 출발지와 목적지 블록 찾기
    start_block, start_blockchain = find_block(starting_point, blockchains)
    dest_block, dest_blockchain = find_block(destination, blockchains)

    if start_block is None or dest_block is None:
        print("출발지나 목적지가 블록체인에 없습니다.")
        return

    # 경로 탐색
    print(f"경로 탐색 시작: {starting_point} -> {destination}")
    current_block = start_block
    current_blockchain = start_blockchain
    total_distance = 0  # 총 이동 거리
    distance_list = []  # 각 블록과 목적지 간의 직선 거리 저장 리스트

    # 최초 출발지 블록과 도착지 블록의 실제 직선 거리
    initial_distance = geodesic((start_block.data3, start_block.data4), (dest_block.data3, dest_block.data4)).kilometers

    while current_block != dest_block:
        # 현재 블록이 "부산대역"이 아닌 경우에만 출력하고 실제 직선 거리 계산
        if current_block.data1 != '"크로스 체인"':
            # 현재 블록과 목적지 간의 실제 직선 거리 계산
            current_coords = (current_block.data3, current_block.data4)
            dest_coords = (dest_block.data3, dest_block.data4)
            current_distance = geodesic(current_coords, dest_coords).kilometers

            # 현재 블록과 목적지 간의 직선 거리가 최초 출발지 블록과 목적지 블록의 실제 직선 거리보다 작거나 같은 경우에만 출력
            if current_distance <= initial_distance:
                # 현재 블록 정보 출력
                print(f"현재 블록: {current_block.data1}, 블록체인: {current_blockchain}")
                print_block_info(current_block)

                distance_list.append(current_distance)
                total_distance += current_distance
                print(f"현재 블록과 목적지 간의 실제 직선 거리: {current_distance:.4f} km")
                print()

        # 다음 블록으로 이동
        if current_block.next_block:
            current_block = current_block.next_block
        else:
            # 현재 블록이 마지막 블록일 경우 다음 블록체인으로 이동
            current_blockchain_index = list(blockchains.keys()).index(current_blockchain)
            next_blockchain_index = (current_blockchain_index + 1) % len(blockchains)
            next_blockchain = list(blockchains.keys())[next_blockchain_index]
            current_block = blockchains[next_blockchain][0]

            # 다음 블록체인으로 이동할 때 크로스 체인 블록 정보 출력
            # print(f"크로스 체인 이동: {current_blockchain} -> {next_blockchain}")
            # print_block_info(current_block)

            current_blockchain = next_blockchain

    # 도착지 블록 정보 출력
    print(f"도착 지점에 도착했습니다: {destination}")
    print_block_info(dest_block)
    print(f"총 이동 거리: {total_distance:.4f} km")

    return distance_list, initial_distance

def find_cross_chain_blocks(blockchains, word_list):
    cross_chain_blocks = {}  # 각 단어와 해당 단어가 있는 블록들 저장

    for word in word_list:
        cross_chain_blocks[word] = []

    for blockchain_key, blockchain in blockchains.items():
        for block in blockchain:
            if block.data1 in word_list:
                cross_chain_blocks[block.data1].append((block, blockchain_key))

    return cross_chain_blocks

def display_cross_chain_blocks(cross_chain_blocks):
    for word, blocks in cross_chain_blocks.items():
        # print(f"단어: {word}")
        # print("블록:")
        # for block, blockchain_key in blocks:
        #     print(f"- 블록체인: {blockchain_key}")
        #     print_block_info(block)
        print()

word_list = ['"서면역"', '"연산역"', '"교대역"','"동래역"','"벡스코역"','"수영역"','"거제역"','"미남역"','"사상역"','"덕천역"','"대저역"']

def find_cross_block(word, blockchain_key):
    cross_chain_blocks = find_cross_chain_blocks(blockchains, [word])
    return cross_chain_blocks[word][0]  # 크로스 체인 블록은 해당 단어가 있는 첫 번째 블록으로 가정

def calculate_distance(start_block, dest_block):
    # 출발지와 목적지의 위도, 경도를 통해 직선 거리 계산
    start_coords = (start_block.data3, start_block.data4)
    dest_coords = (dest_block.data3, dest_block.data4)
    distance = geodesic(start_coords, dest_coords).kilometers
    return distance

def find_block(location, blockchains):
    for blockchain_key, blockchain in blockchains.items():
        for block in blockchain:
            if  block.data1 == f'"{location}역"':
                return block, blockchain_key
    return None, None
           
def print_block_info(block):
    print("블록 인덱스:", block.index)
    print("데이터1:", block.data1)
    # print("데이터2:", block.data2)
    # print("데이터3:", block.data3)
    # print("데이터4:", block.data4)
    # print("타임스탬프:", block.timestamp)
    # print("이전 해시:", block.previous_hash)
    # print("해시:", block.hash)
    print()
    
def find_shortest_path(starting_point, destination, blockchains):
    shortest_chain = None
    shortest_length = float('inf')  # 무한대 값으로 초기화

    for blockchain_key, blockchain in blockchains.items():
        start_block, _ = find_block(starting_point, {blockchain_key: blockchain})
        dest_block, _ = find_block(destination, {blockchain_key: blockchain})

        if start_block and dest_block:
            length = abs(dest_block.index - start_block.index)
            if length < shortest_length:
                shortest_length = length
                shortest_chain = blockchain_key

    return shortest_chain

def on_search(blockchains, previous_hashes):
    start_point = entry_start.get()
    destination = entry_dest.get()

    if start_point.strip() == "" or destination.strip() == "":
        messagebox.showerror("오류", "출발지와 도착지를 모두 입력해주세요.")
        return

    # 출발지와 목적지가 유효한 경우
    start_block, _ = find_block(start_point, blockchains)
    dest_block, _ = find_block(destination, blockchains)

    if start_block is None or dest_block is None:
        messagebox.showerror("오류", "입력한 역이 블록체인 노선에 없습니다.")
        return

    # 블록체인에서 출발지와 목적지 블록을 찾은 경우
    distance = calculate_distance(start_block, dest_block)

    # 결과 출력
    print(f"출발지: {start_point}, 도착지: {destination}")
    print(f"직선 거리: {distance:.4f} km")
    
    search_blocks(start_point, destination, blockchains, previous_hashes)
    

    
    # 블록 정보 출력
    print("출발지 정보:")
    print_block_info(start_block)
    print("도착지 정보:")
    print_block_info(dest_block)


def switch_places():
    current_start = entry_start.get()
    current_dest = entry_dest.get()
    entry_start.delete(0, tk.END)
    entry_dest.delete(0, tk.END)
    entry_start.insert(0, current_dest)
    entry_dest.insert(0, current_start)

if __name__ == "__main__":
    
    blockchains, previous_hashes = load_excel()
    cross_chain_blocks = find_cross_chain_blocks(blockchains, ['"서면역"', '"연산역"', '"교대역"','"동래역"','"벡스코역"','"수영역"','"거제역"','"미남역"','"사상역"','"덕천역"','"대저역"'])
    display_cross_chain_blocks(cross_chain_blocks)
    window = tk.Tk()
    window.title("블록체인 노선도 검색[제작: 신형섭]")

    label_start = tk.Label(window, text="출발지:")
    label_start.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
    entry_start = tk.Entry(window)
    entry_start.grid(row=0, column=1, padx=10, pady=5)

    label_dest = tk.Label(window, text="도착지:")
    label_dest.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    entry_dest = tk.Entry(window)
    entry_dest.grid(row=1, column=1, padx=10, pady=5)

    switch_button = tk.Button(window, text="↔", command=switch_places)
    switch_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

    search_button = tk.Button(window, text="검색", command=lambda: on_search(blockchains, previous_hashes))
    search_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    entry_dest.bind("<Return>", lambda event: on_search(blockchains, previous_hashes))

    window.mainloop()