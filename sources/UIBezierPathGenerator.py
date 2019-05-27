from sources.parser import Parser


class UIBezierPathGenerator:

    # Public methods

    def __init__(self):
        self.__parser = Parser()
        self.__current_pos = [0, 0]

    def generate(self, svg):

        script = ["path = UIBezierPath()"]

        parsed_data = self.__parser.parse_svg(svg)

        for i in parsed_data:
            print(i)

    def __update_current_pos(self, x, y):
        self.__current_pos[0] += x
        self.__current_pos[1] += y

    def __generate_move_to(self, command, coords="absolute"):
        """ Generate string output for move command. """
        if not command:
            raise ValueError("Command is empty")
        output = []

        for x, y in command:
            if coords == "absolute":
                output.append(self.__print_move_to(x, y))
            elif coords == "relative":
                self.__update_current_pos(x, y)
                output.append(self.__print_move_to(
                    self.__current_pos[0],
                    self.__current_pos[1]))
            else:
                raise ValueError("Type is incorrect")
        return output

    def __generate_line_to(self, command, type="absolute", ):
        """ Generate string output for line command. """
        if not command:
            raise ValueError("Command is empty")
        output = []

        for x, y in command:
            if type == "absolute":
                output.append(self.__print_move_to(x, y))
            elif type == "relative":
                self.__update_current_pos(x, y)
                output.append(self.__print_move_to(
                    self.__current_pos[0],
                    self.__current_pos[1]))
            else:
                raise ValueError("Type is incorrect")
        return output



    def __print_move_to(self, x, y):
        return "path.move(to: CGPoint(x: {}, y: {}))".format(x, y)

    def __print_add_line(self, x, y):
        return "path.addLine(to: CGPoint(x: {}, y: {}))".format(x, y)

    def __print_cubic(self, x, y, c1_x, c1_y, c2_x, c2_y):
        return "path.addCurve(to: CGPoint(x: {}, y: {}), controlPoint1: CGPoint(x: {}, y: {}),\
            controlPoint2: CGPoint(x: {}, y: {}))".format(
            x, y, c1_x, c1_y, c2_x, c2_y)

    def __print_quadratic(self, x, y, c_x, c_y):
        return "path.addQuadCurve(to: CGPoint(x: {}, y: {}), controlPoint: CGPoint(x: {}, y: {}))".format(
            x, y, c_x, c_y)

    def __print_elleptical(self, x, y, radius, startAngle, endAngle, clockwise):
        return "path.func addArc(withCenter: CGPoint(x: {}, y: {}), radius: CGFloat({}), startAngle: CGFloat({}),\
                endAngle: CGFloat({}), clockwise: {})".format(
            x, y, radius, startAngle, endAngle, clockwise)

    def __print_close(self):
        return "path.close()"