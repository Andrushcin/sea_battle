from random import randint

my_ship_dict = {}
my_remove_ship = {}

free_cell_dict = {}
comp_remove_ship = {}
comp_ship_dict = {}
comp_bang_list = []


class Board:
    sea = {
        11: '—', 21: '—', 31: '—', 41: '—', 51: '—', 61: '—',
        12: '—', 22: '—', 32: '—', 42: '—', 52: '—', 62: '—',
        13: '—', 23: '—', 33: '—', 43: '—', 53: '—', 63: '—',
        14: '—', 24: '—', 34: '—', 44: '—', 54: '—', 64: '—',
        15: '—', 25: '—', 35: '—', 45: '—', 55: '—', 65: '—',
        16: '—', 26: '—', 36: '—', 46: '—', 56: '—', 66: '—',
    }

    def __init__(self, player, sea=sea):
        self.player = player
        self.sea = sea.copy()

    def print_board(self):
        c = self.sea
        player = self.player

        if player == 'comp':
            print("Поле противника")
            self.sea.update(comp_remove_ship)
            self.sea.update(free_cell_dict)

        elif player == 'gamer':
            print("Ваше поле")
            self.sea.update(my_ship_dict)
            self.sea.update(my_remove_ship)

        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")

        print(f"1 | {c[11]} | {c[21]} | {c[31]} | {c[41]} | {c[51]} | {c[61]} |")

        print(f"2 | {c[12]} | {c[22]} | {c[32]} | {c[42]} | {c[52]} | {c[62]} |")

        print(f"3 | {c[13]} | {c[23]} | {c[33]} | {c[43]} | {c[53]} | {c[63]} |")

        print(f"4 | {c[14]} | {c[24]} | {c[34]} | {c[44]} | {c[54]} | {c[64]} |")

        print(f"5 | {c[15]} | {c[25]} | {c[35]} | {c[45]} | {c[55]} | {c[65]} |")

        print(f"6 | {c[16]} | {c[26]} | {c[36]} | {c[46]} | {c[56]} | {c[66]} |")

        print()


my_board = Board('gamer')
comp_board = Board('comp')


class Ship:
    def __init__(self, coord, ship_dict):
        self.coord = coord
        self.ship_dict = ship_dict
        ship_dict[coord] = "■"


quantity_my_ship = 0
quantity_comp_ship = 0


def start():
    print("Игра Морской Бой\n"
          "Пустые клетки обозначаются символом 'O'\n"
          "Корабли обозначаются символом '■'\n"
          "Убитые корабли обозначаются символом '×'\n"
          "Координаты записываются без пробела в формате xy\n"
          "Введите координаты, чтобы расставить корабли на своём поле: ")

    while len(my_ship_dict) != 11:
        try:
            c = int(input())
        except Exception:
            print("Недопустимый символ")
            continue
        if any(key == c for key in Board.sea.keys()):
            Ship(c, my_ship_dict)

    while len(comp_ship_dict) != 11:
        c = 10 * randint(1, 6) + randint(1, 6)
        Ship(c, comp_ship_dict)

    print()
    comp_board.print_board()
    my_board.print_board()
    print("Игра началась\n")


def comp_bang():
    coord = 10 * randint(1, 6) + randint(1, 6)
    if coord in comp_bang_list:
        return comp_bang()
    else:
        print()
        comp_bang_list.append(coord)
        if coord in my_ship_dict:
            del my_ship_dict[coord]
            my_remove_ship[coord] = "×"

            print("Противник поразил ваш корабль")
            global quantity_my_ship
            quantity_my_ship += 1
            if quantity_my_ship == 11:
                print("Противник выиграл")
                return None
            else:
                return comp_bang()

        else:
            comp_bang_list.append(coord)
            print("Противник промахнулся")
            my_board.print_board()
            return game()


def game():
    print("----------------------------")
    try:
        coord = int(input("Ваш выстрел: "))
    except Exception:
        print("Недопустимый символ")
        return game()

    if coord in comp_remove_ship.keys() or coord in free_cell_dict.keys():
        print("В эту клетку вы уже стреляли")
        return game()

    elif coord in comp_ship_dict.keys():
        del comp_ship_dict[coord]
        comp_remove_ship[coord] = "×"

        global quantity_comp_ship
        quantity_comp_ship += 1
        print("Вы попали")
        if quantity_comp_ship == 11:
            print("Вы выиграли")
            comp_board.print_board()
            return None
        else:
            comp_board.print_board()
            return game()
    else:
        print("Вы промахнулись")
        free_cell_dict[coord] = "O"
        comp_board.print_board()

    print("----------------------------")

    return comp_bang()


start()
game()
