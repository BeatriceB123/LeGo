import os
from configuration import *
from configs_by_color import *


def main_function(user_list, same_bricks, same_color):
    response = dict()
    directory = "configurations"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            config = Configuration()
            config.load_configuration(filename)
            config_number = int(os.path.splitext(filename)[0])
            if same_bricks and same_color:
                pass
            elif same_bricks and not same_color:
                result = verify_if_we_can_build_with_exactly_given_pieces(config, user_list)
            elif not same_bricks and same_color:
                configs_by_color = get_configs_by_color(config)
                result = True
                for key, value in configs_by_color:
                    if result:
                        user_list_filtered = get_pieces_by_color(key, user_list)
                        aux = verify_if_we_can_build(value, user_list_filtered)
                        if not aux:
                            result = False
            elif not same_bricks and not same_color:
                result = verify_if_we_can_build(config, user_list)
            if result:
                response[config_number] = True
            else:
                response[config_number] = False
    return response


if __name__ == '__main__':
    print(main_function([[3001, 8, "White"], [3010, 6, "White"], [3622, 4, "White"], [3039, 1, "White"], [3004, 5, "White"]], False, False))
