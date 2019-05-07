# Gambling

## 競艇
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
