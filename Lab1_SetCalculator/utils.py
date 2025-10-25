import re
import random
from typing import List, Set, Tuple, Optional


def get_variables_from_expression(expression: str) -> List[str]:
    """Извлечь имена переменных из выражения"""
    variables = []
    for char in expression:
        if (char.isalpha() and
                char not in ['v', '^', '#', '$'] and
                char not in variables):
            variables.append(char)
    return sorted(variables)  # Сортируем для consistency


def replace_variables(expression: str, sets_dict: dict) -> str:
    """Заменить переменные в выражении на реальные множества"""
    result = expression
    # Заменяем в определенном порядке для избежания конфликтов
    for var in sorted(sets_dict.keys(), key=len, reverse=True):
        result = result.replace(var, str(list(sets_dict[var])))
    return result


def extract_operators(expr: str) -> List[str]:
    """Извлечь операторы из выражения"""
    # Игнорируем операторы внутри строкового представления множеств
    clean_expr = re.sub(r'\[[^]]*]', '', expr)
    return [char for char in clean_expr if char in ['v', '^', '#', '$']]


def extract_sets_from_string(expr: str) -> List[Set[int]]:
    """Извлечь множества из строкового представления"""
    sets = []
    pattern = r'\[([^]]+)\]'
    matches = re.findall(pattern, expr)

    for match in matches:
        numbers = []
        for num_str in match.split(','):
            num_str = num_str.strip()
            if num_str:
                try:
                    numbers.append(int(num_str))
                except ValueError:
                    # Пропускаем некорректные числа, но логируем
                    continue
        if numbers:
            sets.append(set(numbers))
        else:
            # Добавляем пустое множество если нужно
            sets.append(set())

    return sets


def find_innermost_brackets(expression: str) -> Tuple[int, int]:
    """Найти индексы самых внутренних скобок"""
    stack = []
    for i, char in enumerate(expression):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                if not stack:  # Самые внутренние скобки
                    return start, i
    return -1, -1


def get_validated_input(prompt: str,
                        value_type: type = int,
                        min_val: Optional[float] = None,
                        max_val: Optional[float] = None) -> any:
    """Универсальная функция для валидированного ввода"""
    while True:
        try:
            value = value_type(input(prompt).strip())

            if min_val is not None and value < min_val:
                print(f"Значение не может быть меньше {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"Значение не может быть больше {max_val}")
                continue

            return value

        except ValueError:
            print(f"Введите корректное значение типа {value_type.__name__}!")
        except KeyboardInterrupt:
            raise


def create_set_random() -> List[int]:
    """Создать множество случайных чисел"""
    size = get_validated_input("Введите размер множества: ", int, 0, 1000)

    arr = [random.randint(-256, 255) for _ in range(size)]
    print(f"Сгенерировано множество из {len(arr)} элементов: {arr}")
    return arr


def create_set_manual() -> List[int]:
    """Создать множество ручным вводом"""
    size = get_validated_input("Введите размер множества: ", int, 0, 100)

    arr = []
    for i in range(size):
        element = get_validated_input(f"Введите элемент {i + 1}: ", int, -256, 255)
        arr.append(element)

    print(f"Введено множество: {arr}")
    return arr


def get_range_boundaries() -> Tuple[int, int]:
    """Получить левую и правую границы диапазона"""
    print("Введите границы диапазона [-256, 255]:")
    left = get_validated_input("Левая граница: ", int, -256, 254)
    right = get_validated_input("Правая граница: ", int, left + 1, 255)
    return left, right


def create_set_by_division() -> List[int]:
    """Создать множество чисел, делящихся на k"""
    left, right = get_range_boundaries()

    k = get_validated_input("Введите делитель: ", int, -255, 255)
    if k == 0:
        raise ValueError("Делитель не может быть нулем!")

    result = [i for i in range(left, right + 1) if i % k == 0]
    print(f"Создано множество из {len(result)} элементов, делящихся на {k}: {result}")
    return result