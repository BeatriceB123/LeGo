from PyQt5 import QtWidgets
import json


def write_to_json_file(path, table):
    list_of_dict = []
    with open(path, 'a') as fp:
        for i in range(0, table.rowCount()):
            data = {"Id": table.item(i, 1).text(), "Number": table.item(i, 2).text(), "Color": table.item(i, 3).text()}
            list_of_dict.append(data)
        json.dump(list_of_dict, fp, indent=2)
