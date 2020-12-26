# Trabalho_Pratico 2 - PL 2020/21
# main.py

from Parser import Parser
from Lexer import Lexer
import svg
import sys
import os

file_name = ""
if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        file_name = sys.argv[1]
    else:
        print("Presented argument is not a file", file=sys.stderr)
        exit(1)
else:
    print("File name expected", file=sys.stderr)
    exit(1)


contents = svg.readFile(file_name)

svg.clearFile("result.svg")
svg.createFile("result.svg")

lexer = Lexer()
lexer.Build(contents)

parser = Parser()
parser.Parse(contents)

svg.endFile("result.svg")
print("Drawing has ended with success.")