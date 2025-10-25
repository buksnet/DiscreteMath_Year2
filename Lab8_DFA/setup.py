from DFA import DFA, DFATester

def run():
    """Основная функция программы."""
    try:
        # Создаем автомат
        dfa = DFA()
        tester = DFATester(dfa)

        # Тестовые слова
        test_words = ["acc", "avbccc", "aabccccc", "abcc", "cc", "abccc", "abcd", ""]

        # Тестируем слова
        results = tester.test_multiple_words(test_words)

        # Выводим результаты
        tester.print_results(results)

        # Дополнительная информация
        print(f"\nДополнительная информация:")
        print(f"Алфавит: {sorted(dfa.alphabet)}")
        print(f"Начальное состояние: {dfa.initial_state}")
        print(f"Принимающие состояния: {dfa.accept_states}")
        print(f"Все состояния: {list(dfa.transitions.keys())}")

    except Exception as e:
        print(f"Ошибка при создании автомата: {e}")
