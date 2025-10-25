from typing import List, Set
import numpy as np


def binarize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Преобразует матрицу в бинарный вид (0 и 1).

    Args:
        matrix: Исходная матрица

    Returns:
        Бинаризованная матрица
    """
    return (matrix > 0).astype(int)


def print_matrix(matrix: np.ndarray, title: str = "") -> None:
    """
    Выводит матрицу в читаемом формате.

    Args:
        matrix: Матрица для вывода
        title: Заголовок матрицы
    """
    if title:
        print(title)
        print("-" * len(title))

    for row in matrix:
        print(" ".join(f"{val:2d}" for val in row))
    print()


def print_connectivity_components(components: List[Set[int]]) -> None:
    """
    Выводит компоненты связности в удобном формате.

    Args:
        components: Список компонент связности
    """
    print("\nКОМПОНЕНТЫ СВЯЗНОСТИ:")
    print("=" * 30)

    for i, component in enumerate(components, 1):
        vertices_str = ", ".join(map(str, sorted(component)))
        print(f"Компонента {i}: {vertices_str}")

    print(f"\nВсего компонент связности: {len(components)}")
    print(f"Размеры компонент: {[len(comp) for comp in components]}")

