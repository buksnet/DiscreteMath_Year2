from typing import Dict, List


class BooleanFunction:
    """
    Класс для анализа свойств булевых функций.

    Attributes:
        vector: Вектор значений булевой функции
        num_variables: Количество переменных функции
        properties: Словарь с вычисленными свойствами функции
    """

    # Словарь для отображения имен свойств
    PROPERTY_NAMES = {
        'is_zero_preserving': '0',
        'is_one_preserving': '1',
        'is_self_dual': 'S',
        'is_monotonic': 'M',
        'is_linear': 'L'
    }

    def __init__(self, vector: str):
        self.vector = vector
        self.num_variables = self._calculate_num_variables()
        self._validate_vector()
        self.properties = self._calculate_all_properties()

    def _calculate_num_variables(self) -> int:
        """Вычисляет количество переменных на основе длины вектора."""
        vector_length = len(self.vector)
        num_vars = 0
        while (2 ** num_vars) < vector_length:
            num_vars += 1
        return num_vars

    def _validate_vector(self) -> None:
        """Проверяет корректность вектора функции."""
        expected_length = 2 ** self.num_variables
        if len(self.vector) != expected_length:
            raise ValueError(
                f"Некорректная длина вектора. Ожидается {expected_length}, "
                f"получено {len(self.vector)}"
            )

        if any(char not in ('0', '1') for char in self.vector):
            raise ValueError("Вектор должен содержать только символы '0' и '1'")

    def is_zero_preserving(self) -> bool:
        """Проверяет сохранение нуля (f(0,...,0) = 0)."""
        return self.vector[0] == '0'

    def is_one_preserving(self) -> bool:
        """Проверяет сохранение единицы (f(1,...,1) = 1)."""
        return self.vector[-1] == '1'

    def is_self_dual(self) -> bool:
        """Проверяет самодвойственность функции."""
        n = len(self.vector)
        for i in range(n // 2):
            # Для самодвойственной функции f(x) = ¬f(¬x)
            if self.vector[i] == self.vector[n - 1 - i]:
                return False
        return True

    def is_monotonic(self) -> bool:
        """Проверяет монотонность функции."""
        n = len(self.vector)

        for i in range(n):
            for j in range(i + 1, n):
                # Проверяем, что если i <= j (покомпонентно), то f(i) <= f(j)
                if self._is_less_or_equal(i, j) and self.vector[i] > self.vector[j]:
                    return False
        return True

    def _is_less_or_equal(self, a: int, b: int) -> bool:
        """
        Проверяет, что двоичный вектор a покомпонентно <= двоичного вектора b.

        Args:
            a: Первое число (индекс в таблице истинности)
            b: Второе число (индекс в таблице истинности)

        Returns:
            True если a <= b покомпонентно, иначе False
        """
        for bit in range(self.num_variables):
            bit_a = (a >> bit) & 1
            bit_b = (b >> bit) & 1
            if bit_a > bit_b:
                return False
        return True

    def is_linear(self) -> bool:
        """Проверяет линейность функции (представима в виде полинома Жегалкина)."""
        if self.num_variables != 3:
            raise ValueError("Проверка линейности поддерживается только для функций от 3 переменных")

        # Для функций от 3 переменных проверяем по количеству единиц
        ones_count = self.vector.count('1')
        return ones_count in (0, 1, 3, 4, 6, 7, 8)

    def _calculate_all_properties(self) -> Dict[str, bool]:
        """Вычисляет все свойства функции."""
        return {
            'is_zero_preserving': self.is_zero_preserving(),
            'is_one_preserving': self.is_one_preserving(),
            'is_self_dual': self.is_self_dual(),
            'is_monotonic': self.is_monotonic(),
            'is_linear': self.is_linear() if self.num_variables == 3 else False
        }

    def get_property_display(self) -> str:
        """
        Возвращает строку для отображения свойств функции.

        Returns:
            Строка вида "+ + + + +" где '+' обозначает наличие свойства
        """
        return " ".join(
            "+" if self.properties[prop_name] else " "
            for prop_name in self.PROPERTY_NAMES.keys()
        )

    def get_properties_dict(self) -> Dict[str, bool]:
        """Возвращает словарь со всеми свойствами функции."""
        return self.properties.copy()

    def __str__(self) -> str:
        """Строковое представление функции."""
        return f"BooleanFunction(vector='{self.vector}', vars={self.num_variables})"


class FunctionAnalyzer:
    """Класс для анализа набора булевых функций."""

    @staticmethod
    def input_functions() -> List[BooleanFunction]:
        """
        Запрашивает у пользователя ввод функций.

        Returns:
            Список объектов BooleanFunction
        """
        try:
            amount = int(input("Введите количество функций: "))
            if amount <= 0:
                raise ValueError("Количество функций должно быть положительным числом")

            functions = []
            for i in range(amount):
                while True:
                    try:
                        vector = input(f"Введите вектор функции f{i}: ").strip()
                        function = BooleanFunction(vector)
                        functions.append(function)
                        break
                    except ValueError as e:
                        print(f"Ошибка: {e}. Попробуйте снова.")

            return functions

        except ValueError as e:
            print(f"Ошибка ввода: {e}")
            return []

    @staticmethod
    def display_functions_table(functions: List[BooleanFunction]) -> None:
        """
        Выводит таблицу со свойствами функций.

        Args:
            functions: Список функций для отображения
        """
        if not functions:
            print("Нет функций для отображения")
            return

        # Заголовок таблицы
        header = "   " + " ".join(BooleanFunction.PROPERTY_NAMES.values())
        print(header)
        print("   " + "-" * (len(header) - 3))

        # Данные функций
        for i, func in enumerate(functions):
            print(f"f{i} {func.get_property_display()}")

    @staticmethod
    def display_detailed_analysis(functions: List[BooleanFunction]) -> None:
        """Выводит подробный анализ всех функций."""
        print("\n" + "=" * 50)
        print("ПОДРОБНЫЙ АНАЛИЗ ФУНКЦИЙ")
        print("=" * 50)

        for i, func in enumerate(functions):
            print(f"\nФункция f{i}: {func.vector}")
            print(f"Количество переменных: {func.num_variables}")
            print("Свойства:")

            for prop_name, prop_symbol in BooleanFunction.PROPERTY_NAMES.items():
                value = func.properties[prop_name]
                status = "ДА" if value else "НЕТ"
                print(f"  {prop_symbol} ({prop_name}): {status}")
