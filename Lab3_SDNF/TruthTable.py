from typing import List


class TruthTableGenerator:
    """Класс для работы с таблицами истинности."""

    @staticmethod
    def generate_from_function(func, num_vars: int) -> List[int]:
        """
        Генерирует таблицу истинности для булевой функции.

        Args:
            func: Булева функция
            num_vars: Количество переменных

        Returns:
            Таблица истинности
        """
        truth_table = []
        for i in range(2 ** num_vars):
            # Преобразуем номер в двоичный вид и подаем на вход функции
            inputs = [(i >> j) & 1 for j in range(num_vars)]
            truth_table.append(func(*inputs))
        return truth_table

    @staticmethod
    def print_truth_table(truth_table: List[int]) -> None:
        """Выводит таблицу истинности в читаемом формате."""
        num_vars = (len(truth_table) - 1).bit_length()

        print("\nТаблица истинности:")
        print("-" * (num_vars * 3 + 10))

        # Заголовок
        header = " | ".join(chr(65 + i) for i in range(num_vars)) + " | F"
        print(header)
        print("-" * (num_vars * 3 + 10))

        # Данные
        for i, value in enumerate(truth_table):
            binary_repr = format(i, f'0{num_vars}b')
            row = " | ".join(binary_repr) + f" | {int(value)}"
            print(row)
