from recordclass import RecordClass


class Tokens(RecordClass):
    access_token: str
    refresh_token: str
