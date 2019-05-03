# Gambling

## 競艇
### データ準備

<u>これまでのレース結果</u>

boatRace_raceResults.csvがある状態で、race_result_crawler.pyを回す
 
<u>投票結果</u>
1. 投票結果を公式HPからダウンロードし、not yetフォルダにおく。

    not yet フォルダにおいたファイルを手動でコピペし、voting_result_katagiri.csvファイルをアップデート
    
2. motorboat_odds_crawlerを実行し、not yetフォルダに置かれたファイルに含まれるレースに関して、最終オッズを取得

    boatRace_odds.csvができる。ここまでやったらnot yetフォルダ内のファイルはalready crawled ファイルへ移動

<u>オッズ</u>
3. motorboat_summary_table_maker.pyを回す

### 自動bet
1. XXXX.pyを回し、crontab用の.shファイルを作成
2. .shファイルをcronに読み込ませ、automated_voterを適切な時間に実行させる

### 解析
- make_scatterPlot_raceResult.py
- simulate_race.py
