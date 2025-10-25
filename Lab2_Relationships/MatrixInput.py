import random
from typing import List


class MatrixIO:
    """Класс для операций ввода-вывода матриц."""

    @staticmethod
    def create_random_matrix() -> List[List[int]]:
        """Создает случайную бинарную матрицу."""
        size = int(input("Размер матрицы: "))
        return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

    @staticmethod
    def create_manual_matrix() -> List[List[int]]:
        """Создает матрицу по введенным пользователем значениям."""
        size = int(input("Размер матрицы: "))
        matrix = []
        print("Введите элементы матрицы построчно:")
        for row in range(size):
            row_data = []
            for col in range(size):
                value = int(input(f"Элемент [{row}, {col}]: "))
                row_data.append(value)
            matrix.append(row_data)
        return matrix

    @staticmethod
    def print_matrix(matrix: List[List[int]]) -> None:
        """Выводит матрицу в читаемом формате."""
        for row in matrix:
            print(" ".join(map(str, row)))
        print()

    @staticmethod
    def read_from_file(filename: str) -> List[List[int]]:
        """
        Читает матрицу из файла.

        Args:
            filename: Имя файла для чтения

        Returns:
            Прочитанная матрица
        """
        try:
            with open(filename, 'r') as file:
                matrix = [list(map(int, line.split())) for line in file]
            return matrix
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except ValueError:
            raise ValueError("Некорректный формат данных в файле")

    @staticmethod
    def write_to_file(matrix: List[List[int]], filename: str) -> None:
        """
        Записывает матрицу в файл.

        Args:
            matrix: Матрица для записи
            filename: Имя файла для записи
        """
        with open(filename, 'w') as file:
            for row in matrix:
                file.write(" ".join(map(str, row)) + '\n')


class MatrixInputHandler:
    """Обработчик выбора способа ввода матрицы."""

    @staticmethod
    def get_matrix_input() -> List[List[int]]:
        """Предлагает пользователю выбрать способ ввода матрицы."""
        print("Выберите способ ввода матрицы:")
        print("1 - Случайная генерация")
        print("2 - Ручной ввод")
        print("3 - Загрузка из файла")

        choice = input("Ваш выбор (1-3): ").strip()

        if choice == "1":
            return MatrixIO.create_random_matrix()
        elif choice == "2":
            return MatrixIO.create_manual_matrix()
        elif choice == "3":
            filename = "./Matrix_Mass/" + input("Имя файла: ")
            return MatrixIO.read_from_file(filename)
        else:
            print("Неверный выбор, используется случайная генерация")
            return MatrixIO.create_random_matrix()
