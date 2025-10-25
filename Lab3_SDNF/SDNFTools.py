from typing import List, Optional, Set


class SDNFMinimizer:
    """
    Класс для минимизации Совершенной Дизъюнктивной Нормальной Формы (СДНФ)
    с использованием метода Квайна-МакКласки.
    """

    def __init__(self, truth_table: List[int]):
        self.truth_table = truth_table
        self.num_vars = self._calculate_num_variables()
        self.minterms = self._extract_minterms()

    def _calculate_num_variables(self) -> int:
        """Вычисляет количество переменных на основе размера таблицы истинности."""
        table_size = len(self.truth_table)
        if table_size == 0:
            return 0
        return (table_size - 1).bit_length()

    def _extract_minterms(self) -> List[int]:
        """Извлекает минтермы из таблицы истинности."""
        return [i for i, value in enumerate(self.truth_table) if value == 1]

    @staticmethod
    def _count_ones(binary_number: int) -> int:
        """Подсчитывает количество единиц в двоичном представлении числа."""
        return bin(binary_number).count('1')

    def _get_binary_groups(self) -> List[List[int]]:
        """
        Группирует минтермы по количеству единиц в их двоичном представлении.

        Returns:
            Список групп, где каждая группа содержит минтермы с одинаковым количеством единиц
        """
        groups = [[] for _ in range(self.num_vars + 1)]
        for minterm in self.minterms:
            ones_count = self._count_ones(minterm)
            groups[ones_count].append(minterm)
        return groups

    def _combine_terms(self, term1: int, term2: int) -> Optional[int]:
        """
        Пытается объединить два терма.

        Args:
            term1: Первый терм
            term2: Второй терм

        Returns:
            Объединенный терм или None, если объединение невозможно
        """
        diff_bits = [
            i for i in range(self.num_vars)
            if (term1 >> i & 1) != (term2 >> i & 1)
        ]

        if len(diff_bits) == 1:
            # Убираем различающийся бит (заменяем на '-')
            return term1 & ~(1 << diff_bits[0])
        return None

    def _find_prime_implicants(self) -> Set[int]:
        """
        Находит простые импликанты методом попарного сравнения.

        Returns:
            Множество простых импликантов
        """
        groups = self._get_binary_groups()
        prime_implicants = set()

        # Сравниваем соседние группы
        for i in range(len(groups) - 1):
            current_group = groups[i]
            next_group = groups[i + 1]

            for term1 in current_group:
                for term2 in next_group:
                    combined = self._combine_terms(term1, term2)
                    if combined is not None:
                        prime_implicants.add(combined)

        return prime_implicants

    def _term_to_expression(self, term: int) -> str:
        """
        Преобразует терм в строковое представление.

        Args:
            term: Терм для преобразования

        Returns:
            Строковое представление терма
        """
        variables = []
        for i in range(self.num_vars):
            variable_char = chr(65 + i)  # A, B, C, ...
            if term & (1 << i):
                variables.append(variable_char)
            else:
                variables.append(f'¬{variable_char}')
        return ''.join(variables)

    def get_sdnf_expression(self, terms: List[int]) -> str:
        """
        Формирует СДНФ выражение из списка термов.

        Args:
            terms: Список термов

        Returns:
            Строковое представление СДНФ
        """
        expressions = [self._term_to_expression(term) for term in terms]
        return ' ∨ '.join(expressions)

    def minimize(self) -> str:
        """
        Выполняет минимизацию СДНФ.

        Returns:
            Упрощенное СДНФ выражение
        """
        if not self.minterms:
            return "0"  # Константа 0

        prime_implicants = self._find_prime_implicants()

        if not prime_implicants:
            # Если не удалось объединить, возвращаем исходную СДНФ
            return self.get_sdnf_expression(self.minterms)

        return self.get_sdnf_expression(list(prime_implicants))
