"""
1. 공원 csv 읽어오기
2. 이중 for loop으로 하나의 공원에서 모든 공원사이의 거리 구해서 top N개의 공원만 간선으로 연결하기 위한 후보로 추출
3. 간선의 weight 구하기
4. 최종 return : 모든 공원에 대해 top N 개의 간선으로 연결된 graph return
"""

import pandas as pd
from tqdm import tqdm
from geopy.distance import geodesic
import random
import json

def read_file(filename):
    df = pd.read_csv(filename, encoding='cp949')
    # id가 없을 경우 id 값 부여
    if 'id' not in list(df.columns):
        df["id"] = [i for i in df.index]
        df.to_csv(filename)
    return df

def get_node(df, N):
    result = {}

    for i in tqdm(range(len(df.index))):
        temp = []
        for j in range(len(df.index)):
            if i != j:
                park1 = (df['위도'][i], df['경도'][i])
                park2 = (df['위도'][j], df['경도'][j])
                distance = geodesic(park1, park2)

                temp.append((distance, j))
        temp.sort(reverse=False)
        
        # 가장 가까운 N번째 노드 결과에 할당
        result[i] = temp[:N]
    
    # return 형식 : {0 : [(distanace, j), (distanace, j), (distanace, j)], 1: [(distanace, j), (distanace, j), (distanace, j)], ... }
    return result

def get_vertex_weight(df, nodes):
    edges = []
    
    for node, values in nodes.items():
        for val in values:
            dest = val[1]
            weight = df['value'][node] + df['value'][dest]
            edges.append((int(weight), int(node), int(dest)))

    # return 형식 : [(distance, node1, ndoe2), (distance, node1, ndoe2), ...]
    return edges

def make_graph(lenth, edges):
    graph = {}
    graph['vertices'] = [int(i) for i in range(lenth)]
    graph['edges'] = edges

    return graph

def get_graph(filename, N):
    # 0. 임시 코드 - 임시 value 값 생성
    temp = pd.read_csv('All_Data_2.csv', encoding='cp949')
    if 'value' not in list(temp.columns):
        temp['value'] = [random.randrange(1,100) for _ in tqdm(range(len(temp.index)))]
        temp.to_csv('All_Data_2.csv')
    
    # 1. 공원 csv 읽어오기 - 필요한 것은 각 공원의 id, 위도, 경도
    df = read_file(filename)
    
    # 2. 이중 for loop으로 하나의 공원에서 모든 공원사이의 거리 구해서 top N개의 공원만 간선으로 연결하기 위한 후보로 추출
    nodes = get_node(df, N)

    # 3. 간선의 weight 구하기
    edges = get_vertex_weight(df, nodes)

    # 4. graph 자료구조 init
    graph = make_graph(len(df.index), edges)

    # 5. output txt 로 저장
    print(graph)
    with open('data.json', 'w') as fp:
        json.dump(graph, fp)

    return graph

if __name__ == '__main__':
    
    graph = get_graph('data.csv', 3)
    # output txt 로 저장
    print(graph)
    with open('data.json', 'w') as fp:
        json.dump(graph, fp)

