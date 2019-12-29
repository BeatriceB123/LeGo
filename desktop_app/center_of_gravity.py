from configuration import Configuration, Brick


def calculate_centers_of_gravity(configuration):
    result = []
    for key, value in configuration.occupied_space.items():
        x, y, nr = 0, 0, 0
        for coordinate in value:
            nr += 1
            x += coordinate[0]
            y += coordinate[1]
        result.append([key, x / nr, y / nr, nr])
    return result


def check_configuration(configuration):
    centers_of_gravity = calculate_centers_of_gravity(configuration)
    for element in range(1, len(centers_of_gravity)):
        size_difference = centers_of_gravity[element][3] / centers_of_gravity[element - 1][3]
        nr_difference = abs(centers_of_gravity[element][3] - centers_of_gravity[element - 1][3])
        x_difference = abs(centers_of_gravity[element][1] - centers_of_gravity[element - 1][1])
        y_difference = abs(centers_of_gravity[element][2] - centers_of_gravity[element - 1][2])
        if size_difference >= 2.0:
            if x_difference + y_difference != 0:
                return False
        elif size_difference >= 1.7:
            if x_difference + y_difference < nr_difference * 0.3:
                return False
        elif size_difference >= 1.3:
            if x_difference + y_difference < nr_difference * 0.5:
                return False
        elif size_difference >= 1.0:
            if x_difference + y_difference < nr_difference * 0.7:
                return False
        elif size_difference >= 0.7:
            if x_difference + y_difference < nr_difference * 1.7:
                return False
        elif size_difference >= 0.4:
            if x_difference + y_difference < nr_difference * 1.4:
                return False
        else:
            if x_difference + y_difference < nr_difference * 1.1:
                return False
        # print("Current level is:", centers_of_gravity[element][0],
        #       "- Current center is:", [centers_of_gravity[element][1], centers_of_gravity[element][2]],
        #       "- Previous center is:", [centers_of_gravity[element - 1][1], centers_of_gravity[element - 1][2]],
        #       "- Size difference is:", size_difference,
        #       "- Difference in number of pieces is:", nr_difference)
    return True


if __name__ == '__main__':
    config = Configuration()
    config.place_in_studs(Brick(3010, "White", config), [0, 0, 0], rotation=1)
    config.place_in_studs(Brick(3010, "White", config), [0, 0, 3], rotation=1)
    config.place_in_studs(Brick(3020, "White", config), [0, 0, 6], rotation=0)
    config.place_in_tubes(Brick(3010, "White", config), [0, 3, 3], rotation=1)
    config.place_in_tubes(Brick(3010, "White", config), [0, 3, 0], rotation=1)
    # config.place_in_tubes(Brick(3020, "White", config), [3, 3, 2], rotation=0)
    print(check_configuration(config))
