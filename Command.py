# Command.py

import svg
import math

def do_forward(command, parser):
    dist = command.args['distance']
    new_pos = (parser.pos[0]+dist*math.cos(math.radians(parser.ang)), parser.pos[1]-dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)
    parser.pos = new_pos
    return 0

def do_back(command, parser):
    dist = command.args['distance']
    new_pos = (parser.pos[0]-dist*math.cos(math.radians(parser.ang)), parser.pos[1]+dist*math.sin(math.radians(parser.ang)))
    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)
    parser.pos = new_pos

def do_left(command, parser):
    parser.ang = parser.ang + command.args['degrees']

def do_right(command, parser):
    parser.ang = parser.ang - command.args['degrees']

def do_set_position(command, parser):
    new_pos = parser.pos
    if 'new_pos' in command.args:
        new_pos = command.args['new_pos']
    elif 'new_x' in command.args:
        new_pos = (command.args['new_x'], parser.pos[1])
    elif 'new_y' in command.args:
        new_pos = (parser.pos[1], command.args['new_y'])
    elif len(command.args) == 0:
        new_pos = (100,100)

    if parser.draw_status:
        svg.drawLine("teste.svg", parser.pos, new_pos, parser.color)

    parser.pos = new_pos

def do_change_status(command, parser):
    parser.draw_status = command.args['new_status']

def do_pen_color(command, parser):
    parser.color = command.args['new_color']



class Command:
    dispatch_table = {
        "forward": do_forward,
        "back": do_back,
        "left": do_left,
        "right": do_right,
        "set_position": do_set_position,
        "change_status": do_change_status,
        "pen_color": do_pen_color,
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