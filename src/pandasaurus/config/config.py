import configparser


def get_config():
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    return conf


default_config = get_config()["DEFAULT"]
