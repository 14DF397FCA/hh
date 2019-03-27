from typing import Set, List, Tuple

from start_app import *
from hh import get_access_token, get_resumes, refresh_resumes
from libs import RefreshStatus


def print_results(results: List[RefreshStatus]) -> NoReturn:
    if results is not None and len(results) > 0:
        for r in results:
            if r.status_code == 204:  # is True
                logging.info("Resume %s was updated", r.resume)
            else:
                logging.info("Resume %s was not updated, with error: %s", r.resume, r.description)


def main():
    args = read_args()
    configure_logger(args=args)
    config = read_app_config(args)

    access_token: str = get_access_token(config=config)
    logging.debug("Application token: %s", f"{access_token[:10]}...{access_token[-10:]}")
    resumes: Set = get_resumes(config=config)
    results: List[RefreshStatus] = refresh_resumes(resumes=resumes, token=access_token)
    print_results(results)


if __name__ == '__main__':
    main()
