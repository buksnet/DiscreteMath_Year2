from typing import List, Set
from utils import *


class SetCalculator:
    def __init__(self):
        self.universe = set(range(-256, 256))

    def apply_operation(self, operator: str, stack: List[Set[int]]) -> None:
        """Применить операцию к множествам из стека"""
        try:
            if operator == 'v':  # Объединение
                set2, set1 = stack.pop(), stack.pop()
                stack.append(set1 | set2)
            elif operator == '^':  # Пересечение
                set2, set1 = stack.pop(), stack.pop()
                stack.append(set1 & set2)
            elif operator == '$':  # Разность
                set2, set1 = stack.pop(), stack.pop()
                stack.append(set1 - set2)
            elif operator == '#':  # Отрицание
                set1 = stack.pop()
                stack.append(self.universe - set1)
        except IndexError:
            raise ValueError(f"Недостаточно операндов для операции '{operator}'")

    def evaluate_expression(self, expr: str) -> Set[int]:
        """Вычислить выражение с множествами"""
        current_expr = expr

        while True:
            # Ищем самые внутренние скобки
            start, end = find_innermost_brackets(current_expr)
            if start == -1:  # Скобок больше нет
                break

            # Извлекаем и вычисляем подвыражение в скобках
            sub_expr = current_expr[start + 1:end]
            sets = extract_sets_from_string(sub_expr)
            operators = extract_operators(sub_expr)

            # Проверяем корректность выражения
            if len(sets) != len(operators) + 1:
                raise ValueError("Некорректное выражение: несоответствие количества операндов и операторов")

            # Вычисляем подвыражение
            stack = sets[::-1]
            for op in operators:
                self.apply_operation(op, stack)

            # Заменяем подвыражение результатом
            result_str = str(list(stack[0]))
            current_expr = current_expr[:start] + result_str + current_expr[end + 1:]

        # Обрабатываем оставшееся выражение без скобок
        if any(op in current_expr for op in ['v', '^', '#', '$']):
            sets = extract_sets_from_string(current_expr)
            operators = extract_operators(current_expr)

            if len(sets) != len(operators) + 1:
                raise ValueError("Некорректное выражение: несоответствие количества операндов и операторов")

            stack = sets[::-1]
            for op in operators:
                self.apply_operation(op, stack)

            return stack[0]

        # Если операций не было, возвращаем единственное множество
        final_sets = extract_sets_from_string(current_expr)
        if not final_sets:
            raise ValueError("Не найдено множеств для вычисления")
        return final_sets[0]

    def process_expression(self, expression: str, choice: int) -> None:
        """Обработать выражение с выбранным способом заполнения множеств"""
        variables = get_variables_from_expression(expression)

        if not variables:
            print("В выражении не найдены переменные!")
            return

        # Заполняем множества
        sets_dict = {}
        for var in variables:
            print(f"\nЗаполнение множества {var}:")
            try:
                if choice == 1:
                    sets_dict[var] = set(create_set_random())
                elif choice == 2:
                    sets_dict[var] = set(create_set_manual())
                elif choice == 3:
                    sets_dict[var] = set(create_set_by_division())
            except (ValueError, KeyboardInterrupt) as e:
                print(f"Ошибка при заполнении множества {var}: {e}")
                return

        # Вычисляем выражение
        try:
            expr_with_sets = replace_variables(expression, sets_dict)
            print(f"Вычисляемое выражение: {expr_with_sets}")

            result = self.evaluate_expression(expr_with_sets)
            print(f"Результат ({len(result)} элементов): {sorted(result)}")

        except Exception as e:
            print(f"Ошибка при вычислении: {e}")

    def main(self):
        """Основной цикл программы"""
        print("Калькулятор множеств")
        print("Операции: ^ - пересечение, v - объединение, # - отрицание, $ - разность")

        expression = input("Введите выражение с множествами: ").strip()

        while True:
            print("\n" + "=" * 50)
            print(f"Текущее выражение: {expression}")
            print("1: Заполнить множества случайными числами")
            print("2: Заполнить множества вручную")
            print("3: Заполнить множества числами по условию деления")
            print("4: Ввести новое выражение")
            print("5: Выйти")

            try:
                choice = int(input("Выберите действие: ").strip())
            except ValueError:
                print("Введите число от 1 до 5!")
                continue

            if choice == 5:
                print("До свидания!")
                break
            elif choice == 4:
                new_expr = input("Введите новое выражение: ").strip()
                if new_expr:
                    expression = new_expr
                continue
            elif choice in [1, 2, 3]:
                self.process_expression(expression, choice)
            else:
                print("Неверный выбор! Введите число от 1 до 5.")