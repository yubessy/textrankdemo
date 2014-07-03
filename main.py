# -*- coding: utf-8 -*-
# stdlib
import json
# thirdlib
import bottle
# mylib
import secret
import exception
from utils import tokenize
from utils import textrank

# テキストの長さの上限
MAX_TEXT_LENGTH = 2000

# スコアの小数点以下桁数
SCORE_NDIGIT = 6

# N-gram作成時のウインドウ
NGRAM_WINDOW = 2

# 単語分割器
gen_en = tokenize.Tokenizer("en")
gen_ja = tokenize.Tokenizer("ja")


def check(username, password):
    u"""
    BASIC認証のユーザ名とパスワードをチェック
    @bottle.auth_basic(check)で適用
    """
    if username == secret.USERNAME and password == secret.PASSWORD:
        return True
    else:
        return False


@bottle.post("/textrankdemo/result.json")
@bottle.auth_basic(check)
def result():
    u"""
    与えられた文字列からグラフを作成し、ノード・エッジ・スコアをJSONとして返す
    """
    try:
        # データの取得
        # bottle.request.forms.get()はstrを返すのでdecodeする
        text = bottle.request.forms.get("text").decode("utf-8")
        if len(text) > MAX_TEXT_LENGTH:
            raise exception.IllegalRequestException(
                "text length over {0}".format(MAX_TEXT_LENGTH))

        # テキストを単語に分割して記号やストップワードを除く
        lang = bottle.request.forms.get("lang")
        if lang == "ja":
            words = gen_ja.generate_corpus(text)
        else:
            # 英語の場合は全て小文字化
            words = [w.lower() for w in gen_en.generate_corpus(text)]

        # TextRankオブジェクトの作成とTextRank計算
        tr = textrank.TextRank(words, window=NGRAM_WINDOW)
        nodes = tr.nodes()
        edges = tr.edges()
        scores = tr.scores(ndigit=SCORE_NDIGIT)

        # 結果をまとめる
        result = {
            "nodes": nodes,
            "edges": edges,
            "scores": scores}

        # Content-typeをJSONに指定
        bottle.response.content_type = 'application/json'
        return json.dumps(result)

    except Exception as e:
        # Content-typeをJSONに指定
        bottle.response.content_type = 'application/json'
        return json.dumps({"error": str(e)})


@bottle.get("/textrankdemo/<filepath:path>")
@bottle.auth_basic(check)
def static(filepath):
    u"""
    静的リソースを返す
    """
    return bottle.static_file(filepath, root="./static/")


@bottle.get("/textrankdemo/")
@bottle.auth_basic(check)
def home():
    u"""
    index.htmlを返す
    """
    return bottle.static_file("index.html", root="./static/")


if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
