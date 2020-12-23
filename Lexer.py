# Lexer.py

import ply.lex as lex
import sys

class Lexer:
    literals = "[]"
    t_ignore = " \n\t"
    tokens = ("OPERATOR", "LOGIC", "INT", "VARNAME", "VARUSE", "FD", "FORWARD", "BK", "BACK", "LT", "LEFT", "RT", "RIGHT", "SETPOS", "SETXY", "SETX",
              "SETY", "HOME", "PD", "PENDOWN", "PU", "PENUP", "SETPENCOLOR", "MAKE", "IF", "IFELSE", "REPEAT", "WHILE")

    def t_COMMAND(self, t):
        r"""fd|forward|bk|back|lt|left|rt|right|setpos|setxy|setx|sety|home|pd|pendown|pu|penup|
        setpencolor|make|if(else)?|repeat|while"""
        t.type = t.value.upper()
        return t

    def t_INT(self, t):
        r"""[0-9]+([0-9\.])*"""
        t.value = float(t.value)
        return t

    def t_VARNAME(self, t):
        r"""[\"][A-Za-z][A-Za-z0-9]*"""
        return t

    def t_VARUSE(self, t):
        r"""[\:][A-Za-z][A-Za-z0-9]*"""
        return t

    def t_LOGIC(self, t):
        r"""<|>|=="""  # >= ?
        return t

    def t_OPERATOR(self, t):
        r"""\+|\-|\/|\*"""
        return t


    def t_error(self, t):
        print(f"Erro. Caractere inesperado: {t.value[0]}", file=sys.stderr)
        exit(1)

    def __init__(self):
        self.lexer = None

    def Build(self, content, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(content)