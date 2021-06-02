# COVID19-Yamagata

- 山形県のオープンデータを使用して発表データのサマリーを公表しています。（随時）

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

### 例外データ

- データとして年代などの値がない(NULL)ものは対象外としている
  - 具体的なデータは[こちら](./images/exclusion_data.png)
    - `no` カラム == 山形県が発表している発表番号

## 2. 出力結果
 
