import argparse
import configparser
from configparser import ConfigParser
import logging
import os
from typing import NoReturn


def configure_logger(args) -> NoReturn:
    if args.log_level in logging._nameToLevel:
        level = logging._nameToLevel.get(args.log_level)
        logger = logging.getLogger()
        logger.setLevel(level)
        fh = logging.FileHandler('/var/log/hh/resume.log')
        fh.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s [%(filename)s.%(lineno)d] %(processName)s %(levelname)-1s %(name)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
    else:
        raise Exception(f"Can't recognize log level: {args.log_level}")


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app_conf", type=str, help="Configuration file", required=True)
    parser.add_argument("-l", "--log_level", type=str, help="Log level", required=False, default="INFO")
    return parser.parse_args()


def get_app_configuration(filename: str) -> ConfigParser:
    config = configparser.ConfigParser()
    config.read(filename)
    return config["main"]


def read_app_config(args) -> ConfigParser:
    if not os.path.isfile(args.app_conf):
        logging.error(f"Can't find config file {args.app_conf}")
    return get_app_configuration(filename=args.app_conf)
