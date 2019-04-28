import configparser
from typing import NoReturn, List

from recordclass import RecordClass

from hh import refresh_tokens
from libs import RefreshStatus


class Tokens(RecordClass):
    access_token: str
    refresh_token: str


def refresh_token_if_needed(results: List[RefreshStatus], tokens: Tokens, config_file: str) -> NoReturn:
    tail: RefreshStatus = results[-1]
    if tail.status_code == 403:
        save_tokens(tokens=refresh_tokens(tokens), file_name=config_file)


def save_tokens(tokens: Tokens, file_name: str) -> NoReturn:
    config = configparser.ConfigParser()
    config.add_section("main")
    config.set("main", "access_token", tokens.access_token)
    config.set("main", "refresh_token", tokens.refresh_token)
    with open(file_name, "w") as config_file:
        config.write(config_file)
