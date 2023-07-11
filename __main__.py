from json import load, dump
from os import listdir
from os.path import join

from PIL import Image
from keyboard import add_abbreviation, remove_abbreviation
from pystray import Icon, Menu, MenuItem

from constants import PROJECT_NAME, PROJECT_CODENAME, PROJECT_ICON_PATH, APPDATA_AICE_PACKS


def _get_pack_list():
    return listdir(APPDATA_AICE_PACKS)


def _get_pack_data(pack) -> dict:
    with open(join(APPDATA_AICE_PACKS, pack), 'r', encoding='utf-8') as file:
        data = load(file)
    return data


available_abbreviations = {}
amount = 0


def _add_abbreviation(pack_name: str, key: str, term: str):
    global amount

    if pack_name not in available_abbreviations:
        available_abbreviations[pack_name] = set()
    add_abbreviation(key, term, match_suffix=True)
    available_abbreviations[pack_name].add(key)
    amount += 1
    if term.upper() != term:
        _add_abbreviation(pack_name, key.upper(), term.upper())


def _save_pack(pack_name, data):
    with open(join(APPDATA_AICE_PACKS, pack_name), 'w') as file:
        dump(data, file)


def load_abbreviations():
    for pack_name in _get_pack_list():
        pack = _get_pack_data(pack_name)
        for datum in pack:
            _add_abbreviation(pack_name, datum, pack[datum])


def remove_all_abbreviations():
    global amount

    for pack_name in available_abbreviations.keys():
        for key in available_abbreviations[pack_name]:
            remove_abbreviation(key)
    available_abbreviations.clear()
    amount = 0


def generate_menu() -> Menu:
    return Menu(
        MenuItem(f'{amount} Abbreviations', lambda: None, enabled=False),
        MenuItem('Reload', reload),
        MenuItem('Exit', terminate)
    )


def reload():
    remove_all_abbreviations()
    load_abbreviations()
    icon.menu = generate_menu()


def terminate():
    icon.stop()


def main():
    load_abbreviations()
    icon.menu = generate_menu()
    icon.run()


icon = Icon(
    PROJECT_CODENAME,
    Image.open(PROJECT_ICON_PATH),
    PROJECT_NAME,
    generate_menu()
)

if __name__ == '__main__':
    main()
