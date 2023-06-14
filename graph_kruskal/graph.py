parent = dict()
rank = dict()

#vertice 초기화 - 본인 스스로 집합 생성
def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

#해당 vertice의 최상위 정점을 찾는다 - naive 한 접근 방식
def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]

#두 정점을 연결한다
def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: 
                rank[root2] += 1

def kruskal(graph):
    minimum_spanning_tree = []

    #초기화
    for vertice in graph['vertices']:
        make_set(vertice)
        
    #간선 weight 기반 sorting - weight 적은 것 앞으로
    edges = graph['edges']
    edges.sort(reverse=True)
    
    #간선 연결 (사이클 없게)
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2): # 같은 집합이 아닐 경우 합침
            union(vertice1, vertice2)
            minimum_spanning_tree.append(edge)
	    
    return minimum_spanning_tree

# graph = {
#     'vertices': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
#     'edges': [
#         (7, 'A', 'B'),
#         (5, 'A', 'D'),
#         # (7, 'B', 'A'),
#         (8, 'B', 'C'),
#         (9, 'B', 'D'),
#         (7, 'B', 'E'),
#         # (8, 'C', 'B'),
#         (5, 'C', 'E'),
#         # (5, 'D', 'A'),
#         # (9, 'D', 'B'),
#         (7, 'D', 'E'),
#         (6, 'D', 'F'),
#         # (7, 'E', 'B'),
#         # (5, 'E', 'C'),
#         # (7, 'E', 'D'),
#         (8, 'E', 'F'),
#         (9, 'E', 'G'),
#         # (6, 'F', 'D'),
#         # (8, 'F', 'E'),
#         (11, 'F', 'G'),
#         # (9, 'G', 'E'),
#         # (11, 'G', 'F')
#     ]
# }

# 만들어진 graph load
# import json
# with open('data.json', 'r') as file:
#     graph = json.load(file)

# 모듈로 import해서 사용하기
def init_graph(filename, N):
    from preprocess import get_graph
    graph = get_graph(filename, N)
    
    return kruskal(graph)
