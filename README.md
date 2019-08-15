# boatrace
競艇予想を行うプロジェクト


## Requirement
#### レポジトリのクローン

`git clone https://github.com/griCe14807/boatrace.git`

#### 必要なモジュールをインストール
```
pip3 install selenium
pip3 install pandas
```
#### ChromeDriverのインストール
Google Chronme のバージョンに対応したChromeDriverをインストール

- Google Chromeのバージョンは`google-chrome-stable -version`で確認

- Google Chromeのバージョンと対応するChromeDriverのバージョンの確認は下記url
(https://sites.google.com/a/chromium.org/chromedriver/downloads)

インストールしたGoogle Chromeに対応するversionをダウンロード（下のコード例では2.34）し、`/usr/local/bin/`へ移動

```
wget https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
```

## Demo
#### 過去のレースデータを用いた学習
```
$ python3 src/automated_voting/voting_algolithms/LR_analyzer.py
```
学習済みのclfは`"/Users/grice/mywork/boatrace/data/analysis/LR_dump"`
に保存される。


#### 学習結果を用いて指定したレース結果を予測
下の例では、2019年7月21日に戸田競艇場で行われる第11レースを予想。
クロールを行う関係上、展示タイムが表示されて以降（投票締め切りの10分前以降程度）に実行する必要あり
```
$ python3 src/automated_voting/voting_algolithms/LR_voter.py -rno 11R -jcd 戸　田 -hd 2019/07/21
```
アウトプットは、
- 1号艇の1着率
- 2-6号艇が3着以内に入る確率
- 推奨bet list (3連単)

## 使い方　応用編
### データ準備
※ `git clone` した場合，19年1月1日〜8月10日のデータがダウンロード済み。

※ロードしたデータフレームのカラム名とデータの対応は`\column_descriptions.xlsx`にまとめる.

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

### データロード
レース日・開催場所・レース番号をindexとし、レース結果や諸々の統計量をカラムにしたpandas dfを作成し、変数に格納

```
(in python)
import loader
df = race_results_loader
```

### 解析
準備したデータをロードし、解析を行う。

スクリプトは，共有しやすいよう
`./src/analyze/` 以下にipython notebookファイルとして保存．各ファイルの機能は下記。
 - `racertime_scatter_and_rank_bar.ipynb`: 対象レースに対して，出場レーサーのこれまでのタイムを散布図にplot
 - `k-NN.ipynb`: 一枠の選手が一着になるかどうかをk-NNを用いて予想．
 - `logistic_regression_1.ipynb`: LRを用いて1着の一位率および2-6艇の3着以内率を予測。また、Regression結果を用いて様々な条件でbetしてみた時の回収率を計算。
 -   `logistic_regression_2.ipynb`: 基本logistic_regression_1と同じだが、特徴量を増やした。`LR_analyzer`, `LR_voter`はこのアルゴリズムを用いている。

### 自動ベット
自分のID, passwardをスクリプトに直うちしているため共有なし