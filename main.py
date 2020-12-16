# Trabalho_Pratico 2 - PL 2020/21
# main.py

from Parser import Parser
from Lexer import Lexer

with open("teste", mode="r") as fh:
    contents = fh.read()

lexer = Lexer()
lexer.Build(contents)

for t in iter(lexer.lexer.token, None):
    print(t)

parser = Parser()
parser.Parse(contents)

