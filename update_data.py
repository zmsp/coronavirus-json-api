import csv
import json
import datetime
import requests
import hashlib
import sys
import numpy as np
import pandas as pd
import pycountry
CSV_PATH = "./latest.csv"
JSON_PRETTY_PATH = "./latest_pretty_print.json"
JSON_PATH = "./latest.json"
MD5_FILE_PATH = "./MD5.txt"
README_PATH = "./README.md"
META_FILE = "./metadata.json"
META_PRETTY_FILE = "./metadata_pretty_print.json"


def dumpCsvToJson(CSV_FILE):

    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        reader = csv.DictReader(f, headers)
        out = json.dumps([row for row in reader])
    with open('latest.json', "w") as f:
        f.write(out)
def dumpMetaData(CSV_FILE):
    csvData=pd.read_csv(CSV_FILE, sep=',')
    f=csvData.copy()
    f["Last Update"] = pd.to_datetime(f["Last Update"])
    placeholder = "null";
    data = {}
    for i in f.columns:
        type = f[i].dtypes.name
        max = ""
        min = ""
        mean = ""
        median = ""
        std = ""
        total = ""
        unique = []
        if np.issubdtype(f[i].dtype, np.number):
            max =f[i].max().__str__()
            min =f[i].min().__str__()
            mean = f[i].mean().__str__()
            median =f[i].median().__str__()
            std = f[i].std().__str__()
            total =  f[i].sum().__str__()
        elif np.issubdtype(f[i].dtype, np.datetime64):
            max =f[i].max().__str__()
            min =f[i].min().__str__()
            mean = f[i].mean().__str__()
        elif np.issubdtype(f[i].dtype, np.object):
            unique = f[i].fillna("NaN").unique().tolist()

        data[i] = {"max":max, "min":min, "median":median, "mean":mean, "std":std, "unique": unique, "total":total}

    country_meta = {
    }

    for name in f["Country/Region"].unique():
        try:
            i = name
            correction = {"Mainland China": "China", "South Korea": "Korea, Democratic", "Macao": "Macao"}

            if correction.__contains__(name):
                country = pycountry.countries.search_fuzzy(correction[i])[0]
            else:
                country = pycountry.countries.search_fuzzy(i)[0]

            country_meta[i] = {"name": country.name, "alpha_2": country.alpha_2, "alpha_3": country.alpha_3}
        except:
            country_meta[i] = {"name":i, "alpha_2":"XX", "alpha_3":"XXX"}
    md5 = md5Checksum(CSV_FILE,None)

    meta_data = {
        "country_meta": country_meta,
        "columns_name": f.columns.unique().tolist(),
        "columns_meta": data,
        "data_meta": {"md5":md5, "updated":datetime.datetime.now().strftime('%d %B, %Y  %H:%M:%S')}
    }
    out = json.dumps(meta_data)
    with open(META_FILE, "w") as f:
        f.write(out)
    out = json.dumps(meta_data, sort_keys=True, indent=2, separators=(',', ':'))
    with open(META_PRETTY_FILE, "w") as f:
        f.write(out)







def dumpCsvToJsonPrettyPrint(CSV_FILE):
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        reader = csv.DictReader(f, headers)
        out = json.dumps([row for row in reader], sort_keys=True, indent=2, separators=(',', ':'))
    with open(JSON_PRETTY_PATH, "w") as f:
        f.write(out)

def md5Checksum(filePath,url):
    m = hashlib.md5()
    if url==None:
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    else:
        r = requests.get(url)
        for data in r.iter_content(8192):
             m.update(data)
        return m.hexdigest()

def update_readme(first_line):
    with open(README_PATH) as f:
        lines = f.readlines()
    lines[0] =first_line
    with open(README_PATH, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":


    today = datetime.datetime.now()+datetime.timedelta(days=1)
    template_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{DATE}.csv"
    CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))

    status_code =0
    while( status_code != 200):
        CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))
        r = requests.get(CSV_URL)
        status_code = r.status_code
        today = today - datetime.timedelta(days=1)
    with open(CSV_PATH, 'wb') as f:
        f.write(r.content)

    with open(MD5_FILE_PATH, 'r') as file:
        local_md5 = file.read().replace('\n', '')

    latest_md5 = md5Checksum(CSV_PATH, None)
    if (latest_md5 != local_md5):
        dumpCsvToJson(CSV_PATH)
        dumpCsvToJsonPrettyPrint(CSV_PATH)
        dumpMetaData(CSV_PATH)
        with open(MD5_FILE_PATH, 'w') as file:
            file.write(latest_md5)
        update_readme("# Novel Coronavirus JSON data (Updated: {UPDATED}) \n".format(UPDATED=datetime.datetime.now().strftime('%d %B, %Y  %H:%M:%S')))
        print("updated")
    else:
        sys.exit('Local file is the latest, nothing was updated')




