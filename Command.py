# Command.py

import svg
import math
import sys

def do_forward(command, parser):
    dist = parser.value(command.args['distance'])
    new_pos = (parser.pos[0]+dist*math.cos(math.radians(parser.ang)), parser.pos[1]-dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine(parser.pos, new_pos, parser.color)
    parser.pos = new_pos
    return 0

def do_back(command, parser):
    dist = parser.value(command.args['distance'])
    new_pos = (parser.pos[0]-dist*math.cos(math.radians(parser.ang)), parser.pos[1]+dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine(parser.pos, new_pos, parser.color)
    parser.pos = new_pos

def do_left(command, parser):
    parser.ang = parser.ang + parser.value(command.args['degrees'])

def do_right(command, parser):
    parser.ang = parser.ang - parser.value(command.args['degrees'])

def do_set_position(command, parser):
    new_pos = parser.pos
    if 'new_pos' in command.args:
        new_pos = parser.verif_pos(command.args['new_pos'])
    elif 'new_x' in command.args:
        new_pos = (parser.value(command.args['new_x']), parser.pos[1])
    elif 'new_y' in command.args:
        new_pos = (parser.pos[0], parser.value(command.args['new_y']))
    elif len(command.args) == 0:
        new_pos = (100, 100)

    if parser.draw_status:
        svg.drawLine(parser.pos, new_pos, parser.color)

    parser.pos = new_pos

def do_change_status(command, parser):
    parser.draw_status = command.args['new_status']

def do_pen_color(command, parser):
    parser.color = parser.verif_color(command.args['new_color'])

def do_make(command, parser):
    var_name = command.args['var_name']
    value = parser.value(command.args['value'])
    parser.vars[var_name] = value

def do_if(command, parser):
    condition = command.args['condition']
    code = command.args['code']
    result = parser.value(condition)

    if result:
        parser.exec(code)

def do_ifelse(command, parser):
    condition = command.args['condition']
    result = parser.value(condition)
    code1 = command.args['code1']
    code2 = command.args['code2']

    if result:
        parser.exec(code1)
    else:
        parser.exec(code2)

def do_repeat(command, parser):
    count = 0
    var = parser.value(command.args['var'])
    code = command.args['code']

    while var > count:
        parser.exec(code)
        count += 1

def do_while(command, parser):
    condition = command.args['condition']
    code = command.args['code']
    result = parser.value(condition)

    while result:
        parser.exec(code)
        result = parser.value(condition)

def do_function(command, parser):
    function_name = command.args['nameto']
    code = command.args['code']
    if 'vars' in command.args:
        parser.functions[function_name] = { "vars": command.args['vars'], "code": code }
    else:        
        parser.functions[function_name] = { "code": code }

def do_call_function(command, parser):
    function_name = command.args['nameto']

    if function_name not in parser.functions:
        print(f"Undefined function: {function_name}", file = sys.stderr)
        exit(1)
        
    function = parser.functions[function_name]
    code = function["code"]

    if "vars" in function:
        if 'values' not in command.args:
            print(f"Parameters needed on function: {function_name}", file = sys.stderr)
            exit(1)

        if len(command.args["values"]) != len(function["vars"]):
            print(f"Missmatched number of parameters on function: {function_name}", file = sys.stderr)
            exit(1)

        save_vars = parser.vars.copy()

        for var, value in zip(function['vars'], command.args['values']):
            parser.vars[var] = parser.value(value)

    parser.exec(code)

    if "vars" in function:
        parser.vars = save_vars.copy()
                
class Command:
    dispatch_table = {
        "forward": do_forward,
        "back": do_back,
        "left": do_left,
        "right": do_right,
        "set_position": do_set_position,
        "change_status": do_change_status,
        "pen_color": do_pen_color,
        "make": do_make,
        "if": do_if,
        "ifelse": do_ifelse,
        "repeat": do_repeat,
        "while": do_while,
        "function": do_function,
        "call_function": do_call_function,
    }

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name} => {self.args}"

    def run(self, parser):
        self.dispatch_table[self.name](self, parser)

    @classmethod
    def exec(cls, program, parser):
        for cmd in program:
            cmd.run(parser)