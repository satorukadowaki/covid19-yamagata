#!/usr/bin/env python

import codecs
import pendulum
from urllib import request


def main():
    domain = "https://www.pref.yamagata.jp"

    now = pendulum.now(tz="Asia/Tokyo")
    tst_sfx = now.strftime("%y%m%d")
    pat_sfx = now.subtract(days=1).strftime("%y%m%d")

    covid_files_path = [
        # f"/documents/10045/060003_yamagata_covid19_patients_{pat_sfx}.csv",
        f"/documents/10045/060003_yamagata_covid19_patients_{tst_sfx}.csv",
        f"/documents/10045/060003_yamagata_covid19_test_people_{tst_sfx}.csv",
    ]

    # -- 感染者数0だと過去に遡る必要があるので20日分くらい作っておく
    for i in range(1, 20):
        pat_sfx = now.subtract(days=i).strftime("%y%m%d")
        covid_files_path.append(f"/documents/10045/060003_yamagata_covid19_patients_{pat_sfx}.csv")

    for i in range(1, 10):
        pat_sfx = now.subtract(days=i).strftime("%y%m%d")
        covid_files_path.append(
            f"/documents/10045/060003_yamagata_covid19_test_people_{pat_sfx}.csv"
        )

    save_files_path = ["./master_data/csv/patients_org.csv", "./master_data/csv/tests_org.csv"]

    is_dl_patient = False
    is_dl_test = False
    # -- download patients data
    for idx, path in enumerate(covid_files_path):
        url = domain + path
        if "patients" in url and is_dl_patient:
            continue
        if "test" in url and is_dl_test:
            continue
        # print(f"[Downloading]...{url}")
        try:
            file_data = request.urlopen(url).read()
            print(f"[Download Succeeded]: {url}")
        except:
            print(f"[Download Failed]: {url}")
            continue
        if "patients" in path:
            save_path = save_files_path[0]
            is_dl_patient = True
        else:
            save_path = save_files_path[1]
            is_dl_test = True
        save_path_utf8 = save_path.replace("_org", "")
        with open(save_path, "wb") as f:
            f.write(file_data)
        # -- sjis to utf-8 convert
        with codecs.open(save_path, "r", "shift_jis") as f_in:
            with codecs.open(save_path_utf8, "w", "utf-8") as f_out:
                for row in f_in:
                    f_out.write(row)

        # -- 患者のデータは取れたらやめる
        if is_dl_patient and is_dl_test:
            break


if __name__ == "__main__":
    main()
