import sys  # To process command line arguments


class Util:
    @staticmethod
    def get_command_line_argument(num):
        arg = None
        if num < len(sys.argv):
            arg = sys.argv[num]
        return arg

    @staticmethod
    def repeated_char(char, count):
        string = ""
        for each in range(count):
            string += char
        return string
