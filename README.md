# boatrace
競艇予想を行うプロジェクト


## Requirement
#### レポジトリのクローン

`git clone https://github.com/griCe14807/boatrace.git`

#### 必要なモジュールをインストール
```
pip3 install selenium
pip3 install pandas
pip3 install scikit-learn
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
学習済みのclfは`"src/automated_voting/voting_algolithms/LR_dump"`
に保存される。


#### 学習結果を用いて指定したレース結果を予測
下の例では、2019年7月21日に戸田競艇場で行われる第11レースを予想。
クロールを行う関係上、展示タイムが表示されて以降（投票締め切りの10分前以降程度）に実行する必要あり
```
$ python3 src/automated_voting/voting_algolithms/LR_voter.py -rno 11R -jcd 戸　田 -hd 2019/07/21
```

アウトプットは、

- [1号艇の1着率, 2-6号艇が3着以内に入る確率]

    例：[0.60, 0.68, 0.64, 0.49, 0.21, 0.17]

- 推奨bet list (3連単). 推奨betがない場合空のリストが返される

    例：["1-2-3", "1-2-4"]

デフォルトでは、1号艇の1着率が0.6以上、2号艇の3位以内率が0.5以上かつ3-6号艇の中で3着以内率0.5以上のものiがあった場合に2-1-iの形で3連単bet

## 使い方　応用編
### データ準備
※ロードしたデータフレームのカラム名とデータの対応は`\column_descriptions.xlsx`にまとめる.

##### レース結果
###### レース結果をダウンロード
```
$ src/data_preparing/downloader_race_results.py
```
- ダウンロード元: `http://www1.mbrace.or.jp/od2/K/dindex.html`
- ダウンロード先: `data/results_race/lzh`

※ `git clone` した場合，19年1月1日〜8月17日のデータがダウンロード済み。

###### ダウンロードしたデータを手動で解凍
###### `./boatrace/data/results_race`フォルダへ移動
##### 選手情報
`https://www.boatrace.jp/owpc/pc/extra/data/download.html`からレーサー期別成績をダウンロード（手動）し，`data\racer`へ格納
- 年に二回、4月〜10月分と11月から3月分のデータがまとめてアップロードされるため、そのたびに追加。

※ `git clone` した場合，19年4月までのデータがダウンロード済み。

##### モーター・ボートおよび直近の成績
1. `motor_data_csv_maker`を実行. 下の例では8/15から8/17までcrawlし、csv形式で保存する
```bash
$ python3 src/data_preparing/race_result_supplement_csv_maker.py -s 20190815 -e 20190818
```
- crawl元: 公式HP出走表 (例：'https://boatrace.jp/owpc/pc/race/racelist?rno=6&jcd=01&hd=20190816')
- 保存先: `data/motor_and_boat`

※ `git clone` した場合，19年1月1日〜8月15日のデータがダウンロード済み。

### データロード
レース日・開催場所・レース番号をindexとし、レース結果や諸々の統計量をカラムにしたpandas dfを作成

```
(in python)
import loader
df = loader.main()
```

### 解析
準備したデータをロードし、解析を行う。

スクリプトは，共有しやすいよう
`src/analyze/` 以下にipython notebookファイルとして保存．
これまでに行った解析は下記
 - `racertime_scatter_and_rank_bar.ipynb`: 対象レースに対して，出場レーサーのこれまでのタイムを散布図にplot
 - `k-NN.ipynb`: 一枠の選手が一着になるかどうかをk-NNを用いて予想．
 - `logistic_regression_1.ipynb`: LRを用いて1着の一位率および2-6艇の3着以内率を予測。また、Regression結果を用いて様々な条件でbetしてみた時の回収率を計算。
 -   `logistic_regression_2.ipynb`: 基本logistic_regression_1と同じだが、特徴量を増やした。`LR_analyzer`, `LR_voter`はこのアルゴリズムを用いている。

### 自動ベット
※自分のID, passwardをスクリプトに直うちしているため共有なし

crontab用のスクリプトを作成
```
crontab_generater を実行
```

printされたものを`crontab -e`にコピペ（手動）

これで、`automated_voter`が定期的に実行される。