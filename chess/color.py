class Color(object):
    black = u'black'
    white = u'white'

    @staticmethod
    def code(color):
        """Retuns the Color mapped to the code. Used with one of the serialaztion methods."""
        if color == Color.black:
            return 'B'
        elif color == Color.white:
            return 'W'
        # This should never happen
        raise ValueError("Invalid color code")

    @staticmethod
    def decode(code):
        """Creates a new Color instance based off the color code. Used for serialaztion for historic reasons."""
        if code == 'B':
            return Color.black
        elif code == 'W':
            return Color.white
        raise ValueError("Invalid color code '{0}.".format(code))

    @staticmethod
    def inverse(color):
        if color == Color.black:
            return Color.white
        elif color == Color.white:
            return Color.black
        raise ValueError("Invalid color code '{0}.".format(color))
