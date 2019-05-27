import re


class Parser:
    """
    MoveTo: M, m
    LineTo: L, l, H, h, V, v
    Cubic Bézier Curve: C, c, S, s
    Quadratic Bézier Curve: Q, q, T, t
    Elliptical Arc Curve: A, a
    ClosePath: Z, z
    """

    # Private class properties

    __word_set = "[aAcChHlLmMqQsStTvVzZ]"
    __digit = r"([-|+]?(([0-9]*\.[0-9]+)|([0-9]+)))"

    __commands = {
        "move": "mM",
        "line": "lLhHvV",
        "cubic": "cCsS",
        "quadratic": "qQtT",
        "elliptical": "aA",
        "close": "zZ"
    }

    # Public methods

    def __init__(self):
        pass

    def parse_svg(self, svg_description):
        if not svg_description:
            raise ValueError("Empty input!")

        normalized_input = self.__normalize_input(svg_description)
        split_input = self.__split_input(normalized_input)
        commands = [self.__split_command(i) for i in split_input]
        return commands

    # Private static methods

    @staticmethod
    def __normalize_input(string):
        normalized = []
        for index in range(len(string)):
            if string[index] != ' ':
                normalized += string[index]
            elif not string[index-1].isalpha() and string[index-1] != ',':
                normalized += ','

        return "".join(normalized)

    @staticmethod
    def __find_command(split_symbols, string):
        if not string or not string[0].isalpha():
            ValueError("Input string is empty or incorrect!")

        if len(string) == 1:
            return string, None
        else:
            match = re.search(split_symbols, string[1:])

            # last command
            if not match:
                return string, None
            else:
                return string[:match.start()+1], string[match.start()+1:]

    @staticmethod
    def __group_values(input_list, n):
        return list(zip(*[input_list[i::n] for i in range(n)]))

    # Private methods

    def __split_input(self, string):
        command_list = []
        string = string

        command, string = self.__find_command(self.__word_set, string)
        command_list.append(command)

        while string:
            command, string = self.__find_command(self.__word_set, string)
            command_list.append(command)

        return command_list

    def __split_move_to(self, string):
        if string[0] not in self.__commands["move"]:
            raise ValueError("Wrong command passed")

        return [string[0], self.__find_digits_in_groups(string, group_size=2)]

    def __split_line_to(self, string):
        if string[0] not in self.__commands["line"]:
            raise ValueError("Wrong command passed")

        group_size = 2 if string[0] in self.__commands["line"][:2] else 1
        return [string[0], self.__find_digits_in_groups(string, group_size=group_size)]

    def __split_cubic_bezier_curve(self, string):
        if string[0] not in self.__commands["cubic"]:
            raise ValueError("Wrong command passed")

        group_size = 6 if string[0] in self.__commands["cubic"][:2] else 4
        return [string[0], self.__find_digits_in_groups(string, group_size=group_size)]

    def __split_quadratic_curve(self, string):
        if string[0] not in self.__commands["quadratic"]:
            raise ValueError("Wrong command passed")

        group_size = 4 if string[0] in self.__commands["quadratic"][:2] else 2
        return [string[0], self.__find_digits_in_groups(string, group_size=group_size)]

    def __split_elliptical_curve(self, string):
        if string[0] not in self.__commands["elliptical"]:
            raise ValueError("Wrong command passed")

        group_size = 7
        return [string[0], self.__find_digits_in_groups(string, group_size=group_size)]

    def __find_digits_in_groups(self, string, group_size=2, pattern=__digit):
        values_found = [group[0] for group in re.findall(pattern, string)]
        if len(values_found) % group_size != 0:
            raise ValueError("Can not be grouped. Total number is {}".format(values_found))
        grouped_values = self.__group_values(values_found, group_size)
        return [tuple(map(float, group)) for group in grouped_values]

    def __split_command(self, string):
        command = string[0]

        if command in self.__commands["move"]:
            return self.__split_move_to(string)
        elif command in self.__commands["line"]:
            return self.__split_line_to(string)
        elif command in self.__commands["cubic"]:
            return self.__split_cubic_bezier_curve(string)
        elif command in self.__commands["quadratic"]:
            return self.__split_quadratic_curve(string)
        elif command in self.__commands["elliptical"]:
            return self.__split_elliptical_curve(string)
        elif command in self.__commands["close"]:
            return [command, None]
