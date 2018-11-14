import json


def readjson(filename):
    with open(filename, "r") as file:
        dict = json.load(file)
        return dict