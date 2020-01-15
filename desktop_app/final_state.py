import sys
from configuration import *
sys.path.append("..")


def is_final_state(configuration: Configuration, piece_list_tuple: list):
    # for i in piece_list_tuple:
    #     if i[1] > i[2]:
    #         return False

    # collect piece id from configuration
    result = []
    for i in configuration.occupied_space.values():
        for j in i:
            if [j[3], False] not in result:
                result.append([j[3], False])

    # de fitrat stubs si tubes pentru a verifica stabilitatea
    for key, value in configuration.occupied_tubes.items():
        if key == 0:
            unique_piece_id = []
            for i in configuration.occupied_tubes[key]:
                if i[3] not in unique_piece_id:
                    unique_piece_id.append(i[3])
            for i in configuration.occupied_tubes[key]:
                if i[4] != -1 and [i[3], False] not in result:
                    return False
                elif (i[3], i[4]) == (-1, -1):
                    return False
            for i in unique_piece_id:
                for j in result:
                    if j[0] == i:
                        j[1] = True
        elif key <= max(configuration.occupied_tubes.keys()):
            unique_piece_id = []
            for i in configuration.occupied_tubes[key]:
                if i[3] not in unique_piece_id:
                    unique_piece_id.append(i[3])
            for i in configuration.occupied_tubes[key]:
                if i[4] != -1:
                    if [i[0], i[1], i[2], i[4], i[3]] not in configuration.occupied_studs[key]:
                        return False
            for i in unique_piece_id:
                for j in result:
                    if j[0] == i:
                        j[1] = True
        elif key > max(configuration.occupied_tubes.keys()):
            for i in configuration.occupied_tubes[key]:
                if (i[3], i[4]) != (-1, -1):
                    return False
    for i in result:
        if i[1] is False:
            return False
    return True


if __name__ == '__main__':

    conf = Configuration()
    # conf.place_in_studs(Brick(3010, "White", conf), [0, 0, 0], rotation=1)
    # conf.place_in_studs(Brick(3010, "White", conf), [0, 0, 3], rotation=1)
    # conf.place_in_studs(Brick(3020, "White", conf), [0, 0, 6], rotation=0)
    # # print(configuration.place_in_tubes(Brick(3010, "White", configuration), [0, 0, 3], rotation=1))
    # conf.place_in_tubes(Brick(3010, "White", conf), [0, 3, 3], rotation=1)
    # conf.place_in_tubes(Brick(3003, "White", conf), [3, 3, 0], rotation=0)
    # conf.place_in_studs(Brick(3003, "White", conf), [3, 5, 0], rotation=0)
    #
    # disponible_pices = [[3010, 3], [3003, 2], [3020, 2], [3005, 5]]
    # conf_initial = init_conf_with_placeholders(conf)
    #
    # conf_initial.replace(db_brick_id=3010, start_coordinates=[0, 0, 0], rotation=1)
    # conf_initial.replace(db_brick_id=3010, start_coordinates=[0, 0, 3], rotation=1)
    # conf_initial.replace(db_brick_id=3020, start_coordinates=[0, 0, 6], rotation=0)
    # conf_initial.replace(db_brick_id=3010, start_coordinates=[0, 3, 3], rotation=1)
    # conf_initial.replace(db_brick_id=3003, start_coordinates=[3, 3, 0], rotation=0)
    # conf_initial.replace(db_brick_id=3003, start_coordinates=[3, 5, 0], rotation=0)
    conf.load_configuration("D:\\Informatica\\Anul 3 Semestrul 1\\Inteligenta Artificiala\\ProiectAI\\desktop_app\\configurations\\0.txt")
    verificare(conf)

    print(is_final_state(conf, []))
