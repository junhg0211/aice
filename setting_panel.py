import webview

from util import save_pack, is_valid_filename


# noinspection PyMethodMayBeStatic
class Api:
    def __init__(self, program):
        self.program = program

    def get_packs(self) -> list[str]:
        return list(self.program.abbreviations.keys())

    def get_pack_abbreviations(self, pack_name) -> list[tuple[str, str]]:
        return list(self.program.abbreviations.get(pack_name, dict()).items())

    def edit_abbreviation(self, pack_name: str, key: str, new_key: str, value: str):
        # check existence of pack
        if pack_name not in self.program.abbreviations:
            return

        # change abbreviation
        self.program.remove_abbreviation(pack_name, key)

        # save pack and reload
        self.program.abbreviations[pack_name][new_key] = (value, False)
        save_pack(pack_name, self.program.abbreviations[pack_name])
        del self.program.abbreviations[pack_name][new_key]

        self.program.reload()

    def check_new_available(self, pack_name: str, key: str) -> bool:
        return pack_name in self.program.abbreviations \
            and key \
            and key not in (key for pack in self.program.abbreviations.values() for key in pack.keys())

    def check_change_available(self, pack_name: str, key: str, new_key: str) -> bool:
        if pack_name not in self.program.abbreviations:
            return False

        if key == new_key:
            return True

        return new_key not in (key for pack in self.program.abbreviations.values() for key in pack.keys())

    def new_abbreviation(self, pack_name: str, key: str, value: str):
        if key in self.program.abbreviations.get(pack_name, dict()):
            return

        self.program.abbreviations[pack_name][key] = (value, False)
        save_pack(pack_name, self.program.abbreviations[pack_name])
        del self.program.abbreviations[pack_name][key]
        self.program.reload()

    def remove_abbreviation(self, pack_name: str, key: str):
        self.program.remove_abbreviation(pack_name, key)
        save_pack(pack_name, self.program.abbreviations[pack_name])
        self.program.reload()

    def get_autogenerated_abbreviations(self, pack_name: str) -> list[tuple[str, str]]:
        return list(filter(lambda x: x[1][1], self.program.abbreviations.get(pack_name, dict()).items()))

    def new_pack(self, pack_name: str) -> int:
        if pack_name in self.program.abbreviations:
            return 1

        if not is_valid_filename(pack_name):
            return 2

        if not pack_name.endswith('.json'):
            pack_name += '.json'

        self.program.abbreviations[pack_name] = dict()
        save_pack(pack_name, self.program.abbreviations[pack_name])

        return 0

    def remove_pack(self, pack_name: str):
        if pack_name not in self.program.abbreviations:
            return

        self.program.remove_pack(pack_name)
        self.program.reload()


def start_setting_panel(program):
    webview.create_window('Aicé Setting Panel', 'res/setting_panel/index.html', js_api=Api(program))
    webview.start(debug=True)