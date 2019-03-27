from configparser import ConfigParser
from typing import Set, Tuple, Dict, List
import logging
import requests

from libs import string_to_set, read_value, RefreshStatus

URI_HH_OAUTH_TOKEN = "https://hh.ru/oauth/token"
URI_HH_API = "https://api.hh.ru"


def get_access_token(config: ConfigParser) -> str:
    return read_value(config=config, param="access_token")


def get_refresh_token(config: ConfigParser) -> str:
    return read_value(config=config, param="refresh_token")


def get_resumes(config: ConfigParser) -> Set[str]:
    def read_raw_resumes():
        return read_value(config=config, param="resume_ids")

    return string_to_set(read_raw_resumes())


def make_http_headers(token: str) -> Dict:
    r: Dict = {"User-Agent": "GIlyashenko/1.0 (ilyashenko.gennadiy@gmail.com)",
               "Host": "api.hh.ru",
               "Accept": "*/*",
               "Authorization": str(f"Bearer {token}")}
    logging.debug("HTTP_headers: %s", r)
    return r


def make_refresh_resume_url(resume: str) -> str:
    r: str = f"{URI_HH_API}/resumes/{resume}/publish"
    logging.debug("Refresh resume URI: %s", r)
    return r


def refresh_tokens(access_token: str, refresh_token: str) -> Tuple[str, str]:
    headers = {"grant_type": "refresh_token",
               "refresh_token": refresh_token}
    r = requests.post(url=URI_HH_OAUTH_TOKEN, headers=headers)
    if r.status_code == 200:
        js = r.json()
        return js["access_token"], js["refresh_token"]
    else:
        logging.error("status_code: %s; response: %s", r.status_code, r.text)
        return access_token, refresh_token


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
