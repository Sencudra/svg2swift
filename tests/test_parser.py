import pytest

from tests.helper import show_name
from source.parser import Parser


class TestParser:

    @show_name("Class setup")
    def setup_class(self):
        self.parser = Parser()

    @show_name("Class teardown")
    def teardown_class(self):
        pass

    # Test public methods

    def test_svg_parse_empty_exception(self):
        # Given
        svg = ""

        # When
        # Nothing to do here

        # Then
        with pytest.raises(ValueError):
            self.parser.parse_svg(svg)

    def test_svg_parse(self):
        # Given
        svg = "M .28,35.25 s-2-32,26 -32 c22,0,22,9,37, 9,21,0,23-12,29-12,5,0,9,7,9,16"

        # When
        result = self.parser.parse_svg(svg)

        # Then
        assert result == [["M", [(0.28, 35.25)]],
            ["s", [(-2.0, -32.0, 26.0, -32.0)]],
            ["c", [(22.0, 0.0, 22.0, 9.0, 37.0, 9.0), (21.0, 0.0, 23.0, -12.0, 29.0, -12.0), (5.0, 0.0, 9.0, 7.0, 9.0, 16.0)]]]

    # Test static methods

    def test_normalize_input_1(self):
        # Given
        string = "C 30,90 25,10 50,10"

        # When
        result = self.parser._Parser__normalize_input(string)

        # Then
        assert result == "C30,90,25,10,50,10"

    def test_normalize_input_2(self):
        # Given
        string = "M .28,35.25 s-2-32,26 -32"

        # When
        result = self.parser._Parser__normalize_input(string)

        # Then
        assert result == "M.28,35.25,s-2-32,26,-32"

    @pytest.mark.parametrize(
        "test_input, expected",
        [(("m", "m"), ("m", None)),
         (("m", "m123m"), ("m123", "m")),
         (("m", "m123m123m123"), ("m123", "m123m123"))])
    def test_find_first_occurrence(self, test_input, expected):
        # Given
        # Nothing to do here

        # When
        result = self.parser._Parser__find_command(*test_input)

        # Then
        assert result == expected

    def test_re_split_simple(self):
        # Given
        svg = "M.28,35.25s-2-32,26-32z"

        # When
        result = self.parser._Parser__split_input(svg)

        # Then
        assert result == ["M.28,35.25", "s-2-32,26-32", "z"]

    def test_re_split_hard(self):
        # Given
        svg = "M.28,35.25s-2-32,26-32c22,0,22,9,37,9,21,0,23-12,29-12,5,0,9,7,9,16"
        # When
        result = self.parser._Parser__split_input(svg)

        # Then
        assert result == ["M.28,35.25",
                          "s-2-32,26-32",
                          "c22,0,22,9,37,9,21,0,23-12,29-12,5,0,9,7,9,16"]

    def test_split_move2command(self):
        # Given
        command = "M0,0.0,10,-10,10,-.20,10,40,100,100"

        # Then
        result = self.parser._Parser__split_move_to(command)

        # When
        assert result == ["M", [(0.0, 0.0), (10.0, -10.0), (10.0,-0.2), (10.0, 40.0), (100.0, 100.0)]]

    def test_split_line2command_1(self):
        # Given
        command = "L0,0.0,10,-10,10,-.20,10,40,100,100"

        # Then
        result = self.parser._Parser__split_line_to(command)

        # When
        assert result == ["L", [(0.0, 0.0), (10.0, -10.0), (10.0,-0.2), (10.0, 40.0), (100.0, 100.0)]]

    def test_split_line2command_2(self):
        # Given
        command = "V0,0.0,10,-10,10,-.20,10,40,100,100"

        # Then
        result = self.parser._Parser__split_line_to(command)

        # When
        assert result == ["V", [(0.0,), (0.0,), (10.0,), (-10.0,), (10.0,), (-0.2,), (10.0,), (40.0,), (100.0,), (100.0,)]]

    def test_split_line2command_3(self):
        # Given
        command = "H0,0.0,10,-10,10,-.20,10,40,100,100"

        # Then
        result = self.parser._Parser__split_line_to(command)

        # When
        assert result == ["H", [(0.0,), (0.0,), (10.0,), (-10.0,), (10.0,), (-0.2,), (10.0,), (40.0,), (100.0,), (100.0,)]]

    def test_split_cubic_1(self):
        # Given
        command = "c20,0,15,-80,40,-80"

        # Then
        result = self.parser._Parser__split_cubic_bezier_curve(command)

        # When
        assert result == ["c", [(20.0, 0.0, 15.0, -80.0, 40.0, -80.0)]]

    def test_split_cubic_2(self):
        # Given
        command = "s20,0,15,-80"

        # Then
        result = self.parser._Parser__split_cubic_bezier_curve(command)

        # When
        assert result == ["s", [(20.0, 0.0, 15.0, -80.0)]]

    def test_split_quadratic_1(self):
        # Given
        command = "q20,0,15,-80"

        # Then
        result = self.parser._Parser__split_quadratic_curve(command)

        # When
        assert result == ["q", [(20.0, 0.0, 15.0, -80.0)]]

    def test_split_quadratic_2(self):
        # Given
        command = "t20,0,15,-80"

        # Then
        result = self.parser._Parser__split_quadratic_curve(command)

        # When
        assert result == ["t", [(20.0, 0.0), (15.0, -80.0)]]

    def test_split_elliptical(self):
        # Given
        command = "A6,4,10,0,0,14,10,6,4,10,0,0,14,10"

        # Then
        result = self.parser._Parser__split_elliptical_curve(command)

        # When
        assert result == ["A", [(6.0, 4.0, 10.0, 0.0, 0.0, 14.0, 10.0),
                                (6.0, 4.0, 10.0, 0.0, 0.0, 14.0, 10.0)]]

    def test_split_command(self):
        # Given
        command = "c22,0,22,9,37,9,21,0,23-12,29-12,5,0,9,7,9,16"

        # Then
        result = self.parser._Parser__split_command(command)

        # When
        assert result == ["c", [(22.0, 0.0, 22.0, 9.0, 37.0, 9.0),
                                (21.0, 0.0, 23.0, -12.0, 29.0, -12.0),
                                (5.0, 0.0, 9.0, 7.0, 9.0, 16.0)]]