import random
from typing import List, Callable

INFINITY = 10 ** 12
MATRIX_SIZE = 10
MATRIX_FILE = "Matrix_Mass/g42.txt"


def multiply_matrices(
        matrix_a: List[List[int]],
        matrix_b: List[List[int]],
        operation: Callable[[List[int]], int]
) -> List[List[int]]:
    """
    Умножает две матрицы, применяя заданную операцию (min/max)
    для объединения путей.

    Args:
        matrix_a: Первая матрица смежности
        matrix_b: Вторая матрица смежности
        operation: Функция для выбора значения (min или max)

    Returns:
        Результирующая матрица после умножения
    """
    result_matrix = [[INFINITY for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            path_weights = []

            for k in range(MATRIX_SIZE):
                if matrix_a[i][k] != 0 and matrix_b[k][j] != 0:
                    path_weights.append(matrix_a[i][k] + matrix_b[k][j])

            if path_weights:
                result_matrix[i][j] = operation(path_weights)
            else:
                result_matrix[i][j] = 0

    return result_matrix


def find_min_paths(matrix: List[List[int]]) -> List[List[int]]:
    """Находит матрицу минимальных путей через умножение матриц."""
    base_matrix = read_matrix_from_file(MATRIX_FILE)
    return multiply_matrices(matrix, base_matrix, min)


def find_max_paths(matrix: List[List[int]]) -> List[List[int]]:
    """Находит матрицу максимальных путей через умножение матриц."""
    base_matrix = read_matrix_from_file(MATRIX_FILE)
    return multiply_matrices(matrix, base_matrix, max)


def print_matrix(matrix: List[List[int]]) -> None:
    """Выводит матрицу в читаемом формате."""
    for row in matrix:
        print(" ".join(f"{value:4d}" if value != INFINITY else "  INF" for value in row))
    print()


def read_matrix_from_file(filename: str) -> List[List[int]]:
    """
    Читает матрицу из файла и устанавливает диагональные элементы в 0.

    Args:
        filename: Путь к файлу с матрицей

    Returns:
        Прочитанная матрица с нулевой диагональю
    """
    try:
        with open(filename, 'r') as file:
            matrix = [list(map(int, line.split())) for line in file]

        # Обнуляем диагональ
        for i in range(len(matrix)):
            matrix[i][i] = 0

        return matrix
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        raise
    except ValueError:
        print("Ошибка: некорректный формат данных в файле")
        raise


def generate_random_matrix(size: int = MATRIX_SIZE) -> List[List[int]]:
    """
    Генерирует случайную матрицу смежности.

    Args:
        size: Размер матрицы (по умолчанию MATRIX_SIZE)

    Returns:
        Сгенерированная матрица с нулевой диагональю
    """
    matrix = [[random.randint(0, 10) for _ in range(size)] for _ in range(size)]

    # Обнуляем диагональ
    for i in range(size):
        matrix[i][i] = 0

    return matrix


def get_user_choice() -> tuple:
    """Получает и валидирует ввод пользователя."""
    try:
        search_type = int(input("Введите тип поиска (min - 0 / max - 1): "))
        if search_type not in (0, 1):
            raise ValueError("Тип поиска должен быть 0 или 1")

        path_length = int(input("Введите длину пути: "))
        if path_length < 1:
            raise ValueError("Длина пути должна быть положительным числом")

        return search_type, path_length
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        raise


def main() -> None:
    """Основная функция программы."""
    try:
        search_type, path_length = get_user_choice()

        matrix = read_matrix_from_file(MATRIX_FILE)
        print("Исходная матрица:")
        print_matrix(matrix)

        # Выбираем операцию в зависимости от типа поиска
        operation = find_min_paths if search_type == 0 else find_max_paths

        # Применяем операцию (n-1) раз для пути длины n
        for _ in range(path_length - 1):
            matrix = operation(matrix)

        result_type = "минимальных" if search_type == 0 else "максимальных"
        print(f"Матрица {result_type} путей длины {path_length}:")
        print_matrix(matrix)

    except (ValueError, FileNotFoundError) as e:
        print(f"Программа завершена с ошибкой: {e}")


if __name__ == "__main__":
    main()