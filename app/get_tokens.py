import argparse
from typing import NoReturn

import requests
import logging

from hh import make_auth_http_headers, URI_HH_OAUTH_TOKEN


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--client_id", type=str, help="Client ID", required=True)
    parser.add_argument("-s", "--client_secret", type=str, help="Client Secret", required=True)
    parser.add_argument("-c", "--authorization_code", type=str, help="Authorization code", required=True)
    parser.add_argument("-u", "--redirect_uri", type=str, help="Redirect URI", required=True)
    parser.add_argument("-l", "--log_level", type=str, help="Log level", required=False, default="DEBUG")
    return parser.parse_args()


def configure_logger(args) -> NoReturn:
    if args.log_level in logging._nameToLevel:
        level = logging._nameToLevel.get(args.log_level)
        logger = logging.getLogger()
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s [%(filename)s.%(lineno)d] %(processName)s %(levelname)-1s %(name)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        raise Exception(f"Can't recognize log level: {args.log_level}")


if __name__ == '__main__':
    args = read_args()
    configure_logger(args)
    data = {"grant_type": "authorization_code",
            "client_id": args.client_id,
            "client_secret": args.client_secret,
            "code": args.authorization_code,
            "redirect_uri": args.redirect_uri}

    headers = make_auth_http_headers()

    logging.debug("data: %s", data)
    logging.debug("headers: %s", headers)
    r = requests.post(url=URI_HH_OAUTH_TOKEN, data=data, headers=headers)
    logging.info(r.status_code)
    logging.info(r.text)
