import json
from lego_brick import Brick

def create_all_brick_object():
    with open('../lego_piece_info.json', 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)
    all_lego_data = obj['piece-list']
    result = []
    for i in all_lego_data:
        result.append(Brick(i['id'], i['length'], i['width'], i['height'], 'White', i['space'], i['studs'], i['tubes']))

    for i in result:
        print(i.length, i.height, i.width, i.db_id, i.studs, i.tubes)


create_all_brick_object()