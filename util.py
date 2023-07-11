from json import load, dump
from os import listdir
from os.path import join

from constants import APPDATA_AICE_PACKS


def get_pack_list():
    return listdir(APPDATA_AICE_PACKS)


def get_pack_data(pack) -> dict:
    with open(join(APPDATA_AICE_PACKS, pack), 'r', encoding='utf-8') as file:
        data = load(file)
    return data


def save_pack(pack_name, data):
    with open(join(APPDATA_AICE_PACKS, pack_name), 'w') as file:
        dump(data, file)
