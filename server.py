from flask import Flask, request, send_from_directory
import os

DEBUG = 1

app = Flask(__name__)

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
@app.route("/float_array", methods=["POST"])
def save_float_array():
    if DEBUG:
        print("save_float_array was called")
    float_array = request.get_json()  # クライアントからのJSONデータを取得
    print(float_array)
    # float_arrayの保存処理を実装する
    return "Float array saved successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

