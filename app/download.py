#!/usr/bin/env python

import codecs
import pendulum
from urllib import request


def main():
    domain = "https://www.pref.yamagata.jp"

    now = pendulum.now(tz="Asia/Tokyo")
    tst_sfx = now.strftime("%m%d")
    pat_sfx = now.subtract(days=1).strftime("%m%d")

    covid_files_path = [
        f"/documents/10045/060003_yamagata_covid19_patients_{pat_sfx}.csv",
        f"/documents/10045/060003_yamagata_covid19_test_people_{tst_sfx}.csv",
    ]
    print(covid_files_path)
    save_files_path = ["./master_data/csv/patients_org.csv", "./master_data/csv/tests_org.csv"]

    # -- download patients data
    for idx, path in enumerate(covid_files_path):
        url = domain + path
        print(f"Downloading...{url}")
        file_data = request.urlopen(url).read()
        save_path = save_files_path[idx]
        save_path_utf8 = save_path.replace("_org", "")
        with open(save_path, "wb") as f:
            f.write(file_data)
        # -- sjis to utf-8 convert
        with codecs.open(save_path, "r", "shift_jis") as f_in:
            with codecs.open(save_path_utf8, "w", "utf-8") as f_out:
                for row in f_in:
                    f_out.write(row)


if __name__ == "__main__":
    main()
