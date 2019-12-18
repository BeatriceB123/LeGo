import json


def import_from_image():
    with open("../lego_piece_info.json") as data_file:
        data = json.load(data_file)
    data['piece-list'].append(create_dict_for_json(3068, 2, 2, 1, flag=False))
    data['piece-list'].append(create_dict_for_json(3069, 1, 2, 1, flag=False))
    data['piece-list'].append(create_dict_for_json(3070, 1, 1, 1, flag=False))
    data['piece-list'].append(create_dict_for_json(3260, 1, 8, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3622, 1, 3, 3, flag=True))
    data['piece-list'].append(create_dict_for_json(3623, 1, 3, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3260, 1, 8, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3666, 1, 6, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3710, 1, 4, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3795, 2, 6, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(3958, 6, 6, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(4162, 1, 8, 1, flag=False))
    data['piece-list'].append(create_dict_for_json(4477, 1, 10, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(6636, 1, 6, 1, flag=False))
    data['piece-list'].append(create_dict_for_json(41539, 8, 8, 1, flag=True))
    data['piece-list'].append(create_dict_for_json(63864, 1, 3, 1, flag=False))

    for i in data['piece-list']:
        print(i)

    with open('test_export.json', 'w') as to_write:
        json.dump(data, to_write, indent=4)


def create_dict_for_json(id, length, width, height, flag=True):
    piece = dict()
    piece['id'] = id
    piece['length'] = length
    piece['width'] = width
    piece['height'] = height
    piece['space'] = []
    piece['studs'] = []
    piece['tubes'] =[]
    piece['image-path'] = "./lego_pictures/" + str(id)
    for i in range(0, length):
        for j in range(0, width):
            for k in range(0, height):
                piece['space'].append([i, j, k])
                if k == height - 1 and flag is True:
                    piece['studs'].append([i, j, height + 1])
            piece['tubes'].append([i, j, 0])
    return piece


if __name__ == '__main__':
    import_from_image()
