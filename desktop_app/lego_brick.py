_lego_bricks = dict()  # cheia va fi id-ul, valoarea va fi [obiect, is_used]; lista va contine toate piesele initializate
_occupied_space = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de spatiu
_occupied_studs = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de studs
_occupied_tubes = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de tubes
_db_brick_info = dict()  # cheia va fi id-ul din bd, valoarea va fi o lista de 3 elemente (lungime, latime, inaltime) si 3 liste: spaces, studs, tubes


class Brick:
    def __init__(self, db_id, color):
        global _lego_bricks
        self.db_id = db_id
        self.brick_id = len(_lego_bricks)  # cheia pentru dictionarul _lego_bricks
        self.color = color

        # urmatoarele atribute sunt folosite atunci cand piesa este pusa in alta piesa
        self.rotation = 0  # 0 -> in dreapta, 1 -> in jos, 2 -> in stanga, 3 -> in sus

        _lego_bricks[self.brick_id] = [self, False]

    # functia asta pune obiectul peste alte obiecte (in studs)
    # piesa va fi pusa de la x la x + width, y la y + length, z la z + height
    def place_in_studs(self, start_coordinates, rotation):
        global _lego_bricks, _occupied_space, _occupied_studs, _occupied_tubes, _db_brick_info
        if start_coordinates[2] not in _occupied_space:
            _occupied_space[start_coordinates[2]] = []
        if start_coordinates[2] not in _occupied_tubes:
            _occupied_tubes[start_coordinates[2]] = []
        if start_coordinates[2] not in _occupied_studs:
            _occupied_studs[start_coordinates[2]] = []

        # daca piesa este deja pusa undeva returneaza fals
        if _lego_bricks[self.brick_id][1]:
            return False

        # se verifica daca coordonata de start e valabila
        if start_coordinates[2] != 0:
            if [start_coordinates[0], start_coordinates[1], start_coordinates[2], 0] not in _occupied_studs[start_coordinates[2]]:
                return False

        # calculeaza spatiile ce va ocupa piesa si daca sunt valabile
        all_spaces_to_occupy = []
        for height in range(start_coordinates[2], start_coordinates[2] + _db_brick_info[self.db_id][2]):
            spaces_to_occupy = []
            for space in _db_brick_info[self.db_id][3]:
                if space[2] == height - start_coordinates[2]:
                    spaces_to_occupy.append([space[0] + start_coordinates[0], space[1] + start_coordinates[1], height])
            occupied_space = _occupied_space.get(height)
            if occupied_space is None:
                _occupied_space[height] = []
                occupied_space = []
            for space in spaces_to_occupy:
                if space in occupied_space:
                    return False
                else:
                    all_spaces_to_occupy.append(space)

        # daca s-a ajuns pana aici inseamna ca piesa va fi pusa
        _lego_bricks[self.brick_id] = [self, True]
        for space in all_spaces_to_occupy:
            _occupied_space[space[2]].append(space)
        for stud in _db_brick_info[self.db_id][4]:
            if stud[2] + start_coordinates[2] not in _occupied_studs:
                _occupied_studs[stud[2] + start_coordinates[2]] = []
            _occupied_studs[stud[2] + start_coordinates[2]].append(
                [stud[0] + start_coordinates[0], stud[1] + start_coordinates[1], stud[2] + start_coordinates[2], 0])
        self_tubes = []
        for tube in _db_brick_info[self.db_id][5]:
            self_tubes.append(
                [tube[0] + start_coordinates[0], tube[1] + start_coordinates[1], tube[2] + start_coordinates[2], 0])
        for stud in _occupied_studs[start_coordinates[2]]:
            for tube in self_tubes:
                if stud[0] == tube[0] and stud[1] == tube[1] and stud[2] == tube[2]:
                    tube[3] = stud[3]
                    stud[3] = self.brick_id
        for tube in self_tubes:
            if start_coordinates[2] not in _occupied_tubes:
                _occupied_tubes[start_coordinates[2]] = []
            _occupied_tubes[start_coordinates[2]].append(tube)
        return True

    # functia asta pune obiectul in tuburile altui obiect
    def place_in_tubes(self, start_coordinates, brick_list):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din stud_coordinates a piesei curente, se reseteaza flag-urile din tube_coordinates din piesele respective
    def remove_from_studs(self):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din tube_coordinates a piesei curente, se reseteaza flag-urile din stud_coordinates din piesele respective
    def remove_from_tubes(self):
        pass

    # metoda care incearca sa puna piesa asta in studs/tubes la o lista de id-uri ale pieselor
    #   primeste parametru cu coordonate
    # cum o va face -> face o lista din toate listele cu studs/tubes care au flag de neocupat


def initialize_lego_bricks_dict():
    # base_brick = Brick(0, "")
    # base_brick.stud_coordinates = [[0, 0, 1, 0], [0, 1, 1, 0], [0, 2, 1, 0], [0, 3, 1, 0],
    #                                [1, 0, 1, 0], [1, 1, 1, 0], [1, 2, 1, 0], [1, 3, 1, 0],
    #                                [2, 0, 1, 0], [2, 1, 1, 0], [2, 2, 1, 0], [2, 3, 1, 0],
    #                                [3, 0, 1, 0], [3, 1, 1, 0], [3, 2, 1, 0], [3, 3, 1, 0]]
    # base_brick.occupied_space = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
    #                              [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0],
    #                              [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
    #                              [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    # global _occupied_space
    # _occupied_space[0] = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0],
    #                       [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0],
    #                       [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0],
    #                       [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]]
    # global _db_brick_info
    _db_brick_info[6] = [1, 1, 1, [[0, 0, 0]], [[0, 0, 1]], [[0, 0, 0]]]
    _db_brick_info[9] = [2, 2, 3,
                                [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1],
                                 [0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                                [[0, 0, 3], [0, 1, 3], [1, 0, 3], [1, 1, 3]],
                                [[0, 0, 0], [0, 1, 0], [1, 0, 0],
                                 [1, 1, 0]]]


if __name__ == '__main__':
    initialize_lego_bricks_dict()
    test_brick = Brick(6, "White")  # piesa generica de 1x1x1
    test_brick_2 = Brick(9, "White")  # piesa generica de 2x2x3 (2x2 de inaltime "normala")
    test_brick_3 = Brick(9, "White")
    test_brick_4 = Brick(9, "White")
    test_brick_5 = Brick(9, "White")
    print(test_brick_2.place_in_studs([0, 0, 0], 0))
    # print(_lego_bricks[1][0].stud_coordinates)
    # print(_lego_bricks[1][0].tube_coordinates)
    # print(_lego_bricks[3][0].stud_coordinates)
    # print(_lego_bricks[3][0].tube_coordinates)
    # print(test_brick.place_in_studs([0, 0, 0], [_lego_bricks[1][0]]))
    # print(test_brick.place_in_studs([0, 0, 3], [_lego_bricks[1][0]]))
    # print(_lego_bricks[1][0].stud_coordinates)
    # print(_lego_bricks[1][0].tube_coordinates)
    print(test_brick_3.place_in_studs([0, 2, 0], 0))
    print(test_brick_4.place_in_studs([1, 1, 3], 0))
    print(test_brick_5.place_in_studs([0, 2, 3], 0))
    for key, value in _occupied_space.items():
        print(key, value)
    print("\n")
    for key, value in _occupied_studs.items():
        print(key, value)
    print("\n")
    for key, value in _occupied_tubes.items():
        print(key, value)
    # TODO: folosit rotation
