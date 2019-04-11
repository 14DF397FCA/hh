from collections import namedtuple
from configparser import ConfigParser
from typing import Set

RefreshStatus = namedtuple("RefreshStatus", "resume status_code description")


def is_param_exists(configuration: ConfigParser, param: str) -> bool:
    try:
        _ = configuration[param]
        return True
    except:
        return False


def read_value(config: ConfigParser, param: str) -> str:
    if is_param_exists(configuration=config, param=param):
        return config[param]
    else:
        return ""


def string_to_set(data: str = "", separator: str = ",") -> Set[str]:
    if data is not None and len(data.strip("")) > 0:
        return set([x.strip() for x in data.lower().split(separator)])
    else:
        return set()
