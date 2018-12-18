import json
import sys
sys.path.append('../')


DATA_PATH = "../../data/"


def readjson(filename, number=-1):
    filename = DATA_PATH + filename
    with open(filename, "r") as file:
        dict = json.load(file)
        key = str(number)
        if key in dict:
            return dict[key]
        else:
            return dict
