# Trabalho_Pratico 2 - PL 2020/21
# main.py

from parser import Parser

with open("teste", mode="r") as fh:
    contents = fh.read()

parser = Parser()
parser.Parse(contents)

