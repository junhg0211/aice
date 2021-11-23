from json import load, dump
from os import listdir
from os.path import join
from threading import Thread
from typing import Optional

import eel
from PIL import Image
from keyboard import add_abbreviation, remove_abbreviation, wait
from pystray import Icon, Menu, MenuItem

from constants import PROJECT_NAME, PROJECT_CODENAME, PROJECT_ICON_PATH, EEL_WEB_DIR, EEL_STARTING_PATH, ENGLISH_INI, \
    APPDATA_AICE_PACKS
from util import get_language


@eel.expose
def _get_language():
    return language['web']


@eel.expose
def _get_pack_list():
    return listdir(APPDATA_AICE_PACKS)


@eel.expose
def _get_pack_data(pack) -> dict:
    with open(join(APPDATA_AICE_PACKS, pack), 'r', encoding='utf-8') as file:
        data = load(file)
    return data


@eel.expose
def _get_pack_count() -> int:
    return len(_get_pack_list())


@eel.expose
def _get_available_abbreviation_count() -> int:
    return len(available_abbreviations)


@eel.expose
def what():
    print(_get_pack_count(), _get_available_abbreviation_count())


available_abbreviations = {}


@eel.expose
def _add_abbreviation(pack_name: str, key: str, term: str):
    if pack_name not in available_abbreviations:
        available_abbreviations[pack_name] = set()
    add_abbreviation(key, term, match_suffix=True)
    available_abbreviations[pack_name].add(key)
    if term.upper() != term:
        _add_abbreviation(pack_name, key.upper(), term.upper())


@eel.expose
def _disable_pack(pack_name: str):
    removed = set()
    for key in available_abbreviations[pack_name]:
        remove_abbreviation(key)
        removed.add(key)
    available_abbreviations[pack_name] -= removed


@eel.expose
def _enable_pack(pack_name: str):
    for key, value in _get_pack_data(pack_name).items():
        _add_abbreviation(pack_name, key, value)
        available_abbreviations[pack_name].add(key)


@eel.expose
def _delete_abbreviation(pack_name: str, keyword: str, config=None):
    path = join(APPDATA_AICE_PACKS, pack_name)
    if config is None:
        config = _get_pack_data(pack_name)
    if keyword in available_abbreviations[pack_name]:
        remove_abbreviation(keyword)
        available_abbreviations[pack_name] -= {keyword}
    del config[keyword]
    with open(path, 'w') as file:
        dump(config, file)


@eel.expose
def _edit_key(pack_name: str, original_key: str, key: str, term: str):
    originally_enabled = original_key in available_abbreviations[pack_name]

    data = _get_pack_data(pack_name)
    if originally_enabled:
        remove_abbreviation(original_key)
        available_abbreviations[pack_name] -= {original_key}
        _add_abbreviation(pack_name, key, term)
    data[key] = term
    _save_pack(pack_name, data)


def _save_pack(pack_name, data):
    with open(join(APPDATA_AICE_PACKS, pack_name), 'w') as file:
        dump(data, file)


# noinspection PyUnusedLocal
def _close_callback(page, sockets):
    global window_opened, need_background_working_notified

    if not sockets:
        window_opened = False

    if need_background_working_notified:
        icon.notify(language['notification']['content'], language['notification']['title'].format(PROJECT_NAME))
        need_background_working_notified = False


def open_window(path: str):
    global window_opened

    thread = Thread(target=eel.start, args=(path,), kwargs={'port': 0, 'close_callback': _close_callback})
    thread.setDaemon(True)
    thread.start()
    if path == EEL_STARTING_PATH:
        window_opened = True


def terminate():
    icon.stop()
    if window_opened:
        # noinspection PyUnresolvedReferences
        eel.closeWindow()()


def main():
    global language

    language = get_language(ENGLISH_INI)

    for pack_name in _get_pack_list():
        pack = _get_pack_data(pack_name)
        for datum in pack:
            _add_abbreviation(pack_name, datum, pack[datum])

    eel.init(EEL_WEB_DIR)
    open_window(EEL_STARTING_PATH)

    icon.run()


icon = Icon(
    PROJECT_CODENAME,
    Image.open(PROJECT_ICON_PATH),
    PROJECT_NAME,
    Menu(
        MenuItem('Open Window', lambda: open_window(EEL_STARTING_PATH)),
        MenuItem('Terminate', terminate)
    )
)

window_opened = False
need_background_working_notified = True
language: Optional[dict] = None

if __name__ == '__main__':
    main()
