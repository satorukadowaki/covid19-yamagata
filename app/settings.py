#!/usr/bin/env python

import os

# -- Server Configuration
LOG_FORMAT = "[%(asctime)s] [%(module)s:%(lineno)s] %(levelname)s %(message)s"

RELEASE_VERSION = os.environ.get("VERSION", "v0.0.1")
ENV_NAME = os.environ.get("ENV_NAME", "DEV")

SHONAI_CITIES = ["鶴岡市", "酒田市", "庄内町", "三川町", "遊佐町"]
MOGAMI_CITIES = ["鮭川村", "新庄市", "最上町", "金山町", "真室川町", "戸沢村", "大蔵村", "舟形町"]
OKITAMA_CITIES = ["小国町", "白鷹町", "飯豊町", "長井市", "南陽市", "川西町", "高畠町", "米沢市"]
MURAYAMA_CITIES = [
    "山形市",
    "寒河江市",
    "天童市",
    "東根市",
    "上山市",
    "山辺町",
    "中山町",
    "尾花沢市",
    "村山市",
    "朝日町",
    "大江町",
    "河北町",
    "大石田町",
    "西川町",
]
