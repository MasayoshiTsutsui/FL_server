from flask import Flask, request, send_from_directory
from flask_sslify import SSLify
from model_manager import save_as_file, try_to_update_model

import os

DEBUG = 1

app = Flask(__name__)
sslify = SSLify(app)


# ユーザ名を取得
user = os.getlogin()


# hoge.txtのdirectory
static_directory = f"/home/{user}/fl_server/static"

# クライアントからの要求があった場合のエンドポイント
@app.route("/hoge", methods=["GET"])
def get_hoge_file():
    if DEBUG:
        print("get_hoge was called")
    return send_from_directory(static_directory, "hoge.txt")

# クライアントからの要求があった場合のエンドポイント
@app.route("/submit-params", methods=["POST"])
def save_float_params():
    if DEBUG:
        print("save_float_array was called")
    params_json = request.get_json()  # クライアントからのJSONデータを取得

    save_as_file(params_json)

    try_to_update_model()

    return "Float array saved successfully"

if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/mobile-federated-learning.com/fullchain.pem', '/etc/letsencrypt/live/mobile-federated-learning.com/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
