from PIL import Image
from keyboard import add_abbreviation, remove_abbreviation
from pystray import Icon, Menu, MenuItem

from constants import PROJECT_NAME, PROJECT_CODENAME, PROJECT_ICON_PATH
from util import get_pack_list, get_pack_data


class Program:
    def __init__(self):
        self.available_abbreviations = {}
        self.amount = 0
        self.icon = Icon(
            PROJECT_CODENAME,
            Image.open(PROJECT_ICON_PATH),
            PROJECT_NAME,
            self.generate_menu()
        )

    def add_abbreviation(self, pack_name: str, key: str, term: str):
        if pack_name not in self.available_abbreviations:
            self.available_abbreviations[pack_name] = set()
        add_abbreviation(key, term, match_suffix=True)
        self.available_abbreviations[pack_name].add(key)
        self.amount += 1
        if term.upper() != term:
            self.add_abbreviation(pack_name, key.upper(), term.upper())

    def load_abbreviations(self):
        for pack_name in get_pack_list():
            pack = get_pack_data(pack_name)
            for datum in pack:
                self.add_abbreviation(pack_name, datum, pack[datum])

    def remove_all_abbreviations(self):
        for pack_name in self.available_abbreviations.keys():
            for key in self.available_abbreviations[pack_name]:
                remove_abbreviation(key)
        self.available_abbreviations.clear()
        self.amount = 0

    def generate_menu(self) -> Menu:
        return Menu(
            MenuItem(f'{self.amount} Abbreviations', lambda: None, enabled=False),
            MenuItem('Reload', self.reload),
            MenuItem('Exit', self.terminate)
        )

    def reload(self):
        self.remove_all_abbreviations()
        self.load_abbreviations()
        self.icon.menu = self.generate_menu()

    def terminate(self):
        self.icon.stop()

    def main(self):
        self.load_abbreviations()
        self.icon.menu = self.generate_menu()
        self.icon.run()


if __name__ == '__main__':
    program = Program()
    program.main()
