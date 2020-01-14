from configuration import config1_pieces1, init_conf_with_placeholders, calculates_coordinates_starting_from_the_beginning


def get_possible_start(id_from_db, given_config):
    result_list = []
    for key, value in given_config.occupied_space.items():
        for coordinates in value:
            start_coordinates = [coordinates[0], coordinates[1], coordinates[2]]
            for rotation in range(0, 4):
                # print(start_coordinates, rotation)
                piece_info_in_space = calculates_coordinates_starting_from_the_beginning(given_config.db_brick_info[id_from_db], start_coordinates, rotation)
                # print(piece_info_in_space)
                if given_config.we_can_put_piece(piece_info_in_space):
                    result_list.append((coordinates[0], coordinates[1], coordinates[2], rotation))
    return result_list


if __name__ == '__main__':
    conf = config1_pieces1()
    disponible_pices = [[3010, 3], [3003, 2], [3020, 2], [3005, 5]]
    conf_initial = init_conf_with_placeholders(conf)
    print(get_possible_start(3010, conf_initial))
