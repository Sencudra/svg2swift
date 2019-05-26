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

    # Class properties

    word_set = "[aAcChHlLmMqQsStTvVzZ]"
    digit = r"([-|+]?(([0-9]*\.[0-9]+)|([0-9]+)))"

    # Public methods

    def __init__(self):
        pass

    def parse_svg(self, svg_description):
        if not svg_description:
            raise ValueError("Empty input!")

        normalized_input = self.__normalize_input(svg_description)
        split_input = self.__split_input(normalized_input)

        return split_input

    # Private static methods

    @staticmethod
    def __normalize_input(string):
        return "".join(string.rstrip().split())

    @staticmethod
    def __find_first_occurrence(split_symbols, string):
        if len(string) <= 1:
            return 0

        match = re.search(split_symbols, string[1:])

        if not match:
            return 0
        else:
            return match.start() + 1

    @staticmethod
    def __group_values(input_list, n):
        return list(zip(*[input_list[i::n] for i in range(n)]))

        # Private methods

    def __split_input(self, string):
        command_list = []
        string = string

        while len(string) > 1:
            alpha_pos = self.__find_first_occurrence(self.word_set, string)
            command_list.append(string[:alpha_pos])
            string = string[alpha_pos:]

        command_list.append(string)
        return command_list

    def __split_command(self):
        pass

    def __split_moveTo(self, string):
        if string[0] not in "mM":
            raise ValueError("Wrong command passed")
        values_found = [group[0] for group in re.findall(self.digit, string)]
        grouped_values = self.__group_values(values_found, 2)
        return [string[0], [(float(x), float(y)) for x, y in grouped_values]]