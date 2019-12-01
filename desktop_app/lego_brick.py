_lego_bricks = dict()  # cheia va fi id-ul, valoarea va fi [obiect, is_used]; lista va contine toate piesele initializate
_occupied_space = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate


class Brick:
    def __init__(self, db_id, length, width, height, color, space, studs, tubes):
        global _lego_bricks
        self.db_id = db_id
        self.brick_id = len(_lego_bricks) + 1  # cheia dictionarului
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        # self.weight = weight -> trebuie sau nu?

        # urmatoarele atribute vor avea cate o lista cu coordonatele lor pe un plan in care se afla doar piesa respectiva
        self.space = space
        self.studs = studs
        self.tubes = tubes

        # urmatoarele atribute sunt folosite atunci cand piesa este pusa in alta piesa
        self.start_coordinates = [-1, -1, -1]  # coordonatele de unde incepe (coltul din stanga sus <=> unde x, y minim)
        self.rotation = 0  # 0 -> in dreapta, 1 -> in jos, 2 -> in stanga, 3 -> in sus
        self.occupied_space = []  # lista de liste [x, y, z]
        self.stud_coordinates = []  # studs = spatiile de sus; flagurile vor fi id-ul pieselor inserate (0 daca nu e nicio piesa <=> e liber)
        self.tube_coordinates = []  # tubes = spatiile de jos; la fel ca sus

        _lego_bricks[self.brick_id] = [self, False]

    # functia asta pune obiectul peste alte obiecte (in studs)
    # piesa va fi pusa de la x la x + width, y la y + length, z la z + height
    def place_in_studs(self, start_coordinates, brick_list):
        # se iau toate coordonatele la studs care sunt libere si pe aceeasi inaltime
        empty_studs_in_list = []
        for brick in brick_list:
            for stud in brick.stud_coordinates:
                if stud[3] == 0 and stud[2] == start_coordinates[2]:
                    empty_studs_in_list.append(stud)

        # se verifica daca coordonata de start e valabila
        if [start_coordinates[0], start_coordinates[1], start_coordinates[2], 0] not in empty_studs_in_list:
            return False

        # calculeaza spatiile ce va ocupa piesa si daca sunt valabile
        global _occupied_space
        for height in range(start_coordinates[2], start_coordinates[2] + self.height):
            spaces_to_occupy = []
            for space in self.space:
                if space[2] == height:
                    spaces_to_occupy.append([space[0] + start_coordinates[0], space[1] + start_coordinates[1], height])
            occupied_space = _occupied_space.get(height)
            if occupied_space is None:
                _occupied_space[height] = []
                occupied_space = []
            for space in spaces_to_occupy:
                if space in occupied_space:
                    self.occupied_space = []
                    return False
                else:
                    self.occupied_space.append(space)

        # daca s-a ajuns pana aici inseamna ca piesa va fi pusa
        global _lego_bricks
        _lego_bricks[self.brick_id] = [self, True]
        for space in self.occupied_space:
            _occupied_space[space[2]].append(space)
        for stud in self.studs:
            self.stud_coordinates.append([stud[0] + start_coordinates[0], stud[1] + start_coordinates[1], stud[2] + start_coordinates[2], 0])
        for tube in self.tubes:
            self.tube_coordinates.append([tube[0] + start_coordinates[0], tube[1] + start_coordinates[1], tube[2] + start_coordinates[2], 0])
        for brick in brick_list:
            for stud in brick.stud_coordinates:
                for tube in self.tube_coordinates:
                    if stud[0] == tube[0] and stud[1] == tube[1] and stud[2] == tube[2] and stud[3] == 0:
                        stud[3] = self.brick_id
                        tube[3] = brick.brick_id

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
    base_brick = Brick(0, 0, 0, 0, "", [], [], [])
    base_brick.stud_coordinates = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 2, 0, 0], [0, 3, 0, 0], [0, 4, 0, 0],
                                   [1, 0, 0, 0], [1, 1, 0, 0], [1, 2, 0, 0], [1, 3, 0, 0], [1, 4, 0, 0],
                                   [2, 0, 0, 0], [2, 1, 0, 0], [2, 2, 0, 0], [2, 3, 0, 0], [2, 4, 0, 0],
                                   [3, 0, 0, 0], [3, 1, 0, 0], [3, 2, 0, 0], [3, 3, 0, 0], [3, 4, 0, 0]]


if __name__ == '__main__':
    initialize_lego_bricks_dict()
    test_brick = Brick(6, 1, 1, 1, "White", [[0, 0, 0]], [[0, 0, 0]], [[0, 0, 0]])  # piesa generica de 1x1x1
    test_brick_2 = Brick(9, 2, 2, 3, "White", [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                         [[0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                         [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]])  # piesa generica de 2x2x3 (2x2 de inaltime "normala")
    test_brick_2.place_in_studs([0, 0, 0], [_lego_bricks[1][0]])
    # print(_lego_bricks[1][0].stud_coordinates)
    print(_lego_bricks[3][0].occupied_space)
