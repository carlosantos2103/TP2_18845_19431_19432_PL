# parser.py

import sys
import ply.yacc as yacc
from Lexer import Lexer

class Parser:

    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.lexer = None

    def Parse(self, content, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(content, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        ans = self.parser.parse(lexer=self.lexer.lexer)
        print(ans)

    def p_error(self, t):
        print("Syntax error", file=sys.stderr)
        exit(1)

    def p_program0(self, t):
        """ program : command """

    def p_program1(self, t):
        """ program : program command """

    def p_command0(self, t):
        """ command  :  FORWARD INT
                     |  FD INT """

    def p_command1(self, t):
        """ command  :  BACK INT
                     |  BK INT """

    def p_command2(self, t):
        """ command  :  LT INT
                     |  LEFT INT """

    def p_command3(self, t):
        """ command  :  RT INT
                     |  RIGHT INT """

    def p_command4(self, t):
        """ command  :  SETPOS '[' INT INT ']' """

    def p_command5(self, t):
        """ command  :  SETXY  INT INT """

    def p_command6(self, t):
        """ command  :  SETX  INT """

    def p_command7(self, t):
        """ command  :  SETY  INT """

    def p_command8(self, t):
        """ command  :  HOME """

    def p_command9(self, t):
        """ command  :  PD
                     |  PENDOWN """

    def p_command10(self, t):
        """ command  :  PU
                    |  PENUP """

    def p_command11(self, t):
        """ command  :  SETPENCOLOR '[' INT INT INT ']' """

    def p_command12(self, t):
        """ command  :  MAKE VARNAME INT """

    def p_command13(self, t):
        """ command  :  IF """ # TODO

    def p_command14(self, t):
        """ command  :  IFELSE """  # TODO

    def p_command15(self, t):
        """ command  :  REPEAT INT '[' program ']' 
                     |  REPEAT VARUSE '[' program ']' """

    def p_command16(self, t):
        """ command  :  WHILE '[' ']' '[' program ']'"""  # TODO: Adicionar a expressao (TRUE ou FALSE)

    def p_command17(self, t):
        """ command  :  TO """  # TODO