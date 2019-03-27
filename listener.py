import argparse
import logging
from flask import Flask, request

app = Flask(__name__)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if code is not None:
        logging.info("Callback - %s", code)
        return {"response": True}
    else:
        return {"response": False}


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Listen port", required=False, default=8080)
    parser.add_argument("-i", "--interface", type=str, help="Listen interface", required=False, default="0.0.0.0")
    parser.add_argument("-d", "--debug", type=bool, help="Flask debug", required=False, default=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = read_args()
    app.run(debug=bool(args.debug), port=int(args.port), host=str(args.interface))
