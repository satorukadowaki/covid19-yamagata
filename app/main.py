#!/usr/bin/env python

import pandas as pd
import pandas_bokeh
import numpy as np
import pendulum

from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models import ColumnDataSource
from datetime import datetime

from importer import importer
from population import population_importer

from settings import SHONAI_CITIES, MURAYAMA_CITIES, MOGAMI_CITIES, OKITAMA_CITIES

if __name__ == "__main__":
    now = pendulum.now(tz="Asia/Tokyo")
    page_title = f"COVID19-Yamagata({now.strftime('%Y-%m-%d')})"
    pandas_bokeh.output_file("index.html", title=page_title)

    # 元データの取込
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
    data_table = DataTable(source=data_source, columns=columns, width=800, height=500)

    # -- 無効データの表示
    ignore_data_source = ColumnDataSource(df_ignored)
    ignore_columns = [
        TableColumn(field="no", title="除外発表事例番号"),
        TableColumn(field="published_at", title="除外公表年月日", formatter=DateFormatter()),
    ]

    ignore_data_table = DataTable(
        source=ignore_data_source, columns=ignore_columns, width=300, height=300
    )

    # -- 人口データの読み込み
    (
        df_pop,
        df_pop_,
        shonai_population,
        murayama_population,
        mogami_population,
        okitama_population,
        yamagata_all_population,
    ) = population_importer()

    # -- 30日移動合計を表示
    # todo: 別ファイルに移す
    df_ts = pd.DataFrame()
    df_ts_shonai = pd.DataFrame()  # 庄内用
    df_ts_murayama = pd.DataFrame()  # 村山用
    df_ts_okitama = pd.DataFrame()  # 置賜用
    df_ts_mogami = pd.DataFrame()  # 最上
    today = pendulum.now(tz="Asia/Tokyo")
    range_days = 7
    for i in range(300, -1, -1):  #  30日のループ
        target = today.subtract(days=i)
        minus_1week = target.subtract(days=range_days).strftime("%Y-%m-%d")
        target_str = target.strftime("%Y-%m-%d")
        #     print(i, minus_2week, target)
        df_recent = df_csv.loc[
            (df_csv.published_at > minus_1week) & (df_csv.published_at <= target_str)
        ].copy()
        sr_sum = df_recent.patients_area.value_counts()
        df_sum = sr_sum.to_frame().reset_index()
        df_sum.columns = ["市町村名", "7日間の感染者数合計"]
        for area in ["庄内", "村山", "置賜", "最上"]:
            df_per10 = pd.merge(df_sum, df_pop_, on=["市町村名"], how="outer")
            # -- エリア設定
            if area == "庄内":
                df_per10.loc[df_per10["市町村名"].isin(SHONAI_CITIES), "area"] = area
                df_per10 = df_per10.dropna(how="any").reset_index(drop=True)
                df_per10["10万人あたりの感染者数"] = round(df_per10["7日間の感染者数合計"] / df_per10["pop_per10"], 2)
                df_per10["日付"] = target_str
                target_str = target_str.replace("2021-", "")
                sum_shonai_infect = df_per10["7日間の感染者数合計"].sum()
                df_ts = df_ts.append(
                    df_per10[["市町村名", "7日間の感染者数合計", "人口", "area", "10万人あたりの感染者数", "日付"]]
                )

                df_ts_shonai = df_ts_shonai.append(
                    [
                        {
                            "日付": target_str,
                            "jstdate": datetime.fromtimestamp(
                                target.timestamp()
                            ),  # pendulum.tz.timezone("Asia/Tokyo")
                            "10万人あたりの感染者数": round(
                                sum_shonai_infect / (shonai_population / 100000), 2
                            ),
                            "7日間の感染者数合計": sum_shonai_infect,
                        }
                    ]
                )
            elif area == "村山":
                df_per10.loc[df_per10["市町村名"].isin(MURAYAMA_CITIES), "area"] = area
                df_per10 = df_per10.dropna(how="any").reset_index(drop=True)
                df_per10["10万人あたりの感染者数"] = round(df_per10["7日間の感染者数合計"] / df_per10["pop_per10"], 2)
                df_per10["日付"] = target_str
                target_str = target_str.replace("2021-", "")
                sum_murayama_infect = df_per10["7日間の感染者数合計"].sum()
                df_ts = df_ts.append(
                    df_per10[["市町村名", "7日間の感染者数合計", "人口", "area", "10万人あたりの感染者数", "日付"]]
                )
                df_ts_murayama = df_ts_murayama.append(
                    [
                        {
                            "日付": target_str,
                            "jstdate": datetime.fromtimestamp(target.timestamp()),
                            "10万人あたりの感染者数": round(
                                sum_murayama_infect / (murayama_population / 100000), 2
                            ),
                            "7日間の感染者数合計": sum_murayama_infect,
                        }
                    ]
                )
            elif area == "置賜":
                df_per10.loc[df_per10["市町村名"].isin(OKITAMA_CITIES), "area"] = area
                df_per10 = df_per10.dropna(how="any").reset_index(drop=True)
                df_per10["10万人あたりの感染者数"] = round(df_per10["7日間の感染者数合計"] / df_per10["pop_per10"], 2)
                df_per10["日付"] = target_str
                target_str = target_str.replace("2021-", "")
                sum_okitama_infect = df_per10["7日間の感染者数合計"].sum()
                df_ts = df_ts.append(
                    df_per10[["市町村名", "7日間の感染者数合計", "人口", "area", "10万人あたりの感染者数", "日付"]]
                )
                target_str = target_str.replace("2021-", "")
                df_ts_okitama = df_ts_okitama.append(
                    [
                        {
                            "日付": target_str,
                            "jstdate": datetime.fromtimestamp(target.timestamp()),
                            "10万人あたりの感染者数": round(
                                sum_okitama_infect / (okitama_population / 100000), 2
                            ),
                            "7日間の感染者数合計": sum_okitama_infect,
                        }
                    ]
                )
            elif area == "最上":
                df_per10.loc[df_per10["市町村名"].isin(MOGAMI_CITIES), "area"] = area
                df_per10 = df_per10.dropna(how="any").reset_index(drop=True)
                df_per10["10万人あたりの感染者数"] = round(df_per10["7日間の感染者数合計"] / df_per10["pop_per10"], 2)
                df_per10["日付"] = target_str
                target_str = target_str.replace("2021-", "")
                sum_mogami_infect = df_per10["7日間の感染者数合計"].sum()
                df_ts = df_ts.append(
                    df_per10[["市町村名", "7日間の感染者数合計", "人口", "area", "10万人あたりの感染者数", "日付"]]
                )
                df_ts_mogami = df_ts_mogami.append(
                    [
                        {
                            "日付": target_str,
                            "jstdate": datetime.fromtimestamp(target.timestamp()),
                            "10万人あたりの感染者数": round(
                                sum_mogami_infect / (mogami_population / 100000), 2
                            ),
                            "7日間の感染者数合計": sum_mogami_infect,
                        }
                    ]
                )

    df_ts_shonai = df_ts_shonai.reset_index(drop=True)
    df_ts_murayama = df_ts_murayama.reset_index(drop=True)
    df_ts_okitama = df_ts_okitama.reset_index(drop=True)
    df_ts_mogami = df_ts_mogami.reset_index(drop=True)

    # -- todo: ここは正しくマージする
    df_ts_10d_movesum = pd.DataFrame()
    df_ts_10d_movesum["日付"] = df_ts_shonai["jstdate"].copy()
    # df_ts_10d_movesum["日付"] = df_ts_shonai["日付"].copy()
    shonai_col_title = f"庄内地方[人口{shonai_population}]"
    df_ts_10d_movesum[shonai_col_title] = df_ts_shonai["7日間の感染者数合計"].copy()
    murayama_col_title = f"村山地方[人口{murayama_population}]"
    df_ts_10d_movesum[murayama_col_title] = df_ts_murayama["7日間の感染者数合計"].copy()
    mogami_col_title = f"最上地方[人口{mogami_population}]"
    df_ts_10d_movesum[mogami_col_title] = df_ts_mogami["7日間の感染者数合計"].copy()
    okitama_col_title = f"置賜地方[人口{okitama_population}]"
    df_ts_10d_movesum[okitama_col_title] = df_ts_okitama["7日間の感染者数合計"].copy()
    df_ts_10d_movesum["日付_disp"] = df_ts_10d_movesum["日付"].dt.strftime("%Y-%m-%d").copy()
    df_ts_10d_movesum = df_ts_10d_movesum.set_index("日付")

    movesum_line = df_ts_10d_movesum.plot_bokeh(
        kind="line",
        figsize=(800, 600),
        title="[300days] 地方別感染者数10日間移動合計",
        xlabel="日付",
        ylabel="感染者数",
        # yticks=[0, 100, 200, 300, 400],
        # ylim=(100, 200),
        # xlim=("2021-05-01", "2021-08-01"),
        colormap=["red", "purple", "green", "orange"],
        plot_data_points=True,
        plot_data_points_size=5,
        marker="circle",
        show_figure=False,
    )
    movesum_10d_source = ColumnDataSource(df_ts_10d_movesum)
    columns = [
        TableColumn(field="日付_disp", title="日付"),
        TableColumn(field=shonai_col_title, title=shonai_col_title),
        TableColumn(field=murayama_col_title, title=murayama_col_title),
        TableColumn(field=mogami_col_title, title=mogami_col_title),
        TableColumn(field=okitama_col_title, title=okitama_col_title),
    ]

    movesum_table = DataTable(source=movesum_10d_source, columns=columns, width=300, height=600)
    pandas_bokeh.plot_grid(
        [
            [data_table, ignore_data_table],
            [movesum_line, movesum_table],
        ],
        # plot_width=1000,
        toolbar_location="right",
        # sizing_mode="fixed",
        toolbar_options=dict(logo="grey"),
    )
