#A* Algoritma

import heapq
import pandas as pd
from collections import defaultdict

# Memuat semua file csv baik itu jarak maupun heuristiknya
filejarak = "estimasi_jarak.csv"
fileheuristic = "HeuristikkeBanyuwangi.csv"
dh = pd.read_csv(fileheuristic, sep=";")
df = pd.read_csv(filejarak, delimiter=";")
#Menampilkan file heuristiknya
display(dh)


# Mendefinisikan file jarak menjadi graph sederhana
graph = defaultdict(list)
for _, row in df.iterrows():
    asal = row["Nama_Kota_1"]
    tujuan = row["Nama_Kota_2"]
    jarak = row["Jarak"]
    graph[asal].append((tujuan, jarak))
    graph[tujuan].append((asal, jarak))

# Heuristic values h(n) from the heuristic table (using the dh DataFrame loaded from HeuristikkeBanyuwangi.csv)
h = {} # Initialize h as a regular dictionary
for _, row in dh.iterrows(): # Use dh for building the heuristic dictionary
    asal = row["Kota Asal"]
    heu = row["Heuristik ke Banyuwangi"]
    h[asal] = heu # Store the heuristic value directly as an integer

def astar(start, goal):
    open_list = []
    # Use h for heuristic lookup
    heapq.heappush(open_list, (h.get(start, float('inf')), 0, start, [start]))  # (f, g, node, path)
    visited = set()

    while open_list:
        f, g, node, path = heapq.heappop(open_list)

        if node == goal:
            depth = len(path) - 1
            return path, g, depth

        if node in visited:
            continue
        visited.add(node)

        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                g_new = g + cost
                # Use h for heuristic lookup
                f_new = g_new + h.get(neighbor, float('inf'))
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float('inf'), None

# Jalankan A* dari Cilegon ke Banyuwangi
route, cost, depth = astar('Cilegon', 'Banyuwangi')

print("Rute terbaik:", route)
print("Total node yang dijelajahi:", len(route))
print("Total biaya:", cost)
print("Total kedalaman:", depth)
