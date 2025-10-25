from typing import List


class RelationChecker:
    """Класс для проверки свойств бинарных отношений."""

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.size = len(matrix)

    def check_reflexivity(self) -> str:
        """
        Проверяет рефлексивность отношения.

        Returns:
            Строка с описанием свойства рефлексивности
        """
        is_reflexive = all(self.matrix[i][i] == 1 for i in range(self.size))
        is_anti_reflexive = all(self.matrix[i][i] == 0 for i in range(self.size))

        if is_reflexive:
            return "Отношение рефлексивно"
        elif is_anti_reflexive:
            return "Отношение антирефлексивно"
        else:
            return "Отношение нерефлексивно"

    def check_transitivity(self) -> str:
        """
        Проверяет транзитивность отношения.

        Returns:
            Строка с описанием свойства транзитивности
        """
        is_transitive = True
        is_anti_transitive = True

        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if self.matrix[i][j] == 1 and self.matrix[j][k] == 1:
                        if self.matrix[i][k] != 1:
                            is_transitive = False
                        if self.matrix[i][k] == 1:
                            is_anti_transitive = False

        if is_transitive:
            return "Отношение транзитивно"
        elif is_anti_transitive:
            return "Отношение антитранзитивно"
        else:
            return "Отношение нетранзитивно"

    def check_connectivity(self) -> str:
        """
        Проверяет связность (полноту) отношения.

        Returns:
            Строка с описанием свойства связности
        """
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.matrix[i][j] == 0 and self.matrix[j][i] == 0:
                    return "Отношение несвязно"
        return "Отношение связно"

    def check_symmetry(self) -> str:
        """
        Проверяет симметричность отношения.

        Returns:
            Строка с описанием свойства симметричности
        """
        is_symmetric = True
        is_antisymmetric = True
        is_asymmetric = True

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 1:
                    if i != j and self.matrix[j][i] == 0:
                        is_symmetric = False
                    if i != j and self.matrix[j][i] == 1:
                        is_antisymmetric = False
                        is_asymmetric = False
                    if i == j and self.matrix[i][i] == 1:
                        is_asymmetric = False

        if is_symmetric:
            return "Отношение симметрично"
        elif is_asymmetric:
            return "Отношение асимметрично"
        elif is_antisymmetric:
            return "Отношение антисимметрично"
        else:
            return "Отношение не имеет четкой симметрии"