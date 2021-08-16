#!/usr/bin/env python

import codecs
from urllib import request


def main():
    domain = "https://www.pref.yamagata.jp"
    covid_files_path = [
        "/documents/10045/060003_yamagata_covid19_patients_0815.csv",
        "/documents/10045/060003_yamagata_covid19_test_people_0816.csv",
    ]
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
