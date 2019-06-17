"""
Unit Tests for UIBezierGenerator
"""

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

        # Then
        assert result == [
            'path = UIBezierPath()',
            'path.move(to: CGPoint(x: 0.28, y: 35.25))',
            'path.addLine(to: CGPoint(x: 5.0, y: 35.25))',
            'path.addCurve(to: CGPoint(x: 31.28, y: 38.5), '
            'controlPoint1: CGPoint(x: 5.28, y: 70.5), '
            'controlPoint2: CGPoint(x: 3.2800000000000002, y: 38.5))',
            'path.addCurve(to: CGPoint(x: 73.56, y: 118.0), '
            'controlPoint1: CGPoint(x: 58.56, y: 109.0), '
            'controlPoint2: CGPoint(x: 58.56, y: 118.0))',
            'path.addCurve(to: CGPoint(x: 139.12, y: 215.0), '
            'controlPoint1: CGPoint(x: 131.12, y: 227.0), '
            'controlPoint2: CGPoint(x: 133.12, y: 215.0))',
            'path.addCurve(to: CGPoint(x: 258.24, y: 458.0), '
            'controlPoint1: CGPoint(x: 254.24, y: 442.0), '
            'controlPoint2: CGPoint(x: 258.24, y: 449.0))',
            'path.addCurve(to: CGPoint(x: 472.48, y: 929.0), '
            'controlPoint1: CGPoint(x: 507.48, y: 900.0), '
            'controlPoint2: CGPoint(x: 499.48, y: 929.0))',
            'path.addCurve(to: CGPoint(x: 951.96, y: 1823.0), '
            'controlPoint1: CGPoint(x: 959.96, y: 1829.0), '
            'controlPoint2: CGPoint(x: 962.96, y: 1823.0))',
            'path.addCurve(to: CGPoint(x: 1902.92, y: 3662.0), '
            'controlPoint1: CGPoint(x: 1916.92, y: 3652.0), '
            'controlPoint2: CGPoint(x: 1909.92, y: 3662.0))',
            'path.addCurve(to: CGPoint(x: 0.28, y: 35.25), '
            'controlPoint1: CGPoint(x: 0.28, y: 49.25), '
            'controlPoint2: CGPoint(x: 0.28, y: 35.25))',
            'path.close()'
        ]

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
        command = (6.0, 4.0, 10.0, 1.0, 0.0, 14.0, 10.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_elliptical_curve(
            command,
            coords=CoordinateSystem.ABSOLUTE)

        # Then
        assert result == 'path.addArc(withCenter: CGPoint(x: 14.0, y: 10.0), ' \
                         'radius: CGFloat(6.0), startAngle: CGFloat(0.0), ' \
                         'endAngle: CGFloat(360.0), clockwise: false)'

    def test_generate_elliptical_curve_absolute_previous_relative(self):
        # Given
        # rx, ry, angle, large_arc_flag, sweep-flag, x, y
        command = (6.0, 4.0, 10.0, 1.0, 0.0, 14.0, 10.0)
        self.generator._UIBezierPathGenerator__current_pos = Point(1.0, 4.0)

        # When
        result = self.generator._UIBezierPathGenerator__generate_elliptical_curve(
            command,
            coords=CoordinateSystem.RELATIVE)

        # Then
        assert result == 'path.addArc(withCenter: CGPoint(x: 15.0, y: 14.0), ' \
                         'radius: CGFloat(6.0), startAngle: CGFloat(0.0), ' \
                         'endAngle: CGFloat(360.0), clockwise: false)'

    def test_generate_elliptical_curve_relative_previous_absolute(self):
        # Given
        command = []

        # When
        result = self.generator._UIBezierPathGenerator__generate_close()

        # Then
        assert True

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
