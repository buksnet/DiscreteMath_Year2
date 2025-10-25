import numpy as np

from GraphAnalyzer import GraphAnalyzer
from utils import print_matrix, print_connectivity_components

def run():
    """Основная функция программы."""
    try:
        # Инициализируем анализатор
        analyzer = GraphAnalyzer("Matrix Graph/Matrix4")

        print("МАТРИЦА СМЕЖНОСТИ ГРАФА:")
        print_matrix(analyzer.matrix)

        # Выполняем анализ
        reachability_matrix, components = analyzer.analyze()

        print("МАТРИЦА ДОСТИЖИМОСТИ:")
        print_matrix(reachability_matrix)

        # Выводим компоненты связности
        print_connectivity_components(components)

        # Дополнительная информация
        component_matrix = analyzer.get_component_matrix(components)
        print("\nМАТРИЦА КОМПОНЕНТ СВЯЗНОСТИ:")
        print_matrix(np.array(component_matrix))

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка данных: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")