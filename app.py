import os

from flask import Flask, request, abort, jsonify, Response
from typing import Union, List, Optional

from commands import commands

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query")
def perform_query() -> Response:
    payload: dict[str, Optional[str]] = {
        'file_name': request.args.get('file_name'),
        'cmd1': request.args.get('cmd1'),
        'value1': request.args.get('value1'),
        'cmd2': request.args.get('cmd2'),
        'value2': request.args.get('value2')
    }

    if not (payload['file_name'] and payload['cmd1'] and payload['value1']):
        abort(400, 'Обязательно нужно ввести эти команды: file_name, cmd1, value1')

    file_path: str = os.path.join(DATA_DIR, payload['file_name'])
    if not os.path.exists(file_path):
        return abort(400, 'Файла не существует')

    with open(file_path) as f:
        res: Union[str, List] = commands(f, payload['cmd1'], payload['value1'])

    if payload['cmd2'] and payload['value2']:
        res = commands(res, payload['cmd1'], payload['value1'])

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
