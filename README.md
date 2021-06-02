# COVID19-Yamagata

- 山形県のオープンデータを使用して発表データのサマリーを公表しています。（随時）
- 出力は現在のところ画像になっていますが、いずれ再利用可能な状態にしたい(希望)

## 1. 前口上

### 1.1 データの取得元

- 時系列データ: [新型コロナウイルス感染症（COVID-19）について](https://www.pref.yamagata.jp/090016/bosai/kochibou/kikikanri/covid19/shingata_corona.html)
  - オープンデータとして提供されている 感染者属性 のCSVファイルを使用
  - 検査実施数は日付がズレているように見えるため信頼できないので今は使用していない（いずれ陽性率を計算したい）
  - 当日の発表データは手入力
- 人口データ: [山形県の人口と世帯数（推計）（令和3年5月1日現在）について](https://www.pref.yamagata.jp/020052/kensei/shoukai/toukeijouhou/jinkou/jinkm.html)
  - 人口データは 10万人あたりの感染者数を計算するために使用している
  - 4月時点のExcelデータを使用
    - 5月が出ていることをさっき知った
- プログラム
  - 開発言語: Python (jupyter, pandas+matplotlib)
  - ソースコード: いずれ公開（汚すぎるのでリファクタ後)
  - 計算結果のデータ: pickle 形式でいずれ公開

### 除外データ

- データとして年代などの値がない(NULL)ものは対象外としている
  - 具体的な除外データは[こちら](./images/exclusion_data.png)
    - `no` カラム == 山形県が発表している発表番号

## 2. 出力結果

### [直近2週間] 感染者報告数 (山形県)

![直近2週間の感染者報告数](./images/recent_2week_patients_bar.png)

### [直近2週間] 感染者報告数 (山形県地域別)

![直近2週間の感染者報告数_地域別](./images/14days_yamagata_patients_byday.png)

### [直近2週間] 感染者報告割合(年代別)

![直近2週間の感染者報告割合](./images/recent_2week_age_pie.png)

### [直近2週間] 感染者報告割合(地域別)

![直近2週間の感染者報告割合](./images/recent_2week_area_pie.png)



![直近1週間の地方別10万人あたりの感染者数](./images/7days_per_population_1week.png)
![直近1ヶ月の地方別7日間移動平均](./images/7days_rollingave_patients_1month.png)
![直近1週間の地方別10日間移動平均](./images/7days_rollingsum_1week.png)