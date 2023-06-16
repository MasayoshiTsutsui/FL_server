import flask
from flask_sslify import SSLify
from model_manager import save_as_file, try_to_update_model
from constants import GLOBAL_MODEL_DIR

import os

DEBUG = 1

app = flask.Flask(__name__)
sslify = SSLify(app)


# ユーザ名を取得
user = os.getlogin()


# hoge.txtのdirectory
static_directory = f"/home/{user}/fl_server/static"

# クライアントからの要求があった場合のエンドポイント
@app.route("/load-model", methods=["GET"])
def get_latest_mlmodel():
    if DEBUG:
        print("get_mlmodel_file was called")
    gModel_idx = len(os.listdir(GLOBAL_MODEL_DIR))
    return flask.send_from_directory(static_directory, f"Hands2num_v{gModel_idx}.mlmodel")

# クライアントからの要求があった場合のエンドポイント
@app.route("/submit-params", methods=["POST"])
def save_float_params():
    if DEBUG:
        print("save_float_array was called")
    params_json = flask.request.get_json()  # クライアントからのJSONデータを取得

    gModel_idx = len(os.listdir(GLOBAL_MODEL_DIR))
    save_as_file(params_json, gModel_idx)
    try_to_update_model(gModel_idx)
    return "Float array saved successfully"

if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/mobile-federated-learning.com/fullchain.pem', '/etc/letsencrypt/live/mobile-federated-learning.com/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
