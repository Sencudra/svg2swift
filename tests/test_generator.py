import pytest

from tests.helper import show_name
from sources.UIBezierPathGenerator import UIBezierPathGenerator

class TestGenerator():

    @show_name("Class setup")
    def setup_class(self):
        self.generator = UIBezierPathGenerator()

    @show_name("Class teardown")
    def teardown_class(self):
        pass

    def test_generator(self):
        # Given
        svg = "M.28,35.25H5s-2-32,26-32c22,0,22,9,37,9,21,0,23-12,29-12,5,0,9,7,9,16s-8,29-35,29c-20,0-17-6-28-6-15,0-22,10-29,10C.28,49.25.28,35.25.28,35.25Z"

        # When
        self.generator.generate(svg)

        # Then

    def test_generate_move_to_absolute(self):
        # Given
        command = [(1.0, 2.0), (3.0, 4.0)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_move_to(command)

        # Then
        assert result == ["path.move(to: CGPoint(x: 1.0, y: 2.0))",
                "path.move(to: CGPoint(x: 3.0, y: 4.0))"]

    def test_generate_move_to_relative(self):
        # Given
        command = [(1.0, 2.0), (-10.0, 4.0)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_move_to(command, coords="relative")

        # Then
        assert result == ["path.move(to: CGPoint(x: 1.0, y: 2.0))",
                "path.move(to: CGPoint(x: -9.0, y: 6.0))"]

    def test_generate_line_to_absolute(self):
        # Given
        command = [(1.0, 2.0), (3.0, 4.0)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_line_to(command)

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 1.0, y: 2.0))",
                "path.addLine(to: CGPoint(x: 3.0, y: 4.0))"]

    def test_generate_line_to_relative(self):
        # Given
        command = [(1.0, 2.0), (-10.0, 4.0)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_line_to(command, coords="relative")

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 1.0, y: 2.0))",
                "path.addLine(to: CGPoint(x: -9.0, y: 6.0))"]

    def test_generate_line_to_h_absolute(self):
        # Given
        command = [(1.0,), (3.0,)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_horizontal_line_to(command)

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 1.0, y: 0.0))",
                "path.addLine(to: CGPoint(x: 3.0, y: 0.0))"]

    def test_generate_line_to_h_relative(self):
        # Given
        command = [(1.0,), (3.0,)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_horizontal_line_to(command, coords="relative")

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 1.0, y: 0.0))",
                "path.addLine(to: CGPoint(x: 4.0, y: 0.0))"]

    def test_generate_line_to_v_absolute(self):
        # Given
        command = [(1.0,), (-10.0,)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_vertical_line_to(command)

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 0.0, y: 1.0))",
                "path.addLine(to: CGPoint(x: 0.0, y: -10.0))"]

    def test_generate_line_to_v_relative(self):
        # Given
        command = [(1.0,), (-10.0,)]

        # When
        result = self.generator._UIBezierPathGenerator__generate_vertical_line_to(command, coords="relative")

        # Then
        assert result == ["path.addLine(to: CGPoint(x: 0.0, y: 1.0))",
                "path.addLine(to: CGPoint(x: 0.0, y: -9.0))"]