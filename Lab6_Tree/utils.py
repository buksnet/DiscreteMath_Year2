import os
from typing import List, Tuple, Set, Dict

def calculate_matrix_sum(matrix: List[List[int]]) -> int:
    """Вычисляет сумму всех элементов матрицы"""
    return sum(sum(row) for row in matrix)


def _merge_groups(v1: int, v2: int, groups: Dict) -> None:
    """Объединяет две группы вершин"""
    group1 = groups[v1].copy()
    groups[v1].extend(groups[v2])
    groups[v2].extend(group1)


def _union_vertices(v1: int, v2: int, groups: Dict) -> None:
    """Объединяет вершины в одну компоненту связности"""
    if v1 not in groups and v2 not in groups:
        group = [v1, v2]
        groups[v1] = group
        groups[v2] = group
    elif v1 not in groups:
        groups[v2].append(v1)
        groups[v1] = groups[v2]
    else:
        groups[v1].append(v2)
        groups[v2] = groups[v1]


def _should_add_edge(v1: int, v2: int, connected: Set[int], groups: Dict) -> bool:
    """Проверяет, можно ли добавить ребро без создания цикла"""
    return v1 not in connected or v2 not in connected


def print_matrix(matrix: List[List[int]]) -> None:
    """Выводит матрицу в читаемом формате"""
    for row in matrix:
        print(' '.join(f'{val:2d}' for val in row))


def find_minimum_spanning_tree(edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Находит минимальное остовное дерево алгоритмом Краскала"""
    sorted_edges = sorted(edges, key=lambda x: x[0])
    connected_vertices = set()
    vertex_groups = {}
    mst_edges = []

    # Первый проход - соединение компонент
    for weight, v1, v2 in sorted_edges:
        if _should_add_edge(v1, v2, connected_vertices, vertex_groups):
            _union_vertices(v1, v2, vertex_groups)
            mst_edges.append((weight, v1, v2))
            connected_vertices.update([v1, v2])

    # Второй проход - объединение разрозненных компонент
    for weight, v1, v2 in sorted_edges:
        if v2 not in vertex_groups.get(v1, []):
            mst_edges.append((weight, v1, v2))
            _merge_groups(v1, v2, vertex_groups)

    return mst_edges


def find_minimum_spanning_tree_primm(edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """Находит минимальное остовное дерево алгоритмом прима"""
    if not edges:
        return []

    # Создаем словарь смежности для быстрого доступа к рёбрам из вершины
    graph = {}
    for u, v, weight in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    # Начинаем с первой вершины
    start_vertex = edges[0][0]
    connected_vertices = {start_vertex}
    mst_edges = []

    # Пока не подключили все вершины
    while len(connected_vertices) < len(graph):
        min_edge = None
        min_weight = float('inf')

        # Ищем минимальное ребро, соединяющее подключенные и неподключенные вершины
        for vertex in connected_vertices:
            for neighbor, weight in graph[vertex]:
                if neighbor not in connected_vertices and weight < min_weight:
                    min_weight = weight
                    min_edge = (vertex, neighbor, weight)

        if min_edge:
            u, v, weight = min_edge
            mst_edges.append(min_edge)
            connected_vertices.add(v)
        else:
            break  # Граф несвязный

    return mst_edges


def pick_file_from_matrix_mass():
    print("Выберите файл, который вы хотели бы использовать для тестирования программы (стандартный - g22.txt):\n")
    all_files = list(os.listdir('Matrix_Mass'))
    for i, filename in enumerate(os.listdir('Matrix_Mass')):
        print(f"    [{i+1}]: {filename}")

    print("\n> ", end="")
    try:
        choice = int(input())
    except ValueError:
        print("Ошибка считывания ввода. Убедитесь, что вы вводите действительный номер файла.")
        exit(1)

    return all_files[choice-1]

