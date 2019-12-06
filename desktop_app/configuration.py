class Configuration:
    def __init__(self):
        self.lego_bricks = dict()  # cheia va fi id-ul, valoarea va fi [obiect, is_used]; lista va contine toate piesele initializate
        self.occupied_space = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de spatiu + id piesa (a cui este)
        self.occupied_studs = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de studs + id piesa + id piesa care ocupa
        self.occupied_tubes = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de tubes + id piesa + id piesa care ocupa
        self.db_brick_info = dict()  # cheia va fi id-ul din bd, valoarea va fi o lista de 3 elemente (lungime, latime, inaltime) si 3 liste: spaces, studs, tubes

    # functia asta pune obiectul peste alte obiecte (in studs)
    # piesa va fi pusa de la x la x + width, y la y + length, z la z + height
    def place_in_studs(self, lego_brick, start_coordinates, rotation=0):
        if start_coordinates[2] not in self.occupied_space:
            self.occupied_space[start_coordinates[2]] = []
        if start_coordinates[2] not in self.occupied_tubes:
            self.occupied_tubes[start_coordinates[2]] = []
        if start_coordinates[2] not in self.occupied_studs:
            self.occupied_studs[start_coordinates[2]] = []

        # daca piesa este deja pusa undeva returneaza fals
        if self.lego_bricks[lego_brick.brick_id][1]:
            return False

        # se verifica daca coordonata de start e valabila
        has_at_least_one_stud = False
        self_tubes = []
        for tube in self.db_brick_info[lego_brick.db_id][5]:
            aux_tube = [tube[0] + start_coordinates[0], tube[1] + start_coordinates[1],
                        tube[2] + start_coordinates[2],
                        lego_brick.brick_id, 0]
            if start_coordinates[2] != 0:
                for _tube in self.occupied_studs[start_coordinates[2]]:
                    if aux_tube[0] == _tube[0] and aux_tube[1] == _tube[1] and aux_tube[2] == _tube[2] and _tube[4] == 0:
                        has_at_least_one_stud = True
            self_tubes.append(aux_tube)
        if not has_at_least_one_stud and start_coordinates[2] != 0:
            return False

        # calculeaza spatiile ce va ocupa piesa si daca sunt valabile
        all_spaces_to_occupy = []
        for height in range(start_coordinates[2], start_coordinates[2] + self.db_brick_info[lego_brick.db_id][2]):
            spaces_to_occupy = []
            for space in self.db_brick_info[lego_brick.db_id][3]:
                if space[2] == height - start_coordinates[2]:
                    spaces_to_occupy.append(
                        [space[0] + start_coordinates[0], space[1] + start_coordinates[1], height, lego_brick.brick_id])
            occupied_space = self.occupied_space.get(height)
            if occupied_space is None:
                self.occupied_space[height] = []
                occupied_space = []
            for space in spaces_to_occupy:
                if space in occupied_space:
                    return False
                else:
                    all_spaces_to_occupy.append(space)

        # daca s-a ajuns pana aici inseamna ca piesa va fi pusa
        self.lego_bricks[lego_brick.brick_id] = [self, True]
        for space in all_spaces_to_occupy:
            self.occupied_space[space[2]].append(space)
        for stud in self.db_brick_info[lego_brick.db_id][4]:
            if stud[2] + start_coordinates[2] not in self.occupied_studs:
                self.occupied_studs[stud[2] + start_coordinates[2]] = []
            self.occupied_studs[stud[2] + start_coordinates[2]].append(
                [stud[0] + start_coordinates[0], stud[1] + start_coordinates[1], stud[2] + start_coordinates[2],
                 lego_brick.brick_id, 0])
        for stud in self.occupied_studs[start_coordinates[2]]:
            for tube in self_tubes:
                if stud[0] == tube[0] and stud[1] == tube[1] and stud[2] == tube[2]:
                    tube[4] = stud[3]
                    stud[4] = lego_brick.brick_id
        if start_coordinates[2] not in self.occupied_tubes:
            self.occupied_tubes[start_coordinates[2]] = []
        for tube in self_tubes:
            self.occupied_tubes[start_coordinates[2]].append(tube)
        return True

    # functia asta pune obiectul in tuburile altui obiect
    def place_in_tubes(self, lego_brick, start_coordinates, rotation=0):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din stud_coordinates a piesei curente, se reseteaza flag-urile din tube_coordinates din piesele respective
    def remove_from_studs(self):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din tube_coordinates a piesei curente, se reseteaza flag-urile din stud_coordinates din piesele respective
    def remove_from_tubes(self):
        pass


class Brick:
    def __init__(self, db_id, color, configuration):
        self.db_id = db_id
        self.brick_id = len(configuration.lego_bricks) + 1  # cheia pentru dictionarul _lego_bricks
        self.color = color

        # urmatoarele atribute sunt folosite atunci cand piesa este pusa in alta piesa
        self.rotation = 0  # 0 -> in dreapta, 1 -> in jos, 2 -> in stanga, 3 -> in sus

        configuration.lego_bricks[self.brick_id] = [self, False]


def initialize_lego_bricks_dict(given_configuration):
    given_configuration.db_brick_info[6] = [1, 1, 1, [[0, 0, 0]], [[0, 0, 1]], [[0, 0, 0]]]
    given_configuration.db_brick_info[9] = [2, 2, 3,
                                            [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 1],
                                             [1, 0, 1],
                                             [1, 1, 1],
                                             [0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                                            [[0, 0, 3], [0, 1, 3], [1, 0, 3], [1, 1, 3]],
                                            [[0, 0, 0], [0, 1, 0], [1, 0, 0],
                                             [1, 1, 0]]]


if __name__ == '__main__':
    configuration = Configuration()
    initialize_lego_bricks_dict(configuration)
    # test_brick = Brick(6, "White")  # piesa generica de 1x1x1
    test_brick_2 = Brick(9, "White", configuration)  # piesa generica de 2x2x3 (2x2 de inaltime "normala")
    test_brick_3 = Brick(9, "White", configuration)
    test_brick_4 = Brick(9, "White", configuration)
    test_brick_5 = Brick(9, "White", configuration)
    print(configuration.place_in_studs(test_brick_2, [0, 0, 0]))
    # print(_lego_bricks[1][0].stud_coordinates)
    # print(_lego_bricks[1][0].tube_coordinates)
    # print(_lego_bricks[3][0].stud_coordinates)
    # print(_lego_bricks[3][0].tube_coordinates)
    # print(test_brick.place_in_studs([0, 0, 0], [_lego_bricks[1][0]]))
    # print(test_brick.place_in_studs([0, 0, 3], [_lego_bricks[1][0]]))
    # print(_lego_bricks[1][0].stud_coordinates)
    # print(_lego_bricks[1][0].tube_coordinates)
    print(configuration.place_in_studs(test_brick_3, [0, 2, 0]))
    print(configuration.place_in_studs(test_brick_4, [1, 1, 3]))
    print(configuration.place_in_studs(test_brick_5, [2, 2, 6]))
    for key, value in configuration.occupied_space.items():
        print(key, value)
    print("\n")
    for key, value in configuration.occupied_studs.items():
        print(key, value)
    print("\n")
    for key, value in configuration.occupied_tubes.items():
        print(key, value)
    # TODO: metoda place_in_tubes + folosit rotation + decrementat inaltimea de la tubes pentru toate piesele
