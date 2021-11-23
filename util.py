from configparser import ConfigParser


def get_language(path) -> dict:
    config = ConfigParser()
    config.read(path, encoding='utf-8')
    return {key: dict(value) for key, value in dict(config).items()}
