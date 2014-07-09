// jQueryオブジェクトの取得
var form = $("#form");
var button = $("#button");
var container = $("#container");
var tbody = $("#list>tbody");
var sample = $("#sample");
var error = $("#error");

// レスポンスのオブジェクトからグラフを作成する関数
function draw(data) {
  // エラーがあれば表示
  if (data.error) {
    error.text(data.error);
  }

  // グラフを作成
  // グラフのエッジとノード
  var graphdata = {
    nodes: data.nodes,
    edges: data.edges
  };
  // グラフのオプション
  var options = {};
  // vis.Graph()の第一引数はjQueryオブジェクトではなくDOMオブジェクト
  var graph = new vis.Network(container.get(0), graphdata, options);

  // スコアを更新
  // 古いデータ行を削除
  $("tr.data").remove();
  // 新しいデータ行を追加
  var scores = data.scores;
  $.each(scores, function(i, obj) {
    var newtr = sample.clone().removeAttr("id").addClass("data");
    newtr.children("td:eq(0)").text(obj.label);
    newtr.children("td:eq(1)").text(obj.score);
    tbody.append(newtr);
  });
}

// フォームをPOSTする関数
function post() {
  $.post(
    "./result.json",
    form.serialize(),
    draw,
    "json"
  );
}

// ボタンをクリックするとテキストからグラフを作成
button.click(post);

// ドキュメントのロード時にグラフを作成
post();
