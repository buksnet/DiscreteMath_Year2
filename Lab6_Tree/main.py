from utils import *


class GraphProcessor:
    """Класс для обработки графов и алгоритма Краскала"""

    def __init__(self, filename: str):
        self.filename = filename
        self.matrix = []
        self.size = 0

    def read_matrix_from_file(self) -> List[List[int]]:
        """Читает матрицу смежности из файла"""
        try:
            with open(self.filename, 'r') as file:
                self.matrix = []
                for line in file:
                    row = list(map(int, line.strip().split()))
                    self.matrix.append(row)

                self.size = len(self.matrix)
                self._set_diagonal_to_ones()
                return self.matrix

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не найден")
        except ValueError:
            raise ValueError("Ошибка при преобразовании данных в числа")

    def _set_diagonal_to_ones(self) -> None:
        """Устанавливает диагональные элементы в 1"""
        for i in range(self.size):
            self.matrix[i][i] = 1

    def create_edges_list(self) -> List[Tuple[int, int, int]]:
        """Создает список ребер в формате (вес, вершина1, вершина2)"""
        edges = []
        for i in range(self.size):
            for j in range(i + 1, self.size):  # j > i исключает дубликаты
                weight = self.matrix[i][j]
                if weight != 0:
                    edges.append((weight, i + 1, j + 1))
        return edges

    def create_mst_matrix(self, mst_edges: List[Tuple[int, int, int]]) -> List[List[int]]:
        """Создает матрицу смежности для минимального остовного дерева"""
        mst_matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for weight, v1, v2 in mst_edges:
            mst_matrix[v1 - 1][v2 - 1] = weight
            # Для неориентированного графа добавляем симметричный элемент
            mst_matrix[v2 - 1][v1 - 1] = weight

        return mst_matrix




def main():
    """Основная функция программы"""
    matrix_file = pick_file_from_matrix_mass()
    file = "Matrix_Mass/Matrix4"


    try:
        processor = GraphProcessor(file)

        # Чтение и обработка матрицы
        matrix = processor.read_matrix_from_file()
        print("Исходная матрица:")
        print_matrix(matrix)

        # Создание списка ребер
        edges = processor.create_edges_list()
        print(f"\nСписок ребер: {edges}")

        # Сортировка ребер по весу
        sorted_edges = sorted(edges, key=lambda x: x[0])
        print(f"Отсортированные ребра: {sorted_edges}")

        # Построение минимального остовного дерева
        mst_edges = find_minimum_spanning_tree(edges)

        # Создание результирующей матрицы
        mst_matrix = processor.create_mst_matrix(mst_edges)

        print("\nМатрица минимального остовного дерева:")
        print_matrix(mst_matrix)

        # Вычисление и вывод суммы
        matrix_sum = calculate_matrix_sum(mst_matrix)
        print(f"\nСумма элементов матрицы: {matrix_sum}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
