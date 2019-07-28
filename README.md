競艇のデータ解析をするためのプロジェクト

## How to use
### Demo

レポジトリのクローン

`git clone https://github.com/griCe14807/boatrace.git`

実行ファイルのあるフォルダへ移動

`$ cd ./boatrace/src/automated_voting/voting_algolithms`

レース予測を実行
```
$ python3 LR_analyzer.py
$ python3 LR_voter.py -rno 11R -jcd 戸　田 -hd 2019/07/21
```
- １行目でLogistic regressionを用いた学習を行い、2行目でそれを用いて実際にbet
- 学習は初めの一回のみ行えば良い。
- この例では、2019年7月21日に戸田競艇場で行われる第11レースを予想。

### データ準備
※ `git clone` した場合は，上記ディレクトリにもともと19年1月から6月までのデータがダウンロードしてあります．
##### レース結果
1. `downloader_race_results.py`
を実行し、レース結果をダウンロード. 
    - ダウンロード元: `http://www1.mbrace.or.jp/od2/K/dindex.html`
    - ダウンロード先: `./boatrace/data/results_race/lzh`
2. ダウンロードしたデータを手動で解凍し、`./boatrace/data/results_race`フォルダへ移動
##### 選手情報
1. `https://www.boatrace.jp/owpc/pc/extra/data/download.html`からレーサー期別成績をダウンロード（手動）し，`.boatrace\data\racer`へ格納
##### モーターおよびボートのデータ
1. `motor_data_csv_maker`を実行し、データをcrawl
    - crawl元: 公式HP ('https://boatrace.jp/owpc/pc/race/')
    - 保存先: `./boatrace/data/motor_and_boat`

※ロードしたデータフレームのカラム名とデータの対応は`\column_descriptions.xlsx`にまとめる.

### データロード
`race_results_loader`を実行し、レース結果をdfにロード
※ `race_results_loader` には，レース結果のみをロードする`load_race_results`, 
レーサー情報のみをロードする`load_racer_data`もありますが，
実際に使うのはほぼ`make_merged_df`のみ．

### 解析
1. 準備したデータをロード
2. 解析用のスクリプトを書きましょう！

スクリプトは，共有しやすいよう
`./src/analyze/` 以下にipython notebookファイルとして保存．下記ファイルを参考にしてください．
 - `racertime_scatter_and_rank_bar.ipynb`: 対象レースに対して，出場レーサーのこれまでのタイムを散布図にplot
 - `k-NN.ipynb`: 一枠の選手が一着になるかどうかをk-NNを用いて予想．
 

### 自動ベット
解析した結果を元に、実用化できそうなアルゴリズムは
自分のID, passwardをスクリプトに直うちしているため共有なしで笑

必要とあらば書き直して共有します．


## 自分用メモ
