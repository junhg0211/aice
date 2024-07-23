from os import system
from collections import deque

from PIL import Image
from pystray import Icon, Menu, MenuItem
from pynput.keyboard import Controller, Listener, Key

from constants import PROJECT_NAME, PROJECT_CODENAME, PROJECT_ICON_PATH
from setting_panel import start_setting_panel
from util import get_pack_list, get_pack_data, remove_pack


class EventHandler:
    def __init__(self, abbreviations: dict):
        self.buffer = deque()
        self.abbreviations = abbreviations
        self.controller = Controller()

    def on_press(self, key):
        if key == Key.space:
            buffer_string = "".join(self.buffer)
            for pack in self.abbreviations.values():
                for key, value in pack.items():
                    if buffer_string.endswith(key):
                        for _ in range(len(key) + 1):
                            self.controller.press(Key.backspace)
                            self.controller.release(Key.backspace)
                        self.controller.type(value[0])
                        break

            self.buffer.clear()
            return

        if not hasattr(key, "char"):
            self.buffer.clear()
            return
        if key.char is None:
            return

        self.buffer.append(key.char)

        while len(self.buffer) > 20:
            self.buffer.popleft()

    def on_release(self, _):
        pass

    def start(self):
        listener = Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()


class Program:
    def __init__(self):
        self.abbreviations: dict[str, dict[str, tuple[str, bool]]] = dict()
        self.amount = 0
        self.icon = Icon(
            PROJECT_CODENAME,
            Image.open(PROJECT_ICON_PATH),
            PROJECT_NAME,
            self.generate_menu(),
        )
        self.enabled = True

    def add_abbreviation(
        self, pack_name: str, key: str, term: str, *, autogenerated: bool = False
    ):
        if pack_name not in self.abbreviations:
            self.abbreviations[pack_name] = dict()
        self.abbreviations[pack_name][key] = (term, autogenerated)
        self.amount += 1
        if term.upper() != term:
            self.add_abbreviation(
                pack_name, key.upper(), term.upper(), autogenerated=True
            )

    def load_abbreviations(self):
        for pack_name in get_pack_list():
            if pack_name not in self.abbreviations:
                self.abbreviations[pack_name] = dict()

            pack = get_pack_data(pack_name)
            for datum in pack:
                self.add_abbreviation(pack_name, datum, pack[datum])

    def remove_abbreviation(self, pack_name: str, key: str):
        # check existence
        if key not in self.abbreviations.get(pack_name, dict()):
            return

        # remove abbreviation
        self.amount -= 1
        del self.abbreviations[pack_name][key]

        # remove upper case abbreviation
        if (upper := key.upper()) in self.abbreviations[pack_name]:
            self.remove_abbreviation(pack_name, upper)

    def remove_pack(self, pack_name: str):
        for key, value in tuple(self.abbreviations[pack_name].items()):
            if value[1]:
                continue
            self.remove_abbreviation(pack_name, key)
        del self.abbreviations[pack_name]
        remove_pack(pack_name)

    def remove_all_abbreviations(self):
        self.abbreviations.clear()
        self.amount = 0

    def toggle_enable(self):
        if self.enabled:
            self.remove_all_abbreviations()
        else:
            self.reload()
        self.enabled = not self.enabled

    def is_enable_checked(self, _: MenuItem) -> bool:
        return self.enabled

    def generate_menu(self) -> Menu:
        return Menu(
            MenuItem(f"{self.amount} Abbreviations", lambda: None, enabled=False),
            Menu.SEPARATOR,
            MenuItem(
                "Enable Abbreviation",
                self.toggle_enable,
                checked=self.is_enable_checked,
            ),
            MenuItem("Open Setting Panel", lambda: start_setting_panel(self)),
            MenuItem(
                "Open Packs Directory", lambda: system("start %APPDATA%\\Aice\\packs")
            ),
            MenuItem("Reload", self.reload),
            MenuItem("Exit", self.terminate),
        )

    def reload(self):
        self.remove_all_abbreviations()
        self.load_abbreviations()
        self.icon.menu = self.generate_menu()

    def terminate(self):
        self.icon.stop()

    def main(self):
        self.load_abbreviations()

        handler = EventHandler(self.abbreviations)
        handler.start()

        self.icon.menu = self.generate_menu()
        self.icon.run()


if __name__ == "__main__":
    program = Program()
    program.main()
