# Parser.py

import sys
import ply.yacc as yacc
from Lexer import Lexer
from Command import Command


def math(operator, p1, p2):
    if operator == "*":
        return p1 * p2
    elif operator == "/":
        if p2 == 0:
            print("Division by zero", file=sys.stderr)
            exit(1)
        return p1 / p2
    elif operator == "+":
        return p1 + p2
    elif operator == "-":
        return p1 - p2

    if operator == "<":
        if p1 < p2:
            return True
        else:
            return False
    elif operator == ">":
        if p1 > p2:
            return True
        else:
            return False
    elif operator == "==":
        if p1 == p2:
            return True
        else:
            return False
    elif operator == "<=":
        if p1 <= p2:
            return True
        else:
            return False
    elif operator == ">=":
        if p1 >= p2:
            return True
        else:
            return False
    elif operator == "!=":
        if p1 >= p2:
            return True
        else:
            return False

    print("Operator not found", file=sys.stderr)
    exit(1)


class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.lexer = None
        self.vars = {}
        self.function = {}
        self.color = (0, 0, 0)
        self.pos = (100, 100)
        self.ang = 90
        self.draw_status = True

    def verif_pos(self, pos):
        return self.value(pos[0]), self.value(pos[1])

    def verif_color(self, color):
        return self.value(color[0]), self.value(color[1]), self.value(color[2])

    def value(self, val):
        if type(val) == tuple:
            v1 = self.value(val[0])
            v2 = self.value(val[2])
            return math(val[1], v1, v2)
        if type(val) == float:
            return val
        val = val[1:]
        if val in self.vars:
            return self.vars[val]
        print(f"Undefined variable: {val}", file = sys.stderr)
        exit(1)

    def Parse(self, content, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(content, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        program = self.parser.parse(lexer=self.lexer.lexer)
        Command.exec(program, self)

    def p_error(self, p):
        print(f"Syntax error: {p}", file=sys.stderr)
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
        """ command  :  FORWARD value
                     |  FD value """
        args = {'distance': p[2]}
        p[0] = Command("forward", args)

    def p_command1(self, p):
        """ command  :  BACK value
                     |  BK value """
        args = {'distance': p[2]}
        p[0] = Command("back", args)

    def p_command2(self, p):
        """ command  :  LT value
                     |  LEFT value """
        args = {'degrees': p[2]}
        p[0] = Command("left", args)

    def p_command3(self, p):
        """ command  :  RT value
                     |  RIGHT value """
        args = {'degrees': p[2]}
        p[0] = Command("right", args)

    def p_command4(self, p):
        """ command  :  SETPOS '[' value value ']' """

        args = {'new_pos': (p[3], p[4])}
        p[0] = Command("set_position", args)

    def p_command5(self, p):
        """ command  :  SETXY  value value """

        args = {'new_pos': (p[2], p[3])}
        p[0] = Command("set_position", args)

    def p_command6(self, p):
        """ command  :  SETX  value """

        args = {'new_x': p[2]}
        p[0] = Command("set_position", args)

    def p_command7(self, p):
        """ command  :  SETY  value """

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
        """ command  :  SETPENCOLOR '[' value value value ']' """
        args = {'new_color': (p[3], p[4], p[5])}
        p[0] = Command("pen_color", args)

    def p_command12(self, p):
        """ command  :  MAKE VARNAME value """
        args = {'var_name': p[2], 'value': p[3]}
        p[0] = Command("make", args)

    def p_command13(self, p):
        """ command  :  IF condition '[' program ']'"""
        p[0] = Command("if", {
            'condition': p[2],
            'code': p[4]
        })

    def p_command14(self, p):
        """ command  :  IFELSE condition '[' program ']' '[' program ']' """
        p[0] = Command("ifelse", {
            'condition': p[2],
            'code1': p[4],
            'code2': p[7],
        })

    def p_command15(self, p):
        """ command  :  REPEAT value '[' program ']' """
        p[0] = Command("repeat", {
            'var': p[2],
            'code': p[4]
        })

    def p_command16(self, p):
        """ command  :  WHILE '[' condition ']' '[' program ']'"""
        p[0] = Command("while", {
            'condition': p[3],
            'code': p[6],
        })

    def p_command17(self, p):
        """ command  :  TO NAMETO VARUSE program END"""  # TODO
        args = {'nameto': p[2], 'varuse': p[3], 'code': p[4]}
        p[0] = Command('to', args)

    def p_command18(self, p):
        """ command  : NAMETO value"""
        args = {'nameto': p[1], 'value': p[2]}
        p[0] = Command('nameto', args)

    def p_command19(self, p):
        """ value  :  NUM
                  |  VARUSE
                  |  VARUSE OPERATOR NUM
                  |  NUM OPERATOR VARUSE
                  |  NUM OPERATOR NUM
                  |  VARUSE OPERATOR VARUSE """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2], p[3])

    def p_condition(self, p):
        """ condition  :  value
                      |  value LOGIC value """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2], p[3])
