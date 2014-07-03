# TextRank Demo

Demonstration of TextRank Algorithm

[Original paper](http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf "TextRank: Bringing order into texts")

***

TextRankアルゴリズムのデモ

[元論文](http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf "TextRank: Bringing order into texts")

日本語と英語の両方で動きます。
TextRankの仕組みを視覚的に理解したかったので作りました。

何に使えるのかわかりませんがとりあえず公開。

# Requirements

めっちゃいろいろなものに依存してます。

## Python libraries

* bottle
* networkx
* nltk
* MeCab

## JavaScript Library

* jQuery
* vis.js

# Usage

```shell-session
$ python main.py
```

# Passwords

BASIC認証をかけるため、`secret.py`を用意する必要があります。

```python
# -*- coding: utf-8 -*-

USERNAME = "username" # ユーザ名
PASSWORD = "password" # パスワード
```
