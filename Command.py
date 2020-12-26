# Command.py

import svg
import math

def do_forward(command, parser):
    dist = parser.value(command.args['distance'])
    new_pos = (parser.pos[0]+dist*math.cos(math.radians(parser.ang)), parser.pos[1]-dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)
    parser.pos = new_pos
    return 0

def do_back(command, parser):
    dist = parser.value(command.args['distance'])
    new_pos = (parser.pos[0]-dist*math.cos(math.radians(parser.ang)), parser.pos[1]+dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)
    parser.pos = new_pos

def do_left(command, parser):
    parser.ang = parser.ang + parser.value(command.args['degrees'])

def do_right(command, parser):
    parser.ang = parser.ang - parser.value(command.args['degrees'])

def do_set_position(command, parser):
    new_pos = parser.pos
    if 'new_pos' in command.args:
        new_pos = parser.verif_pos(command.args['new_pos'])
        print(f"New x:y {new_pos}")
    elif 'new_x' in command.args:
        new_pos = (parser.value(command.args['new_x']), parser.pos[1])
        print(f"New x {new_pos}")
    elif 'new_y' in command.args:
        new_pos = (parser.pos[0], parser.value(command.args['new_y']))
        print(f"New y {new_pos}")
    elif len(command.args) == 0:
        new_pos = (100, 100)
        print(f"New {new_pos}")

    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)

    parser.pos = new_pos

def do_change_status(command, parser):
    parser.draw_status = command.args['new_status']

def do_pen_color(command, parser):
    parser.color = parser.verif_color(command.args['new_color'])

def do_make(command, parser):
    var_name = command.args['var_name'][1:]
    value = parser.value(command.args['value'])
    parser.vars[var_name] = value

def do_if(command, parser):
    condition = command.args['condition']
    code = command.args['code']
    result = parser.value(condition)

    if result:
        Command.exec(code, parser)

def do_ifelse(command, parser):
    condition = command.args['condition']
    result = parser.value(condition)
    code1 = command.args['code1']
    code2 = command.args['code2']

    if result:
        Command.exec(code1, parser)
    else:
        Command.exec(code2, parser)

def do_repeat(command, parser):
    count = 0
    var = parser.value(command.args['var'])
    code = command.args['code']

    while var > count:
        Command.exec(code, parser)
        count += 1



def do_while(command, parser):
    condition = command.args['condition']
    code = command.args['code']
    result = parser.value(condition)

    while result:
        Command.exec(code, parser)
        result = parser.value(condition)

def do_to(command, parser):
    if command.args['varuse'] == -1:
        parser.function[command.args['nameto']] = command.args['code']
    else:
        parser.function[command.args['nameto']] = command.args['code']
        parser.vars_function[command.args['nameto']] = command.args['varuse'][1:]
        # parser.vars[command.args['nameto']] = command.args['varuse'][1:]

def do_nameto(command, parser):
    if command.args['value'] == -1:
        program = parser.function[command.args['nameto']]
        command.exec(program, parser)
    else:
        program = parser.function[command.args['nameto']]
        # Saber qual o argumento da funcao  tree -> :size
        var = parser.vars_function[command.args['nameto']]
        # Assegura que aquele argumento fica com o determinado valor :size -> 0,1...
        parser.vars[var] = parser.value(command.args['value'])
        command.exec(program, parser)

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
        "to": do_to,
        "nameto": do_nameto,
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