from os import path, mkdir
from os.path import join, isdir, split
from sys import platform

PWD = split(__file__)[0]
print(PWD)

PROJECT_NAME = "Aicé"
PROJECT_CODENAME = "aice"
PROJECT_ICON_PATH = join(PWD, "res/icon/icon256.png")

ENGLISH_INI = join(PWD, "res/language/english.ini")

if platform == "win32":
    APPDATA_AICE = join(path.expandvars("%APPDATA%"), "Aice")
else:
    APPDATA_AICE = join(path.expandvars("$HOME"), ".aice")
APPDATA_AICE_PACKS = join(APPDATA_AICE, "packs")

if not isdir(APPDATA_AICE):
    mkdir(APPDATA_AICE)

if not isdir(APPDATA_AICE_PACKS):
    mkdir(APPDATA_AICE_PACKS)
