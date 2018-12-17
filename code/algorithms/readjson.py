import json
import sys
sys.path.append('../')
from classes.chip import Chip


DATA_PATH = "../../data/"
RESULTS_PATH = "../../results/"


def readjson(filename, number=-1):
    filename = DATA_PATH + filename
    with open(filename, "r") as file:
        dict = json.load(file)
        key = str(number)
        if key in dict:
            return dict[key]
        else:
            return dict


def loadchip(filename):
    filename = RESULTS_PATH + filename
    with open(filename, 'r') as f:
        dic = json.load(f)
    c = chip(dic["size"], dic["gate"], dic["net"])
    c.grid = dic["grid"]
    c.wire = dic["wire"]
    c.used_wired = dic["used_wired"]
    c.map_line = dic["map_line"]
    return c
