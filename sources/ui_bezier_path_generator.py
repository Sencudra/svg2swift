"""

    UIBezierPathGenerator

"""

from sources.parser import Parser

# TODO: simplify functions
# TODO: probably should be a struct or class for x and y cause self.__current_pos is ugly


class UIBezierPathGenerator:
    """
        This is UIBezierPathGenerator
    """

    # Public methods

    def __init__(self):
        self.__parser = Parser()

        self.__current_pos = [0.0, 0.0]

        self.__last_cubic_control_point = None
        self.__last_quadratic_control_point = None

    def generate(self, svg):
        """ Generates Swift Code for UIBezierPath"""

        script = ["path = UIBezierPath()"]
        parsed_data = self.__parser.parse_svg(svg)

        for command in parsed_data:
            print(command)
            # Do stuff

        return script

    # Private methods

    def __update_last_quadratic_control_point(self, x_0, y_0):
        self.__last_quadratic_control_point = x_0, y_0

    def __update_last_cubic_control_point(self, x_0, y_0):
        self.__last_cubic_control_point = x_0, y_0

    def __update_current_pos(self, x_0, y_0):
        self.__current_pos[0] += x_0
        self.__current_pos[1] += y_0

    def __generate_move_to(self, command, coords="absolute"):
        """ Generate string output for move commands. """
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_0, y_0 = command

        if coords == "absolute":
            output.append(self.__print_move_to(x_0, y_0))
        elif coords == "relative":
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_move_to(
                self.__current_pos[0],
                self.__current_pos[1]))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_line_to(self, command, coords='absolute'):
        """ Generate string output for line command. """
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_0, y_0 = command

        if coords == "absolute":
            output.append(self.__print_add_line(x_0, y_0))
        elif coords == "relative":
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_add_line(
                self.__current_pos[0],
                self.__current_pos[1]))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_horizontal_line_to(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_0 = command[0]

        if coords == "absolute":
            output.append(self.__print_add_line(x_0, self.__current_pos[1]))
        elif coords == "relative":
            self.__update_current_pos(x_0, 0.0)
            output.append(self.__print_add_line(
                self.__current_pos[0],
                self.__current_pos[1]))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_vertical_line_to(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        y_0 = command[0]

        if coords == "absolute":
            output.append(self.__print_add_line(self.__current_pos[0], y_0))
        elif coords == "relative":
            self.__update_current_pos(0, y_0)
            output.append(self.__print_add_line(
                self.__current_pos[0],
                self.__current_pos[1]))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_cubic_curve(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_1, y_1, x_2, y_2, x_0, y_0 = command

        if coords == "absolute":
            output.append(self.__print_cubic(x_0, y_0, x_1, y_1, x_2, y_2))
            self.__update_last_cubic_control_point(x_2, x_2)
        elif coords == "relative":
            cs_x, cs_y = self.__current_pos[0] + x_1, self.__current_pos[1] + y_1
            ce_x, ce_y = self.__current_pos[0] + x_2, self.__current_pos[1] + y_2
            self.__update_last_cubic_control_point(ce_x, ce_y)
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_cubic(self.__current_pos[0], self.__current_pos[1],
                                             cs_x, cs_y, ce_x, ce_y))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_cubic_smooth_curve(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_2, y_2, x_0, y_0 = command

        c_x = 2 * self.__current_pos[0] - self.__last_cubic_control_point[0]
        c_y = 2 * self.__current_pos[1] - self.__last_cubic_control_point[1]

        if coords == "absolute":
            output.append(self.__print_cubic(x_0, y_0, c_x, c_y, x_2, y_2))
        elif coords == "relative":
            cs_x2, cs_y2 = self.__current_pos[0] + x_2, self.__current_pos[1] + y_2
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_cubic(self.__current_pos[0], self.__current_pos[1],
                                             c_x, c_y, cs_x2, cs_y2))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_quadratic_curve(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_1, y_1, x_0, y_0 = command

        if coords == "absolute":
            output.append(self.__print_quadratic(x_0, y_0, x_1, y_1))
            self.__update_last_quadratic_control_point(x_1, y_1)
        elif coords == "relative":
            c_x, c_y = self.__current_pos[0] + x_1, self.__current_pos[1] + y_1
            self.__update_last_quadratic_control_point(c_x, c_y)
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_quadratic(
                self.__current_pos[0], self.__current_pos[1], c_x, c_y))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_quadratic_smooth_curve(self, command, coords='absolute'):
        if not command:
            raise ValueError("Command is empty")

        output = []
        x_0, y_0 = command

        c_x = 2 * self.__current_pos[0] - self.__last_quadratic_control_point[0]
        c_y = 2 * self.__current_pos[1] - self.__last_quadratic_control_point[1]
        self.__update_last_quadratic_control_point(c_x, c_y)

        if coords == "absolute":
            output.append(self.__print_quadratic(x_0, y_0, c_x, c_y))
        elif coords == "relative":
            self.__update_current_pos(x_0, y_0)
            output.append(self.__print_quadratic(
                self.__current_pos[0], self.__current_pos[1], c_x, c_y))
        else:
            raise ValueError("Type of coords is incorrect: {}".format(coords))
        return output

    def __generate_elleptical_curve(self):
        pass

    def __generate_close(self):
        return [self.__print_close()]

    @staticmethod
    def __print_move_to(x_0, y_0):
        return "path.move(to: CGPoint(x: {}, y: {}))".format(x_0, y_0)

    @staticmethod
    def __print_add_line(x_0, y_0):
        return "path.addLine(to: CGPoint(x: {}, y: {}))".format(x_0, y_0)

    @staticmethod
    def __print_cubic(x_0, y_0, c1_x, c1_y, c2_x, c2_y):
        return 'path.addCurve(to: CGPoint(x: {}, y: {}), ' \
               'controlPoint1: CGPoint(x: {}, y: {}), ' \
               'controlPoint2: CGPoint(x: {}, y: {}))'.format(
                   x_0, y_0, c1_x, c1_y, c2_x, c2_y)

    @staticmethod
    def __print_quadratic(x_0, y_0, c_x, c_y):
        return "path.addQuadCurve(to: CGPoint(x: {}, y: {}), " \
               "controlPoint: CGPoint(x: {}, y: {}))".format(x_0, y_0, c_x, c_y)

    @staticmethod
    def __print_elliptical(x_0, y_0, radius, start_angle, end_angle, clockwise):
        return "path.func addArc(withCenter: CGPoint(x: {}, y: {}), " \
               "radius: CGFloat({}), startAngle: CGFloat({}),\
                endAngle: CGFloat({}), clockwise: {})".format(
                    x_0, y_0, radius, start_angle, end_angle, clockwise)

    @staticmethod
    def __print_close():
        return "path.close()"
