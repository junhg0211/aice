from json import load, dump
from os import listdir
from os.path import join

from constants import APPDATA_AICE_PACKS


def get_pack_list():
    return filter(lambda x: x.endswith('.json'), listdir(APPDATA_AICE_PACKS))


def get_pack_data(pack) -> dict:
    with open(join(APPDATA_AICE_PACKS, pack), 'r', encoding='utf-8') as file:
        data = load(file)
    return data


def save_pack(pack_name: str, data: dict[str, [str, bool]]):
    data = {key: value[0] for key, value in data.items() if not value[1]}
    with open(join(APPDATA_AICE_PACKS, pack_name), 'w') as file:
        dump(data, file, indent=2)
