#UCS ALGORITMA
import heapq
import pandas as pd
from collections import defaultdict

# import file csv
file1 = "estimasi_jarak.csv"
data = pd.read_csv(file1, delimiter=";")

file2 = "HeuristikkeBanyuwangi.csv"
data2 = pd.read_csv(file2, delimiter=";")

# menampilkan 5 data pertama untuk memastikan file dapat terbaca oleh sistem
print(data.head())
print(data2.head())

# === Bentuk graph logic ===
graph = defaultdict(list)
for index, row in data.iterrows():
    node1_id = row["Posisi_1"]
    node2_id = row["Posisi_2"]
    distance = row["Jarak"]
    graph[node1_id].append((node2_id, distance))
    graph[node2_id].append((node1_id, distance))

def uniform_cost_search(graph, start, goal):
    pq = [(0, start)]  # (cost, node)
    visited = set()
    # To store the path
    path = {start: [start]}
    # To store the cost to reach each node
    cost_so_far = {start: 0}

    while pq:
        current_cost, current_node = heapq.heappop(pq)

        if current_node == goal:
            return path[current_node], cost_so_far[current_node]

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                new_cost = cost_so_far[current_node] + weight
                # Check if the neighbor has not been visited or if the new path is cheaper
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    # The priority queue stores (cost, node) for efficient retrieval of the minimum cost node
                    heapq.heappush(pq, (new_cost, neighbor))
                    # Update the path to the neighbor
                    path[neighbor] = path[current_node] + [neighbor]

    return None, None

# Inisiasi start dan goal done
start_node = 1
goal_node = 38
path, cost = uniform_cost_search(graph, start_node, goal_node)

print(f"Hasil jalur UCS dari node {start_node} ke node {goal_node}:", path)
print(f"Total biaya: {cost}")
