from PyQt6.QtWidgets import *
from gui02 import *

class Logic(QMainWindow, Ui_Calculator):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.__pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862
        self.__given_input = ''
        self.__given_code = ''
        self.__input_length = 0

        self.one_button.clicked.connect(lambda: self.input_adder('1', '1'))
        self.two_button.clicked.connect(lambda: self.input_adder('2', '2'))
        self.three_button.clicked.connect(lambda: self.input_adder('3', '3'))
        self.four_button.clicked.connect(lambda: self.input_adder('4', '4'))
        self.five_button.clicked.connect(lambda: self.input_adder('5', '5'))
        self.six_button.clicked.connect(lambda: self.input_adder('6', '6'))
        self.seven_button.clicked.connect(lambda: self.input_adder('7', '7'))
        self.eight_button.clicked.connect(lambda: self.input_adder('8', '8'))
        self.nine_button.clicked.connect(lambda: self.input_adder('9', '9'))
        self.zero_button.clicked.connect(lambda: self.input_adder('0', '0'))

        self.sin_button.clicked.connect(lambda: self.input_adder('Sin(', 'S('))
        self.cos_button.clicked.connect(lambda: self.input_adder('Cos(', 'C('))
        self.tan_button.clicked.connect(lambda: self.input_adder('Tan(', 'T('))
        self.pi_button.clicked.connect(lambda: self.input_adder('π', 'P'))
        self.root_button.clicked.connect(lambda: self.input_adder('√(', 'R('))
        self.multiply_button.clicked.connect(lambda: self.input_adder('*', '*'))
        self.divide_button.clicked.connect(lambda: self.input_adder('/', '/'))
        self.plus_button.clicked.connect(lambda: self.input_adder('+', '+'))
        self.minus_button.clicked.connect(lambda: self.input_adder('-', '-'))
        self.decimal_button.clicked.connect(lambda: self.input_adder('.', '.'))
        self.equal_button.clicked.connect(lambda: self.equal())

        self.clear_button.clicked.connect(lambda: self.clear())
        self.l_param_button.clicked.connect(lambda: self.input_adder('(', '('))
        self.r_param_button.clicked.connect(lambda: self.input_adder(')', ')'))

    def fact(self, value: int) -> int:
        """
        Returns the factorial of the integer variable value
        :param value:
        :return:
        """
        if value != 0:
            total = value
            i = value - 1
            while i > 0:
                total *= i
                i -= 1
            return total
        return 1

    def root(self, value: float) -> float:
        """
        Returns the square root of the float variable value
        :param value:
        :return:
        """
        return value ** (1 / 2)

    def sin(self, value: float) -> float:
        """
        Returns an approximate estimation of the trig function sine from the radian variable value using a taylor series
        :param value:
        :return:
        """
        while value < (2 * self.__pi):
            value += (2 * self.__pi)
        while value > (2 * self.__pi):
            value -= (2 * self.__pi)
        total = 0
        k = 0
        while k < 50:
            total += (pow(-1, k) * pow(value, (2 * k) + 1) / self.fact((2 * k) + 1))
            k += 1
        return total

    def cos(self, value: float) -> float:
        """
        Returns an approximate estimation of the trig function cosine from the radian variable value using a taylor series
        :param value:
        :return:
        """
        value = abs(value)
        while value > (2 * self.__pi):
            value -= (2 * self.__pi)
        total = 0
        k = 0
        while k < 50:
            total += (pow(-1, k) * pow(value, (2 * k)) / self.fact(2 * k))
            k += 1
        return total

    def tan(self, value: float) -> float | type[ZeroDivisionError]:
        """
        Returns an approximate estimation of the trig function tangent from the radian variable value using sine/cosine
        :param value:
        :return:
        """
        while value < (2 * self.__pi):
            value += (2 * self.__pi)
        while value > (2 * self.__pi):
            value -= (2 * self.__pi)
        if abs(value) == (self.__pi / 2) or abs(value) == (3 * self.__pi / 2):
            return ZeroDivisionError
        return self.sin(value) / self.cos(value)

    def input_adder(self, strValue: str, codeName: str) -> None:
        """
        executed everytime a non-equal gui button is pressed
        :param strValue: displayed initially for the gui
        :param codeName: used to give the actual computations for the equal method
        :return:
        """
        try:
            self.__given_input += str(strValue)
            self.__given_code += str(codeName)
            self.input_display.setText(self.__given_input)
        except:
            self.input_display.setText("ERR")

    def clear(self) -> None:
        """
        clears any previously given input
        :return:
        """
        self.__given_input = ''
        self.__given_code = ''
        self.input_display.setText(self.__given_input)

    def equal(self) -> None:
        """
        displays the evaluated computation previously entered from the given_code str variable
        :return:
        """
        if self.__given_code.count('(') >= self.__given_code.count(')'):
            unpaired_params = self.__given_code.count('(') - self.__given_code.count(')')
            self.__given_code += (unpaired_params * ')')

        j = 1
        while j < len(self.__given_code):
            if (self.__given_code[j] == '(' or self.__given_code[j] == 'C' or self.__given_code[j] == 'S' or
                self.__given_code[j] == 'T' or
                self.__given_code[j] == 'R' or self.__given_code[j] == 'P') and \
                    (self.__given_code[j - 1] == 'P' or self.__given_code[j - 1] == ')' or self.__given_code[
                        j - 1].isdigit()):
                self.__given_code = f'{self.__given_code[0:j]}*{self.__given_code[j:]}'
                j += 2
            else:
                j += 1
        self.__given_code = self.__given_code.replace('C(', 'self.cos(')
        self.__given_code = self.__given_code.replace('S(', 'self.sin(')
        self.__given_code = self.__given_code.replace('T(', 'self.tan(')
        self.__given_code = self.__given_code.replace('P', 'self.__pi')
        self.__given_code = self.__given_code.replace('R(', 'self.root(')
        try:
            answer = eval(self.__given_code)
            answer = answer.__round__(8)
        except ZeroDivisionError:
            answer = "ERR: ZERO DIV"
        except SyntaxError:
            answer = "SYNTAX ERR"
        except:
            answer = "ERROR"
        self.input_display.setText(str(answer))
        self.__given_input = ''
        self.__given_code = ''
