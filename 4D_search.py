import numpy as np
from itertools import permutations


def judge(cycle1, cycle2):
    return len(set(cycle1) & set(cycle2)) == 0


def dfs_all(graph, node, visited, path, target_length, cycles):
    if len(path) > target_length:
        return

    visited[node] = True
    path.append(node)

    if len(path) == target_length:
        if graph[path[-1]][path[0]] == 1:  # 判断环闭合
            cycles.append(path[:])
    else:
        for neighbor in range(len(graph)):
            if graph[node][neighbor] == 1 and not visited[neighbor]:
                dfs_all(graph, neighbor, visited, path, target_length, cycles)

    visited[node] = False
    path.pop()


def find_cycles(graph, cycle_length1, cycle_length2):
    all_cycles1 = []

    # 找到所有长度为 cycle_length1 的环
    for start_node in range(len(graph)):
        visited = [False] * len(graph)
        path = []
        dfs_all(graph, start_node, visited, path, cycle_length1, all_cycles1)


    # 遍历每个找到的 cycle1
    for cycle1 in all_cycles1:
        used_nodes = set(cycle1)
        remaining_nodes = [node for node in range(len(graph)) if node not in used_nodes]

        if len(remaining_nodes) < cycle_length2:
            continue

        subgraph = graph[np.ix_(remaining_nodes, remaining_nodes)]
        all_cycles2 = []
        for start_node in range(len(remaining_nodes)):
            visited = [False] * len(remaining_nodes)
            path = []
            dfs_all(subgraph, start_node, visited, path, cycle_length2, all_cycles2)

        for cycle2 in all_cycles2:
            cycle2_mapped = [remaining_nodes[node] for node in cycle2]
            return cycle1, cycle2_mapped

    return None




# 生成图的所有可能组合
def input_graph():
    n = 8
    fixed_first_row = [0] * n
    fixed_first_row[0] = 1

    remaining_perms = permutations(range(1, n))
    all_matrices = []

    for perm in remaining_perms:
        matrix2 = np.zeros((n, n), dtype=int)
        matrix2[0] = fixed_first_row
        for i, col in enumerate(perm):
            matrix2[i + 1][col] = 1
        all_matrices.append(matrix2)

    matrix1 = np.array([
        [0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 0, 0]
    ])

    graphs = []
    for matrix2 in all_matrices:
        matrix3 = np.transpose(matrix2)
        graph = np.block([[matrix1, matrix2], [matrix3, matrix1]])
        graphs.append(graph)

    return graphs


graphs = input_graph()
cycle_length1 = 7
cycle_length2 = 9

for i, g in enumerate(graphs, start=1):
    result = find_cycles(g, cycle_length1, cycle_length2)
    if not result:
        print(g)
        print(i, "no")
