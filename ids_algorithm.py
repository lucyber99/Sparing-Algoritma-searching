#IDS Algoritma (Opsional)
import pandas as pd
from collections import defaultdict
data1 = "estimasi_jarak.csv"
df = pd.read_csv(data1, delimiter=";")

print(df.head())

graph = defaultdict(list)
for _, row in df.iterrows():
    asal = row["Nama_Kota_1"]
    tujuan = row["Nama_Kota_2"]
    jarak = row["Jarak"]
    graph[asal].append((tujuan, jarak))

# Depth Limited Search dengan biaya
def dls(node, goal, limit, path, cost, visited):
    if node == goal:
        return path, cost
    if limit <= 0:
        return None

    for neighbor, edge_cost in graph.get(node, []):
        if neighbor not in visited:
            result = dls(
                neighbor, goal, limit-1,
                path + [neighbor],
                cost + edge_cost,
                visited | {neighbor}
            )
            if result:
                return result
    return None

# Iterative Deepening Search (IDS) dengan biaya
def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        result = dls(start, goal, depth, [start], 0, {start})
        if result:
            return result, depth
    return None, -1

# Jalankan IDS
(route, total_cost), depth = ids("Cilegon", "Banyuwangi")
print("Rute IDS:", route)
print("total node yang dijelajahi", len(route))
print("Total biaya:", total_cost)
print("Kedalaman solusi:", depth)
