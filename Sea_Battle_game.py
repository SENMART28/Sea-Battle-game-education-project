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
    LETTERS_LIST = ['А', 'Б', 'В', 'Г', 'Д',
                    'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н']

    def __init__(self):
        self._ships = []
        self.create_pole()
        
    @classmethod
    def coords_convertor(cls, x, y, size):
        if x.isdigit():
            x = int(x)
        else:
            x = cls.LETTERS_LIST.index(x) + 1
        if not y.isdigit() or not (1 <= x <= size) or not (1 <= int(y) <= size):
            raise IndexException()
        y = int(y)
        return x, y

    def create_pole(self):
        self._pole = [[Cell() for k in range(Controller.POLE_SIZE)]
                      for i in range(Controller.POLE_SIZE)]
        self._closed_pole = [[Closed_Cell() for k in range(Controller.POLE_SIZE)]
                             for i in range(Controller.POLE_SIZE)]
        
    @property
    def get_pole(self):
        return self._pole

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
                x, y = self.coords_convertor(x, y, Controller.POLE_SIZE)
                ship = Ship(int(length), tp, x - 1, y - 1)
                if ship.is_out_pole(Controller.POLE_SIZE):
                    continue
                for k in self._ships:
                    if k != ship:
                        if ship.is_collide(k):
                            print('Такой корабль невозможно расположить на поле!')
                            break
                else:
                    self._ships.append(ship)
                    ships_counter[length] -= 1
                    self.set_cell(ship, 'ship')
                    self.show()
            except Exception:
                print('Вы ввели недопустимые значения!')
        print('Отлично, мы готовы начать игру!')

    def init(self):
        self._ships = [Ship(i+1, randint(1, 2))
                       for i in range(4) for k in range(4-i)][::-1]

        for k in self._ships:
            for counter in range(20):
                x, y = randint(0, Controller.POLE_SIZE - 1), randint(0, Controller.POLE_SIZE - 1)
                k.set_start_coords(x, y)
                if k.is_out_pole(Controller.POLE_SIZE):
                    continue
                for i in self._ships:
                    if i != k:
                        if k.is_collide(i):
                            break
                else:
                    self.set_cell(k, 'ship')
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
        print(('    ' + '  '.join(self.LETTERS_LIST))[:4+Controller.POLE_SIZE*3])
        for ind, k in enumerate(self._pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('⬜' if i._cell == 'closed' else '🟫' if i._cell ==
                      'hit' else '⬛' if i._cell == 'ship' else '🟨', end=' ')
            print()

    def show_closed(self):
        print(('    ' + '  '.join(self.LETTERS_LIST))[:4+Controller.POLE_SIZE*3])
        for ind, k in enumerate(self._closed_pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('🟦' if i._cell == 'closed' else '⬛' if i._cell ==
                      'opened and hit' else '⬜', end=' ')
            print()


class Game:
    def __init__(self, custom_mode=False):
        self.pole = GamePole()
        if not custom_mode:
            self.pole.init()
        else:
            self.pole.player_init()

    def show(self):
        self.pole.show()

    def show_closed(self):
        self.pole.show_closed()

    def set_shot(self, x, y, obj):
        x, y = GamePole.coords_convertor(x, y, Controller.POLE_SIZE)
        pole = obj.pole.get_pole[y - 1][x - 1]
        closed_pole = self.pole._closed_pole[y - 1][x - 1]
        if closed_pole._cell in ('opened and hit', 'opened'):
            return 'opened'
        if not (pole._cell == 'hit' or pole.owner_ship is None or pole.owner_number is None):
            pole.owner_ship._cells[pole.owner_number] = 0
            pole._cell = 'hit'
            pole.owner_number = None
            closed_pole._cell = 'opened and hit'
            if all(map(lambda x: x == 0, pole.owner_ship._cells)):
                return 'destroyed'
            return 'hit'
        closed_pole._cell = 'hit'
        pole._cell = 'opened'
        return 'missed'


class Controller:
    POLE_SIZE = 10
    
    def __init__(self, size, mode=False):
        self.set_size(size)
        self.player = Game(mode)
        self.bot = Game()
        
    @classmethod
    def set_size(cls, size):
        cls.POLE_SIZE = size

    def player_turn(self):
        print('Ваше поле:')
        self.player.show_closed()
        print('Ваша очередь ходить!')
        while True:
            x, y = input(
                'Для выстрела введимте координаты клетки в формате Буква - номер строки: ').split()
            answer = self.player.set_shot(x, y, self.bot)
            if answer == 'opened':
                print('Данная клетка уже открыта, попробуйте другую!')
            else:
                break
        print('Ваш результат: ' + answer)
        self.bot_turn()

    def bot_turn(self):
        while True:
            x, y = randint(1, self.POLE_SIZE), randint(1, self.POLE_SIZE)
            answer = self.bot.set_shot(str(x), str(y), self.player)
            if answer != 'opened':
                break
        bot_choice = f'{GamePole.LETTERS_LIST[x - 1]} {y}'
        print('Бот сходил: ' + bot_choice)
        self.player.show()
        self.player_turn()



class Cell:
    def __init__(self):
        self._cell = 'closed'
        self.owner_ship = None
        self.owner_number = None


class Closed_Cell:
    def __init__(self):
        self._cell = 'closed'


class PoleExceptions(Exception):
    pass


class IndexException(PoleExceptions):
    pass


SIZE_GAME_POLE = 10


game = Controller(SIZE_GAME_POLE, True)
game.player_turn()