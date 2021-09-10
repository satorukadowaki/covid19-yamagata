import pandas as pd
import pandas_bokeh
import numpy as np

# from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models import ColumnDataSource

from settings import SHONAI_CITIES, MURAYAMA_CITIES, MOGAMI_CITIES, OKITAMA_CITIES


def population_importer():
    raw_df = pd.read_excel("./master_data/population/r30801.xlsx")
    df_pop = raw_df.iloc[16:, 62:]  # 固定位置でスライス
    columns = [
        "市町村名",
        "総数",
        "男",
        "女",
        "自然動態_出生",
        "自然動態_死亡",
        "自然動態_増減",
        "社会動態_転入",
        "社会動態_転出",
        "社会動態_増減",
        "総増減",
        "世帯数",
        "世帯数_増減",
        # 'dummy_1', 'dummy_2'  # 月によってかわる
    ]
    df_pop.columns = columns
    # del df_pop['dummy_1']
    # del df_pop['dummy_2']
    df_pop = df_pop.dropna(how="all")
    df_pop["市町村名"] = df_pop["市町村名"].str.replace(" ", "", regex=False)
    df_pop["人口"] = df_pop["総数"].astype(int)
    df_pop["pop_per10"] = round(df_pop["人口"] / 100000, 2)

    # -- エリア設定
    shonai = SHONAI_CITIES
    df_pop.loc[df_pop["市町村名"].isin(shonai), "area"] = "庄内"
    murayama = MURAYAMA_CITIES
    df_pop.loc[df_pop["市町村名"].isin(murayama), "area"] = "村山"
    mogami = MOGAMI_CITIES
    df_pop.loc[df_pop["市町村名"].isin(mogami), "area"] = "最上"
    okitama = OKITAMA_CITIES
    df_pop.loc[df_pop["市町村名"].isin(okitama), "area"] = "置賜"

    # -- 市町村のリストに合わせて地方別に集計
    shonai_population = df_pop.loc[df_pop.area == "庄内"]["人口"].sum()
    murayama_population = df_pop.loc[df_pop.area == "村山"]["人口"].sum()
    mogami_population = df_pop.loc[df_pop.area == "最上"]["人口"].sum()
    okitama_population = df_pop.loc[df_pop.area == "置賜"]["人口"].sum()

    yamagata_all_population = (
        shonai_population + murayama_population + mogami_population + okitama_population
    )

    df_pop_ = df_pop[["市町村名", "人口", "pop_per10"]].copy()
    df_pop_ = df_pop_.reset_index(drop=True)

    return (
        df_pop,
        df_pop_,
        shonai_population,
        murayama_population,
        mogami_population,
        okitama_population,
        yamagata_all_population,
    )


if __name__ == "__main__":
    pandas_bokeh.output_file("population.html")
    (
        df_pop,
        df_pop_,
        shonai_population,
        murayama_population,
        mogami_population,
        okitama_population,
        yamagata_all_population,
    ) = population_importer()
    # Combine Table and Scatterplot via grid layout:
    # pandas_bokeh.plot_grid([[data_table]])
