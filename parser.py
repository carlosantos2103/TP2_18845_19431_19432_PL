# parser.py

import sys
import math
import ply.yacc as yacc
from Lexer import Lexer
from Command import Command

class Parser:

    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.lexer = None
        self.vars = {}      # Symbol table
        self.color = (0, 0, 0)
        self.pos = (100, 100)
        self.ang = 90
        self.draw_status = True

    def Parse(self, content, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(content, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        program = self.parser.parse(lexer=self.lexer.lexer)
        Command.exec(program, self)

    def p_error(self, p):
        print("Syntax error", file=sys.stderr)
        exit(1)

    def p_program0(self, p):
        """ program : command """
        p[0] = [p[1]]

    def p_program1(self, p):
        """ program : program command """
        lst = p[1]
        lst.append(p[2])
        p[0] = lst

    def p_command0(self, p):
        """ command  :  FORWARD INT
                     |  FD INT """
        args = {'distance': p[2]}
        p[0] = Command("forward", args)

    def p_command1(self, p):
        """ command  :  BACK INT
                     |  BK INT """
        args = {'distance': p[2]}
        p[0] = Command("back", args)

    def p_command2(self, p):
        """ command  :  LT INT
                     |  LEFT INT """
        args = {'degrees': p[2]}
        p[0] = Command("left", args)

    def p_command3(self, p):
        """ command  :  RT INT
                     |  RIGHT INT """
        args = {'degrees': p[2]}
        p[0] = Command("right", args)

    def p_command4(self, p):
        """ command  :  SETPOS '[' INT INT ']' """
        # new_pos = (p[3], p[4])

        args = {'new_pos': (p[3], p[4])}
        p[0] = Command("set_position", args)

    def p_command5(self, p):
        """ command  :  SETXY  INT INT """
        # new_pos = (p[2], p[3])
        args = {'new_pos': (p[2], p[3])}
        p[0] = Command("set_position", args)

    def p_command6(self, p):
        """ command  :  SETX  INT """
        # new_pos = (p[2], self.pos[1])
        args = {'new_x': p[2]}
        p[0] = Command("set_position", args)

    def p_command7(self, p):
        """ command  :  SETY  INT """
        # new_pos = (self.pos[0], p[2])
        args = {'new_y': p[2]}
        p[0] = Command("set_position", args)

    def p_command8(self, p):
        """ command  :  HOME """
        args = {}
        p[0] = Command("set_position", args)

    def p_command9(self, p):
        """ command  :  PD
                     |  PENDOWN """
        args = {'new_status': True}
        p[0] = Command("change_status", args)

    def p_command10(self, p):
        """ command  :  PU
                    |  PENUP """
        args = {'new_status': False}
        p[0] = Command("change_status", args)

    def p_command11(self, p):
        """ command  :  SETPENCOLOR '[' INT INT INT ']' """
        args={'new_color': (p[3], p[4], p[5])}
        p[0] = Command("pen_color", args)

    def p_command12(self, p):
        """ command  :  MAKE VARNAME INT """ # TODO

    def p_command13(self, p):
        """ command  :  IF """ # TODO

    def p_command14(self, p):
        """ command  :  IFELSE """  # TODO

    def p_command15(self, p):
        """ command  :  REPEAT INT '[' program ']' 
                     |  REPEAT VARUSE '[' program ']' """

    # def p_command16(self, p):
    #    """ command  :  WHILE '[' ']' '[' program ']'"""  # TODO: Adicionar a expressao (TRUE ou FALSE)

    # def p_command17(self, p):
    #    """ command  :  TO """  # TODO