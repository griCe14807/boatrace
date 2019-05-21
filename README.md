# Gambling

### 使い方概要
下記のファイルを実行し、これまでのレース結果、oddsをクロールしておく
- rece_result_crawler
- motorboat_odds_crawler

クロールしてきたレースおよびオッズを元に、自動betを行う。
- crontab_generaterを実行し、printされた文字をcrontabにペースト。


### 使いかた詳細
#### 基礎データ準備
<u>これまでのレース結果</u>

boatRace_raceResults.csvがある状態で、race_result_crawler.pyを回す
 
<u>オッズ</u>
1. motorboat_summary_table_maker.pyを回す

<u>投票結果</u>
1. 投票結果を公式HPからダウンロードし、not yetフォルダにおく。

    not yet フォルダにおいたファイルを手動でコピペし、voting_result_katagiri.csvファイルをアップデート
    
2. motorboat_odds_crawlerを実行し、not yetフォルダに置かれたファイルに含まれるレースに関して、最終オッズを取得

    boatRace_odds.csvができる。ここまでやったらnot yetフォルダ内のファイルはalready crawled ファイルへ移動

#### simulationデータ作成
- simulate_race: シミュレーションした結果、各組番が来る確率をcsvに保存

#### 解析
- 190421_simulation_validater_1: ある期待値以上の組み番にbetした場合に、input期間の収支がどうなるかを計算。
- 190419_make_scatterPlot_raceResult.py: 特定のレースについて、過去の結果と今回の期待値を図示


### Projectの構造
src以下の各フォルダごとの役割の説明

#### analyze
解析用のソースコード置き場。これまでに行った解析は主に以下。
1. simulation
クロールしてきた過去の結果から、該当レースと同じ人かつ同じ枠のデータを抽出し、そのタイムデータを使ってレースのシミュレーションを行い、各組番のくる率を推定する。
2. XXX

#### automated_voting
自動投票に関連したスクリプトの保存場所

#### conf
全体に関わるconfファイルが置いてある。今の所、データファイルのパスを示したファイルのみ

#### crawl
crawlerの保存場所

#### supplement
その場で必要に迫られてとりあえず作成したスクリプトとか。ここはいつ消えても問題ないようなプロジェクト構造にしておく（リファーしない）


## 日記的記録
19年4月
- 新宿租界予想師の出す予想をオッズごとに切り分けて、回収率が高いオッズのところだけ乗ろうとした。偶然要素が大きすぎ、意味ない気がしてやめた。

19年5月上旬
- 過去の結果からレースをシミュレートし、オッズと合わせて期待値が基準を超える組番にbetしてみることに。大損。

19年5月中旬
- 租界予想に対してマーチンゲールで乗ることにし始める。新宿租界乗りの分が浮き始める。
