from json import load, dump
from os import listdir


def main():
    for filename in listdir('.'):
        if not filename.endswith('.json'):
            continue
        with open(filename, 'r', encoding='utf-8') as file:
            data = load(file)
        with open(filename, 'w', encoding='utf-8') as file:
            dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
