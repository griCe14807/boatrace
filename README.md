競艇のデータ解析をするためのプロジェクト

## How to use
### Demo

`git clone https://github.com/griCe14807/boatrace.git`

jupyter notebookを用いて，下記のファイルを実行．

`racertime_scatter_and_rank_bar.ipynb`: 対象レースに対して，出場レーサーのこれまでのタイムを散布図にplot

`src/analysis/k-NN.ipynb`: 一枠の選手が一着になるかどうかをk-NNを用いて予想．


### データ準備
※ `git clone` した場合は，上記ディレクトリにもともと19年1月から6月までのデータがダウンロードしてあります．
- レース結果
1. `downloader_race_results.py`
を実行し、レース結果をダウンロード. 
    - ダウンロード元: `http://www1.mbrace.or.jp/od2/K/dindex.html`
    - ダウンロード先: `./boatrace/data/results_race/lzh`
2. ダウンロードしたデータを手動で解凍し、`./boatrace/data/results_race`フォルダへ移動
3. `race_results_loader`を実行し、レース結果をdfにロード
- 選手情報
1. `https://www.boatrace.jp/owpc/pc/extra/data/download.html`からレーサー期別成績をダウンロード（手動）し，`.boatrace\data\racer`へ格納
2. `race_results_loader.`を実行し，レース結果をdfにロード

※ロードしたデータフレームのカラム名とデータの対応は`\column_descriptions.xlsx`にまとめられている.

※ `race_results_loader` には，レース結果のみをロードする`load_race_results`, 
レーサー情報のみをロードする`load_racer_data`もありますが，
実際に使うのはほぼ`make_merged_df`のみです．使い方は`.boatrace/src/analyze/k-NN.ipynb`を参照．

### 解析
1. 準備したデータをロード
2. 解析用のスクリプトを書きましょう！

スクリプトは，共有しやすいよう
`./src/analyze/` 以下にipython notebookファイルとして保存．下記ファイルを参考にしてください．
 - `racertime_scatter_and_rank_bar.ipynb`: 対象レースに対して，出場レーサーのこれまでのタイムを散布図にplot
 - `k-NN.ipynb`: 一枠の選手が一着になるかどうかをk-NNを用いて予想．
 

### 自動ベット
自分のID, passwardをスクリプトに直うちしているため共有なしで笑

必要とあらば書き直して共有します．