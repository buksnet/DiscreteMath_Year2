from FunctionParser import FunctionAnalyzer


def run():
    """Основная функция программы."""
    print("АНАЛИЗАТОР БУЛЕВЫХ ФУНКЦИЙ")
    print("=" * 30)

    # Ввод функций
    functions = FunctionAnalyzer.input_functions()

    if not functions:
        print("Не удалось загрузить функции. Завершение работы.")
        return

    # Отображение результатов
    print("\nТАБЛИЦА СВОЙСТВ")
    FunctionAnalyzer.display_functions_table(functions)

    # Подробный анализ (опционально)
    show_detailed = input("\nПоказать подробный анализ? (y/n): ").lower().strip()
    if show_detailed == 'y':
        FunctionAnalyzer.display_detailed_analysis(functions)
