from random import randint, choice, seed
# seed(1)


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

    def __init__(self, size=10):
        self._size = size
        self._ships = []

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
        self._pole = [[Cell() for k in range(self._size)]
                      for i in range(self._size)]
        self._closed_pole = [[Closed_Cell() for k in range(self._size)]
                             for i in range(self._size)]

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
        self.create_pole()
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
                x, y = self.coords_convertor(x, y, self._size)
                ship = Ship(int(length), tp, x - 1, y - 1)
                if ship.is_out_pole(self._size):
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
        self.create_pole()

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
                    self.set_cell(k, 'ship')
                    break
            else:
                raise CantCreatePoleException()

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
            
    def set_cell_around(self, ship, value):
        x, y = ship.get_start_coords()
        if ship._tp == 1:
            if x >= 1:
                self._closed_pole[y][x - 1]._cell = value
                if y >= 1:
                    self._closed_pole[y - 1][x - 1]._cell = value
                if y < self._size - 1:
                    self._closed_pole[y + 1][x - 1]._cell = value
            if x + ship._length < self._size:
                self._closed_pole[y][x + ship._length]._cell = value
                if y >= 1:
                    self._closed_pole[y - 1][x + ship._length]._cell = value
                if y < self._size - 1:
                    self._closed_pole[y + 1][x + ship._length]._cell = value
                
        else:
            if y >= 1:
                self._closed_pole[y - 1][x]._cell = value
                if x >= 1:
                    self._closed_pole[y - 1][x - 1]._cell = value
                if x < self._size - 1:
                    self._closed_pole[y - 1][x + 1]._cell = value
            if y + ship._length < self._size:
                self._closed_pole[y + ship._length][x]._cell = value
                if x >= 1:
                    self._closed_pole[y + ship._length][x - 1]._cell = value
                if x < self._size - 1:
                    self._closed_pole[y + ship._length][x + 1]._cell = value
                    
        for i in range(ship._length):
            if ship._tp == 1:
                if y >= 1:
                    self._closed_pole[y - 1][x + i]._cell = value
                if y < self._size - 1:
                    self._closed_pole[y + 1][x + i]._cell = value
            else:
                if x >= 1:
                    self._closed_pole[y + i][x - 1]._cell = value
                if x < self._size - 1:
                    self._closed_pole[y + i][x + 1]._cell = value
                    

    def show(self):
        print(('    ' + '  '.join(self.LETTERS_LIST))[:4+self._size*3])
        for ind, k in enumerate(self._pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('⬜' if i._cell == 'closed' else '🟫' if i._cell ==
                      'hit' else '⬛' if i._cell == 'ship' else '🟨', end=' ')
            print()

    def show_closed(self):
        print(('    ' + '  '.join(self.LETTERS_LIST))[:4+self._size*3])
        for ind, k in enumerate(self._closed_pole):
            print(str(ind + 1).rjust(2, ' '), end=' ')
            for i in k:
                print('🟦' if i._cell == 'closed' else '⬛' if i._cell ==
                      'hit' else '⬜', end=' ')
            print()


class Game:
    def __init__(self, size=10, custom_mode=False):
        self._size = size
        self.pole = GamePole(size)
        if not custom_mode:
            while True:
                try:
                    self.pole.init()
                    break
                except CantCreatePoleException:
                    continue
        else:
            self.pole.player_init()

    def show(self):
        self.pole.show()

    def show_closed(self):
        self.pole.show_closed()

    def set_shot(self, x, y, obj):
        x, y = GamePole.coords_convertor(x, y, self._size)
        pole = obj.pole.get_pole[y - 1][x - 1]
        closed_pole = self.pole._closed_pole[y - 1][x - 1]
        if closed_pole._cell in ('hit', 'miss'):
            return 'opened'
        if not (pole._cell in ('hit', 'miss') or pole.owner_ship is None or pole.owner_number is None):
            pole.owner_ship._cells[pole.owner_number] = 0
            pole._cell = 'hit'
            pole.owner_number = None
            closed_pole._cell = 'hit'
            if all(map(lambda x: x == 0, pole.owner_ship._cells)):
                obj.pole._ships.remove(pole.owner_ship)
                return 'destroyed'
            return 'hit'
        closed_pole._cell = 'miss'
        pole._cell = 'miss'
        return 'missed'


class Controller:
    def __init__(self, size=10, mode=False, helper=False):
        self._size = size
        self.player = Game(size, mode)
        self.bot = Game(size)
        self.last_bot_choice = []
        self._helper = helper

    def player_turn(self):
        print('Ваше поле:')
        self.player.show_closed()
        print('Ваша очередь ходить!')
        while True:
            try:
                x, y = input(
                    'Для выстрела введимте координаты клетки в формате Буква - номер строки: ').split()
                answer = self.player.set_shot(x, y, self.bot)
                if answer == 'opened':
                    print('Данная клетка уже открыта, попробуйте другую!')
                else:
                    if answer in ('hit', 'destroyed'):
                        return True
                    break
            except Exception as e:
                print('Что-то пошло не так...')
                print('Попробуйте снова!')
                print(e)
                continue
        
        if answer == 'destroyed' and self._helper:
            x, y = GamePole.coords_convertor(x, y, self._size)
            ship = self.bot.pole._pole[y - 1][x - 1].owner_ship
            self.round_destroyed_ship(ship)
        print('Ваш результат: ' + answer)
        
    def bot_set_shot(self, x, y):
        return self.bot.set_shot(str(x), str(y), self.player)
    
    def bot_random_choice(self):
            while True:
                x, y = randint(1, self._size), randint(1, self._size)
                answer = self.bot.set_shot(str(x), str(y), self.player)
                if answer != 'opened':
                    break
            self.last_bot_choice.append((x, y, None, answer))
            if answer == 'destroyed':
                self.round_destroyed_ship()
            return x, y, answer
            

    def bot_turn(self):
        if not self.last_bot_choice:
            x, y, ans = self.bot_random_choice()
        else:
            
            temp_x, temp_y, tp, ans = self.last_bot_choice[-1]
            variants = set()
            if ans == 'hit':
                while True:
                    temp_x, temp_y, tp, ans = self.last_bot_choice[-1]
                    if tp is None:
                        bot_choice = randint(1, 4)
                    elif tp == 1:
                        bot_choice = choice([2, 4])
                    elif tp == 2:
                        bot_choice = choice([1, 3])
                        
                    if (len(variants) == 4 and tp is None) or (len(variants) == 2 and tp is not None):
                        self.last_bot_choice.pop(-1)
                        variants = set()
                        continue

                    if bot_choice == 1:
                        if temp_y - 1 <= 0:
                            variants.add(bot_choice)
                            continue
                        x, y = temp_x, temp_y - 1
                        bot_ans = self.bot_set_shot(x, y)
                    elif bot_choice == 2:
                        if temp_x + 1 > self._size:
                            variants.add(bot_choice)
                            continue
                        x, y = temp_x + 1, temp_y
                        bot_ans = self.bot_set_shot(x, y)
                    elif bot_choice == 3:
                        if temp_y + 1 > self._size:
                            variants.add(bot_choice)
                            continue
                        x, y = temp_x, temp_y + 1
                        bot_ans = self.bot_set_shot(x, y)
                    elif bot_choice == 4:
                        if temp_x - 1 <= 0:
                            variants.add(bot_choice)
                            continue
                        x, y = temp_x - 1, temp_y
                        bot_ans = self.bot_set_shot(x, y)

                    if bot_ans == 'opened':
                        variants.add(bot_choice)
                        continue
                    elif bot_ans == 'destroyed':
                        self.round_destroyed_ship()
                        self.last_bot_choice = []
                        ans = 'destroyed'
                        break
                    elif bot_ans == 'missed':
                        if tp is not None:
                            self.last_bot_choice.pop(-1)
                        ans = 'missed'
                        break
                    elif bot_ans == 'hit':
                        bot_tp = 1 if bot_choice in (2, 4) and self.last_bot_choice[-1][3] == 'hit' else 2
                        self.last_bot_choice[-1] = (temp_x, temp_y, bot_tp, ans)
                        self.last_bot_choice.append((x, y, bot_tp, bot_ans))
                        ans = 'hit'
                        break
            else:
                x, y, ans = self.bot_random_choice()
        print('Бот сходил:', GamePole.LETTERS_LIST[x - 1], y)
        return ans
    
    def round_destroyed_ship(self, ship=None):
        if ship is None:
            ship_info = self.last_bot_choice[-1]
            x, y = ship_info[0], ship_info[1]
            x, y = x - 1, y - 1
            ship = self.player.pole._pole[y][x].owner_ship
            self.bot.pole.set_cell_around(ship, 'miss')
        else:
            self.player.pole.set_cell_around(ship, 'miss')

    def check_winner(self):
        if not self.bot.pole._ships:
            print('Победил Игрок, проиграл бот!')
            return True
        elif not self.player.pole._ships:
            print('Победил бот, проиграл Игрок!')
            return True
        return False


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


class CantCreatePoleException(PoleExceptions):
    pass


SIZE_GAME_POLE = int(input('Введите размер поля от 8 до 13: '))
if not (8 <= SIZE_GAME_POLE <= 13):
    raise CantCreatePoleException()

mode = bool(input(
    'Введите 1 если желаете сами расставить корабли, иначе пропустите этот этап: '))
helper = bool(input('Для включения помощи в отображения потопленных кораблей напишите 1, иначе пропустите этот пункт: '))
game = Controller(SIZE_GAME_POLE, mode, helper)
turn = 'player'
while True:
    if turn == 'player':
        if game.player_turn():
            if game.check_winner():
                break
            continue
        turn = 'player' if turn == 'bot' else 'bot'
    else:
        res = game.bot_turn()
        if res == 'hit':
            continue
        if res == 'destroyed':
            if game.check_winner():
                break
            continue
        if res == 'missed':
            turn = 'player' if turn == 'bot' else 'bot'
            game.player.show()
