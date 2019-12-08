def rotate_1(li_coord, length):
    new_li_coord = []
    for coords in li_coord:
        # observatie: inaltimea va ramane ca la inceput, lucram doar cu x si y, ca in plan
        new_x = coords[1]
        new_y = length - 1 - coords[0]
        new_li_coord.append((new_x, new_y, coords[2]))
    return new_li_coord


def rotate_2(li_coord, length, width):
    new_li_coord = []
    for coords in li_coord:
        new_x = length - 1 - coords[0]
        new_y = width - 1 - coords[1]
        new_li_coord.append((new_x, new_y, coords[2]))
    return new_li_coord


def rotate_3(li_coord, width):
    new_li_coord = []
    for coords in li_coord:
        new_x = width - 1 - coords[1]
        new_y = coords[0]
        new_li_coord.append((new_x, new_y, coords[2]))
    return new_li_coord


def rotate_our_coordinates(brick_db_info, rotation):
    # facem rotatia in sensul acelor de ceasornic; rotatia apartine {0, 1, 2, 3}
    new_brick_info = brick_db_info.copy()
    brick_length = new_brick_info[0]
    brick_width = new_brick_info[1]
    li_all_coords_spaces = new_brick_info[3]
    li_all_coords_studs = new_brick_info[4]
    li_all_coords_tubes = new_brick_info[5]

    if rotation % 4 == 0:
        pass
    if rotation % 4== 1:
        new_brick_info[3] = rotate_1(li_all_coords_spaces, brick_length)
        new_brick_info[4] = rotate_1(li_all_coords_studs, brick_length)
        new_brick_info[5] = rotate_1(li_all_coords_tubes, brick_length)
        new_brick_info[0] = brick_width
        new_brick_info[1] = brick_length
    if rotation % 4 == 2:
        new_brick_info[3] = rotate_2(li_all_coords_spaces, brick_length, brick_width)
        new_brick_info[4] = rotate_2(li_all_coords_studs, brick_length, brick_width)
        new_brick_info[5] = rotate_2(li_all_coords_tubes, brick_length, brick_width)
    if rotation % 4 == 3:
        new_brick_info[3] = rotate_3(li_all_coords_spaces, brick_width)
        new_brick_info[4] = rotate_3(li_all_coords_studs, brick_width)
        new_brick_info[5] = rotate_3(li_all_coords_tubes, brick_width)
        new_brick_info[0] = brick_width
        new_brick_info[1] = brick_length
    return new_brick_info


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

        # informatii despre piesa rotita
        our_piece_new_info = rotate_our_coordinates(self.db_brick_info[lego_brick.db_id], rotation)
        # print(self.db_brick_info[lego_brick.db_id])
        # print(our_piece_new_info)

        # se verifica daca coordonata de start e valabila
        has_at_least_one_stud = False
        self_tubes = []
        for tube in our_piece_new_info[5]:
            aux_tube = [tube[0] + start_coordinates[0], tube[1] + start_coordinates[1], tube[2] + start_coordinates[2],
                        lego_brick.brick_id, 0]
            if start_coordinates[2] != 0:
                for _tube in self.occupied_studs[start_coordinates[2]]:
                    if aux_tube[0] == _tube[0] and aux_tube[1] == _tube[1] and aux_tube[2] == _tube[2] and _tube[4] == 0:
                        has_at_least_one_stud = True
            self_tubes.append(aux_tube)
        if not has_at_least_one_stud and start_coordinates[2] != 0:
            return False

        # calculeaza spatiile pe care le va ocupa piesa si daca sunt valabile
        all_spaces_to_occupy = []
        for height in range(start_coordinates[2], start_coordinates[2] + our_piece_new_info[2]):
            spaces_to_occupy = []
            for space in our_piece_new_info[3]:
                if space[2] == height - start_coordinates[2]:
                    spaces_to_occupy.append(
                        [space[0] + start_coordinates[0], space[1] + start_coordinates[1], height, lego_brick.brick_id])
            occupied_space = self.occupied_space.get(height)
            if occupied_space is None:
                self.occupied_space[height] = []
                occupied_space = []
            for space in spaces_to_occupy:
                for aux_space in occupied_space:
                    if space[0] == aux_space[0] and space[1] == aux_space[1] and space[2] == aux_space[2]:
                        return False
                else:
                    all_spaces_to_occupy.append(space)

        # daca s-a ajuns pana aici inseamna ca piesa va fi pusa
        lego_brick.rotation = rotation  # !!?
        self.lego_bricks[lego_brick.brick_id] = [self, True]
        for space in all_spaces_to_occupy:
            self.occupied_space[space[2]].append(space)
        for stud in our_piece_new_info[4]:
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
    def __init__(self, db_id, color, given_configuration):
        self.db_id = db_id
        self.brick_id = len(given_configuration.lego_bricks) + 1  # cheia pentru dictionarul _lego_bricks
        self.color = color

        # urmatoarele atribute sunt folosite atunci cand piesa este pusa in alta piesa
        self.rotation = 0  # 0 -> in dreapta, 1 -> in jos, 2 -> in stanga, 3 -> in sus

        given_configuration.lego_bricks[self.brick_id] = [self, False]


def initialize_lego_bricks_dict(given_configuration):
    file_json = './lego_piece_info.json'
    db_brick_info = dict()
    with open(file_json, 'rb') as data_file:
        import json
        data = json.load(data_file)
        for elm in data['piece-list']:
            db_brick_info[elm['id']] = [elm['length'], elm['width'], elm['height'],
                                        (elm['space']),
                                        (elm['studs']),
                                        (elm['tubes'])]
    given_configuration.db_brick_info = db_brick_info


if __name__ == '__main__':
    configuration = Configuration()
    initialize_lego_bricks_dict(configuration)

    print(configuration.place_in_studs(Brick(3020, "White", configuration), [0, 0, 0], rotation=0))
    print(configuration.place_in_studs(Brick(2420, "White", configuration), [0, 0, 1], rotation=1))
    print(configuration.place_in_studs(Brick(2420, "White", configuration), [0, 0, 2], rotation=2))
    print(configuration.place_in_studs(Brick(2420, "White", configuration), [0, 0, 3], rotation=3))
    print(configuration.place_in_studs(Brick(3020, "White", configuration), [0, 0, 4], rotation=2))
    print(configuration.place_in_studs(Brick(3020, "White", configuration), [0, 0, 5], rotation=3))

    for key, value in configuration.occupied_space.items():
        print(key, value)
    print("\n")
    for key, value in configuration.occupied_studs.items():
        print(key, value)
    print("\n")
    for key, value in configuration.occupied_tubes.items():
        print(key, value)
    # TODO: metoda place_in_tubes + folosit rotation + decrementat inaltimea de la tubes pentru toate piesele
