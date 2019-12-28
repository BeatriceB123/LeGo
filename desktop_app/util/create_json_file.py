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

    for i in create_bridge():
        data['piece-list'].append(i)

    for i in data['piece-list']:
        print(i)

    with open('test_export.json', 'w') as to_write:
        json.dump(data, to_write, indent=4)


def create_bridge():
    piece_list = []
    piece = dict()
    piece['id'] = 4490
    piece['length'] = 1
    piece['width'] = 3
    piece['height'] = 3
    piece['space'] = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2],
        [0, 1, 2],
        [0, 2, 0], [0, 2, 1], [0, 2, 2]
    ]
    piece['studs'] = [
        [0, 0, 3], [0, 1, 3], [0, 2, 3]
    ]
    piece['tubes'] = [
        [0, 0, 0], [0, 1, 0], [0, 2, 0]
    ]
    piece['image-path'] = "./lego_pictures/" + str(4490)
    piece_list.append(piece)
    del piece
    piece = dict()
    piece['id'] = 3659
    piece['length'] = 1
    piece['width'] = 4
    piece['height'] = 3
    piece['space'] = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2],
        [0, 1, 2], [0, 2, 2],
        [0, 3, 0], [0, 3, 1], [0, 3, 2]
    ]
    piece['studs'] = [
        [0, 0, 3], [0, 1, 3], [0, 2, 3], [0, 3, 3]
    ]
    piece['tubes'] = [
        [0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0]
    ]
    piece['image-path'] = "./lego_pictures/" + str(3659)
    piece_list.append(piece)
    piece = dict()
    piece['id'] = 3307
    piece['length'] = 1
    piece['width'] = 6
    piece['height'] = 6
    piece['space'] = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4], [0, 0, 5],
        [0, 1, 5], [0, 1, 4], [0, 2, 3],
        [0, 2, 5], [0, 2, 4],
        [0, 3, 5], [0, 3, 4],
        [0, 4, 5], [0, 4, 4], [0, 4, 3],
        [0, 5, 0], [0, 5, 1], [0, 5, 2], [0, 5, 3], [0, 5, 4], [0, 5, 5]
    ]
    piece['studs'] = [
        [0, 0, 6], [0, 1, 6], [0, 2, 6],
        [0, 3, 6], [0, 4, 6], [0, 5, 6]
    ]
    piece['tubes'] = [
        [0, 0, 0], [0, 1, 0], [0, 2, 0],
        [0, 3, 0], [0, 4, 0], [0, 5, 0]
    ]
    piece['image-path'] = "./lego_pictures/" + str(3307)
    piece_list.append(piece)
    return piece_list


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
