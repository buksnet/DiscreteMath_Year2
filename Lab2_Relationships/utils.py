import random
from typing import List
from MatrixInput import MatrixIO, MatrixInputHandler
from RelationChecker import RelationChecker


def analyze_relation(matrix: List[List[int]]) -> None:
    """
    Проводит полный анализ свойств бинарного отношения.

    Args:
        matrix: Матрица бинарного отношения
    """
    print("\n" + "=" * 50)
    print("Анализ бинарного отношения:")
    print("=" * 50)

    MatrixIO.print_matrix(matrix)

    checker = RelationChecker(matrix)

    properties = [
        ("Рефлексивность", checker.check_reflexivity),
        ("Транзитивность", checker.check_transitivity),
        ("Симметричность", checker.check_symmetry),
        ("Связность", checker.check_connectivity),
    ]

    for property_name, check_function in properties:
        result = check_function()
        print(f"{property_name}: {result}")

def run():
    """Основная функция программы."""
    try:
        # Получаем матрицу от пользователя
        matrix = MatrixInputHandler.get_matrix_input()

        # Анализируем отношение
        analyze_relation(matrix)

        # Сохраняем результат
        MatrixIO.write_to_file(matrix, "relation_analysis_result.txt")
        print("\nРезультат сохранен в файл 'relation_analysis_result.txt'")

    except (ValueError, FileNotFoundError) as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")