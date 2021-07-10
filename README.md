# COVID19-Yamagata (2021-07-10)

- 山形県のオープンデータを使用して発表データのサマリーを公表しています。（随時）
   - 県内全般の内容と庄内地方のデータを掲載しています。
- 出力は現在のところ画像になっていますが、いずれ再利用可能な状態にしたい(希望)
- 2021-06-27 追記
   - github上の画像プロットをグラフライブラリ Bokeh を使用したチャートに変更中です。
   - 元データのテーブルと移動合計をサンプル的にリリースしました。
       - https://covid19-yamagata.vercel.app/

## 1. 前口上

### 1.1 データの取得元

- 時系列データ: [新型コロナウイルス感染症（COVID-19）について](https://www.pref.yamagata.jp/090016/bosai/kochibou/kikikanri/covid19/shingata_corona.html)
  - オープンデータとして提供されている 感染者属性 のCSVファイルを使用
  - 検査実施数は日付がズレているように見え、信頼できないため今は使用していない（いずれ陽性率を計算したいかも...）
  - 当日の発表データは手入力
- 人口データ: [山形県の人口と世帯数（推計）（令和3年5月1日現在）について](https://www.pref.yamagata.jp/020052/kensei/shoukai/toukeijouhou/jinkou/jinkm.html)
  - 人口データは 10万人あたりの感染者数を計算するために使用している
  - 令和3年5月時点のExcelデータを使用 (2021-06-04)
- プログラム
  - 開発言語: Python 3.8.5 (Conda: jupyter, pandas+matplotlib)
  - ソースコード: いずれ...（リファクタ中)
  - 計算結果のデータ: いずれ...

### 除外データ

- データとして年代などの値がない(NULL)ものは対象外としている
  - 具体的な除外データは[こちら](./images/exclusion_data.png)
    - `no` カラム == 山形県が発表している発表番号

## 2. 出力結果

- Remarks (2021-07-03)
  - 移動平均ではなく移動合計を最初に掲載するように変更しました。
    - 感染者数が少ない場合により少なく見えてしまうため

### 直近1ヶ月の地方別10日間移動合計

![直近1ヶ月の地方別10日間移動合計](./images/10days_rollingsum_patients_1month.png)

<details>
<summary>直近2週間分だけのグラフはこちらに</summary>
<img src="./images/10days_rollingsum_patients_2week.png"></img>
</details>


### [直近2週間] 感染者報告数 (山形県)

![直近2週間の感染者報告数](./images/recent_2week_patients_bar.png)

### [直近2週間] 感染者報告数 (地方別)

![直近2週間の感染者報告数_地域別](./images/14days_yamagata_patients_byday.png)

####  [直近1週間] 地方別10万人あたりの感染者数

![直近1週間の地方別10万人あたりの感染者数](./images/7days_per_population_1week.png)

### [直近2週間] 感染者報告割合(年代別)

![直近2週間の感染者報告割合](./images/recent_2week_age_pie.png)

### [直近2週間] 感染者報告割合(地方別)

![直近2週間の感染者報告割合](./images/recent_2week_area_pie.png)

### 庄内地方

- [直近2週間] 庄内市町村別の感染報告

![直近2週間庄内市町村別感染報告](./images/14days_shonai_patients_byday.png)

- 上記グラフのテーブルビューとメモ

![直近2週間庄内市町村別感染報告表](./images/14days_shonai_table_view.png)

- [直近2週間] 庄内市町村別14日間移動合計
  - 感染者数報告がゼロのときにプロットされない問題を修正しました(20210-06-26)

![直近2週間庄内市町村別14日間移動合計](./images/14days_rollingsum_patients_shonai_area.png)

### その他参考的に出力しているもの

#### [直近1ヶ月] 地方別7日間移動平均

- プロットが飛んだり、移動平均が計算できない場合に描画されない問題を修正 (2021-06-05), 県内がゼロの場合の問題を修正 2021-06-13, 2021-06-26再修正)

![直近1ヶ月の地方別7日間移動平均](./images/7days_rollingave_patients_1month.png)

#### [直近1週間] 地方別7日間移動合計

![直近1週間 地方別7日間移動合計](./images/7days_rollingsum_1week.png)

- [直近2週間] 庄内地方10万人あたりの感染者数

![直近2週間 庄内地方10万人あたりの感染者数](./images/14days_per_population_shonai.png)

- [直近2週間] 庄内市町村別10万人あたりの感染者数
  - プロットされていない部分は2週間以上感染者報告がないことを示す

![直近2週間 庄内市町村別10万人あたりの感染者数](./images/14days_per_population_shonai_area.png)

#### [直近30日] 検査数の時系列 (日別の検査数と検査数の7日間移動平均)

![直近30日 日別の検査数と移動平均](./images/7days_rollingave_with_tests_30days.png)

#### 前年との比較(7日間移動平均を60日分で重ねて比較)

- 過去分は少し先の日付まで描画するように修正(2021-07-02)

![昨年同時期の移動平均との比較](./images/7days_rollingave_patients_100days.png)

- [全期間] 感染者報告割合(地方別)

![全期間 地方別感染者報告割合](./images/all_range_area_pie.png)

- [全期間] 感染者報告割合(年代別)

![全期間年代別感染者報告割合](./images/all_range_age_pie.png)

## 3. ToDo (以下は個人的なメモ)

- 特徴抽出を追加予定
  - 以下のような同様のケースを抽出するロジックを追加する

![期間比較](./images/compare.png)

- 簡易的な実行再生算数の計算(東洋経済を参考に)
  - https://toyokeizai.net/articles/-/351826?page=3
  - 計算式の抜粋
    - 実効再生産数=（直近7日間の新規陽性者数／その前の7日間の新規陽性者数）^（平均世代時間／報告間隔）
    - メモコピー: 平均世代時間とは、「感染源の感染から2次感染者の感染までに要する平均時間」を指す。東洋経済オンラインでの計算では、西浦教授のアドバイスに沿って5（日）をデータに使っている。報告間隔は7（日）だ。

- 山形県のオープンデータコンテストへの応募 (7/19までに提出する。締め切りは 7/26)
  - https://www.pref.yamagata.jp/020051/kensei/shoukai/toukeijouhou/tokeijoho-opendate/opendata/opendatacontest.html
  - 県民の意見に送った回答へのダメ出しも入れる

