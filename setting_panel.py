import webview


# noinspection PyMethodMayBeStatic
class Api:
    def __init__(self, program):
        self.program = program

    def get_packs(self) -> list[str]:
        return list(self.program.abbreviations.keys())

    def get_pack_abbreviations(self, pack_name) -> list[tuple[str, str]]:
        return list(self.program.abbreviations.get(pack_name, dict()).items())


def start_setting_panel(program):
    webview.create_window('Aicé Setting Panel', 'res/setting_panel/index.html', js_api=Api(program))
    webview.start(debug=True)
