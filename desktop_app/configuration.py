import copy
import os
import re
from itertools import combinations, permutations, product
from pprint import pprint
ID_EXCEP = -1


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

    if rotation % 4 == 1:
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


def calculates_coordinates_starting_from_the_beginning(brick_db_info, start_coordinates, rotation):
    new_brick_info = rotate_our_coordinates(brick_db_info, rotation)
    for i in [3, 4, 5]:
        new_brick_info[i] = [(new_brick_info[i][j][0] + start_coordinates[0],
                              new_brick_info[i][j][1] + start_coordinates[1],
                              new_brick_info[i][j][2] + start_coordinates[2]) for j in range(len(new_brick_info[i]))]
    return new_brick_info


class Configuration:
    def __init__(self, interface=False):
        self.lego_bricks = dict()  # cheia va fi id-ul, valoarea va fi [obiect, is_used]; lista va contine toate piesele initializate
        self.occupied_space = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de spatiu + id piesa (a cui este)
        self.occupied_studs = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de studs + id piesa + id piesa care ocupa
        self.occupied_tubes = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de tubes + id piesa + id piesa care ocupa
        self.db_brick_info = dict()  # cheia va fi id-ul din bd, valoarea va fi o lista de 3 elemente (lungime, latime, inaltime) si 3 liste: spaces, studs, tubes
        self.image = "configurations\\placeholder.jpg"
        initialize_lego_bricks_dict(self, interface)

    def get_config_info(self):
        to_write = ""
        to_write += "lego_bricks\n"
        for key, value in self.lego_bricks.items():
            if value[1]:
                to_write += str(key) + ", " + str(value[0].db_id) + ", " + str(value[0].color) + "\n"
        to_write += "occupied_space\n"
        for key, value in self.occupied_space.items():
            if len(value) > 0:
                to_write += str(key) + ", "
                for val in value:
                    to_write += str(val) + ", "
                to_write = to_write[:-2]
                to_write += "\n"
        to_write += "occupied_studs\n"
        for key, value in self.occupied_studs.items():
            if len(value) > 0:
                to_write += str(key) + ", "
                for val in value:
                    to_write += str(val) + ", "
                to_write = to_write[:-2]
                to_write += "\n"
        to_write += "occupied_tubes\n"
        for key, value in self.occupied_tubes.items():
            if len(value) > 0:
                to_write += str(key) + ", "
                for val in value:
                    to_write += str(val) + ", "
                to_write = to_write[:-2]
                to_write += "\n"
        to_write += "image_path\n"
        image_path = repr(self.image)[:-1]
        image_path = image_path[1:]
        to_write += image_path + "\n"
        return to_write

    def save_configuration(self, file_name, interface=False):
        to_write = self.get_config_info()
        if interface:
            file_path = os.path.join("..\\configurations", file_name)
        else:
            file_path = os.path.join("configurations", file_name)
        file = open(file_path, "w+")
        file.write(to_write)
        file.close()
        return True

    def load_configuration(self, file_name):
        self.lego_bricks = dict()
        self.occupied_space = dict()
        self.occupied_studs = dict()
        self.occupied_tubes = dict()
        self.image = "configurations\\placeholder.jpg"
        file_path = os.path.join("configurations\\", file_name)
        file = open(file_path, "r")
        mode = 0
        r = r"\[.+?\]"
        for line in file.readlines():
            line = line[:-1]
            if line == "lego_bricks":
                mode = 1
            elif line == "occupied_space":
                mode = 2
            elif line == "occupied_studs":
                mode = 3
            elif line == "occupied_tubes":
                mode = 4
            elif line == "image_path":
                mode = 5
            elif mode == 1:
                info = line.split(", ")
                lego_brick = Brick(int(info[1]), info[2], self, int(info[0]))
                self.lego_bricks[int(info[0])][1] = True
            elif mode == 2:
                info = line.split(",")
                self.occupied_space[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    self.occupied_space[int(info[0])].append([int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3][:-1])])
            elif mode == 3:
                info = line.split(",")
                self.occupied_studs[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    aux = int(info2[4][:-1]) if int(info2[4][:-1]) != 0 else -1
                    self.occupied_studs[int(info[0])].append([int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3]), aux])
            elif mode == 4:
                info = line.split(",")
                self.occupied_tubes[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    aux = int(info2[4][:-1]) if int(info2[4][:-1]) != 0 else -1
                    self.occupied_tubes[int(info[0])].append([int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3]), aux])
            elif mode == 5:
                info = line.split("\\")
                self.image = os.path.join("configurations", info[2])

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

        our_piece_new_info = rotate_our_coordinates(self.db_brick_info[lego_brick.db_id], rotation)

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
        self.lego_bricks[lego_brick.brick_id] = [self.lego_bricks[lego_brick.brick_id][0], True]
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

    def get_studs_which_connects_tubes_for_piece(self, piece_info_in_space, id_piece, get_all_with_flag=0):
        studs_list = []
        for stud in piece_info_in_space[4]:
            found = False
            for tubes in self.occupied_tubes.values():
                for x, y, z, id1, id2 in tubes:
                    if stud[0] == x and stud[1] == y and stud[2] == z and (id2 == 0 or id1 == 0):
                        id_existent_piece = max(id1, id2)
                        studs_list.append([x, y, z, id_piece, id_existent_piece])
                        found = True
            if (not found) and get_all_with_flag == 1:
                studs_list.append([stud[0], stud[1], stud[2], id_piece, 0])
        return studs_list

    # validare
    def we_can_add_piece_to_existent_configuration(self, lego_brick, piece_info_in_space):
        if self.lego_bricks[lego_brick.brick_id][1]:
            return False

        number_of_studs_that_connects_a_tube = len(self.get_studs_which_connects_tubes_for_piece(piece_info_in_space, lego_brick.brick_id))
        if number_of_studs_that_connects_a_tube == 0:
            return False

        overlap_with_another_piece = False
        for occupied_position_list_for_level in self.occupied_space.values():
            for occupied_position in occupied_position_list_for_level:
                if (occupied_position[0], occupied_position[1], occupied_position[2]) in piece_info_in_space[3]:
                    overlap_with_another_piece = True
        if overlap_with_another_piece:
            return False
        return True

    # tranzitie
    def add_piece_to_existent_configuration(self, lego_brick, start_coordinates, piece_info_in_space):
        self.lego_bricks[lego_brick.brick_id] = [self.lego_bricks[lego_brick.brick_id][0], True]
        for space in piece_info_in_space[3]:
            self.occupied_space[space[2]].append([space[0], space[1], space[2], lego_brick.brick_id])

        # print(piece_info_in_space[5])
        for tube in piece_info_in_space[5]:
            if tube[2] not in self.occupied_tubes:
                self.occupied_tubes[tube[2]] = []
            self.occupied_tubes[tube[2]].append([tube[0], tube[1], tube[2], lego_brick.brick_id, 0])

        all_studs_with_connection_info = self.get_studs_which_connects_tubes_for_piece(piece_info_in_space, lego_brick.brick_id, 1)
        # print(all_studs_with_connection_info)
        for tube in self.occupied_tubes[piece_info_in_space[2] + start_coordinates[2]]:
            for stud in all_studs_with_connection_info:
                if stud[0] == tube[0] and stud[1] == tube[1] and stud[2] == tube[2]:
                    stud[4] = tube[3]
                    tube[4] = lego_brick.brick_id
        if start_coordinates[2] not in self.occupied_studs:
            self.occupied_studs[start_coordinates[2]] = []
        for stud in all_studs_with_connection_info:
            self.occupied_studs[stud[2]].append(stud)

    def place_in_tubes(self, lego_brick, start_coordinates, rotation=0):
        piece_info_in_space = calculates_coordinates_starting_from_the_beginning(self.db_brick_info[lego_brick.db_id], start_coordinates, rotation)
        if self.we_can_add_piece_to_existent_configuration(lego_brick, piece_info_in_space):
            self.add_piece_to_existent_configuration(lego_brick, start_coordinates, piece_info_in_space)
            return True
        return False

    # se va incerca scoaterea piesei date din configuratie, flag-urile si dictionarele updatandu-se corespunzator
    def remove_brick(self, config_id):
        if config_id not in self.lego_bricks.keys():
            return False
        if not self.lego_bricks[config_id][1]:
            return False
        in_tubes, in_studs = False, False
        for key, value in self.occupied_tubes.items():
            for tube in value:
                if tube[4] == config_id:
                    in_tubes = True
                    break
            if in_tubes:
                break
        for key, value in self.occupied_studs.items():
            for stud in value:
                if stud[4] == config_id:
                    in_studs = True
                    break
            if in_studs:
                break
        if in_tubes and in_studs:
            return False
        self.lego_bricks[config_id][1] = False
        occupied_tubes_copy = copy.deepcopy(self.occupied_tubes)
        for key, value in occupied_tubes_copy.items():
            for tube in value:
                if tube[3] == config_id:
                    self.occupied_tubes[key].remove(tube)
        for key, value in self.occupied_tubes.items():
            for tube in value:
                if tube[4] == config_id:
                    tube[4] = 0
        occupied_studs_copy = copy.deepcopy(self.occupied_studs)
        for key, value in occupied_studs_copy.items():
            for stud in value:
                if stud[3] == config_id:
                    self.occupied_studs[key].remove(stud)
        for key, value in self.occupied_studs.items():
            for stud in value:
                if stud[4] == config_id:
                    stud[4] = 0
        occupied_space_copy = copy.deepcopy(self.occupied_space)
        for key, value in occupied_space_copy.items():
            for space in value:
                if space[3] == config_id:
                    self.occupied_space[key].remove(space)
        return True

    def we_can_put_piece(self, piece_info_in_space):
        for coord_space in piece_info_in_space[3]:
            h = coord_space[2]
            if h in self.occupied_space:
                if [coord_space[0], coord_space[1], coord_space[2], ID_EXCEP] not in self.occupied_space[h]:
                    return False
            else:
                return False

        for coord_stud in piece_info_in_space[4]:
            h = coord_stud[2]
            if h in self.occupied_studs:
                if [coord_stud[0], coord_stud[1], coord_stud[2], ID_EXCEP, ID_EXCEP] not in self.occupied_studs[h]:
                    return False
            else:
                return False

        for coord_tube in piece_info_in_space[5]:
            h = coord_tube[2]
            if h in self.occupied_tubes:
                if [coord_tube[0], coord_tube[1], coord_tube[2], ID_EXCEP, ID_EXCEP] not in self.occupied_tubes[h]:
                    return False
            else:
                return False

        return True

    def get_neighbour_stud_id_for_given_tube(self, tube_coord):
        h = tube_coord[2]
        if len(self.occupied_studs[h]) < 1:
            return ID_EXCEP
        for coords in self.occupied_studs[h]:
            if coords[0] == tube_coord[0] and coords[1] == tube_coord[1] and coords[2] == tube_coord[2]:
                return coords[3]
        return ID_EXCEP

    def get_neighbour_tube_id_for_given_stud(self, stud_coord):
        h = stud_coord[2]
        if h in self.occupied_tubes:
            for coords in self.occupied_tubes[h]:
                if coords[0] == stud_coord[0] and coords[1] == stud_coord[1] and coords[2] == stud_coord[2]:
                    return coords[3]
        return ID_EXCEP

    def replace(self, db_brick_id, place):
        start_coordinates = [place[0], place[1], place[2]]
        rotation = place[3]
        piece_info_in_space = calculates_coordinates_starting_from_the_beginning(self.db_brick_info[db_brick_id], start_coordinates, rotation)
        my_brick = Brick(db_brick_id, "alb", self)
        my_brick_id = my_brick.brick_id

        if self.we_can_put_piece(piece_info_in_space):
            for coord_space in piece_info_in_space[3]:
                h = coord_space[2]
                loc = self.occupied_space[h].index([coord_space[0], coord_space[1], coord_space[2], ID_EXCEP])
                self.occupied_space[h].remove([coord_space[0], coord_space[1], coord_space[2], ID_EXCEP])
                self.occupied_space[h].insert(loc, [coord_space[0], coord_space[1], coord_space[2], my_brick_id])

            for coord_stud in piece_info_in_space[4]:
                h = coord_stud[2]
                to_remove = [coord_stud[0], coord_stud[1], coord_stud[2], ID_EXCEP, ID_EXCEP]
                loc = self.occupied_studs[h].index(to_remove)
                self.occupied_studs[h].remove(to_remove)
                id_brick_neighbour = self.get_neighbour_tube_id_for_given_stud(coord_stud)
                to_remove[3] = my_brick_id
                to_remove[4] = id_brick_neighbour
                self.occupied_studs[h].insert(loc, to_remove)

                # punem si la vecin in tub informatia despre studul conectat
                coord_tube = coord_stud
                if id_brick_neighbour != ID_EXCEP and [coord_tube[0], coord_tube[1], coord_tube[2], id_brick_neighbour, ID_EXCEP] in self.occupied_tubes[h]:
                    to_remove = [coord_tube[0], coord_tube[1], coord_tube[2], id_brick_neighbour, ID_EXCEP]
                    loc = self.occupied_tubes[h].index(to_remove)
                    self.occupied_tubes[h].remove(to_remove)
                    to_remove[4] = my_brick_id
                    self.occupied_tubes[h].insert(loc, to_remove)

            for coord_tube in piece_info_in_space[5]:
                h = coord_tube[2]
                to_remove = [coord_tube[0], coord_tube[1], coord_tube[2], ID_EXCEP, ID_EXCEP]
                loc = self.occupied_tubes[h].index(to_remove)
                self.occupied_tubes[h].remove(to_remove)
                id_brick_neighbour = self.get_neighbour_stud_id_for_given_tube(coord_tube)
                to_remove[3] = my_brick_id
                to_remove[4] = id_brick_neighbour
                self.occupied_tubes[h].insert(loc, to_remove)

                # punem si la vecin in stud informatia despre tubul conectat
                coord_stud = coord_tube
                if id_brick_neighbour != ID_EXCEP and [coord_stud[0], coord_stud[1], coord_stud[2], id_brick_neighbour, ID_EXCEP] in self.occupied_studs[h]:
                    to_remove = [coord_stud[0], coord_stud[1], coord_stud[2], id_brick_neighbour, ID_EXCEP]
                    loc = self.occupied_studs[h].index(to_remove)
                    self.occupied_studs[h].remove(to_remove)
                    to_remove[4] = my_brick_id
                    self.occupied_studs[h].insert(loc, to_remove)
        else:
            print("Replace error", db_brick_id, start_coordinates)
        return self

    def sort_conf(self):
        self.occupied_space = get_coordinates_from_dict(self.occupied_space)
        self.occupied_studs = get_coordinates_from_dict(self.occupied_studs)
        self.occupied_tubes = get_coordinates_from_dict(self.occupied_tubes)
        return conf

    def stare_finala(self, disponible_pieces):
        if len(disponible_pieces) == 0:
            return True
        return False

def get_coordinates_from_dict(my_dict):
    li = []
    for key, value in my_dict.items():
        for elm in value:
            li.append(elm[:3])
    return sorted(li, key=lambda tup: (tup[0], tup[1], tup[2]), reverse=False)


class Brick:
    def __init__(self, db_id, color, given_configuration, dict_value=-1):
        self.db_id = db_id
        self.color = color

        if given_configuration is not None:
            if dict_value == -1:
                self.brick_id = len(given_configuration.lego_bricks) + 1  # cheia pentru dictionarul _lego_bricks
            else:
                self.brick_id = dict_value
            given_configuration.lego_bricks[self.brick_id] = [self, False]


def initialize_lego_bricks_dict(given_configuration, interface=False):
    if interface:
        file_json = '../lego_piece_info.json'
    else:
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


def verificare(configuration):
    print("******************BRICKS*********************")
    for key, value in configuration.lego_bricks.items():
        print(key, value)
    print("******************SPACE**********************")
    for key, value in configuration.occupied_space.items():
        print(key, value)
    print("******************STUDS**********************")
    for key, value in configuration.occupied_studs.items():
        print(key, value)
    print("******************TUBES**********************")
    for key, value in configuration.occupied_tubes.items():
        print(key, value)


def get_all_places_where_you_can_put_piece(given_config, id_from_db):
    result_list = []
    for key, value in given_config.occupied_space.items():
        for coordinates in value:
            start_coordinates = [coordinates[0], coordinates[1], coordinates[2]]
            for rotation in range(0, 4):
                piece_info_in_space = calculates_coordinates_starting_from_the_beginning(
                  given_config.db_brick_info[id_from_db], start_coordinates, rotation)
                if given_config.we_can_put_piece(piece_info_in_space):
                    result_list.append((coordinates[0], coordinates[1], coordinates[2], rotation))
    return result_list


def remove_piece_from_disponible_pieces(disponible_pieces, piece_id_to_remove):
    for count, piece in enumerate(disponible_pieces):
        if piece[0] == piece_id_to_remove:
            if disponible_pieces[count][1] == 0:
                disponible_pieces.remove(piece)
                return disponible_pieces

            disponible_pieces[count][1] -= 1
            if disponible_pieces[count][1] == 0:
                disponible_pieces.remove(piece)
            return disponible_pieces
    return disponible_pieces


def volume(configuration, chosen_pieces):
    input_volume = 0
    for db_brick_id, nr_of_pieces in chosen_pieces:
        brick_info = configuration.db_brick_info[db_brick_id]
        input_volume += nr_of_pieces * brick_info[0] * brick_info[1] * brick_info[2]
    return input_volume


def volume_conf(configuration):
    configuration_volume = 0
    for values in configuration.occupied_space.values():
        configuration_volume += len(values)
    return configuration_volume


def bkt(actual_config, disponible_pieces):
    for piece in disponible_pieces:
        places = get_all_places_where_you_can_put_piece(actual_config, piece[0])
        for place in places:
            piece_info_in_space = calculates_coordinates_starting_from_the_beginning(actual_config.db_brick_info[piece[0]], [place[0], place[1], place[2]], place[3])
            if actual_config.we_can_put_piece(piece_info_in_space):
                aux_conf = actual_config.replace(piece[0], place)
                aux_disponible_pieces = remove_piece_from_disponible_pieces(copy.deepcopy(disponible_pieces), piece[0])
                if aux_conf.stare_finala(aux_disponible_pieces):
                    print("Yes, we can")
                    return True
                    return
                else:
                    bkt(aux_conf, aux_disponible_pieces)
    return False


def get_all_plausible_combinations_of_pieces(configuration, disponible_pices):
    posli = [list(range(x[1]+1)) for x in disponible_pices]
    possible_combinations = product(*posli)
    expected_volume = volume_conf(configuration)

    good_combination = []
    for combination in possible_combinations:
        pieces = [[brick_id, combination[i]] for i, [brick_id, _] in enumerate(disponible_pices) if combination[i] > 0]
        if volume(configuration, pieces) == expected_volume:
            good_combination.append(pieces)
    # si tot in functia asta am putea verifica daca avem piese speciale ce acopera posibilele cazuri speciale
    return good_combination


def verify_if_we_can_build(configuration, disponible_pices):
    good_combination = get_all_plausible_combinations_of_pieces(configuration, disponible_pices)
    for pieces in good_combination:
        print("Verificam combinatia de piese", pieces, sep=" : ")
        configuration_aux = init_conf_with_placeholders(configuration)
        flag = bkt(init_conf_with_placeholders(configuration_aux), pieces)
        print(flag)
        if flag:
            return True
    return False


def verify_if_we_can_build_with_exactly_given_pieces(configuration, disponible_pices):
    if volume(configuration, disponible_pices) == volume_conf(configuration):
        if bkt(configuration, disponible_pices):
            return True
    return False


# o configuratie exemplu
def config1_pieces1():
    configuration = Configuration()
    configuration.place_in_studs(Brick(3010, "White", configuration), [0, 0, 0], rotation=1)
    configuration.place_in_studs(Brick(3010, "White", configuration), [0, 0, 3], rotation=1)
    configuration.place_in_studs(Brick(3020, "White", configuration), [0, 0, 6], rotation=0)
    # print(configuration.place_in_tubes(Brick(3010, "White", configuration), [0, 0, 3], rotation=1))
    configuration.place_in_tubes(Brick(3010, "White", configuration), [0, 3, 3], rotation=1)
    configuration.place_in_tubes(Brick(3003, "White", configuration), [3, 3, 0], rotation=0)
    configuration.place_in_studs(Brick(3003, "White", configuration), [3, 5, 0], rotation=0)
    # print(configuration.place_in_studs(Brick(4490, "White", configuration), [0, 4, 0], rotation=0))
    print("Configuratie creata cu succes")
    return configuration


def init_conf_with_placeholders(configuration):
    conf_init = copy.deepcopy(configuration)
    conf_init.lego_bricks = dict()

    for h, value in conf_init.occupied_studs.items():
        conf_init.occupied_studs[h] = [[x, y, z, ID_EXCEP, ID_EXCEP] for x, y, z, _, not_visible in value]
    for h, value in conf_init.occupied_tubes.items():
        conf_init.occupied_tubes[h] = [[x, y, z, ID_EXCEP, ID_EXCEP] for x, y, z, _, _ in value]

    for h, value in conf_init.occupied_space.items():
        conf_init.occupied_space[h] = []
        for x, y, z, _ in value:
            conf_init.occupied_space[h].append([x, y, z, ID_EXCEP])
            if h + 1 in conf_init.occupied_studs:
                if [x, y, z+1, ID_EXCEP, ID_EXCEP] not in conf_init.occupied_studs[h+1]:
                    conf_init.occupied_studs[h + 1].append([x, y, z+1, ID_EXCEP, ID_EXCEP])
            else:
                conf_init.occupied_studs[h + 1] = [[x, y, z+1, ID_EXCEP, ID_EXCEP]]

            if h in conf_init.occupied_tubes:
                if [x, y, z, ID_EXCEP, ID_EXCEP] not in conf_init.occupied_tubes[h]:
                    conf_init.occupied_tubes[h].append([x, y, z, ID_EXCEP, ID_EXCEP])
            else:
                conf_init.occupied_tubes[h] = [[x, y, z, ID_EXCEP, ID_EXCEP]]

    return conf_init


if __name__ == '__main__':
    conf = config1_pieces1()
    disp_pices = [[3005, 20], [3020, 1], [3003, 4], [3010, 3], [3020, 1]]
    print("We can build", verify_if_we_can_build(conf, disp_pices), sep=" : ")
    print("We can build with all the pieces received", verify_if_we_can_build_with_exactly_given_pieces(conf, disp_pices), sep=" : ")
