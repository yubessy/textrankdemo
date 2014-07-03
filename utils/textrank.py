# -*- coding: utf-8 -*-
# third-party lib
import networkx


def ngram(items, window=2):
    u"""
    N-gramを生成
    """
    return [tuple(items[i:i+window]) for i in range(len(items)-window+1)]


def comb(items):
    u"""
    組み合わせを生成
    """
    return list(set([(x, y) for x in items for y in items if x > y]))


class TextRank(object):
    def __init__(self, words, window=2):
        u"""
        コンストラクタ
        与えられた単語リストからグラフを生成
        """
        # 各単語にIDを付与し、ID: 単語と単語: IDの辞書を作成
        self._id2l = {i: w for i, w in enumerate(set(words))}
        self._l2id = {w: i for i, w in self._id2l.items()}

        # idを使ってグラフを作成
        ids = [self._l2id[w] for w in words]
        self._graph = networkx.Graph()
        ng = ngram(ids, window)
        for ng_unit in ng:
            edges = comb(ng_unit)
            self._graph.add_edges_from(edges)
        self._scores = networkx.pagerank(self._graph)

    def nodes(self):
        u"""
        ノードのリスト
        [{"id": id, "label": label}]
        を返す
        """
        return [{"id": i, "label": self._id2l[i]} for i in self._graph.nodes()]

    def edges(self):
        u"""
        エッジのリスト
        [{"from": from_id, "to": to_id}]
        を返す
        """
        return [{"from": f, "to": t} for f, t in self._graph.edges()]

    def scores(self, ndigit=6):
        u"""
        スコアのリスト
        [{"label": label, "score": score}]
        を返す
        """
        f = lambda i, s: {"label": self._id2l[i], "score": round(s, ndigit)}
        scores = [f(i, s) for i, s in self._scores.items()]
        return sorted(scores, key=lambda d: d["score"], reverse=True)
