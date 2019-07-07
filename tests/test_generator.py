"""
Unit Tests for UIBezierGenerator
"""

import pytest

from tests.helper import show_name
from source.ui_bezier_path_generator import UIBezierPathGenerator
from source.ui_bezier_path_generator import CoordinateSystem, Point


class TestGenerator:
    """Simple test suite"""

    @show_name('Class setup')
    def setup_class(self):
        """Test suite setup"""
        self.generator = UIBezierPathGenerator()

    @show_name('Class teardown')
    def teardown_class(self):
        """Test suite teardown"""
        pass

    def test_generator(self):
        # Given
        svg = 'M.28,35.25H5s-2-32,26-32c22,0,22,9,37,9,21,0,23-12,29-12,5,0,9,7,9,16s-8,\
               29-35,29c-20,0-17-6-28-6-15,0-22,10-29,10C.28,49.25.28,35.25.28,35.25Z'

        # When
        result = self.generator.generate(svg)

    def test_generate_move_to_absolute(self):
        # Given
        command = (1.0, 2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1, -2)

        # When
        result = self.generator._UIBezierPathGenerator__generate_move_to(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.move(to: CGPoint(x: 1.0, y: 2.0))'

    def test_generate_move_to_relative(self):
        # Given
        command = (1.0, 2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1, -2)

        # When
        result = self.generator._UIBezierPathGenerator__generate_move_to(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.move(to: CGPoint(x: 2.0, y: 0.0))'

    def test_generate_line_to_absolute(self):
        # Given
        command = (1.0, 2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(2, 1)

        # When
        result = self.generator._UIBezierPathGenerator__generate_line_to(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: 1.0, y: 2.0))'

    def test_generate_line_to_relative(self):
        # Given
        command = (1.0, 2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1, 1)

        # When
        result = self.generator._UIBezierPathGenerator__generate_line_to(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: 0.0, y: 3.0))'

    def test_generate_line_to_h_absolute(self):
        # Given
        command = (1.0,)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 3.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_horizontal_line_to(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: 1.0, y: 3.0))'

    def test_generate_line_to_h_relative(self):
        # Given
        command = (1.0,)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 3.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_horizontal_line_to(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: 0.0, y: 3.0))'

    def test_generate_line_to_v_absolute(self):
        # Given
        command = (1.0,)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 3.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_vertical_line_to(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: -1.0, y: 1.0))'

    def test_generate_line_to_v_relative(self):
        # Given
        command = (1.0,)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 3.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_vertical_line_to(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addLine(to: CGPoint(x: -1.0, y: 4.0))'

    def test_generate_cubic_curve_absolute(self):
        # Given
        command = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 2.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_cubic_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addCurve(to: CGPoint(x: 5.0, y: 6.0), ' \
                         'controlPoint1: CGPoint(x: 1.0, y: 2.0), ' \
                         'controlPoint2: CGPoint(x: 3.0, y: 4.0))'

    def test_generate_cubic_curve_relative(self):
        # Given
        command = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(-1.0, 2.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_cubic_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addCurve(to: CGPoint(x: 4.0, y: 8.0), ' \
                         'controlPoint1: CGPoint(x: 0.0, y: 4.0), ' \
                         'controlPoint2: CGPoint(x: 2.0, y: 6.0))'

    def test_generate_cubic_smooth_curve_absolute(self):
        # Given
        command = (1.0, -2.0, -3.0, 4.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(26.0, -32.0)
        self.generator._UIBezierPathGenerator__last_cubic_control_point = Point(-2.0, -32.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_cubic_smooth_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addCurve(to: CGPoint(x: -3.0, y: 4.0), ' \
                         'controlPoint1: CGPoint(x: 54.0, y: -32.0), ' \
                         'controlPoint2: CGPoint(x: 1.0, y: -2.0))'

    def test_generate_cubic_smooth_curve_relative(self):
        # Given
        command = (1.0, -2.0, -3.0, 4.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(26.0, -32.0)
        self.generator._UIBezierPathGenerator__last_cubic_control_point = Point(-2.0, -32.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_cubic_smooth_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addCurve(to: CGPoint(x: 23.0, y: -28.0), ' \
                         'controlPoint1: CGPoint(x: 54.0, y: -32.0), ' \
                         'controlPoint2: CGPoint(x: 27.0, y: -34.0))'

    def test_generate_quadratic_curve_absolute(self):
        # Given
        command = (-1.0, 2.0, 3.0, -4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_quadratic_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addQuadCurve(to: CGPoint(x: 3.0, y: -4.0), ' \
                         'controlPoint: CGPoint(x: -1.0, y: 2.0))'

    def test_generate_quadratic_curve_relative(self):
        # Given
        command = (1.0, -2.0, -3.0, 4.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, -2.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_quadratic_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addQuadCurve(to: CGPoint(x: -2.0, y: 2.0), ' \
                         'controlPoint: CGPoint(x: 2.0, y: -4.0))'

    def test_generate_quadratic_smooth_curve_absolute(self):
        # Given
        command = (1.0, -2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)
        self.generator._UIBezierPathGenerator__last_quadratic_control_point = Point(2.0, -4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_quadratic_smooth_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addQuadCurve(to: CGPoint(x: 1.0, y: -2.0), ' \
                         'controlPoint: CGPoint(x: 0.0, y: 12.0))'

    def test_generate_quadratic_smooth_curve_relative(self):
        # Given
        command = (1.0, -2.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)
        self.generator._UIBezierPathGenerator__last_quadratic_control_point = Point(2.0, -4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_quadratic_smooth_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addQuadCurve(to: CGPoint(x: 2.0, y: 2.0), ' \
                         'controlPoint: CGPoint(x: 0.0, y: 12.0))'

    def test_generate_elliptical_curve_absolute_previous_absolute(self):
        # Given
        # rx, ry, angle, large_arc_flag, sweep-flag, x, y
        command = (6.0, 6.0, 10.0, 1.0, 0.0, 14.0, 10.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_elliptical_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addArc(withCenter: CGPoint(x: 7.5, y: 7.0), ' \
                         'radius: CGFloat(6.0), startAngle: CGFloat(0.0), ' \
                         'endAngle: CGFloat(360.0), clockwise: false)'
        assert self.generator._UIBezierPathGenerator__current_pos == Point(14.0, 10.0)

    def test_generate_elliptical_curve_absolute_previous_relative(self):
        # Given
        # rx, ry, angle, large_arc_flag, sweep-flag, x, y
        command = (6.0, 6.0, 10.0, 1.0, 0.0, 14.0, 10.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_elliptical_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addArc(withCenter: CGPoint(x: 8.0, y: 9.0), ' \
                         'radius: CGFloat(6.0), startAngle: CGFloat(0.0), ' \
                         'endAngle: CGFloat(360.0), clockwise: false)'
        assert self.generator._UIBezierPathGenerator__current_pos == Point(15.0, 14.0)

    @pytest.mark.skip(reason="Old")
    def test_generate_elliptical_curve_relative_previous_absolute(self):
        # Given
        command = []

        # When
        result = self.generator._UIBezierPathGenerator__generate_close()

        # Then
        assert True

    @pytest.mark.skip(reason="Old")
    def test_generate_elliptical_curve_relative_previous_relative(self):
        # Given
        command = []

        # When
        result = self.generator._UIBezierPathGenerator__generate_close()

        # Then
        assert True

    def test_generate_close(self):
        # Given
        # Nothing here

        #When
        result = self.generator._UIBezierPathGenerator__generate_close()

        # Then
        assert result == 'path.close()'
