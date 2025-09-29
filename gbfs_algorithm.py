#GBFS ALGORITMA
import pandas as pd
import heapq
from collections import defaultdict

# Import file dan membaca file csv jarak cilegon ke banyuwangi
filejarak = "/content/estimasi_jarak.csv"  # sesuaikan path setelah upload
df = pd.read_csv(filejarak, delimiter=";")

# === 2. Bangun graph (adjacency list) ===
graph = defaultdict(list)
for _, row in df.iterrows():
    asal = row["Nama_Kota_1"]
    tujuan = row["Nama_Kota_2"]
    jarak = row["Jarak"]
    graph[asal].append((tujuan, jarak))
    graph[tujuan].append((asal, jarak))  # diasumsikan jalan 2 arah
#display(graph)
# === 3. Bangun heuristik sederhana ===
# Di sini kita pakai data jarak langsung ke Banyuwangi sebagai heuristik,
# jika tidak ada koneksi langsung → kasih nilai besar (∞).
heuristic = {city: float('inf') for city in graph}
for _, row in df.iterrows():
    if row["Nama_Kota_2"] == "Banyuwangi":
        heuristic[row["Nama_Kota_1"]] = row["Jarak"]
    elif row["Nama_Kota_1"] == "Banyuwangi":
        heuristic[row["Nama_Kota_2"]] = row["Jarak"]

heuristic["Banyuwangi"] = 0  # heuristik ke goal = 0

# === 4. Implementasi GBFS ===
def greedy_best_first_search(graph, start, goal, heuristic):
    # (heuristik, biaya g(n), node, path)
    pq = [(heuristic.get(start, float('inf')), 0, start, [start])]
    visited = set()

    while pq:
        h, cost, node, path = heapq.heappop(pq)


        if node == goal:
            return path, cost
            #print(f"Expand: {node}, Cost sampai sini: {cost}, Heuristik: {h}, Path: {path}")

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    g_new = cost + weight  # update biaya akumulatif
                    h_new = heuristic.get(neighbor, float('inf'))
                    heapq.heappush(pq, (h_new, g_new, neighbor, path + [neighbor]))

    return None, None


# === 5. Jalankan GBFS dari Cilegon ke Banyuwangi ===
path = greedy_best_first_search(graph, "Cilegon", "Banyuwangi", heuristic)
print("Hasil jalur GBFS dari Cilegon ke Banyuwangi:")
print("Cost: ", path)
# print("banyak node yang ditempuh: ", len(graph))
