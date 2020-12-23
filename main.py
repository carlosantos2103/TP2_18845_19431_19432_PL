# Trabalho_Pratico 2 - PL 2020/21
# main.py

from Parser import Parser
from Lexer import Lexer
import svg

with open("tests/ex4.logo", mode="r") as fh:
    contents = fh.read()


def clearFile(file_name):
    open(file_name, 'w+').close()

clearFile("teste.svg")

svg.createFile("teste.svg")

lexer = Lexer()
lexer.Build(contents)


parser = Parser()
parser.Parse(contents)

svg.endFile("teste.svg")