from configuration import Configuration, Brick


def get_configs_by_color(configuration):
    result_dict = dict()
    for key, value in configuration.lego_bricks.items():
        if value[0].color not in result_dict:
            result_dict[value[0].color] = Configuration()
        lego_brick = Brick(value[0].db_id, value[0].color, None)
        lego_brick.brick_id = value[0].brick_id
        result_dict[value[0].color].lego_bricks[lego_brick.brick_id] = [lego_brick, True]
    for key, value in configuration.occupied_space.items():
        for space in value:
            color = configuration.lego_bricks[space[3]][0].color
            if key not in result_dict[color].occupied_space:
                result_dict[color].occupied_space[key] = []
            result_dict[color].occupied_space[key].append(space)
    for key, value in configuration.occupied_studs.items():
        for stud in value:
            color = configuration.lego_bricks[stud[3]][0].color
            if key not in result_dict[color].occupied_studs:
                result_dict[color].occupied_studs[key] = []
            result_dict[color].occupied_studs[key].append(stud)
    for key, value in configuration.occupied_tubes.items():
        for tube in value:
            color = configuration.lego_bricks[tube[3]][0].color
            if key not in result_dict[color].occupied_tubes:
                result_dict[color].occupied_tubes[key] = []
            result_dict[color].occupied_tubes[key].append(tube)
    return result_dict


if __name__ == '__main__':
    config = Configuration()
    config.place_in_studs(Brick(3010, "White", config), [0, 0, 0], rotation=1)
    config.place_in_studs(Brick(3010, "Blue", config), [0, 0, 3], rotation=1)
    config.place_in_studs(Brick(3020, "White", config), [0, 0, 6], rotation=0)
    config.place_in_tubes(Brick(3010, "Red", config), [0, 3, 3], rotation=1)
    config.place_in_tubes(Brick(3020, "Red", config), [3, 3, 2], rotation=0)
    # config.place_in_tubes(Brick(3020, "White", config), [3, 3, 2], rotation=0)
    res = get_configs_by_color(config)
    for _key, _value in res.items():
        print(_key)
        for a, b in _value.lego_bricks.items():
            print(b[0].db_id, b[0].color, b[0].brick_id)
        print("SPACES")
        for a, b in _value.occupied_space.items():
            print(a, b)
        print("STUDS")
        for a, b in _value.occupied_studs.items():
            print(a, b)
        print("TUBES")
        for a, b in _value.occupied_tubes.items():
            print(a, b)
        print("\n\n")
