from json import load, dump
from os import listdir
from os.path import join
from typing import Optional

from PIL import Image
from keyboard import add_abbreviation
from pystray import Icon, Menu, MenuItem

from constants import PROJECT_NAME, PROJECT_CODENAME, PROJECT_ICON_PATH, ENGLISH_INI, APPDATA_AICE_PACKS
from util import get_language


def _get_pack_list():
    return listdir(APPDATA_AICE_PACKS)


def _get_pack_data(pack) -> dict:
    with open(join(APPDATA_AICE_PACKS, pack), 'r', encoding='utf-8') as file:
        data = load(file)
    return data


available_abbreviations = {}


def _add_abbreviation(pack_name: str, key: str, term: str):
    if pack_name not in available_abbreviations:
        available_abbreviations[pack_name] = set()
    add_abbreviation(key, term, match_suffix=True)
    available_abbreviations[pack_name].add(key)
    if term.upper() != term:
        _add_abbreviation(pack_name, key.upper(), term.upper())


def _save_pack(pack_name, data):
    with open(join(APPDATA_AICE_PACKS, pack_name), 'w') as file:
        dump(data, file)


def terminate():
    icon.stop()


def main():
    global language

    language = get_language(ENGLISH_INI)

    for pack_name in _get_pack_list():
        pack = _get_pack_data(pack_name)
        for datum in pack:
            _add_abbreviation(pack_name, datum, pack[datum])

    icon.run()


icon = Icon(
    PROJECT_CODENAME,
    Image.open(PROJECT_ICON_PATH),
    PROJECT_NAME,
    Menu(
        MenuItem('Exit', terminate)
    )
)

window_opened = False
need_background_working_notified = True
language: Optional[dict] = None

if __name__ == '__main__':
    main()
