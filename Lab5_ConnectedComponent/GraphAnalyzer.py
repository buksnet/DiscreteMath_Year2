import numpy as np

from utils import binarize_matrix

from typing import Tuple, List, Set

class GraphAnalyzer:
    """
    Класс для анализа компонент связности графа по матрице смежности.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.matrix = self._read_matrix_from_file()
        self.num_vertices = len(self.matrix)

    def _read_matrix_from_file(self) -> np.ndarray:
        """
        Читает матрицу смежности из файла и устанавливает диагональные элементы в 1.

        Returns:
            Матрица смежности как numpy array

        Raises:
            FileNotFoundError: если файл не найден
            ValueError: если данные в файле некорректны
        """
        try:
            with open(self.filename, 'r') as file:
                matrix = []
                for line in file:
                    row = list(map(int, line.split()))
                    matrix.append(row)

            # Преобразуем в numpy array для удобства операций
            matrix = np.array(matrix, dtype=int)

            # Устанавливаем диагональ в 1 (каждая вершина связана сама с собой)
            np.fill_diagonal(matrix, 1)

            return matrix

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не найден")
        except ValueError:
            raise ValueError("Некорректный формат данных в файле")

    def _compute_reachability_matrix(self) -> np.ndarray:
        """
        Вычисляет матрицу достижимости графа.

        Returns:
            Матрица достижимости
        """
        reachability_matrix = self.matrix.copy()

        # Суммируем степени матрицы смежности до n-1
        for power in range(2, self.num_vertices + 1):
            reachability_matrix += np.linalg.matrix_power(self.matrix, power)

        return binarize_matrix(reachability_matrix)

    def _find_connected_components(self, reachability_matrix: np.ndarray) -> List[Set[int]]:
        """
        Находит компоненты связности графа.

        Args:
            reachability_matrix: Матрица достижимости

        Returns:
            Список компонент связности (каждая компонента - множество вершин)
        """
        # Находим уникальные строки матрицы достижимости
        unique_rows = np.unique(reachability_matrix, axis=0)

        components = []
        used_vertices = set()

        for row in unique_rows:
            component = set()
            for vertex in range(self.num_vertices):
                # Если вершина достижима из текущей компоненты
                if reachability_matrix[vertex].tolist() == row.tolist():
                    component.add(vertex + 1)  # +1 для нумерации с 1
                    used_vertices.add(vertex)

            if component:
                components.append(component)

        return components

    def _get_connectivity_components_matrix(self, components: List[Set[int]]) -> List[List[int]]:
        """
        Создает матрицу компонент связности.

        Args:
            components: Список компонент связности

        Returns:
            Матрица, где каждая строка представляет компоненту связности
        """
        component_matrix = []

        for component in components:
            row = [1 if vertex in component else 0 for vertex in range(1, self.num_vertices + 1)]
            component_matrix.append(row)

        return component_matrix

    def analyze(self) -> Tuple[np.ndarray, List[Set[int]]]:
        """
        Выполняет полный анализ графа.

        Returns:
            Кортеж (матрица достижимости, список компонент связности)
        """
        # Вычисляем матрицу достижимости
        reachability_matrix = self._compute_reachability_matrix()

        # Находим компоненты связности
        components = self._find_connected_components(reachability_matrix)

        return reachability_matrix, components

    def get_component_matrix(self, components: List[Set[int]]) -> List[List[int]]:
        """
        Возвращает матрицу компонент связности.

        Args:
            components: Список компонент связности

        Returns:
            Матрица компонент связности
        """
        return self._get_connectivity_components_matrix(components)