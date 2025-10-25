from SDNFTools import SDNFMinimizer
from TruthTable import TruthTableGenerator


def example_function(a: int, b: int, c: int, d: int) -> int:
    """Пример булевой функции для тестирования."""
    return (a and b) or (c and not d)


def run():
    """Основная функция программы."""
    # Пример 1: Готовый массив
    print("Пример 1: Минимизация СДНФ из готового массива")
    truth_table = [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]

    minimizer = SDNFMinimizer(truth_table)
    minimized_sdnf = minimizer.minimize()

    TruthTableGenerator.print_truth_table(truth_table)
    print(f"\nУпрощенная СДНФ: {minimized_sdnf}")

    # Пример 2: Генерация из функции
    print("\n" + "=" * 50)
    print("Пример 2: Генерация  из булевой функции")

    truth_table2 = TruthTableGenerator.generate_from_function(example_function, 4)
    minimizer2 = SDNFMinimizer(truth_table2)
    minimized_sdnf2 = minimizer2.minimize()

    TruthTableGenerator.print_truth_table(truth_table2)
    print(f"\nУпрощенная СДНФ: {minimized_sdnf2}")
