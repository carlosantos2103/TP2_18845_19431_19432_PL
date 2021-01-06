# svg.py

import sys

text = ""

def writeFile(file_name, content):
    with open(file_name, mode="a") as fh:
        fh.write(content)
    fh.close()
    pass

def readFile(file_name):
    fh = open(file_name, mode="r")
    content = fh.read()
    fh.close()
    return content

def drawLine(pos1, pos2, color):
    global text
    if pos2[0] <= 200 and pos2[1] <= 200 and pos2[0] >= 0 and pos2[1] >= 0 and pos1[0] <= 200 and pos1[1] <= 200 and pos1[0] >= 0 and pos1[1] >= 0:
        line = f'<line x1="{pos1[0]}" y1="{pos1[1]}" \
                        x2="{pos2[0]}" y2="{pos2[1]}" \
                        style="stroke: rgb({color[0]}, {color[1]}, {color[2]}); stroke-width: 1px"/>\n'
        text += line
    else:
        print("Drawing is out of limits", file=sys.stderr)
        exit(1)

def drawAll(file_name):
    global text
    open(file_name, 'w+').close()
    writeFile(file_name, '<svg viewBox="0 0 200.00 200.00" xmlns="http://www.w3.org/2000/svg">\n')
    writeFile(file_name, text)
    writeFile(file_name, '</svg>')