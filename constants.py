import math

HELP_TEXT_FONT = ('consolas', 16, '')
HELP_CONFIRM_BUTTON_FONT = ('consolas', 20, 'bold')

# Functions
FUNCTION_NAMES_WITH_X = ['sin(x)', 'cos(x)', 'tg(x)', 'ctg(x)', 'x^2', 'x^3']
FUNCTION_NAMES = ['sin', 'cos', 'tg', 'ctg', 'квадрат', 'куб']
FUNCTIONS = [math.sin, math.cos, math.tan, lambda x: 1 / math.tan(x), lambda x: x ** 2, lambda x: x ** 3]

# Math
EPSILON = 1e-10
INFINITY = 1e10
DEFAULT_BEGIN_VALUE = -10
DEFAULT_END_VALUE = 10
