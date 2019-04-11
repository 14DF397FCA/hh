from typing import Set, List

from hh import get_resumes, refresh_resumes, refresh_tokens, get_tokens
from libs import RefreshStatus
from start_app import *
from tokens import Tokens


def print_results(results: List[RefreshStatus]) -> NoReturn:
    if results is not None and len(results) > 0:
        for r in results:
            if r.status_code == 204:  # is True
                logging.info("Resume %s was updated", r.resume)
            else:
                logging.info("Resume %s was not updated, with error: %s", r.resume, r.description)


def refresh_token_if_needed(results: List[RefreshStatus], tokens: Tokens, config_file: str) -> NoReturn:
    tail: RefreshStatus = results[-1]
    if tail.status_code == 403:
        save_tokens(tokens=refresh_tokens(tokens), file_name=config_file)


def save_tokens(tokens: Tokens, file_name: str) -> NoReturn:
    config = configparser.ConfigParser()
    config.set("main", "access_token", tokens.access_token)
    config.set("main", "refresh_token", tokens.refresh_token)
    with open(file_name, "w") as config_file:
        config.write(config_file)


def main():
    args = read_args()
    configure_logger(args=args)
    config = read_app_config(args)

    tokens = get_tokens(config=config)

    logging.debug("Application token: %s", f"{tokens.access_token[:10]}...{tokens.access_token[-10:]}")
    resumes: Set = get_resumes(config=config)
    results: List[RefreshStatus] = refresh_resumes(resumes=resumes, token=tokens.access_token)
    print_results(results)

    refresh_token_if_needed(results=results, tokens=tokens, config_file=args.app_conf)


if __name__ == '__main__':
    main()
