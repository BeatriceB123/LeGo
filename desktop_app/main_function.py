import os
from configuration import *
from configs_by_color import *
import sys
# sys.path.append("..\\")


def main_function(user_list, same_bricks, same_color, flg = False):
    response = dict()
    os.chdir("..\\")
    directory = "configurations\\"
    # if flg == True:
    #     directory = "..\\configurations\\"
    # else:
    #     directory = "configurations"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            config = Configuration()
            config.load_configuration(filename)
            config_number = int(os.path.splitext(filename)[0])
            if same_bricks and same_color:
                result = verify_if_we_can_build_with_exactly_given_pieces_and_color(config, user_list)
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
    print(main_function([[3034, 1, "Green"], [3004, 4, "Green"], [3659, 2, "Green"], [2456, 1, "Green"], [3003, 1, "Green"], [3062, 2, "Green"]], True, True))
