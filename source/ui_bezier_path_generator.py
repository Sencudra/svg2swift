"""
UIBezierPathGenerator
"""

from source.parser import Parser
from source.point import Point, CoordinateSystem


class WrongCoordinateSystem(Exception):
    """Exception for wrongs coordinate system being passed"""
    def __init__(self):
        Exception.__init__(self, "Wrong coordinate type")


class UIBezierPathGenerator:
    """Generates swift code for UIBezierPath"""

    # Public methods

    def __init__(self):
        """Setup generator"""
        self.__parser = Parser()
        self.__current_pos = Point(0.0, 0.0)
        self.__last_cubic_control_point = None
        self.__last_quadratic_control_point = None
        self.__command_map = {
            'm': self.__generate_move_to,
            'l': self.__generate_line_to,
            'h': self.__generate_horizontal_line_to,
            'v': self.__generate_vertical_line_to,
            'c': self.__generate_cubic_curve,
            's': self.__generate_cubic_smooth_curve,
            'q': self.__generate_quadratic_curve,
            't': self.__generate_quadratic_smooth_curve,
            'a': self.__generate_elliptical_curve,
            'z': self.__generate_close
        }

    def generate(self, svg):
        """Generates and returns Swift Code for UIBezierPath"""
        script = ["path = UIBezierPath()"]
        parsed_data = self.__parser.parse_svg(svg)

        for command in parsed_data:

            specifier = command[0]
            if specifier not in self.__parser.commands['cubic'] or \
               specifier not in self.__parser.commands['quadratic']:
                self.__update_last_cubic_control_point(self.__current_pos)
                self.__update_last_quadratic_control_point(self.__current_pos)

            if specifier.isupper():
                coordinate_system = CoordinateSystem.ABSOLUTE
            else:
                coordinate_system = CoordinateSystem.RELATIVE

            result = self.__command_map[specifier.lower()](command[1], coordinate_system)
            script.append(result)

        return script

    # Private methods

    def __update_last_quadratic_control_point(self, point: Point):
        self.__last_quadratic_control_point = point

    def __update_last_cubic_control_point(self, point: Point):
        self.__last_cubic_control_point = point

    def __update_current_pos(self, point: Point):
        self.__current_pos += point

    def __generate_move_to(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for move commands"""
        end_point = Point(command[0], command[1])

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_move_to(end_point)

    def __generate_line_to(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for line command"""
        end_point = Point(command[0], command[1])

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_add_line(end_point)

    def __generate_horizontal_line_to(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for horizontal line command"""
        end_point = Point(command[0], self.__current_pos.y)

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + Point(command[0], 0.0)
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_add_line(end_point)

    def __generate_vertical_line_to(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for vertical line command"""
        end_point = Point(self.__current_pos.x, command[0])

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + Point(0.0, command[0])
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_add_line(end_point)

    def __generate_cubic_curve(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for cubic curve command"""
        first_control_point = Point(command[0], command[1])
        second_control_point = Point(command[2], command[3])
        end_point = Point(command[4], command[5])

        if coords == CoordinateSystem.RELATIVE:
            first_control_point = self.__current_pos + first_control_point
            second_control_point = self.__current_pos + second_control_point
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        self.__update_last_cubic_control_point(second_control_point)
        return self.__print_cubic(end_point, first_control_point, second_control_point)

    def __generate_cubic_smooth_curve(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for cubic smooth curve command"""

        first_control_point = 2 * self.__current_pos - self.__last_cubic_control_point
        second_control_point = Point(command[0], command[1])
        end_point = Point(command[2], command[3])

        if coords == CoordinateSystem.RELATIVE:
            second_control_point = self.__current_pos + second_control_point
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_cubic(end_point, first_control_point, second_control_point)

    def __generate_quadratic_curve(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for quadratic curve command"""

        control_point = Point(command[0], command[1])
        end_point = Point(command[2], command[3])

        if coords == CoordinateSystem.RELATIVE:
            control_point = self.__current_pos + control_point
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        self.__update_last_quadratic_control_point(control_point)
        return self.__print_quadratic(end_point, control_point)

    def __generate_quadratic_smooth_curve(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for smooth quadratic curve command"""

        end_point = Point(command[0], command[1])
        control_point = 2 * self.__current_pos - self.__last_quadratic_control_point

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        self.__update_last_quadratic_control_point(control_point)
        return self.__print_quadratic(end_point, control_point)

    def __generate_elliptical_curve(self, command, coords=CoordinateSystem.ABSOLUTE):
        """Generates string output for elliptical curve command"""
        radius = Point(command[0], command[1])
        # angle = command[2]
        # large_arc_flag = command[3]
        sweep_flag = 'true' if command[4] == 1 else 'false'
        end_point = Point(command[5], command[6])

        if coords == CoordinateSystem.RELATIVE:
            end_point = self.__current_pos + end_point
        elif coords != CoordinateSystem.ABSOLUTE:
            raise WrongCoordinateSystem()

        self.__update_current_pos(end_point)
        return self.__print_elliptical(
            end_point,
            radius.x,
            0.0,
            360.0,
            sweep_flag)

    def __generate_close(self, *argc):
        _ = argc
        return self.__print_close()

    # Static methods

    @staticmethod
    def __print_move_to(end_point: Point):
        """Returns swift code string for line path"""
        return "path.move(to: CGPoint(x: {}, y: {}))".format(end_point.x, end_point.y)

    @staticmethod
    def __print_add_line(end_point: Point):
        """Returns swift code string for line path"""
        return "path.addLine(to: CGPoint(x: {}, y: {}))".format(end_point.x, end_point.y)

    @staticmethod
    def __print_cubic(end_point: Point, first_control_point: Point, second_control_point: Point):
        """Returns swift code string for cubic curve path"""
        return 'path.addCurve(to: CGPoint(x: {}, y: {}), ' \
               'controlPoint1: CGPoint(x: {}, y: {}), ' \
               'controlPoint2: CGPoint(x: {}, y: {}))'.format(
                   end_point.x,
                   end_point.y,
                   first_control_point.x,
                   first_control_point.y,
                   second_control_point.x,
                   second_control_point.y)

    @staticmethod
    def __print_quadratic(end_point: Point, control_point: Point):
        """Returns swift code string for quadratic curve path"""
        return "path.addQuadCurve(to: CGPoint(x: {}, y: {}), " \
               "controlPoint: CGPoint(x: {}, y: {}))".format(
                   end_point.x,
                   end_point.y,
                   control_point.x,
                   control_point.y)

    @staticmethod
    def __print_elliptical(end_point: Point, radius, start_angle, end_angle, clockwise):
        """Returns swift code string for elliptical path"""
        return "path.addArc(withCenter: CGPoint(x: {}, y: {}), " \
               "radius: CGFloat({}), startAngle: CGFloat({}), " \
               "endAngle: CGFloat({}), clockwise: {})".format(
                   end_point.x,
                   end_point.y,
                   radius,
                   start_angle,
                   end_angle,
                   clockwise)

    @staticmethod
    def __print_close():
        """Returns swift code string for close path command"""
        return "path.close()"
