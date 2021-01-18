# Trabalho Pratico 2 - PL 2020/21
# 18845 - 19431 - 19432
# main.py

from Parser import Parser
from Lexer import Lexer
import svg
import sys
import os
contents = svg.readFile("teste")

lexer = Lexer()
lexer.Build(contents)

parser = Parser()
parser.Parse(contents)

svg.drawAll("result.svg")

'''
file_name = ""
if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        file_name = sys.argv[1]
    else:
        print(f"Presented argument is not a file: {sys.argv[1]}", file=sys.stderr)
        exit(1)
else:
    print("File name expected", file=sys.stderr)
    exit(1)

contents = svg.readFile(file_name)

lexer = Lexer()
lexer.Build(contents)

parser = Parser()
parser.Parse(contents)

svg.drawAll("result.svg")
print("Drawing has ended with success.")'''