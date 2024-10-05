from itertools import product, permutations
import re


__all__ = ['TruthTable']


class BoolVar:
    def __init__(self, value):
        try:
            if int(value) in (0, 1):
                self.value = value
            else:
                raise ValueError("В функции присутствует целочисленное значение!")
        except ValueError as e:
            print('Ошибка:', e)

    # '-' — отрицание "нет"
    def __neg__(self):
        return BoolVar(not self.value)

    # '+' — дизъюнкция "или"
    def __add__(self, other):
        return BoolVar(self.value or other.value)

    # '*' — конъюнкция "и"
    def __mul__(self, other):
        return BoolVar(self.value and other.value)

    # '<=' — импликация "если ..., тогда"
    def __le__(self, other):
        return BoolVar((not self.value) or other.value)

    # '^' — исключающее или "или только ..., или только ..."
    def __xor__(self, other):
        return BoolVar(self.value != other.value)

    # '=' — эквивалентность "ровно"
    def __eq__(self, other):
        return BoolVar(self.value == other.value)

    # строковое представление значения
    def __str__(self):
        return "1" if self.value else "0"

    def __format__(self, format_spec):
        return format(str(self), format_spec)


class TruthTable:
    """
    Класс таблицы истинности, строящейся по функции\n
    Пример: \n
    table = TruthTable('x or (not y) and z <= w')\n
    table = TruthTable('x + (- y) * z -> w')\n
    table = TruthTable('x ∨ (¬ y) ∧ z → w')
    """

    @staticmethod
    def __format_func1(func) -> str:
        func = (func
                .replace('xor', '^')
                .replace('or', '+')
                .replace('∨', '+')
                .replace('and', '*')
                .replace('∧', '*')
                .replace('not', '-')
                .replace('¬', '-')
                .replace('->', '<=')
                .replace('→', '<=')
                .replace(' = ', ' == ')
                .replace('≡', '==')
                .replace('True', '1')
                .replace('False', '0'))
        return func

    @staticmethod
    def __format_func2(func) -> str:
        new_func = ''
        for symbol in func:
            if symbol.isdigit():
                new_func += f'BoolVar({symbol})'
            else:
                new_func += symbol
        return new_func

    @staticmethod
    def __get_table(variables, func) -> list:
        try:
            vars_for_eval = {}
            lines = []
            for values in product((BoolVar(0), BoolVar(1)), repeat=len(variables)):
                for i, value in list(enumerate(values)):
                    vars_for_eval[variables[i]] = value
                line = list(vars_for_eval.values())
                line.append(eval(func, {'BoolVar': BoolVar}, vars_for_eval))
                lines.append(line)
            return lines
        except AttributeError:
            return []

    def __init__(self, func: str):
        self.func = self.__format_func1(func)
        self.variables = sorted(set(re.findall(r"[A-Za-z]", self.func)))
        self.func = self.__format_func2(self.func)
        self.lines = self.__get_table(self.variables, self.func)
        self.columns = {
            self.variables[i]: [str(line[i]) for line in self.lines]
            for i in range(len(self.variables))
        }
        self.columns['F'] = [str(line[-1]) for line in self.lines]

    def __str__(self, where_result=None):
        text = ''
        for var in self.variables:
            text += f" {var} |"
        text += " | F"
        res = []
        for line in self.lines:
            res.append(tuple(map(str, line)))
        for line in res:
            if not where_result:
                text += '\n ' + ' | '.join(line[:-1]) + f" | | {line[-1]}"
            elif line[-1] == str(int(where_result)):
                text += '\n ' + ' | '.join(line[:-1]) + f" | | {line[-1]}"
        return text

    def where_result(self, result) -> str:
        """
        Выводит все строки таблицы где значение функции равно выбранному\n
        Пример: print(table.where_result(0))

        :param result: 0 или 1 (True или False)
        """
        text = ''
        for var in self.variables:
            text += f" {var} |"
        text += " | F"
        res = []
        for line in self.lines:
            res.append(tuple(map(str, line)))
        for line in res:
            if line[-1] == str(int(result)):
                text += '\n ' + ' | '.join(line[:-1]) + f" | | {line[-1]}"
        return text

    def combine(self, *matrix: str) -> str:
        """
        Сопоставляет одну таблицу с другой по известным значениям\n
        Пример: table.combine('1.00', '.1.0')

        :param matrix: '10..0', где . - неизвестное значение
        :return: Последовательность переменных
        """
        for vars_ in permutations(self.variables):
            keys = (*vars_, 'F')
            truth_t = '\n'
            for i in range(len(self.columns['F'])):
                for key in keys:
                    truth_t += self.columns[key][i]
                truth_t += '\n'
            for pattern in matrix:
                if not re.search(pattern, truth_t):
                    break
                else:
                    truth_t = re.sub(pattern, '', truth_t, count=1)
            else:
                self.variables = keys[:-1]
                self.lines = self.__get_table(self.variables, self.func)
                return ''.join(keys[:-1])
        return 'Соответствий не найдено!'
