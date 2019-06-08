## How to use
#### データ準備
`./src/data_preparing/`以下の.pyファイル

1. `downloader_race_results.py`
を実行し、レース結果をダウンロード. ダウンロード先は`./boatrace/data/results_race/lzh`
2. ダウンロードしたデータを手動で解凍し、`./boatrace/data/results_race`フォルダへ移動
3. `race_results_loader`を実行し、ダウンロード、解凍したレース結果をdfにロード


#### 解析
1. 準備したデータをロード
2. 解析用のスクリプトを書きましょう！

`./src/analyze/` 以下の.pyファイル、例えば `racertime_scatter_and_rank_bar.py`などを参考に。

#### 自動ベット