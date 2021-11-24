from os import path, mkdir
from os.path import join, isdir
from sys import platform

PROJECT_NAME = 'Aicé'
PROJECT_CODENAME = 'aice'
PROJECT_ICON_PATH = 'res/icon/icon256.png'

EEL_WEB_DIR = './res/web/'
EEL_STARTING_PATH = './index.html'

ENGLISH_INI = './res/language/english.ini'

if platform == 'win32':
    APPDATA_AICE = join(path.expandvars('%APPDATA%'), 'Aice')
else:
    APPDATA_AICE = join(path.expandvars('$HOME'), '.aice')
APPDATA_AICE_PACKS = join(APPDATA_AICE, 'packs')

if not isdir(APPDATA_AICE):
    mkdir(APPDATA_AICE)

if not isdir(APPDATA_AICE_PACKS):
    mkdir(APPDATA_AICE_PACKS)
