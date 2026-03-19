from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._x, self._y = x, y
        self._length = length
        self._tp = tp
        self._cells = [1] * length

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def is_collide(self, ship):
        x, y = ship.get_start_coords()
        if x is not None:
            if self._tp != ship._tp:
                if ship._tp == 1:
                    return ship.is_collide(self)
                x_max = self._x + self._length - 1
                y_max = y + ship._length - 1
                if self._x - 1 <= x <= x_max + 1:
                    return y - 1 <= self._y <= y_max + 1
            else:
                self_x, self_y = self.get_start_coords()
                if self._tp == 2:
                    x, y = y, x
                    self_x, self_y = self_y, self_x
                x_max_self = self_x + self._length
                x_max_ship = x + ship._length
                if not (x_max_self < x - 1 or self_x > x_max_ship + 1):
                    return y - 1 <= self_y <= y + 1
        return False

    def is_out_pole(self, size):
        return self._x + self._length > size if self._tp == 1 else self._y + self._length > size


class GamePole:
    LETTERS_LIST = ['А', 'Б', 'В', 'Г', 'Д',
                    'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н']

    def __init__(self, size=10):
        self._size = size
        self._ships = []

    def init(self):
        self._ships = [Ship(i+1, randint(1, 2))
                       for i in range(4) for k in range(4-i)][::-1]
        self._pole = [[Cell() for k in range(self._size)]
                      for i in range(self._size)]

        for k in self._ships:
            for counter in range(20):
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)
                k.set_start_coords(x, y)
                for i in self._ships:
                    if i != k:
                        if k.is_collide(i) or k.is_out_pole(self._size):
                            break
                else:
                    self.set_cell(k, 1)
                    break
            else:
                self.init()
                break

    def set_cell(self, ship, value):
        x, y = ship.get_start_coords()
        for i in range(ship._length):
            if ship._tp == 1:
                pole = self._pole[y][x + i]
            else:
                pole = self._pole[y + i][x]
            pole._cell = value
            pole.owner_ship = ship
            pole.owner_number = i

    def show(self):
        print('    А  Б  В  Г  Д  Е  Ж  З  И  К  Л  М  Н'[:4+self._size*3])
        for ind, k in enumerate(self._pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('⬜' if i._cell == 0 else '🟫' if i._cell ==
                      2 else '⬛', end=' ')
            print()


class Game:
    def __init__(self, size=10):
        self.pole = GamePole(size)
        self.pole.init()

    def show(self):
        self.pole.show()

    def set_shot(self, x, y):
        if x.isdigit():
            x = int(x)
        else:
            x = self.pole.LETTERS_LIST.index(x) + 1
        if not y.isdigit() or not (1 <= x <= self.pole._size) or not (1 <= int(y) <= self.pole._size):
            raise IndexException()
        y = int(y)

        pole = self.pole._pole[y - 1][x - 1]
        if not (pole._cell == 2 or pole.owner_ship is None or pole.owner_number is None):
            pole.owner_ship._cells[pole.owner_number] = 2
            pole._cell = 2
            pole.owner_number = None
            if all(map(lambda x: x == 2, pole.owner_ship._cells)):
                print('Корабль уничтожен')
            return True
        return False

    def bot_turn(self):
        ...


class Cell:
    def __init__(self):
        self._cell = 0
        self.owner_ship = None
        self.owner_number = None


class PoleExceptions(Exception):
    pass


class IndexException(PoleExceptions):
    pass


SIZE_GAME_POLE = 10

pole = Game(SIZE_GAME_POLE)
while True:
    pole.show()
    if pole.set_shot(*input().split()):
        print('Ходит бот!')
    else:
        print('Попробуйте снова!')
