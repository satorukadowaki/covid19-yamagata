#!/usr/bin/env python

import pandas as pd
import numpy as np
import pendulum
import pdb

from datetime import datetime


def filler():
    now = pendulum.now(tz="Asia/Tokyo")
    excel_file = "./master_data/excel/yamagata_covid.xlsx"
    csv_file = "./master_data/csv/yamagata_patients.csv"

    # -- csv データの最終行から行番号を取得
    column_names = [
        "no",  # 発表事例No.
        "code",  # 全国地方公共団体コード
        "prefecture",  # 都道府県名
        "published_at",  # 公表年月日
        "infected_at",  # 感染確認年月日
        "patients_area",  # 患者居住地
        "patients_age",  # 患者年代
        "patients_sex",  # 患者性別
    ]
    df_csv = pd.read_csv(
        csv_file,
        na_values=["−"],
        names=column_names,
        skiprows=1,
    )
    last_no = int(df_csv.iloc[-1]["no"])

    # -- init: 出力用CSVに合わせて初期値を用意しておく
    pref_code = "060003"
    pref_name = "山形県"
    # publish_date = now.subtract(days=1).strftime("%Y/%-m/%-d")
    # infected_date = now.subtract(days=2).strftime("%Y/%-m/%-d")  # today - 1day
    publish_date = now.strftime("%Y/%-m/%-d")
    infected_date = now.subtract(days=1).strftime("%Y/%-m/%-d")  # today - 1day

    # 元データの取込
    padding_rows = []
    df = pd.read_excel(excel_file)
    df = df.dropna(subset=["市町村"])  # 不要な行を削除
    for key, row in df.iterrows():
        valid_row = row.dropna()
        municipal_name = valid_row["市町村"]
        for idx in valid_row.index:  # 有効なカラムからCSVを作る
            if idx in ["市町村", "合計"]:
                continue
            age, sex = idx.split(",")
            sex += "性"
            for i in range(int(row[idx])):
                last_no += 1
                padding_rows.append(
                    {
                        "no": last_no,
                        "pref_code": pref_code,
                        "pref_name": pref_name,
                        "publish_date": publish_date,
                        "infetcted_date": infected_date,
                        "municipal_name": municipal_name,
                        "age": age,
                        "sex": sex,
                    }
                )

    df_pad = pd.DataFrame(padding_rows)
    print(df_pad.to_csv(index=False))


if __name__ == "__main__":
    filler()
