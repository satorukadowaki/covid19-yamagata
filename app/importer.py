import pandas as pd
import pandas_bokeh
import numpy as np

# from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models import ColumnDataSource


def importer():
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
        "./master_data/csv/yamagata_patients.csv",
        na_values=["−"],
        # dtype={}
        names=column_names,
        skiprows=1,
    )

    df_ignored = df_csv.loc[
        (df_csv.published_at.isnull())
        | (df_csv.infected_at.isnull())
        | (df_csv.patients_area.isnull())
        | (df_csv.patients_age.isnull())
        | (df_csv.patients_sex.isnull())
    ].copy()

    ## 使用しないフィールドを削除
    # del df_csv['no']
    del df_csv["code"]
    del df_csv["prefecture"]
    df_csv = df_csv.dropna(how="any")

    # -- 当日発表分の入力
    published_at = "2021/06/19"
    infected_at = "2021/06/18"
    recent_published_datum = [
        #     {"no": 2024, "patients_area": "天童市", "patients_age": "40代", "patients_sex": "男性", "infected_at": infected_at, "published_at": published_at},
        #     {"no": 2025, "patients_area": "山形市", "patients_age": "80代", "patients_sex": "女性", "infected_at": infected_at, "published_at": published_at},
        #     {"no": 2026, "patients_area": "山形市", "patients_age": "60代", "patients_sex": "男性", "infected_at": infected_at, "published_at": published_at},
    ]
    df_csv = df_csv.append(recent_published_datum).reset_index(drop=True)

    # -- 発表日と感染確認日を日付型に変換
    df_csv["published_at"] = pd.to_datetime(
        df_csv["published_at"], format="%Y/%m/%d", infer_datetime_format=True
    )
    df_csv["infected_at"] = pd.to_datetime(
        df_csv["infected_at"], format="%Y/%m/%d", infer_datetime_format=True
    )

    return df_csv, df_ignored


if __name__ == "__main__":
    pandas_bokeh.output_file("importdatatable.html")
    df_csv, df_ignored = importer()
    data_source = ColumnDataSource(df_csv)
    columns = [
        TableColumn(field="no", title="発表事例番号"),
        TableColumn(field="published_at", title="公表年月日", formatter=DateFormatter()),
        TableColumn(field="infected_at", title="感染確認日", formatter=DateFormatter()),
        TableColumn(field="patients_area", title="患者居住地"),
        TableColumn(field="patients_age", title="患者年代"),
        TableColumn(field="patients_sex", title="患者性別"),
    ]
    data_table = DataTable(source=data_source, columns=columns, width=700, height=500)

    # Combine Table and Scatterplot via grid layout:
    pandas_bokeh.plot_grid([[data_table]])
