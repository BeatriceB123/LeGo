import copy
import os
import re


# urmatoarele 3 functii sunt folosite pentru a roti o coordonatele date in li_coord in jurul originii
# rotatia se face in sensul acelor de ceasornic
# numarul de la rotatie reprezinta numarul de cadrane cu care se roteste.
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


# functia rotate_our_coordinates primeste informatiile despre o piesa
# si returneaza noile informatii pentru piesa rotita
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


# primeste informatiile din json despre o piesa, coordonata stanga-jos in care e asezata si gradul de rotatie(0, 1, 2, 3)
# si returneaza informatiile in spatiu cu privire la piesa (width, length, h, space, studs, tubes)
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
        self.occupied_space = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de spatiu(x, y, z) + id piesa (a cui este) + flag (pt bkt)
        self.occupied_studs = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de studs + id piesa + id piesa care ocupa + flag (pt bkt)
        self.occupied_tubes = dict()  # cheia va fi inaltimea, valoarea va fi lista cu coordonate de tubes + id piesa + id piesa care ocupa + flag (pt bkt)
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
                lego_brick = Brick(int(info[1]), info[2], self)
                self.lego_bricks[int(info[0])][1] = True
            elif mode == 2:
                info = line.split(",")
                self.occupied_space[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    self.occupied_space[int(info[0])].append(
                        [int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3][:-1])])
            elif mode == 3:
                info = line.split(",")
                self.occupied_studs[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    self.occupied_studs[int(info[0])].append(
                        [int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3]), int(info2[4][:-1])])
            elif mode == 4:
                info = line.split(",")
                self.occupied_tubes[int(info[0])] = []
                res = re.findall(r, line)
                for result in res:
                    info2 = result.split(", ")
                    self.occupied_tubes[int(info[0])].append(
                        [int(info2[0][1:]), int(info2[1]), int(info2[2]), int(info2[3]), int(info2[4][:-1])])
            elif mode == 5:
                info = line.split("\\")
                self.image = os.path.join("configurations", info[2])

    # functia asta e facuta de Tiberiu
    # pune obiectul peste alte obiecte (in studs)
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
                    if aux_tube[0] == _tube[0] and aux_tube[1] == _tube[1] and aux_tube[2] == _tube[2] and _tube[ 4] == 0:
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

    # primeste informatiile in spatiu cu privire la o piesa
    # si returneaza o lista cu studurile(adica cele de sus) din piesa data ce ar putea intra in tuburile prezente in configuratie (adica self)
    # REV!! flagul este 0 daca vrem toata lista de studs
    def get_piece_studs_which_connects_existent_tubes(self, piece_info_in_space, id_piece=-1, get_all_with_flag=0):
        studs_list = []
        # parcurgem stud-urile din piesa
        for stud in piece_info_in_space[4]:
            found = False
            # si pentru ficare tub din configuratie
            for tubes in self.occupied_tubes.values():
                for x, y, z, id1, id2 in tubes:
                    # verificam daca studul si tubul vor fi la aceeasi coordonata
                    # si tubul este liber (id = 0) (pentru ca  daca nu e 0, inseamnca ca o alta piesa are un stud in acel tub)
                    if stud[0] == x and stud[1] == y and stud[2] == z and (id2 == 0 or id1 == 0):
                        id_existent_piece = max(id1, id2)
                        studs_list.append([x, y, z, id_piece, id_existent_piece])
                        found = True
            if (not found) and get_all_with_flag == 1:
                studs_list.append([stud[0], stud[1], stud[2], id_piece, 0])
        return studs_list

    # primeste informatiile in spatiu cu privire la o piesa
    # si returneaza o lista cu tuburile(adica cele de jos) din piesa data in care pot intra studsurile prezente in configuratie (adica self)
    # TODOdef get_piece_tubes_which_connects_existent_studs(self, piece_info_in_space, id_piece=-1, get_all_with_flag=0):

    # validare (verificam daca se poate adauga piesa in tuburi)
    def we_can_add_piece_to_existent_configuration_in_tubes(self, lego_brick, piece_info_in_space):
        # daca piesa a fost deja folosita in configuratie
        if self.lego_bricks[lego_brick.brick_id][1]:
            return False

        # daca nu exista macar un tub de care sa se lege piesa, inseamnca ca nu o putem adauga la configuratie
        number_of_studs_that_connects_a_tube = len(self.get_piece_studs_which_connects_existent_tubes(piece_info_in_space, lego_brick.brick_id, 0))
        if number_of_studs_that_connects_a_tube == 0:
            return False

        # verificam sa nu se suprapuna coordonatele ei cu ale altei piese existe in configuratie
        overlap_with_another_piece = False
        for occupied_position_list_for_level in self.occupied_space.values():
            for occupied_position in occupied_position_list_for_level:
                if (occupied_position[0], occupied_position[1], occupied_position[2]) in piece_info_in_space[3]:
                    overlap_with_another_piece = True
        if overlap_with_another_piece:
            return False
        return True

    # tranzitie (adaugarea efectiva a piesei noastre in tuburi)
    def add_piece_to_existent_configuration_in_tubes(self, lego_brick, start_coordinates, piece_info_in_space):
        # se actualizeaza dict self.lego_bricks astfel: marcam cu true faptul ca piesa noastra este pusa
        self.lego_bricks[lego_brick.brick_id] = [self.lego_bricks[lego_brick.brick_id][0], True]

        # se actualizeaza dict occupied_space astfel:  adaugam in dictionarul de spatii ocupate spatiile pe care le ocupa piesa noastra in spatiu
        for space in piece_info_in_space[3]:
            self.occupied_space[space[2]].append([space[0], space[1], space[2], lego_brick.brick_id])

        # se actualizeaza dict occupied_tubes astfel: adaugam tuburile din piesa noastra in dictionarul de tuburi (al doilea id e 0 pentru ca nu e nimic pus in acel tub)
        # in cazul in care e prima piesa ce are tuburi la acea inaltimea, deci in dictionar nu exista cheia tube[2], cream o noua lista [] pentru toate tuburile ce vor fi la aceasta inaltime
        for tube in piece_info_in_space[5]:
            if tube[2] not in self.occupied_tubes:
                self.occupied_tubes[tube[2]] = []
            self.occupied_tubes[tube[2]].append([tube[0], tube[1], tube[2], lego_brick.brick_id, 0])

        # se actualizeaza dict occupied_tubes astfel:
        # se creeaza o lista cu toate studurile din piesa noastra (indiferent daca se leaga de un tub sau nu)
        all_studs_with_connection_info = self.get_piece_studs_which_connects_existent_tubes(piece_info_in_space, lego_brick.brick_id, 1)

        # inaltimea unui tub ce s-ar putea uni cu un stud al piesei noastre este
        # inaltimea la care e pozitionata piesa in cadrul configuratiei (adica piece_info_in_space[2]), la care se adauga inaltimea piesei (adica start_coordinates[2])
        for tube in self.occupied_tubes[piece_info_in_space[2] + start_coordinates[2]]:
            for stud in all_studs_with_connection_info:
                # daca vom gasi un stud al piesei la aceleasi coordonate cu un tub existent, inseamnca ca cele doua se unesc, si marcam asta in dictionar
                # studul piesei adaugate va avea id2 = id-ul piesei de deasupra ei
                # tubul piesei de sus va avea id2 = brick_id(id unic al piesei puse)
                if stud[0] == tube[0] and stud[1] == tube[1] and stud[2] == tube[2]:
                    stud[4] = tube[3]
                    tube[4] = lego_brick.brick_id

        # se termina actualizarea la studs:
        if start_coordinates[2] not in self.occupied_studs:
            self.occupied_studs[start_coordinates[2]] = []
        for stud in all_studs_with_connection_info:
            self.occupied_studs[stud[2]].append(stud)

    # e o functie care sa demnstreze functionalitatea celor scrise mai sus,
    # si care sa aiba aceeasi signatura ca place_in_studs.
    def place_in_tubes(self, lego_brick, start_coordinates, rotation=0):
        piece_info_in_space = calculates_coordinates_starting_from_the_beginning(self.db_brick_info[lego_brick.db_id],
                                                                                 start_coordinates, rotation)
        if self.we_can_add_piece_to_existent_configuration_in_tubes(lego_brick, piece_info_in_space):
            self.add_piece_to_existent_configuration_in_tubes(lego_brick, start_coordinates, piece_info_in_space)
            return True
        return False

    # se va incerca scoaterea piesei date din configuratie, flag-urile si dictionarele updatandu-se corespunzator
    # piesa este data prin id-ul din configuratie
    def remove_brick_tiberiu(self, config_id):
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

    # se executa actiunea de scoatere a piesei din configuratie.
    # piesa este data print lista de coordonate pa care le ocupa -> nu se poate scoate din dictionarul lego_bricks
    # REV - sa se soata si din a doua coordonata de studs / tubes de la alte piese
    def remove_brick(self, piece_info_in_space, id_piesa=-1):
        # scoatem coordonatele din dictionare
        # daca flagul e setat, inseamna ca avem o piese -> scoatem si dictionar / piesele vecine

        if id_piesa != -1:
            self.remove_brick_tiberiu(id_piesa)
            return

        # daca flagul nu e setat, inseamnca ca scoatem doar volumnul dat din cele 3 dictionare.

        # print(piece_info_in_space)
        # print(get_coordinates_from_dict(self.occupied_space))
        for space in piece_info_in_space[3]:
            self.occupied_space[space[2]] = [[x, y, z, pid] for x, y, z, pid in self.occupied_space[space[2]]
                                             if x != space[0] or y != space[1] or z != space[2]]
        # print(get_coordinates_from_dict(self.occupied_space))
        # print(get_coordinates_from_dict(self.occupied_studs))
        for studs in piece_info_in_space[4]:
            self.occupied_studs[studs[2]] = [[x, y, z, pid1, pid2] for x, y, z, pid1, pid2 in
                                             self.occupied_studs[studs[2]]
                                             if x != studs[0] or y != studs[1] or z != studs[2]]
        # print(get_coordinates_from_dict(self.occupied_studs))
        # print(get_coordinates_from_dict(self.occupied_tubes))
        for tubes in piece_info_in_space[5]:
            self.occupied_tubes[tubes[2]] = [[x, y, z, pid1, pid2] for x, y, z, pid1, pid2 in
                                             self.occupied_tubes[tubes[2]]
                                             if x != tubes[0] or y != tubes[1] or z != tubes[2]]
        # verificare(self)

    def we_can_remove_brick(self, piece_info_in_space):
        # vedem daca se suprapune exact cu un volum existent
        # adica orice spatiu/tub/stud din piesa noastra, trebuie sa existe in configuratie fix la coordonatele in spatiu ale piesei
        print("See if we can remove brick", piece_info_in_space[3], sep=": ")
        for space in piece_info_in_space[3]:
            x = space[0]
            y = space[1]
            z = space[2]
            it_is = False
            if z in self.occupied_space:
                for xx, yy, zz, _ in self.occupied_space[z]:
                    if xx == x and yy == y and zz == z:
                        it_is = True
            if not it_is:
                return False
        for stud in piece_info_in_space[4]:
            x = stud[0]
            y = stud[1]
            z = stud[2]
            it_is = False
            if z in self.occupied_studs:
                for xx, yy, zz, _, _ in self.occupied_studs[z]:
                    if xx == x and yy == y and zz == z:
                        it_is = True
            if not it_is:
                return False
        for tube in piece_info_in_space[5]:
            x = tube[0]
            y = tube[1]
            z = tube[2]
            it_is = False
            if z in self.occupied_tubes:
                for xx, yy, zz, _, _ in self.occupied_tubes[z]:
                    if xx == x and yy == y and zz == z:
                        it_is = True
            if not it_is:
                return False
        return True


class Brick:
    def __init__(self, db_id, color, given_configuration):
        self.db_id = db_id
        self.color = color

        if given_configuration is not None:
            self.brick_id = len(given_configuration.lego_bricks)  # cheia pentru dictionarul _lego_bricks
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
        if value[1]:
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


# configuratia nula de la care se porneste construirea
def config0():
    configuration = Configuration()
    # print(configuration.place_in_studs(Brick(3005, "White", configuration), [0, 0, 0], rotation=0))
    # print(configuration.place_in_studs(Brick(3010, "White", configuration), [0, 0, 0], rotation=1))
    return configuration


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

# inca o configuratie exemplu - care e apoape la fel
def config1_pieces2():
    configuration = Configuration()
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [0, 0, 0], rotation=0))
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [1, 0, 0], rotation=0))
    print(configuration.place_in_studs(Brick(3004, "White", configuration), [2, 0, 0], rotation=1))
    print(configuration.place_in_studs(Brick(3004, "White", configuration), [0, 0, 3], rotation=1))
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [2, 0, 3], rotation=0))
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [3, 0, 3], rotation=0))

    print(configuration.place_in_studs(Brick(3710, "White", configuration), [0, 0, 6], rotation=0))
    print(configuration.place_in_studs(Brick(3710, "White", configuration), [1, 0, 6], rotation=0))

    print(configuration.place_in_tubes(Brick(3010, "White", configuration), [0, 3, 3], rotation=1))

    print(configuration.place_in_tubes(Brick(2357, "White", configuration), [3, 3, 0], rotation=3))
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [4, 4, 0], rotation=0))
    print(configuration.place_in_studs(Brick(2357, "White", configuration), [3, 5, 0], rotation=0))
    print(configuration.place_in_studs(Brick(3005, "White", configuration), [4, 5, 0], rotation=0))
    # print(configuration.place_in_studs(Brick(4490, "White", configuration), [0, 4, 0], rotation=0))
    # piece_info_in_space = calculates_coordinates_starting_from_the_beginning(configuration.db_brick_info[2357], [3, 5, 0], 0)
    # print(configuration.we_can_remove_brick(piece_info_in_space))
    # print(configuration.remove_brick(piece_info_in_space))

    piece_info_in_space = calculates_coordinates_starting_from_the_beginning(configuration.db_brick_info[3010],
                                                                             [0, 3, 3], 1)
    print(configuration.we_can_remove_brick(piece_info_in_space))
    print(configuration.remove_brick(piece_info_in_space))
    print("Configuratie creata cu succes")
    return configuration

# verifica daca doua dictionare ce elemente de tipul cheie:valoare(valoare fiind o lista neordonata) sunt la fel
# adica au aceleasi elemente, dar in ordine diferita
def the_same_dict_coordinates_maybe_faster(dict1, dict2):
    aux_li_occupied = []
    for key, value in dict1.items():
        for elm in value:
            print(elm)
            aux_li_occupied.append(elm[:3])
    for key, value in dict2.items():
        for elm in value:
            if elm[:3] in aux_li_occupied:
                aux_li_occupied.remove(elm[:3])
            else:
                return False
    if len(aux_li_occupied) > 0:
        return False
    return True

# returneaza lista ce contine doar primele trei valoari din listele ce apar ca si valori in dictionar
# sortata de jos in sus, de la stanga la dreapta
def get_coordinates_from_dict(my_dict):
    li = []
    for key, value in my_dict.items():
        for elm in value:
            li.append(elm[:3])
    print(li)
    return sorted(li, key=lambda tup: (tup[2], tup[0], tup[1]), reverse=False)
    # return sorted(li, key=lambda tup: (tup[0], tup[1], tup[2]), reverse=False)


# verifica daca doua configuratii sunt la fel (adica cele 3 dictionare au aceleasi coordonate, chiar daca sunt puse diferit piesele)
def the_same_config(config1, config2):
    print("Called the_same_config")
    return get_coordinates_from_dict(config1.occupied_space) == get_coordinates_from_dict(config2.occupied_space) \
           and get_coordinates_from_dict(config1.occupied_studs) == get_coordinates_from_dict(config2.occupied_studs) \
           and get_coordinates_from_dict(config1.occupied_tubes) == get_coordinates_from_dict(config2.occupied_tubes)

    # return the_same_dict_coordinates_maybe_faster(config1.occupied_space, config2.occupied_space) \
    #        and the_same_dict_coordinates_maybe_faster(config1.occupied_studs, config2.occupied_studs) \
    #        and the_same_dict_coordinates_maybe_faster(config1.occupied_tubes, config2.occupied_tubes)


# returneaza o lista cu piese pentru verificarea bkt-ului,
# astea ar trebui luate din interfata/ de la user automat
def get_the_pieces_selected_by_the_user():
    # id, numar
    # user_pieces = [[3003, 2], [2357, 2], [3004, 4], [3005, 6], [3010, 1], [4490, 1]]
    user_pieces = [[3003, 2], [3010, 3], [3020, 2]]
    return user_pieces


# sunt piese care oricum nu pot fi compuse din altele si nici nu ajuta la compunere; pe ele le eliminam din start din configuratia noastra
def eliminate_special_pieces_from_config(config, disponible_pieces):
    li_id_for_special_pieces_global = [4286, 2431, 4490]  # DE COMPLETAT - VA FI O VARIABILA GLOBALA cu piese de acest tip
    we_have_enough_special_pieces = True

    for key, brick in config.lego_bricks.items():
        used_brick_id = brick[0].db_id
        if used_brick_id in li_id_for_special_pieces_global:
            disponible_pieces, we_can_remove_piece = remove_piece_from_pieces_list(disponible_pieces, used_brick_id)
            if we_can_remove_piece:
                config.remove_brick(used_brick_id)
            else:
                we_have_enough_special_pieces = False
    return config, disponible_pieces, we_have_enough_special_pieces

# compara cele doua configuratii, si returneaza cea mai de jos si din stanga piesa ce lipseste din configuratia partiala
# none daca nu lipseste nimic.
def get_next_unassigned_coord(partial_config, complete_config):
    partial_config_occupied_spaces = get_coordinates_from_dict(partial_config.occupied_space)
    complete_config_occupied_spaces = get_coordinates_from_dict(complete_config.occupied_space)
    # print(partial_config_occupied_spaces)
    # print(complete_config_occupied_spaces)
    for coord in complete_config_occupied_spaces:
        if coord not in partial_config_occupied_spaces:
            return coord
    return None

# elimina o piesa din lista de piese
def remove_piece_from_pieces_list(pieces_list, piece_id_to_remove):
    pieces_list_aux = pieces_list.copy()
    for piece_id, pieces_count in pieces_list_aux:
        if piece_id == piece_id_to_remove:
            pieces_count -= 1
            if pieces_count < 0:
                return pieces_list, False
            return pieces_list_aux, True
    return pieces_list, False

# adauga o piesa in lista de piese
def add_piece_to_pieces_list(pieces_list, piece_id_to_add):
    pieces_list_aux = pieces_list.copy()
    for piece_id, pieces_count in pieces_list_aux:
        if piece_id == piece_id_to_add:
            pieces_count += 1
            return pieces_list_aux
    pieces_list_aux.append([piece_id_to_add, 1])
    return pieces_list_aux


good_conf = []


# REV - scoaterea pieselor suspendate
# user_pieces = [[3003, 2], [3010, 3], [3020, 2]]
def backtracking(builded_config, target_config, disponible_pieces):
    # pasul din bkt va fi definit ca prima pozitie din stanga jos ce nu a fost acoperita
    step = get_next_unassigned_coord(builded_config, target_config)
    if not step:
        return builded_config
    print("Step", step, sep=": ")
    for disponible_piece_id, number_of_disponible_pieces in disponible_pieces:
        possible_rotations_for_piece = [0, 1, 2,
                                        3]  # la unele piese vor fi mai putine rotatii, REV, se poate reduce de 4 ori complexitatea
        for rotation in possible_rotations_for_piece:
            aux = builded_config.db_brick_info[disponible_piece_id]
            piece_info_in_space = calculates_coordinates_starting_from_the_beginning(aux, step, rotation)

            # validare
            aux_lego_brick = Brick(disponible_piece_id, "culoare", builded_config)
            if target_config.we_can_remove_brick(piece_info_in_space):
                # if builded_config.we_can_add_piece_to_existent_configuration(aux_lego_brick, piece_info_in_space):
                print("!!!Validare trecuta")
                print("Actual piece info simple", disponible_piece_id, aux, sep=": ")
                print("Actual piece info in space", piece_info_in_space, sep=": ")

                builded_config.place_in_studs(aux_lego_brick, step, rotation)
                target_config.remove_brick(piece_info_in_space)
                disponible_pieces, _ = remove_piece_from_pieces_list(disponible_pieces, disponible_piece_id)
                # solutie
                # if the_same_config(builded_config, target_config):
                # if not get_next_unassigned_coord(builded_config, target_config):

                if the_same_config(builded_config, config1_pieces1()):
                    print(
                        "SOLUTIA EXISTA SI TOCMAI AM GASIT-O SI O AFISEZ. DE CE NU VREI SA O RETURNEZI!?!?!??!awDASFAF")
                    print(verificare(builded_config))
                    good_conf.append(builded_config)
                    return True, builded_config
                else:
                    backtracking(builded_config, target_config, disponible_pieces)

                piesa_noua = Brick(disponible_piece_id, "culoare", target_config)
                target_config.place_in_studs(piesa_noua, step, rotation)
                builded_config.remove_brick(piece_info_in_space)
                disponible_pieces = add_piece_to_pieces_list(disponible_pieces, disponible_piece_id)
    return False, None


def get_all_configurations_that_we_can_do():
    configurations_to_verify = [config1_pieces1()]  # si aici trebuie inlocuit cu ce se da din interfata
    indices_for_configurations_that_we_can_do = []

    for config_index, config in enumerate(configurations_to_verify):
        disponible_pieces = get_the_pieces_selected_by_the_user()
        config, disponible_pieces, we_have_special_pieces = eliminate_special_pieces_from_config(config,
                                                                                                 disponible_pieces)
        empty_config = config0()
        if True:
            if backtracking(empty_config, config, disponible_pieces):
                indices_for_configurations_that_we_can_do.append(config_index)
    return indices_for_configurations_that_we_can_do


def comparare_vizuala_config(config1, config2):
    print("Comparare vizuala")
    print(get_coordinates_from_dict(config1.occupied_space))
    print(get_coordinates_from_dict(config2.occupied_space))
    print(get_coordinates_from_dict(config1.occupied_studs))
    print(get_coordinates_from_dict(config2.occupied_studs))
    print(get_coordinates_from_dict(config1.occupied_tubes))
    print(get_coordinates_from_dict(config2.occupied_tubes))


if __name__ == '__main__':
    configuration1 = config1_pieces1()
    # configuration2 = config1_pieces2()
    # print("Is the same ?", the_same_config(configuration1, configuration2))

    dp = get_the_pieces_selected_by_the_user()
    ec = config0()
    se_poate_construi, config = backtracking(ec, configuration1, dp)

    if se_poate_construi:
        print("Comparare rezultate")
        print(comparare_vizuala_config(config1_pieces1(), config))
    else:
        print("Nu a putut construi")

    if len(good_conf) > 0:
        print("Ba se poate")
        config_initiala_era = config1_pieces1()  # Masajul pe care il returneaza e Configuratie creata cu succes
        comparare_vizuala_config(config_initiala_era, good_conf[0])
