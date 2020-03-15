import csv
import json
import datetime
import requests
import hashlib
import sys
import numpy as np
import pandas as pd
import pycountry

JSON_PRETTY_PATH = "./latest_pretty_print.json"
JSON_PATH = "./latest.json"

README_PATH = "./README.md"
META_FILE = "./metadata.json"
META_PRETTY_FILE = "./metadata_pretty_print.json"

DOWNLOAD_PATH = "./csse_covid_19_data/"
DOWNLOAD_INFO_FILE = DOWNLOAD_PATH + "download_info.json"


class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

country_dict = []


def dumpCsvToJson(CSV_FILE):
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        reader = csv.DictReader(f, headers)
        out = json.dumps([row for row in reader])
    with open('latest.json', "w") as f:
        f.write(out)


def dumpMetaData(CSV_FILE):
    csvData = pd.read_csv(CSV_FILE, sep=',')
    f = csvData.copy()
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
            max = f[i].max().__str__()
            min = f[i].min().__str__()
            mean = f[i].mean().__str__()
            median = f[i].median().__str__()
            std = f[i].std().__str__()
            total = f[i].sum().__str__()
        elif np.issubdtype(f[i].dtype, np.datetime64):
            max = f[i].max().__str__()
            min = f[i].min().__str__()
            mean = f[i].mean().__str__()
        elif np.issubdtype(f[i].dtype, np.object):
            unique = f[i].fillna("NaN").unique().tolist()

        data[i] = {"max": max, "min": min, "median": median, "mean": mean, "std": std, "unique": unique, "total": total}

    country_meta = {
    }
    correction = {"Mainland China": "China", "Korea, South": "Korea, Republic of", "Macao": "Macau",
                          "UK": "United Kingdom", "Republic of Ireland": "Ireland", "Taiwan*":"Taiwan", "Congo (Kinshasa)": "Congo", "occupied Palestinian territory" :"Palestine"}


    for name in f["Country/Region"].unique():
        try:
            i = name
            tmp = name


            if correction.__contains__(name):
                country = pycountry.countries.search_fuzzy(correction[i])[0]
                tmp = correction[i]
            else:
                country = pycountry.countries.search_fuzzy(i)[0]



            country_meta[i] = {"name": country.name, "alpha_2": country.alpha_2, "alpha_3": country.alpha_3}

        except:
            country_meta[i] = {"name": i, "alpha_2": "XX", "alpha_3": "XXX"}
    md5 = md5Checksum(CSV_FILE, None)

    meta_data = {
        "country_meta": country_meta,
        "columns_name": f.columns.unique().tolist(),
        "columns_meta": data,
        "data_meta": {"md5": md5, "updated": datetime.datetime.now().strftime('%d %B, %Y  %H:%M:%S')}
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


def md5Checksum(filePath, url):
    m = hashlib.md5()
    if url == None:
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
    lines[0] = first_line
    with open(README_PATH, "w") as f:
        f.writelines(lines)


def get_data_url():
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    template_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{DATE}.csv"
    CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))

    status_code = 0
    while (status_code != 200):
        CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))
        r = requests.get(CSV_URL)
        status_code = r.status_code
        today = today - datetime.timedelta(days=1)
    return CSV_URL


def dumpTimeSeries(CSV_FILE):
    my_data = pd.read_csv(CSV_FILE)
    agg = pd.DataFrame(columns=my_data.columns)
    agg.loc[0] = "!summary"

    f = {'Province/State': 'nunique',
         'Lat': 'mean',
         'Long': 'mean',
         }
    my_data[my_data.columns[4:]] = my_data[my_data.columns[4:]].fillna(0).astype(np.int64)

    for i in my_data.columns[4:]:
        my_data[i] = pd.to_numeric(my_data[i], downcast='integer')
        agg[i].loc[0] = my_data[i].sum()
        f[i] = "sum"
    if "Lat" in my_data.columns:
        agg.loc[0]["Lat"] = my_data["Lat"].mean()
        agg.loc[0]["Long"] = my_data["Long"].mean()
    my_data.loc[-1] =agg.loc[0]


    my_data = my_data.replace(np.nan, '', regex=True)
    g = my_data.groupby(['Country/Region'])
    dataGroupedByCountry = g.agg(f)

    results = {}
    for key, df_gb in g:
        records = df_gb.to_dict('records')
        data = {}
        for i in records:
            data_label = i['Province/State']
            if data_label == "":
                data_label = "*"
            data[data_label] = i

        results[str(key)] = {
            "total": dataGroupedByCountry.loc[str(key)].to_dict(),
            "province": data
        }

    filename, ext = (CSV_FILE.split('/')[-1].split('.'))

    filename = filename.replace("-","_").lower()
    with open('./{}.json'.format(filename), "w") as f:
        f.write(json.dumps(results))
    with open('./{}_pretty_print.json'.format(filename), "w") as f:
        f.write(json.dumps(results, indent=4))


def download_data():
    with open(DOWNLOAD_INFO_FILE, 'r') as file:
        download_info = json.load(file)

    URL_CONFIRMED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    URL_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    URL_RECOVERED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
    URL_DAILY_REPORT = "generated/csse_covid_19_daily_reports.csv"
    changed = []
    data_changed = False;
    for i in [URL_CONFIRMED, URL_DEATHS, URL_RECOVERED, URL_DAILY_REPORT]:
        filename = i.split('/')[-1]
        if (i == "generated/csse_covid_19_daily_reports.csv"):
            i = get_data_url()
        if filename in download_info:
            old_md5 = download_info[filename]
        else:
            old_md5 = ""

        curr_md5 = md5Checksum(None, i)
        if (old_md5 != curr_md5):
            r = requests.get(i)
            with open(DOWNLOAD_PATH + filename, 'wb') as f:
                f.write(r.content)
                download_info[filename] = curr_md5
                data_changed = True
            changed.append(filename)




    if (data_changed):
        out = json.dumps(download_info, indent=4, sort_keys=True)
        with open(DOWNLOAD_INFO_FILE, 'w') as f:
            f.write(out)
        print(out)
    return changed



def dumpRecordData(CSV_FILE):
    import pandas as pd
    my_data = pd.read_csv(CSV_FILE)

    my_data["Last Update"] = pd.to_datetime(my_data["Last Update"])
    agg = pd.DataFrame(columns=my_data.columns)
    agg.loc[0] = "!summary"


    operations = {'Province/State': 'nunique',
         'Latitude': 'mean',
         'Longitude': 'mean',
         'Last Update': 'max'
         }



    for i in my_data.columns[3:]:
        agg[i].loc[0] = my_data[i].sum()
        operations[i] = "sum"
    agg.loc[0]["Province/State"] = my_data["Province/State"].unique().shape[0]
    agg.loc[0]["Last Update"] = my_data["Last Update"].max()

    if  "Latitudee" in my_data.columns:
        agg.loc[0]["Latitude"] = my_data["Latitude"].mean()
        agg.loc[0]["Longitude"] = my_data["Longitude"].mean()
    if "Lat" in my_data.columns:
        agg.loc[0]["Lat"] = my_data["Lat"].mean()
        agg.loc[0]["Long"] = my_data["Long"].mean()
    my_data.loc[-1] =agg.loc[0]
    my_data["Last Update"] = my_data["Last Update"].dt.strftime('%Y-%m-%d %H:%M:%S')



    my_data = my_data.replace(np.nan, '', regex=True)
    # my_data["Confirmed"]= my_data["Confirmed"].astype(np.int32)
    # my_data["Deaths"] =my_data["Deaths"].astype(np.int32)
    # my_data["Recovered"] =my_data["Recovered"].astype(np.int32)



    g = my_data.groupby(['Country/Region'])
    aggra = g.agg(operations)

    aggra["Province/State"] = aggra["Province/State"].astype(np.int32)
    results = {}
    for key, df_gb in g:
        agg_dict = aggra.loc[str(key)].to_dict()
        agg_dict["Province/State"] = "None"


        records = df_gb.to_dict('records')
        data = {}
        for i in records:
            data_label = i['Province/State']
            if data_label == "":
                data_label = "*"
            data[data_label] = i
        results[str(key)] = {
            "total": aggra.loc[str(key)].to_dict(),
            "Province":data
        }


    filename, ext = (CSV_FILE.split('/')[-1].split('.'))
    filename = filename.replace("-","_").lower()
    with open('./{}.json'.format(filename), "w") as file:
        file.write(json.dumps(results, cls=npEncoder))
    with open('./{}_pretty_print.json'.format(filename), "w") as file:
        file.write(json.dumps(results, cls=npEncoder, indent=4, sort_keys=True))



def runTest():
    test = "csse_covid_19_data/csse_covid_19_daily_reports.csv"
    dumpMetaData(test)


debug = False
if __name__ == "__main__":
    if (debug):
        runTest()
        sys.exit('tested')


    changed = download_data()

    if (len(changed) != 0):
        print("processing :" + changed.__str__())


        for filename in changed:
            print("Processing {}".format(filename))
            CSV_PATH = DOWNLOAD_PATH + filename;
            if filename == "csse_covid_19_daily_reports.csv":
                dumpRecordData(CSV_PATH)
                dumpCsvToJson(CSV_PATH)
                dumpCsvToJsonPrettyPrint(CSV_PATH)
                dumpMetaData(CSV_PATH)

            else:
                dumpTimeSeries(CSV_PATH)
        update_readme("# Novel Coronavirus JSON data (Updated: {UPDATED}) \n".format(
            UPDATED=datetime.datetime.now().strftime('%d %B, %Y  %H:%M:%S')))



    else:
        sys.exit('Local file is the latest, nothing was updated')


