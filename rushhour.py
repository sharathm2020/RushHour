import util

DEFAULT_STATE = '  b aa|  b   |xxb   |ccc  d|     d|     d'
ddddddddddddd = 'abb   |a  c  |axxc  |   c e|dff  e|d ggge'
aaaaaaaaaaaaa = '   a  |   abb|xx d  |e fdgg|e fhhi|e f  i'

class Cell:

    EMPTY = ' '

    @classmethod
    def color(cls, c):
        if c == ' ':
            return util.color_string(' ', back='black')
        elif c == 'x':
            return util.color_string(c, fore='white', back='red')
        else:
            code = '\033[37;4{}m'.format(ord(c.lower()) - 95)
            return code + c + '\033[0m'


class Action:

    def __init__(self, c, x, y, x2, y2, dx, dy):
        self.c = c
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f'move "{self.c}" ({self.x},{self.y})-({self.x2},{self.y2}) ({self.dx},{self.dy})'


class State:

    SIZE = 6
    EXIT_Y = 3

    def __init__(self, string):
        self.b = [list(line) for line in string.split('|')]

    def __str__(self):
        return '|'.join([''.join(row) for row in self.b])

    def __eq__(self, state):
        return str(self) == str(state)

    def is_legal(self, x, y=None):
        return (x >= 0 and x < self.SIZE and
                ((not y) or (y >= 0 and y < self.SIZE)))

    def row(self, y):
        return self.b[self.SIZE-y-1] if self.is_legal(y) else None

    def get(self, x, y):
        return self.b[self.SIZE-y-1][x] if self.is_legal(x, y) else None

    def set(self, x, y, c):
        if self.is_legal(x, y):
            self.b[self.SIZE-y-1][x] = c

    def all_y(self, y1=None, y2=None):
        y1 = y1 or 0
        y2 = y2+1 if y2 is not None else self.SIZE
        for y in range(y1, y2):
            yield y

    def all_x(self, x1=None, x2=None):
        x1 = x1 or 0
        x2 = x2+1 if x2 is not None else self.SIZE
        for x in range(x1, x2):
            yield x

    def all_xy(self):
        for y in self.all_y():
            for x in self.all_x():
                yield x, y

    def is_goal(self):
        return self.get(self.SIZE - 1, self.EXIT_Y) == 'x'

    def _get_actions(self, c, x, y):
        actions = []

        x2, y2 = x, y
        while self.get(x2 + 1, y) == c:
            x2 += 1
        while self.get(x, y2 + 1) == c:
            y2 += 1

        if x != x2:
            dx = -1
            while self.get(x + dx, y) == Cell.EMPTY:
                actions.append(Action(c, x, y, x2, y2, dx, 0))
                dx -= 1
            dx = 1
            while self.get(x2 + dx, y) == Cell.EMPTY:
                actions.append(Action(c, x, y, x2, y2, dx, 0))
                dx += 1
        else:
            dy = -1
            while self.get(x, y + dy) == Cell.EMPTY:
                actions.append(Action(c, x, y, x2, y2, 0, dy))
                dy -= 1
            dy = 1
            while self.get(x, y2 + dy) == Cell.EMPTY:
                actions.append(Action(c, x, y, x2, y2, 0, dy))
                dy += 1

        return actions

    def actions(self):
        actions = []
        seen = set()
        for x, y in self.all_xy():
            c = self.get(x, y)
            if c != Cell.EMPTY and c not in seen:
                actions.extend(self._get_actions(c, x, y))
                seen.add(c)
        actions.sort(key=lambda action: str(action))
        return actions

    def _clone(self):
        return State(str(self))

    def _execute(self, action):
        for y in self.all_y(action.y, action.y2):
            for x in self.all_x(action.x, action.x2):
                self.set(x, y, Cell.EMPTY)
        for y in self.all_y(action.y, action.y2):
            for x in self.all_x(action.x, action.x2):
                self.set(x + action.dx, y + action.dy, action.c)
        return self

    def execute(self, action):
        return self._clone()._execute(action)

    def pprint_string(self):
        top_bottom = util.color_string(' ' * (self.SIZE + 2), back='blue')
        side = util.color_string(' ', back='blue')
        s = top_bottom + '\n'
        for y in reversed(list(self.all_y())):
            s += (side
                  + ''.join([Cell.color(c) for c in self.row(y)])
                  + (Cell.color(' ') if y == self.EXIT_Y else side)
                  + '\n')
        return s + top_bottom


if __name__ == '__main__':

    cmd = util.get_arg(1)
    if cmd:

        string = util.get_arg(2) or DEFAULT_STATE
        state = State(string)

        if cmd == 'print':
            util.pprint([state])
        elif cmd == 'goal':
            print(state.is_goal())
        elif cmd == 'actions':
            for action in state.actions():
                print(action)
