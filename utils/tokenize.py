# -*- encoding:utf-8 -*-
# stdlib
import re


class Tokenizer(object):
    u"""
    テキストからコーパスを作成
    """

    def __init__(self, lang="en"):
        u"""
        コンストラクタ
        言語を選択
        """
        if lang == "ja":
            self._setup_ja()
        else:
            self._setup_en()

    def _setup_en(self):
        u"""
        英語用の処理器をセットアップ
        """
        # 単語が含むべき文字
        _wchar = re.compile(r'[a-zA-Z]')
        self._isword = lambda w: _wchar.search(w)

        # ストップワード
        from stopen import isstop
        self._isstop = isstop

        # 単語分割
        from nltk.tokenize import sent_tokenize, word_tokenize

        def _tokenize(text):
            sents = sent_tokenize(text)
            words = [word_tokenize(s) for s in sents]
            return sum(words, [])

        self._tokenize = _tokenize

    def _setup_ja(self):
        u"""
        日本語用の処理器をセットアップ
        """
        # 単語が含むべき文字
        _wchar = re.compile(ur"[一-龠ぁ-ゔァ-ヴa-zA-Z]")
        self._isword = lambda w: _wchar.search(w)

        # ストップワード
        from stopja import isstop
        self._isstop = isstop

        # 単語分割
        from MeCab import Tagger
        from unicodedata import normalize
        tagger = Tagger()

        def _tokenize(text):
            # encodeしたものを変数に代入しておかないといけないらしい
            str_text = text.encode("utf-8")
            node = tagger.parseToNode(str_text)

            # リストにする
            word_list = []
            while node.next:
                node = node.next
                # ここでdecodeしておく
                word = node.surface.decode("utf-8")
                if word:
                    # NFKC正規化する
                    word_list.append(normalize("NFKC", word))

            return word_list

        self._tokenize = _tokenize

    def istoken(self, word):
        u"""
        単語が要素かを判定
        """
        return self._isword(word) and not self._isstop(word)

    def generate_corpus(self, text):
        u"""
        コーパスの生成
        """
        assert isinstance(text, unicode)
        return [w for w in self._tokenize(text) if self.istoken(w)]
