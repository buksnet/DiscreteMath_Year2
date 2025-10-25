from typing import List, Dict


class DFA:
    """
    Детерминированный конечный автомат для распознавания языка.

    Автомат принимает строки, содержащие определенные последовательности символов.
    """

    def __init__(self):
        self.initial_state = 'q0'
        self.current_state = self.initial_state
        self.accept_states = {'q1'}
        self.alphabet = {'a', 'b', 'c', 'd'}

        # Таблица переходов между состояниями
        self.transitions = {
            'q0': {'a': 'q0', 'b': 'q0', 'c': 'q1', 'd': 'q0'},
            'q1': {'a': 'q0', 'b': 'q0', 'c': 'q2', 'd': 'q0'},
            'q2': {'a': 'q0', 'b': 'q0', 'c': 'q1', 'd': 'q0'}
        }

        self._validate_automaton()

    def _validate_automaton(self) -> None:
        """Проверяет корректность определения автомата."""
        # Проверяем, что все состояния в переходах существуют
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                if next_state not in self.transitions:
                    raise ValueError(f"Состояние {next_state} не определено в таблице переходов")

        # Проверяем, что все принимающие состояния существуют
        for state in self.accept_states:
            if state not in self.transitions:
                raise ValueError(f"Принимающее состояние {state} не определено в таблице переходов")

        # Проверяем, что начальное состояние существует
        if self.initial_state not in self.transitions:
            raise ValueError(f"Начальное состояние {self.initial_state} не определено")

    def reset(self) -> None:
        """Сбрасывает автомат в начальное состояние."""
        self.current_state = self.initial_state

    def process_symbol(self, symbol: str) -> str:
        """
        Обрабатывает один символ и переходит в следующее состояние.

        Args:
            symbol: Входной символ для обработки

        Returns:
            Новое состояние автомата

        Raises:
            ValueError: если символ не принадлежит алфавиту
        """
        if symbol not in self.alphabet:
            raise ValueError(f"Недопустимый символ: '{symbol}'. Допустимые символы: {self.alphabet}")

        if symbol not in self.transitions[self.current_state]:
            raise ValueError(f"Неопределенный переход из состояния {self.current_state} по символу '{symbol}'")

        self.current_state = self.transitions[self.current_state][symbol]
        return self.current_state

    def process_input(self, input_string: str) -> bool:
        """
        Обрабатывает входную строку и возвращает, принимает ли её автомат.

        Args:
            input_string: Входная строка для обработки

        Returns:
            True если автомат принимает строку, иначе False

        Raises:
            ValueError: если строка содержит недопустимые символы
        """
        self.reset()

        for char in input_string:
            self.process_symbol(char)

        return self.current_state in self.accept_states

    def get_current_state(self) -> str:
        """Возвращает текущее состояние автомата."""
        return self.current_state

    def is_accepting(self) -> bool:
        """Проверяет, находится ли автомат в принимающем состоянии."""
        return self.current_state in self.accept_states


class DFATester:
    """Класс для тестирования DFA с различными входными данными."""

    def __init__(self, dfa: DFA):
        self.dfa = dfa

    def test_single_word(self, word: str) -> dict[str, str | bool | None] | dict[str, str | bool]:
        """
        Тестирует одно слово и возвращает подробный результат.

        Args:
            word: Слово для тестирования

        Returns:
            Словарь с информацией о результате тестирования
        """
        try:
            if word == "":
                accepted = self.dfa.process_input("")
                return {
                    'word': '"" (пустая строка)',
                    'accepted': accepted,
                    'error': None
                }
            else:
                accepted = self.dfa.process_input(word)
                return {
                    'word': word,
                    'accepted': accepted,
                    'error': None
                }

        except ValueError as e:
            return {
                'word': word,
                'accepted': False,
                'error': str(e)
            }

    def test_multiple_words(self, words: List[str]) -> List[Dict[str, str]]:
        """
        Тестирует список слов и возвращает результаты.

        Args:
            words: Список слов для тестирования

        Returns:
            Список результатов тестирования
        """
        results = []
        for word in words:
            results.append(self.test_single_word(word))
        return results

    def print_results(self, results: List[Dict[str, str]]) -> None:
        """Выводит результаты тестирования в читаемом формате."""
        print("\nРЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ DFA")
        print("=" * 50)

        for result in results:
            word = result['word']
            accepted = result['accepted']
            error = result['error']

            if error:
                print(f"Слово '{word}': ОШИБКА - {error}")
            else:
                status = "принимается" if accepted else "не принимается"
                print(f"Слово '{word}': {status}")
