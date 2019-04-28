import configparser
import logging
from configparser import ConfigParser
from typing import Set, Dict, List, NoReturn

import requests

from libs import string_to_set, read_value, RefreshStatus
from tokens import Tokens

URI_HH_OAUTH_TOKEN = "https://hh.ru/oauth/token"
URI_HH_API_SHORT = "api.hh.ru"
URI_HH_API = f"https://{URI_HH_API_SHORT}"
USER_AGENT = "GIlyashenko/1.0 (ilyashenko.gennadiy@gmail.com)"


def get_tokens(config: ConfigParser) -> Tokens:
    access_token: str = get_access_token(config=config)
    refresh_token: str = get_refresh_token(config=config)
    return Tokens(access_token=access_token,
                  refresh_token=refresh_token)


def get_access_token(config: ConfigParser) -> str:
    return read_value(config=config, param="access_token")


def get_refresh_token(config: ConfigParser) -> str:
    return read_value(config=config, param="refresh_token")


def get_resumes(config: ConfigParser) -> Set[str]:
    def read_raw_resumes():
        return read_value(config=config, param="resume_ids")

    return string_to_set(read_raw_resumes())


def make_auth_http_headers() -> Dict:
    return {"Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
            "Accept": "*/*"
            }


def make_http_headers(token: str) -> Dict:
    r: Dict = {"User-Agent": USER_AGENT,
               "Host": URI_HH_API_SHORT,
               "Accept": "*/*",
               "Authorization": str(f"Bearer {token}")
               }
    logging.debug("HTTP_headers: %s", r)
    return r


def make_refresh_resume_url(resume: str) -> str:
    r: str = f"{URI_HH_API}/resumes/{resume}/publish"
    logging.debug("Refresh resume URI: %s", r)
    return r


def refresh_tokens(tokens: Tokens) -> Tokens:
    logging.debug("Try to refresh tokens")
    data = {"grant_type": "refresh_token",
            "refresh_token": tokens.refresh_token}

    headers = make_auth_http_headers()

    r = requests.post(url=URI_HH_OAUTH_TOKEN, headers=headers, data=data)
    logging.info(r.text)
    if r.status_code == 200:
        js = r.json()
        r = Tokens(access_token=js["access_token"],
                   refresh_token=js["refresh_token"])
        logging.debug("Tokens: %s", r)
        return r
    else:
        logging.error("status_code: %s; response: %s", r.status_code, r.text)
        return tokens


def make_http_request(resume: str, token: str) -> RefreshStatus:
    """
    https://hh.ru/
    User-Agent: MyApp/1.0 (my-app-feedback@example.com)

    https://github.com/hhru/api/blob/master/docs/resumes.md#publish
    POST /resumes/{resume_id}/publish
    :return:
    """
    header: Dict = make_http_headers(token=token)
    url: str = make_refresh_resume_url(resume=resume)
    r = requests.post(url=url, headers=header)
    if r.status_code != 204:
        logging.error("status_code: %s; Response: %s", r.status_code, r.text)
        return RefreshStatus(resume=resume,
                             status_code=r.status_code,
                             description=r.json()["description"])
    else:
        return RefreshStatus(resume=resume,
                             status_code=r.status_code,
                             description="ok")


def refresh_resume(resume: str, token: str) -> RefreshStatus:
    logging.debug("Refresh resume with ID: %s", resume)
    return make_http_request(resume=resume, token=token)


def refresh_resumes(resumes: Set[str], token: str) -> List[RefreshStatus]:
    logging.debug("Refresh resumes: %s", resumes)
    results = []
    for resume in resumes:
        results.append(refresh_resume(resume=resume, token=token))
    return results
