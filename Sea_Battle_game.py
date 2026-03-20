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
                x_max_self = self_x + self._length - 1
                x_max_ship = x + ship._length - 1
                if not (x_max_self < x - 1 or self_x > x_max_ship + 1):
                    return y - 1 <= self_y <= y + 1
        return False

    def is_out_pole(self, size):
        return self._x + self._length > size if self._tp == 1 else self._y + self._length > size


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self.create_pole()

    def create_pole(self):
        self._pole = [[Cell() for k in range(self._size)]
                      for i in range(self._size)]
        self._closed_pole = [[Closed_Cell() for k in range(self._size)]
                             for i in range(self._size)]

    def player_init(self):
        print('Для смостоятельного создания поля вам необходимо понимать принцип расстановки кораблей на карте!')
        print('Правило 1: Запрещается расставлять корабли соприкасающиеся друг с другом')
        print('Правило 2: Запрещается расставлять корабли выходящие за границы поля')
        print(
            'Правило 3: Независимо от размеров поля, должно быть расставленно 10 кораблей')
        ships_counter = {'1': 4, '2': 3, '3': 2, '4': 1}
        self.show()
        while any(list(ships_counter.values())):
            try:
                length = input('Введите длину корабля: ')
                if type(ships_counter.get(length, False)) == bool:
                    print('Введите число от 1 до 4!')
                    continue
                elif ships_counter.get(length) == 0:
                    print(
                        'Вы уже создали максимальное количество кораблей длиной ' + length + ' клетки')
                    continue
                tp = int(
                    input('Введите направление корабля (1 - горизонтально, 2 - вертикально): '))
                if tp not in (1, 2):
                    print('Вы ввели неверное значение поворота корабля!')
                    continue
                x, y = input(
                    'Введите координаты корабля в формате Буква - номер строки! Координата корабля считается от его верхней или крайней левой точки: ').split()
                if x not in Game.LETTERS_LIST or not (1 <= int(y) <= self._size):
                    print('координаты некорректны')
                    continue
                x = Game.LETTERS_LIST.index(x)
                y = int(y) - 1
                ship = Ship(int(length), tp, x, y)
                if ship.is_out_pole(self._size):
                    continue
                for k in self._ships:
                    if k != ship:
                        if ship.is_collide(k):
                            print(k.get_start_coords())
                            print(ship.get_start_coords())
                            print(ship.is_collide(k))
                            print(ship.is_out_pole(self._size))
                            print('Такой корабль невозможно расположить на поле!')
                            break
                else:
                    self._ships.append(ship)
                    ships_counter[length] -= 1
                    self.set_cell(ship, 1)
                    self.show()
            except:
                print('Вы ввели недопустимые значения!')
        print('Отлично, мы готовы начать игру!')

    def init(self):
        self._ships = [Ship(i+1, randint(1, 2))
                       for i in range(4) for k in range(4-i)][::-1]

        for k in self._ships:
            for counter in range(20):
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)
                k.set_start_coords(x, y)
                if k.is_out_pole(self._size):
                    continue
                for i in self._ships:
                    if i != k:
                        if k.is_collide(i):
                            break
                else:
                    self.set_cell(k, 1)
                    break
            else:
                self.create_pole()
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
        print(('    ' + '  '.join(Game.LETTERS_LIST))[:4+self._size*3])
        for ind, k in enumerate(self._pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('⬜' if i._cell == 0 else '🟫' if i._cell ==
                      2 else '⬛', end=' ')
            print()

    def show_closed(self):
        print(('    ' + '  '.join(Game.LETTERS_LIST))[:4+self._size*3])
        for ind, k in enumerate(self._closed_pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('🟦' if i._cell == 0 else '⬛', end=' ')
            print()


class Game:
    LETTERS_LIST = ['А', 'Б', 'В', 'Г', 'Д',
                    'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н']

    def __init__(self, size=10, custom_mode=False):
        self.pole = GamePole(size)
        if not custom_mode:
            self.pole.init()
        else:
            self.pole.player_init()

    def show(self):
        self.pole.show()

    def show_closed(self):
        self.pole.show_closed()

    def set_shot(self, x, y, obj):
        if x.isdigit():
            x = int(x)
        else:
            x = self.LETTERS_LIST.index(x) + 1
        if not y.isdigit() or not (1 <= x <= self.pole._size) or not (1 <= int(y) <= self.pole._size):
            raise IndexException()
        y = int(y)

        pole = obj.pole._pole[y - 1][x - 1]
        closed_pole = self.pole._closed_pole[y - 1][x - 1]
        if not (pole._cell == 2 or pole.owner_ship is None or pole.owner_number is None):
            pole.owner_ship._cells[pole.owner_number] = 0
            pole._cell = 2
            pole.owner_number = None
            closed_pole._cell = 1
            if all(map(lambda x: x == 0, pole.owner_ship._cells)):
                return 'destroyed'
            return 'hit'
        return 'missed'


class Cell:
    def __init__(self):
        self._cell = 0
        self.owner_ship = None
        self.owner_number = None


class Closed_Cell:
    def __init__(self):
        self._cell = 0


class PoleExceptions(Exception):
    pass


class IndexException(PoleExceptions):
    pass


SIZE_GAME_POLE = 10


player = Game(SIZE_GAME_POLE, True)
player.show()

# while True:
#     pole.show()
#     if pole.set_shot(*input().split()):
#         print('Ходит бот!')
#     else:
#         print('Попробуйте снова!')
